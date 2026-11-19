#!/usr/bin/env python3
"""build-whole-md.py — regenerate the Whole taxonomy table in worldview.md.

Reads docs/index.html (the source table) and rewrites the Markdown copy in
development/standards/worldview.md. Use `--check` to report drift without
writing; the heavy release (`updaty4`) runs it before packaging.

    python3 development/scripts/build-whole-md.py            # rewrite
    python3 development/scripts/build-whole-md.py --check    # exit 1 on drift
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/index.html"
DST = ROOT / "development/standards/worldview.md"
COLS = ["Category", "Substance", "Field", "Paradigm",
        "Related paradigms", "App", "Related apps", "Description"]
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "area",
        "base", "col", "embed", "param", "track", "wbr"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []
        self.parent = parent

    def cls(self):
        return (self.attrs.get("class") or "").split()

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def walk(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.walk()


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [])
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, self.stack[-1]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def en_text(node):
    if node is None:
        return ""
    for child in node.walk():
        if "en" in child.cls():
            return re.sub(r"\s+", " ", child.text()).strip()
    return re.sub(r"\s+", " ", node.text()).strip()


def direct(node, cls):
    return [c for c in node.children if isinstance(c, Node) and cls in c.cls()]


def primary(cell, tag, cls):
    if cell is None:
        return None
    for child in cell.children:
        if isinstance(child, Node) and child.tag == tag and cls in child.cls():
            return child
    for child in cell.children:
        if isinstance(child, Node) and "added-item" in child.cls():
            for node in child.walk():
                if node.tag == tag and cls in node.cls():
                    return node
    return None


def related(cell, tag, cls):
    if cell is None:
        return []
    for child in cell.children:
        if isinstance(child, Node) and "more" in child.cls():
            for body in child.walk():
                if "more-body" in body.cls():
                    return [n for n in body.walk() if n.tag == tag and cls in n.cls()]
    return []


def rows():
    parser = Parser()
    parser.feed(SRC.read_text(encoding="utf-8"))
    out = []
    sections = [n for n in parser.root.walk()
                if n.tag == "section" and any(c.startswith("section") for c in n.cls())]
    for section in sections:
        category = ""
        for node in section.walk():
            if "section-title" in node.cls():
                category = en_text(node)
                break
        category = category or section.attrs.get("data-title", "")
        for item in [n for n in section.walk() if n.tag == "div" and "item" in n.cls()]:
            sub = (direct(item, "sub") or [None])[0]
            par = (direct(item, "par") or [None])[0]
            app = (direct(item, "app-cell") or [None])[0]
            fld = (direct(item, "field") or [None])[0]
            p_par = primary(par, "a", "std-link")
            p_app = primary(app, "a", "app-btn")
            out.append([
                category, en_text(sub), en_text(fld),
                p_par.text().strip() if p_par is not None else "",
                "; ".join(a.text().strip() for a in related(par, "a", "std-link")),
                p_app.text().strip() if p_app is not None else "",
                "; ".join(a.text().strip() for a in related(app, "a", "app-btn")),
                sub.attrs.get("data-tip-en", "") if sub is not None else "",
            ])
    return out


def table(data):
    def cell(value):
        return str(value or "").replace("|", "\\|")
    lines = ["| " + " | ".join(COLS) + " |",
             "|" + "|".join("---" for _ in COLS) + "|"]
    lines += ["| " + " | ".join(cell(c) for c in row) + " |" for row in data]
    return "\n".join(lines)


def main() -> int:
    data = rows()
    new = table(data) + f"\n\n_Exported from `docs/index.html` — {len(data)} rows._"
    text = DST.read_text(encoding="utf-8")
    match = re.search(r"(\| Category \| Substance \|.*?_Exported from `docs/index.html` — \d+ rows\._?)", text, re.S)
    if not match:
        print("build-whole-md: table not found in worldview.md", file=sys.stderr)
        return 2
    if match.group(1) == new:
        print(f"build-whole-md: worldview table current ({len(data)} rows)")
        return 0
    if "--check" in sys.argv:
        print(f"build-whole-md: DRIFT — {len(data)} rows in docs/index.html", file=sys.stderr)
        return 1
    DST.write_text(text[:match.start(1)] + new + text[match.end(1):], encoding="utf-8")
    print(f"build-whole-md: worldview table updated ({len(data)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
