#!/usr/bin/env python3
"""Tests for tools/serve-edit.py (run: python3 tools/test_serve_edit.py)."""

from __future__ import annotations

import http.client
import importlib.util
import json
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
_MISSING = object()
spec = importlib.util.spec_from_file_location("serve_edit", HERE / "serve-edit.py")
serve_edit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(serve_edit)


class ServerCase(unittest.TestCase):
    token = None

    def setUp(self) -> None:
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.editable = self.root / "docs"
        self.editable.mkdir()
        self.page = self.editable / "page.md"
        self.page.write_text("# Title\n\nBody.\n", encoding="utf-8")
        serve_edit.WikiHandler.editor = serve_edit.Editor(
            self.root, "docs", token=self.token, backup_dir=self.root / "_backs"
        )
        handler = partial(serve_edit.WikiHandler, directory=str(self.root))
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.tmp.cleanup()

    # ---- helpers -------------------------------------------------------

    def request(self, method, path, payload=None, *, origin=True, token=_MISSING):
        if token is _MISSING:
            token = self.token
        headers = {}
        body = None
        if payload is not None:
            body = json.dumps(payload)
            headers["Content-Type"] = "application/json"
        if origin:
            headers["Origin"] = f"http://127.0.0.1:{self.port}"
        if token is not None:
            headers["X-Edit-Token"] = token
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=headers)
            res = conn.getresponse()
            raw = res.read()
            try:
                data = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                data = raw
            return res.status, data
        finally:
            conn.close()

    def save(self, *, origin=True, token=_MISSING, **payload):
        payload.setdefault("path", "page.md")
        payload.setdefault("markdown", "# Changed\n\nNew body.\n")
        return self.request("POST", "/__edit/save", payload, origin=origin, token=token)

    # ---- tests ---------------------------------------------------------

    def test_ping(self):
        status, data = self.request("GET", "/__edit/ping", origin=False)
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["api"], 1)
        self.assertEqual(data["auth"], "token" if self.token else "none")

    def test_save_writes_and_backs_up(self):
        before = self.page.read_text(encoding="utf-8")
        status, data = self.save()
        self.assertEqual(status, 200, data)
        self.assertEqual(self.page.read_text(encoding="utf-8"), "# Changed\n\nNew body.\n")
        self.assertTrue(Path(data["backup"]).is_file())
        self.assertEqual(Path(data["backup"]).read_text(encoding="utf-8"), before)
        self.assertEqual(len(data["base"]), 64)

    def test_requires_same_origin(self):
        status, _ = self.save(origin=False)
        self.assertEqual(status, 403)
        self.assertEqual(self.page.read_text(encoding="utf-8"), "# Title\n\nBody.\n")

    def test_rejects_traversal(self):
        for rel in ("../page.md", "/etc/passwd", "sub/../../page.md"):
            status, _ = self.save(path=rel)
            self.assertIn(status, (400, 403), rel)

    def test_rejects_non_markdown_and_missing(self):
        (self.editable / "page.html").write_text("x", encoding="utf-8")
        self.assertIn(self.save(path="page.html")[0], (400, 403))
        self.assertEqual(self.save(path="missing.md")[0], 404)

    def test_base_conflict(self):
        status, data = self.request("GET", "/__edit/ping", origin=False)
        self.assertEqual(status, 200)
        stale = "0" * 64
        status, data = self.save(base=stale)
        self.assertEqual(status, 409, data)
        self.assertEqual(data["code"], "conflict")
        self.assertEqual(self.page.read_text(encoding="utf-8"), "# Title\n\nBody.\n")

    def test_dry_run_does_not_write(self):
        status, data = self.save(dryRun=True)
        self.assertEqual(status, 200, data)
        self.assertTrue(data["dryRun"])
        self.assertEqual(self.page.read_text(encoding="utf-8"), "# Title\n\nBody.\n")

    def test_preserves_crlf(self):
        self.page.write_bytes(b"# Title\r\n\r\nBody.\r\n")
        status, _ = self.save(markdown="# Changed\n\nNew.\n")
        self.assertEqual(status, 200)
        self.assertEqual(self.page.read_bytes(), b"# Changed\r\n\r\nNew.\r\n")

    def test_preserves_bom(self):
        self.page.write_bytes(b"\xef\xbb\xbf# Title\n")
        status, _ = self.save(markdown="# Changed\n")
        self.assertEqual(status, 200)
        self.assertEqual(self.page.read_bytes(), b"\xef\xbb\xbf# Changed\n")

    def test_rejects_empty_body(self):
        status, _ = self.request("POST", "/__edit/save", None)
        self.assertEqual(status, 400)

    def test_rejects_huge_body(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.putrequest("POST", "/__edit/save")
        conn.putheader("Content-Length", str(serve_edit.MAX_BODY + 1))
        conn.putheader("Origin", f"http://127.0.0.1:{self.port}")
        if self.token:
            conn.putheader("X-Edit-Token", self.token)
        conn.endheaders()
        res = conn.getresponse()
        self.assertEqual(res.status, 413)
        res.read()
        conn.close()


class TokenCase(ServerCase):
    token = "s3cret"

    def test_save_requires_token(self):
        status, _ = self.save(token=None)
        self.assertEqual(status, 403)
        status, data = self.save(token="s3cret")
        self.assertEqual(status, 200, data)
        status, _ = self.save(token="wrong")
        self.assertEqual(status, 403)


if __name__ == "__main__":
    unittest.main(verbosity=2)
