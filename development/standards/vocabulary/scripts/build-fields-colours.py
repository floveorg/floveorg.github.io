#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the questy-flove fields & colours export (fields-colours.ods) from the
canonical hats dataset (fields-colours.json, schema flove-hats/1).

Layout, rows of the sheet:
  1  category-colour banner (watch chips, one merged cell per category)
  2  per-category hat analogies (italic)
  3  header: Category | App | Signature hat | Accent | Field | Input | 6 hat columns
  … one signature row per app, then one row per kind:input slot with a ● in
    the slot's hat column. Category + App repeat on every row so Calc/Excel
    filtering works. The Accent column shows the app's polished sub-colour
    (from the apps-full launcher tiles) as a coloured chip; Field groups some
    apps within a category (e.g. Inside → Metaphysics/Psychology). No colour
    hex columns beyond Accent, no "wears", no review markers — the plain sheet.
    The hexes live in the canonical JSON; the sheet only shows chips.

Writes the .ods directly (a zipped ODF/OpenDocument spreadsheet), so no heavy
toolchain (soffice/Calc) is required to regenerate.
"""
import json
import os
import sys
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.dirname(HERE)
DATA = os.path.join(VOCAB, "fields-colours.json")
OUT = os.path.join(VOCAB, "fields-colours.ods")

HAT_ICONS = {"facts": "⚪", "heart": "❤", "risk": "⬛",
             "optimism": "🟡", "creative": "🟢", "make": "🔵"}

COL_WIDTHS = ["2.5cm", "2.3cm", "3.1cm", "2.6cm", "3.2cm", "6.5cm"] + ["2.6cm"] * 6

OFFICE_NS = 'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" ' \
            'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" ' \
            'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" ' \
            'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" ' \
            'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"'


def build_rows(data):
    """Return (hat_columns, rows). Hat order follows data["hats"].

    Hat resolution is the parent-prevails ladder: slot -> app -> category.
    A slot without its own hat inherits the app's; an app without one the
    category's, so the sheet never drops an input just because its hat is
    inherited rather than explicit.
    """
    hats = data["hats"]
    cat_hats = {cat["name"]: cat["hat"] for cat in data["categories"]}
    cat_order = [cat["name"] for cat in data["categories"]]
    apps_by_cat = {}
    for app in data["apps"]:
        apps_by_cat.setdefault(app["category"], []).append(app)
    rows = []
    for cat in cat_order:
        cat_hat = cat_hats[cat]
        for app in apps_by_cat.get(cat, []):
            app_hat = app.get("hat") or cat_hat
            accent = app.get("colour") or ""
            field = app.get("field") or ""
            also = app.get("also") or []
            label = app["id"]
            if also:
                label = f"{label}  ·  also {' + '.join(also)}"
            rows.append({"cat": cat, "app": label, "sig": hat_label(app_hat),
                         "accent": accent, "field": field,
                         "slot": "", "marks": [False] * len(hats)})
            for slot, hat in app.get("slots", {}).items():
                marks = [False] * len(hats)
                marks[hats.index(hat or app_hat or cat_hat)] = True
                rows.append({"cat": cat, "app": label, "sig": "",
                             "accent": accent, "field": field,
                             "slot": slot, "marks": marks})
    return hats, rows


def hat_label(hat):
    return f"{HAT_ICONS[hat]} {hat}"


def content_xml(data, rows):
    hats = data["hats"]
    col_styles = "".join(
        f'<style:style style:name="co{i+1}" style:family="table-column">'
        f'<style:table-column-properties style:column-width="{w}"/></style:style>'
        for i, w in enumerate(COL_WIDTHS))
    columns = "".join(f'<table:table-column table:style-name="co{i+1}"/>'
                      for i in range(len(COL_WIDTHS)))

    def cell(text, style="ce-w"):
        return (f'<table:table-cell table:style-name="{style}" office:value-type="string">'
                f'<text:p>{escape(text)}</text:p></table:table-cell>')

    def spanned_cell(text, style, span=2):
        return (f'<table:table-cell table:style-name="{style}" '
                f'table:number-columns-spanned="{span}" '
                f'office:value-type="string"><text:p>{escape(text)}</text:p></table:table-cell>')

    cats = data["categories"]
    cat_styles = "".join(
        f'<style:style style:name="ce-c{i}" style:family="table-cell">'
        f'<style:table-cell-properties fo:background-color="{cat["colour"]}"/>'
        f'<style:text-properties fo:font-weight="bold" fo:color="#1f1f1f"/></style:style>'
        for i, cat in enumerate(cats))
    accents = sorted({r["accent"] for r in rows if r["accent"]})
    accent_map = {}
    for i, hexv in enumerate(accents):
        name = f"ce-a{i}"
        accent_map[hexv] = name
        cat_styles += (f'<style:style style:name="{name}" style:family="table-cell">'
                       f'<style:table-cell-properties fo:background-color="{hexv}"/>'
                       f'<style:text-properties fo:font-weight="bold" '
                       f'fo:color="#ffffff"/></style:style>')

    def accent_cell(hexv):
        if not hexv:
            return cell("")
        return cell(f"●  {hexv}", accent_map[hexv])

    banner_colours = "".join(
        spanned_cell(f"{cat['name']} {HAT_ICONS[cat['hat']]} {cat['colour']}", f"ce-c{i}")
        for i, cat in enumerate(cats))
    banner_analogies = "".join(spanned_cell(cat["analogy"], "ce-an") for cat in cats)

    header = ["Category", "App", "Signature hat", "Accent", "Field", "Input"] + \
             [hat_label(h) for h in hats]
    rows_xml = [
        f"<table:table-row>{banner_colours}</table:table-row>",
        f"<table:table-row>{banner_analogies}</table:table-row>",
        f"<table:table-row>{''.join(cell(c, 'ce-hdr') for c in header)}</table:table-row>",
    ]
    for r in rows:
        values = [r["cat"], r["app"], r["sig"], "", r["field"] or "—", r["slot"]] + \
                 ["●" if m else "" for m in r["marks"]]
        row_xml = "".join(
            accent_cell(r["accent"]) if i == 3 else cell(v)
            for i, v in enumerate(values))
        rows_xml.append(f"<table:table-row>{row_xml}</table:table-row>")

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<office:document-content {OFFICE_NS} office:version="1.2">'
        '<office:automatic-styles>'
        f'{col_styles}'
        f'{cat_styles}'
        '<style:style style:name="ce-an" style:family="table-cell">'
        '<style:text-properties fo:font-style="italic"/></style:style>'
        '<style:style style:name="ce-hdr" style:family="table-cell">'
        '<style:text-properties fo:font-weight="bold"/></style:style>'
        '<style:style style:name="ce-w" style:family="table-cell"/>'
        '</office:automatic-styles>'
        '<office:body><office:spreadsheet>'
        f'<table:table table:name="Fields &amp; colours">{columns}{"".join(rows_xml)}</table:table>'
        '</office:spreadsheet></office:body>'
        '</office:document-content>'
    )


def styles_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<office:document-styles {OFFICE_NS} office:version="1.2">'
        '<office:styles><style:default-style style:family="table-cell">'
        '<style:text-properties fo:font-size="10pt" '
        'style:font-name="OpenSymbol"/></style:default-style></office:styles>'
        '</office:document-styles>'
    )


def meta_xml():
    extra = 'xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" ' \
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<office:document-meta {OFFICE_NS} {extra}office:version="1.2">'
        '<office:meta><meta:generator>flove build-fields-colours</meta:generator>'
        '<dc:title>Fields &amp; colours</dc:title></office:meta>'
        '</office:document-meta>'
    )


def manifest_xml():
    entries = [
        ("/", "application/vnd.oasis.opendocument.spreadsheet"),
        ("content.xml", "text/xml"),
        ("styles.xml", "text/xml"),
        ("meta.xml", "text/xml"),
        ("settings.xml", "text/xml"),
    ]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" '
        'manifest:version="1.2">' +
        "".join(f'<manifest:file-entry manifest:full-path="{p}" manifest:media-type="{m}"/>'
                for p, m in entries) +
        '</manifest:manifest>'
    )


def settings_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<office:document-settings {OFFICE_NS} office:version="1.2">'
        '<office:settings/></office:document-settings>'
    )


def write_ods(rows_xml_data, path):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("mimetype", "application/vnd.oasis.opendocument.spreadsheet",
                    compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/manifest.xml", manifest_xml())
        zf.writestr("content.xml", rows_xml_data)
        zf.writestr("styles.xml", styles_xml())
        zf.writestr("meta.xml", meta_xml())
        zf.writestr("settings.xml", settings_xml())


def main():
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    hats, rows = build_rows(data)
    write_ods(content_xml(data, rows), OUT)
    apps = len(data["apps"])
    inputs = sum(len(a["slots"]) for a in data["apps"])
    print(f"ods written: {OUT}")
    print(f"schema: {data['schema']} · apps: {apps} · input slots: {inputs} · "
          f"rows: {2 + 1 + apps + inputs} (banners + header + data)")
    return 0


if __name__ == "__main__":
    sys.exit(main())