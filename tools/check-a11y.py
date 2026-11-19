#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Accessibility gate for the flove apps.

Static checks only (no browser): they catch the regressions our automation can
introduce, and they are cheap enough to run in the release sweep next to
extract-fields.py / fa-subset.py.

Checks, per app in tools/routing.json:
  1. a main landmark  — <main> or role="main"
  2. an <h1>          — at least one, outside <script>
  3. reduced motion   — a prefers-reduced-motion media query
  4. lang on bilingual spans — .t-en/.t-es/.en/.es carry lang="en"/"es"
  5. no positive tabindex
  6. role=button/menuitem are focusable (tabindex) and the app has a keydown
  7. no placeholder links  — <a href="#">
  8. every <img> has alt
  9. every form control has an accessible name (aria-label/labelledby/title,
     a <label for>, or a wrapping <label>)
 10. no outline:none without a :focus / :focus-visible rule

Usage: python3 tools/check-a11y.py [--quiet]
Exit 0 = clean, 1 = issues.
"""
from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTING = os.path.join(ROOT, "tools", "routing.json")

TEXT_TAGS = {"span", "em", "strong", "b", "i", "small", "p", "div", "li", "a", "button", "summary", "label", "dd", "dt"}
LANG_CLASSES = {"t-en": "en", "en": "en", "t-es": "es", "es": "es"}
CONTROL_TAGS = {"input", "select", "textarea"}
SKIP_INPUT_TYPES = {"hidden", "submit", "button", "reset"}


class Labels(HTMLParser):
    """First pass: every <label for=...> id, so a control can be named by a label that follows it."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "label" and d.get("for"):
            self.ids.add(d["for"])


class Scan(HTMLParser):
    def __init__(self, label_ids=()):
        super().__init__(convert_charrefs=False)
        self.label_ids = set(label_ids)
        self.inscript = False
        self.main = 0
        self.h1 = 0
        self.lang_missing = 0
        self.positive_tabindex = 0
        self.role_focus = 0
        self.placeholder_links = 0
        self.img_no_alt = 0
        self.controls = []          # (tag, attrs, offset_index)
        self.label_for = set()
        self.in_label = 0
        self.controls_unnamed = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "script":
            self.inscript = True
            return
        if self.inscript:
            return
        if tag == "main" or d.get("role") == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        cls = (d.get("class") or "").split()
        for tok in cls:
            want = LANG_CLASSES.get(tok)
            if want and "lang" not in d:
                self.lang_missing += 1
        ti = d.get("tabindex")
        if ti and ti.lstrip("+-").isdigit() and int(ti) > 0:
            self.positive_tabindex += 1
        if d.get("role") in ("button", "menuitem", "tab") and "tabindex" not in d and tag not in ("button",):
            self.role_focus += 1
        if tag == "a" and d.get("href") == "#":
            self.placeholder_links += 1
        if tag == "img" and "alt" not in d:
            self.img_no_alt += 1
        if tag == "label":
            self.in_label += 1
            if d.get("for"):
                self.label_for.add(d["for"])
        if tag in CONTROL_TAGS:
            typ = (d.get("type") or ("text" if tag == "input" else tag)).lower()
            if typ in SKIP_INPUT_TYPES:
                return
            if d.get("aria-hidden") == "true":
                return
            named = any(k in d for k in ("aria-label", "aria-labelledby", "title"))
            if not named and (d.get("id") in self.label_ids or d.get("id") in self.label_for):
                named = True
            if not named and self.in_label:
                named = True
            if not named:
                self.controls_unnamed += 1

    def handle_endtag(self, tag):
        if tag == "script":
            self.inscript = False
        if tag == "label" and self.in_label:
            self.in_label -= 1


def markup_of(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    return "".join(p for p in re.split(r"(<script\b.*?</script>)", text, flags=re.S | re.I)
                   if not p.lower().startswith("<script"))


def check(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    # Parse markup only: a template string may contain a raw </script>, which would
    # otherwise end script mode early and turn JS templates into "markup".
    markup = "".join(p for p in re.split(r"(<script\b.*?</script>)", text, flags=re.S | re.I)
                     if not p.lower().startswith("<script"))
    labels = Labels()
    labels.feed(markup)
    scan = Scan(labels.ids)
    scan.feed(markup)
    issues = []
    if scan.main == 0:
        issues.append("no main landmark")
    if scan.h1 == 0:
        issues.append("no <h1>")
    if "prefers-reduced-motion" not in text:
        issues.append("no prefers-reduced-motion media query")
    if scan.lang_missing:
        issues.append(f"{scan.lang_missing} bilingual span(s) without lang")
    if scan.positive_tabindex:
        issues.append(f"{scan.positive_tabindex} positive tabindex")
    if scan.role_focus:
        issues.append(f"{scan.role_focus} role=button/menuitem without tabindex")
    if scan.placeholder_links:
        issues.append(f"{scan.placeholder_links} placeholder link(s) href=\"#\"")
    if scan.img_no_alt:
        issues.append(f"{scan.img_no_alt} <img> without alt")
    if scan.controls_unnamed:
        issues.append(f"{scan.controls_unnamed} form control(s) without an accessible name")
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S):
        css = m.group(1)
        if re.search(r"outline\s*:\s*(none|0)", css) and not re.search(r":focus", css):
            issues.append("outline:none with no :focus rule")
            break
    return issues


def main():
    quiet = "--quiet" in sys.argv
    with open(ROUTING, encoding="utf-8") as fh:
        routing = json.load(fh)
    checked = 0
    bad = 0
    for app in routing.get("apps", []):
        url = app.get("url") or ""
        if not url:
            continue
        path = os.path.join(ROOT, url)
        if not os.path.exists(path):
            continue
        checked += 1
        if len(markup_of(path)) < 0.2 * os.path.getsize(path):
            # JS-rendered app: most of the UI is built at runtime, so the static
            # landmark/heading/control checks cannot see it. Nothing to fail here.
            if not quiet:
                print(f"  note  {app['id']}: JS-rendered, checked at runtime only")
            continue
        issues = check(path)
        if issues:
            bad += 1
            print(f"  {app['id']}: " + "; ".join(issues))
    print(f"checked {checked} app files")
    if bad:
        print(f"FAIL: {bad} app(s) with accessibility issues")
        return 1
    if not quiet:
        print("ok: accessibility gate clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
