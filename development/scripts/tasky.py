#!/usr/bin/env python3
"""tasky — read-only task-queue helper for the flove register.

Nothing here edits any file. The canonical PROC policy lives in
development/AGENTS.md and is parsed by procedures_source; milestones.json owns
only hitos and tasks. This tool prints the PROC-07 queue, a task's context, the
live chapter and the short work card. Gates are the existing checkers.

    python3 development/scripts/tasky.py next [N]
    python3 development/scripts/tasky.py show <task-id>
    python3 development/scripts/tasky.py procedure [PROC-ID]
    python3 development/scripts/tasky.py card
    python3 development/scripts/tasky.py check
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import procedures_source

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / 'development/standards/debates/milestones.json'
CARD_TEXT = """Work ONE ongoing task from milestones.json by the canonical procedure.
1. python3 development/scripts/tasky.py next          # PROC-07 order
2. Pick one; check hito and task depends_on. Never change stage/state to pick.
3. python3 development/scripts/tasky.py show <chosen-id>
   -> Deliverable / Done when / Decision, done-criterion, owner path.
4. Deliver in the owner doc; run its checker (PROC 01-06 in tasky SKILL.md #2).
5. Attach a followable evidence pointer; parcial names what remains (08).
6. python3 development/scripts/tasky.py check         # four register gates
7. Work Done -> Export moves -> reviewed work-moves.json -> --apply-moves --commit;
   regenerate common.json and the Work block; keep ~30 window tasks (09).
8. Report changes, checkers, dirty files, next task. No commit unless asked.
Full policy: python3 development/scripts/tasky.py procedure
"""
EFFORT = {'fácil': 0, 'difícil': 1, 'muy difícil': 2}
STAGES = ['seed', 'infant', 'mature', 'grown', 'full']


def load() -> dict:
    return json.loads(REGISTER.read_text(encoding='utf-8'))


def rows(register: dict) -> list[tuple[dict, dict]]:
    """(hito, task) pairs, in register order."""
    return [(m, t)
            for area in register.get('sections', [])
            for box in area.get('subsections', [])
            for m in box.get('milestones', [])
            for t in (m.get('tasks') or [])]


def unlocked_by(register: dict) -> Counter:
    hitos = [m for area in register.get('sections', [])
             for box in area.get('subsections', [])
             for m in box.get('milestones', [])]
    open_ids = {m['id'] for m in hitos if m.get('state') != 'on'}
    return Counter(dep for m in hitos if m.get('state') != 'on'
                   for dep in (m.get('depends_on') or [])
                   if dep in open_ids)


def proc07_key(pair: tuple[dict, dict], unlock: Counter) -> tuple:
    """PROC-07: unlock rank, then effort, then stable ids. Advisory only."""
    m, t = pair
    return (-unlock[m['id']], EFFORT.get(t.get('effort'), 9),
            m['id'], t['id'])


def cmd_next(args: argparse.Namespace) -> int:
    reg = load()
    unlock = unlocked_by(reg)
    pending = [(m, t) for m, t in rows(reg)
               if m.get('state') != 'on' and t.get('state') in ('pendiente', 'parcial')]
    pending.sort(key=lambda p: proc07_key(p, unlock))
    ts = reg.get('taskSet', {})
    window = set((ts.get('activeWindow') or {}).get('order') or [])
    print('PROC-07 order — advisory: unlock rank → effort → id; no state changes')
    print('live %s / archived %s · active window %s · queued %d'
          % (ts.get('live'), ts.get('archived'), len(window), len(pending)))
    print()
    for rank, (m, t) in enumerate(pending[:args.n], 1):
        criterion = (((t.get('evidence') or {}).get('gaps') or [''])[0]).strip()
        print('%2d. %-18s unlock=%d %-11s %-7s %s'
              % (rank, t['id'], unlock[m['id']], t.get('effort'),
                 t.get('stage'), m.get('en', '')[:52]))
        print('    %s%s' % (criterion[:104], '…' if len(criterion) > 104 else ''))
        print('    owner=%s  hito=%s  %s'
              % (t.get('owner') or '(unset)', m['id'],
                 'WINDOW' if t['id'] in window else ''))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    reg = load()
    hit = [(m, t) for m, t in rows(reg) if t['id'] == args.task_id]
    if not hit:
        print('unknown live task: ' + args.task_id, file=sys.stderr)
        return 1
    m, t = hit[0]
    print('task     %s  [%s / %s / %s]' % (t['id'], m['id'], t.get('stage'),
                                          t.get('effort')))
    print('title    %s' % t.get('en'))
    print('state    %s' % t.get('state'))
    print('owner    %s' % t.get('owner'))
    print('depends  %s' % ', '.join(t.get('depends_on') or []) or '(none)')
    print('done     %s' % (((t.get('evidence') or {}).get('gaps') or [''])[0]).strip())
    print('hito     %s — %s' % (m['id'], m.get('en')))
    print('notes    %s' % (m.get('notes') or '').strip())
    print('source   %s' % m.get('source'))
    print('\napplicable procedures:')
    for p in procedures_source.load():
        if p['id'] in ('PROC-07', 'PROC-08', 'PROC-09', 'PROC-01') or \
                (args.task_id.endswith('.3') and p['id'] == 'PROC-03'):
            print('  %s  %s  [checker %s]' % (p['id'], p['title'], p.get('checker')))
    print('\nfull policy: python3 development/scripts/tasky.py procedure')
    return 0


def cmd_procedure(args: argparse.Namespace) -> int:
    procs = procedures_source.load()
    for p in procs:
        if args.proc_id and p['id'] != args.proc_id:
            continue
        print('%s — %s' % (p['id'], p['title']))
        print('  standard : %s' % p.get('standard'))
        print('  checker  : %s' % p.get('checker'))
        print('  advice   : %s' % p.get('advice'))
        print('  inputs   : %s' % p.get('inputs'))
        print('  outputs  : %s' % p.get('outputs'))
        print('  gates    : %s' % p.get('gates'))
        print()
    if args.proc_id and not any(p['id'] == args.proc_id for p in procs):
        print('unknown procedure: ' + args.proc_id, file=sys.stderr)
        return 1
    return 0


def cmd_card(_args: argparse.Namespace) -> int:
    print(CARD_TEXT, end='')
    return 0


def cmd_check(_args: argparse.Namespace) -> int:
    gates = [
        'development/scripts/build-work-tracker.py --check',
        'development/scripts/build-common.py --check',
        'development/scripts/jsony_check.py',
        'development/scripts/check-restore.py',
    ]
    failed = 0
    for gate in gates:
        print('$ python3 ' + gate)
        r = subprocess.run([sys.executable] + gate.split(), cwd=ROOT,
                           capture_output=True, text=True)
        out = [line.strip() for line in (r.stdout + r.stderr).splitlines() if line.strip()]
        for line in out or ['(no output)']:
            print('  ' + line)
        failed += bool(r.returncode)
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('next', help='next tasks by PROC-07 order')
    p.add_argument('n', nargs='?', type=int, default=10)
    p.set_defaults(fn=cmd_next)
    p = sub.add_parser('show', help='one task with its hito context')
    p.add_argument('task_id')
    p.set_defaults(fn=cmd_show)
    p = sub.add_parser('procedure', help='print the canonical procedures chapter')
    p.add_argument('proc_id', nargs='?')
    p.set_defaults(fn=cmd_procedure)
    p = sub.add_parser('card', help='print the short work card')
    p.set_defaults(fn=cmd_card)
    p = sub.add_parser('check', help='run the four register gates')
    p.set_defaults(fn=cmd_check)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
