#!/usr/bin/env python3
"""flove-loader-check.py — CI lint rule (main/central layout)

Flags:
1. Any normal/advanced/super/mega-tier app missing enrichment markers
2. Any pro-tier app with markers but no `flove:lib-base` meta (warning)
3. Any pro-tier app with markers but no flove-loader.js ref (warning)
4. Any mini/basic app with enrichment without a documented opt-in reason

Exit code 0 = pass, 1 = fail.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'solo', 'apps'))

TIER_ORDER = {'nano': 0, 'mini': 1, 'basic': 2, 'normal': 3, 'advanced': 4, 'super': 5, 'mega': 6}
DEFAULT_TIER = 'advanced'
PRO_MIN = 3

SKIP_PATTERNS = [
    r'index\.html$',
    r'logos(-demos)?\.html$',
    r'-brand\.html$',
    r'help\.html$',
    r'new-wizard-help\.html$',
]


def get_tier(filename):
    base = os.path.splitext(os.path.basename(filename))[0]
    for t in TIER_ORDER:
        if f'-{t}' in base:
            return t
    return DEFAULT_TIER


def is_support_page(filename):
    return any(re.search(p, os.path.basename(filename)) for p in SKIP_PATTERNS)


def main():
    errors, warnings = [], []

    for root, dirs, files in os.walk(APPS_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'new']
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, APPS_DIR)

            if is_support_page(f):
                continue

            tier = get_tier(f)
            tier_num = TIER_ORDER.get(tier, DEFAULT_TIER)

            with open(fpath, 'r') as fp:
                html = fp.read()

            has_markers = 'data-flove-css' in html or 'data-flove-js' in html
            has_loader = 'flove-loader.js' in html
            has_lib_base = 'flove:lib-base' in html

            if tier_num >= PRO_MIN:
                if not has_markers:
                    errors.append(f'{rel} ({tier}): pro tier missing enrichment markers (data-flove-css/data-flove-js)')
                elif not has_loader:
                    warnings.append(f'{rel} ({tier}): has markers but missing flove-loader.js ref')
                if has_markers and not has_lib_base:
                    warnings.append(f'{rel} ({tier}): has markers but no <meta name="flove:lib-base">')
            else:
                if has_markers and 'flove:enrich-optin' not in html:
                    errors.append(f'{rel} ({tier}): has enrichment but no opt-in comment (add <!-- flove:enrich-optin -->)')

    if errors or warnings:
        print('=== flove-loader-check ===')
        for e in errors:
            print(f'  ERROR: {e}')
        for w in warnings:
            print(f'  WARN:  {w}')
        print(f'\n{len(errors)} errors, {len(warnings)} warnings')
        return 1 if errors else 0
    else:
        print('flove-loader-check: all apps OK')
        return 0


if __name__ == '__main__':
    sys.exit(main())
