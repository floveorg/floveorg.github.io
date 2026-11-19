#!/usr/bin/env python3
"""serve-edit.py — static docs server + save API for the docsify-edit plugin.

Serves the repository root with the same URL layout as the published site and
adds a tiny, local-only API:

    GET  /__edit/ping
        {"ok": true, "api": 1, "version": "...", "editable": "development/standards",
         "auth": "none" | "token", "maxBody": 4194304}

    POST /__edit/save
        {"path": "frontend/wizy.md", "markdown": "...",
         "base": "<sha256 of the file when editing started>"}   # base optional
        → {"ok": true, "path": "...", "bytes": 1234,
           "backup": "/home/…/.cache/docsify-edit/…", "mtime": 1234.5}

    POST /__edit/save {"dryRun": true, …} does everything except writing.

Safety rails
    * binds localhost by default (``--host`` to override; IPv6 dual-stack)
    * only existing ``*.md`` files inside ``--editable`` can be written
    * the POST must be same-origin; optional shared token (``--token``)
    * the previous file is copied to ``~/.cache/docsify-edit/`` first
    * writes are atomic (temp file + rename) and serialized per path
    * a ``base`` SHA-256 is checked so a stale tab cannot overwrite a newer file
    * CRLF, BOM and the file's UTF-8 encoding are preserved
    * every response carries ``Cache-Control: no-store``

Usage
    python3 tools/serve-edit.py [--port 8642] [--host ::]
                                [--root .] [--editable development/standards]
                                [--token secret]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import functools
import hashlib
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

API_VERSION = 1
SERVER_VERSION = "1.0.0"
MAX_BODY = 4 * 1024 * 1024
DEFAULT_EDITABLE = "development/standards"
DEFAULT_BACKUP_DIR = Path.home() / ".cache" / "docsify-edit"
MAX_BACKUPS = 200


class ApiError(Exception):
    def __init__(self, status: int, message: str, code: str = "error") -> None:
        super().__init__(message)
        self.status = status
        self.code = code


class Editor:
    """The filesystem side of the editor: resolve, guard, back up, write."""

    def __init__(
        self,
        root: Path,
        editable: str,
        token: str | None = None,
        backup_dir: Path = DEFAULT_BACKUP_DIR,
    ) -> None:
        self.root = root.resolve()
        self.editable = (self.root / editable).resolve()
        self.token = token
        self.backup_dir = backup_dir
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    # ---- paths ---------------------------------------------------------

    def resolve(self, rel: str) -> Path:
        if not rel or "\x00" in rel or "\\" in rel or rel.startswith("/"):
            raise ApiError(400, "invalid path")
        candidate = (self.editable / rel).resolve()
        try:
            candidate.relative_to(self.editable)
        except ValueError:
            raise ApiError(403, f"outside {self.editable.name}/") from None
        if candidate.suffix.lower() != ".md":
            raise ApiError(403, "only .md files are editable")
        if not candidate.is_file():
            raise ApiError(404, "file not found")
        return candidate

    def _lock_for(self, target: Path) -> threading.Lock:
        key = str(target)
        with self._locks_guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = self._locks[key] = threading.Lock()
            return lock

    # ---- save ----------------------------------------------------------

    def save(
        self,
        rel: str,
        markdown: str,
        base: str | None = None,
        dry_run: bool = False,
    ) -> dict:
        target = self.resolve(rel)
        with self._lock_for(target):
            original = target.read_bytes()
            try:
                original.decode("utf-8")
            except UnicodeDecodeError:
                raise ApiError(500, "file is not valid UTF-8") from None

            if base:
                digest = hashlib.sha256(original).hexdigest()
                if digest != base:
                    raise ApiError(
                        409,
                        "the file changed on disk since you opened the editor",
                        code="conflict",
                    )

            text = markdown.replace("\r\n", "\n")
            crlf = b"\r\n" in original
            if crlf:
                text = text.replace("\n", "\r\n")
            data = text.encode("utf-8")
            if original.startswith(b"\xef\xbb\xbf") and not data.startswith(b"\xef\xbb\xbf"):
                data = b"\xef\xbb\xbf" + data

            backup = None
            if not dry_run:
                backup = self._backup(target, rel)
                self._atomic_write(target, data)

            return {
                "ok": True,
                "path": rel,
                "bytes": len(data),
                "base": hashlib.sha256(data).hexdigest(),
                "backup": str(backup) if backup else None,
                "mtime": target.stat().st_mtime,
                "dryRun": dry_run,
            }

    def _backup(self, target: Path, rel: str) -> Path | None:
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            slug = rel.replace("/", "__")
            backup = self.backup_dir / f"{stamp}--{slug}"
            shutil.copy2(target, backup)
            self._prune_backups()
            return backup
        except OSError as exc:
            raise ApiError(500, f"backup failed: {exc}") from exc

    def _prune_backups(self) -> None:
        try:
            files = sorted(
                (p for p in self.backup_dir.iterdir() if p.is_file()),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for old in files[MAX_BACKUPS:]:
                old.unlink(missing_ok=True)
        except OSError:
            pass

    @staticmethod
    def _atomic_write(target: Path, data: bytes) -> None:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
        )
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(data)
            os.replace(tmp_name, target)
        except OSError as exc:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise ApiError(500, f"write failed: {exc}") from exc


class WikiHandler(SimpleHTTPRequestHandler):
    editor: Editor  # set by main()

    # ---- headers -------------------------------------------------------

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    # ---- helpers -------------------------------------------------------

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _same_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return False
        host = self.headers.get("Host", "")
        return origin in {f"http://{host}", f"https://{host}"}

    def _authorized(self) -> bool:
        if not self.editor.token:
            return True
        return self.headers.get("X-Edit-Token") == self.editor.token

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            raise ApiError(400, "empty body")
        if length > MAX_BODY:
            raise ApiError(413, f"body larger than {MAX_BODY} bytes")
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ApiError(400, "invalid JSON") from None
        if not isinstance(payload, dict):
            raise ApiError(400, "JSON object required")
        return payload

    # ---- routes --------------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        if self.path.split("?", 1)[0] == "/__edit/ping":
            self._json(
                200,
                {
                    "ok": True,
                    "api": API_VERSION,
                    "version": SERVER_VERSION,
                    "editable": self.editor.editable.relative_to(self.editor.root).as_posix(),
                    "auth": "token" if self.editor.token else "none",
                    "authOk": self._authorized(),
                    "maxBody": MAX_BODY,
                },
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/__edit/save":
            self._json(404, {"ok": False, "code": "not_found", "error": "unknown endpoint"})
            return
        try:
            if not self._same_origin():
                raise ApiError(403, "cross-origin write refused", code="origin")
            if not self._authorized():
                raise ApiError(403, "bad or missing X-Edit-Token", code="auth")
            payload = self._read_json()

            rel = payload.get("path")
            markdown = payload.get("markdown")
            base = payload.get("base")
            dry_run = bool(payload.get("dryRun"))
            if not isinstance(rel, str) or not isinstance(markdown, str):
                raise ApiError(400, "path and markdown (strings) are required")
            if "\x00" in markdown:
                raise ApiError(400, "NUL byte in markdown")
            if base is not None and not isinstance(base, str):
                raise ApiError(400, "base must be a SHA-256 string")
            self._json(200, self.editor.save(rel, markdown, base, dry_run))
        except ApiError as exc:
            self._json(exc.status, {"ok": False, "code": exc.code, "error": str(exc)})
        except Exception as exc:  # keep the server alive and the client informed
            self._json(500, {"ok": False, "code": "server", "error": str(exc)})


class DualStackServer(ThreadingHTTPServer):
    """Listen on IPv4 and IPv6 when bound to ``::``."""

    address_family = socket.AF_INET6

    def server_bind(self) -> None:
        if hasattr(socket, "IPV6_V6ONLY"):
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except OSError:
                pass
        super().server_bind()


def make_server(host: str, port: int, handler) -> ThreadingHTTPServer:
    if host in ("::", "::1") and socket.has_ipv6:
        try:
            return DualStackServer((host, port), handler)
        except OSError:
            if host == "::1":
                raise
    return ThreadingHTTPServer((host, port), handler)


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="static docs server + docsify-edit save API")
    ap.add_argument("--port", type=int, default=8642)
    ap.add_argument("--host", default="::", help="bind address (default: :: = IPv4+IPv6)")
    ap.add_argument("--root", default=str(here.parent), help="site root to serve")
    ap.add_argument("--editable", default=DEFAULT_EDITABLE, help="directory that may be written")
    ap.add_argument("--token", default=None, help="require this X-Edit-Token on saves")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    editable = (root / args.editable).resolve()
    if not editable.is_dir():
        print(f"✗ {root} has no {args.editable}/", file=sys.stderr)
        return 2

    WikiHandler.editor = Editor(root, args.editable, token=args.token)
    handler = functools.partial(WikiHandler, directory=str(root))
    try:
        server = make_server(args.host, args.port, handler)
    except OSError as exc:
        print(f"✗ cannot bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1
    server.daemon_threads = True

    host, port = server.server_address[:2]
    shown = "127.0.0.1" if host in ("::", "0.0.0.0", "") else host
    print(f"🌱 docsify-edit → http://{shown}:{port}/{args.editable}/")
    print(f"   root      {root}")
    print(f"   editable  {editable}")
    print(f"   auth      {'token' if args.token else 'none'}")
    if shown not in ("127.0.0.1", "::1", "localhost"):
        print("   ⚠  not bound to localhost — anyone who can reach this port can edit")
    print("   Ctrl-C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
