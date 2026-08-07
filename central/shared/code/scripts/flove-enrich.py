#!/usr/bin/env python3
"""flove-enrich.py — batch enrichment transformer (main/central layout)

Moved from the retired `central/solo` branch (2026-07-31). Adapted to the
current layout: apps live in `solo/apps/`, the shared lib in `central/shared/`,
and enrichment is browsy-gift gated (the loader decides at runtime; this
script only declares the markers + lib base + loader ref).

Injects, for normal/advanced/super/mega-tier apps:
  <meta name="flove:lib-base" content="<rel to central/shared>">
  <meta name="flove:gift-min"  content="40">
  <script src="<rel>/code/js/flove-loader.js" defer></script>
  <link  data-flove-css href="flove.css" rel="stylesheet">
  <script data-flove-js  src="flove.js"></script>

mini/basic apps get an opt-in comment instead:
  <!-- flove:enrich-optin -->

Idempotent: skips files that already carry the markers.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'solo', 'apps'))
GIFT_MIN = '40'

TIER_ORDER = {'nano': 0, 'mini': 1, 'basic': 2, 'normal': 3, 'advanced': 4, 'super': 5, 'mega': 6}
DEFAULT_TIER = 'advanced'
PRO_MIN = 3  # normal+ are pro tiers

# Support/aux pages (not apps) — never enriched
SKIP_PATTERNS = [
    r'index\.html$',
    r'logos(-demos)?\.html$',
    r'-brand\.html$',
    r'help\.html$',
    r'new-wizard-help\.html$',
]


def get_tier(filename):
    name = os.path.basename(filename)
    base = os.path.splitext(name)[0]
    for t in TIER_ORDER:
        if f'-{t}' in base:
            return t
    return DEFAULT_TIER


def is_support_page(filename):
    return any(re.search(p, os.path.basename(filename)) for p in SKIP_PATTERNS)


def has_enrichment_markers(html):
    return 'data-flove-css' in html or 'data-flove-js' in html


def rel_lib_base(rel_path):
    """Relative path from the app file's dir up to central/shared/."""
    depth = len(rel_path.split('/')) - 1          # app dirs below solo/apps/
    return '../' * (depth + 2) + 'central/shared'  # +2: apps/ → solo/ → root


def inject_enrichment(html, rel_path):
    lib_base = rel_lib_base(rel_path)
    loader = f'<script src="{lib_base}/code/js/flove-loader.js" defer></script>'
    head_close = html.rfind('</head>')
    if head_close == -1:
        return html
    block = (
        f'\n  <!-- flove enrichment (browsy-gift gated) -->\n'
        f'  <meta name="flove:lib-base" content="{lib_base}">\n'
        f'  <meta name="flove:gift-min" content="{GIFT_MIN}">\n'
        f'{loader}\n'
        f'  <link data-flove-css href="flove.css">\n'
        f'  <script data-flove-js src="flove.js" type="text/plain"></script>\n'
    )
    return html[:head_close] + block + html[head_close:]


def main():
    changed, optin, skipped, support = [], [], [], []

    for root, dirs, files in os.walk(APPS_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'new']
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, APPS_DIR)
            tier = get_tier(f)

            if is_support_page(f):
                support.append(rel)
                continue

            with open(fpath, 'r') as fp:
                html = fp.read()

            if has_enrichment_markers(html):
                skipped.append(f'{rel} ({tier})')
                continue

            if TIER_ORDER.get(tier, DEFAULT_TIER) >= PRO_MIN:
                new_html = inject_enrichment(html, rel)
                if new_html != html:
                    with open(fpath, 'w') as fp:
                        fp.write(new_html)
                    changed.append(f'{rel} ({tier})')
            elif 'flove:enrich-optin' not in html:
                head_close = html.rfind('</head>')
                if head_close != -1:
                    html = html[:head_close] + '\n  <!-- flove:enrich-optin -->\n' + html[head_close:]
                    with open(fpath, 'w') as fp:
                        fp.write(html)
                optin.append(f'{rel} ({tier})')

    print(f'=== flove-enrich (main/central) ===')
    print(f'\nEnriched ({len(changed)}):')
    for c in changed:
        print(f'  + {c}')
    print(f'\nOpt-in eligible mini/basic ({len(optin)}):')
    for o in optin:
        print(f'  ~ {o}')
    print(f'\nAlready enriched ({len(skipped)}):')
    for s in skipped:
        print(f'  - {s}')
    print(f'\nSupport pages ({len(support)}):')
    for s in support:
        print(f'  . {s}')
    print(f'\nTotal: {len(changed)} enriched, {len(optin)} opt-in, {len(skipped)} skipped, {len(support)} support')


if __name__ == '__main__':
    main()
