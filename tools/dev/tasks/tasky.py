#!/usr/bin/env python3
"""tasky — public read-only task-picker; `flove` is the default profile.

Nothing here edits any file. A profile maps an advanced context bundle to paths;
in flove the PROC policy lives in development/AGENTS.md (parsed by
procedures_source) and milestones.json owns only hitos and tasks. The tool turns
that ground into one decision: `pick` gives the next ready task, `next` shows the
window, `show` proves readiness, `context` loads the bundle, `audit` checks
window hygiene and reports the registered C6 exceptions on request. PROC-07 is
advisory: state inversions never warn in routine checks and never fail a gate.
Gates are the existing checkers.

    python3 tools/dev/tasks/tasky.py pick [--all] [--skip ID ...] [--include-bookkeeping]
      (.3c/.3b/.3 scaffold tasks are skipped by default — decision, publish check
       and canonical index already exist in the hito notes and owner doc)
    python3 tools/dev/tasks/tasky.py next [N] [--all] [--ready] [--do]
    python3 tools/dev/tasks/tasky.py easy [N] [--batch N]
      (count of easiest tasks, ready now; proposes batches — read-only)
    python3 tools/dev/tasks/tasky.py questy
    python3 tools/dev/tasks/tasky.py rewindow [N] [--survey] [--impact]
    python3 tools/dev/tasks/tasky.py context [flove]
    python3 tools/dev/tasks/tasky.py show <task-id>
    python3 tools/dev/tasks/tasky.py weight <task-id>
    python3 tools/dev/tasks/tasky.py options <task-id>
    python3 tools/dev/tasks/tasky.py procedure [PROC-ID]
    python3 tools/dev/tasks/tasky.py audit
    python3 tools/dev/tasks/tasky.py card
    python3 tools/dev/tasks/tasky.py check
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import procedures_source
import register_projection as projection

ROOT = Path(__file__).resolve().parents[3]
REGISTER = ROOT / 'development/tasks/milestones.json'
CARD_TEXT = """Work ONE ready task by the canonical procedure in development/AGENTS.md.
1. python3 tools/dev/tasks/tasky.py pick          # one decision, window first
2. python3 tools/dev/tasks/tasky.py show <id>     # criterion, owner, proof
3. Check the proof lines: owner exists, depends satisfied, pointer present (08).
4. Deliver in the owner doc; run its checker (PROC 01-06 in tasky SKILL.md §2).
5. Verify the pointer; move state to hecha automatically (no ask), record the
   Decision; parcial names what remains (08). `tasky.py easy` counts easiest
   tasks and proposes batches; `next --do` queues them with direct + easy.
6. python3 tools/dev/tasks/tasky.py check         # four register gates
7. Work Done -> Export moves -> tasks-moves.json -> --apply-moves --commit;
   regenerate common.json and the Work block; keep ~30 window tasks (09).
8. Report changes, checkers, dirty files, next task. No git commit unless asked.
Full policy: python3 tools/dev/tasks/tasky.py procedure
"""
EFFORT = {'easiest': 1, 'easy': 2, 'medium': 3, 'hard': 4, 'hardest': 5}
EASY = 'easiest'
GENERIC = 'Done when the local definition of'

# A profile is the adapter: it maps the questy-all Context tree chapters and the
# Plan/Work tab content managers to real paths. The core below stays generic.
PROFILES = {
    'flove': {
        'register': 'development/tasks/milestones.json',
        'tree': [
            ('standards', 'development/standards'),
            ('plans', 'development/plans'),
            ('questy-docs', ''),
            ('questy-pending', 'development/tasks/pendings.md'),
            ('conflicts', 'development/plans/conflicts.md'),
            ('proposals', 'development/archive/old/proposals.md'),
            ('questy-agents', 'development/archive/old/agents.md'),
        ],
        'tabs': [
            ('plan index', 'development/INDEX.md'),
            ('work authority', 'development/INDEX.md'),
            ('work content plan', 'development/tasks/measures.md'),
            ('register', 'development/tasks/milestones.json'),
            ('work builder', 'tools/dev/tasks/build-work-tracker.py'),
            ('join builder', 'tools/dev/tasks/build-common.py'),
            ('surface', 'development/index.html'),
        ],
    },
}


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
    """PROC-07 unlock rank; the shared projection is the single source."""
    return projection.unlocked_by(register)


def impact_index(register: dict) -> projection.ImpactIndex:
    """PROC-10 question depth, computed from the same register."""
    return projection.ImpactIndex(register)


def proc07_key(pair: tuple[dict, dict], unlock: Counter) -> tuple:
    """PROC-07: unlock rank, then effort, then stable ids. Advisory only."""
    m, t = pair
    return (-unlock[m['id']], EFFORT.get(t.get('effort'), 9),
            m['id'], t['id'])


def window(register: dict) -> list[str]:
    return list((register.get('taskSet', {}).get('activeWindow') or {}).get('order') or [])


def states(register: dict) -> dict:
    return {t['id']: t.get('state') for _, t in rows(register)}


def criterion(task: dict) -> str:
    return str((((task.get('evidence') or {}).get('gaps') or [''])[0]) or '').strip()


def is_generic(task: dict) -> bool:
    return not criterion(task) or criterion(task).startswith(GENERIC)


def blockers(task: dict, state: dict) -> list[str]:
    return [d for d in (task.get('depends_on') or []) if state.get(d) != 'hecha']


def owner_ok(task: dict) -> bool:
    return bool(task.get('owner')) and (ROOT / task['owner']).exists()


def pointer(task: dict) -> str:
    p = (task.get('evidence') or {}).get('pointer') or {}
    return '%s=%s' % (p.get('kind'), p.get('value')) if p.get('kind') and p.get('value') else 'missing'


def ready(task: dict, state: dict) -> bool:
    return not blockers(task, state) and not is_generic(task)


def candidates(register: dict, unlock: Counter, all_queue: bool) -> list[tuple[dict, dict]]:
    pairs = [(m, t) for m, t in rows(register)
             if m.get('state') != 'on' and t.get('state') in ('pendiente', 'parcial')]
    if all_queue:
        return sorted(pairs, key=lambda p: proc07_key(p, unlock))
    by_id = {t['id']: (m, t) for m, t in pairs}
    return [by_id[i] for i in window(register) if i in by_id]


def status(task: dict, state: dict) -> str:
    parts = []
    if blockers(task, state):
        parts.append('BLOCKED:' + ','.join(blockers(task, state)))
    if is_generic(task):
        parts.append('SPEC')
    return ' '.join(parts) or 'READY'


def cmd_next(args: argparse.Namespace) -> int:
    reg = load()
    unlock = unlocked_by(reg)
    ci = impact_index(reg)
    state = states(reg)
    win = window(reg)
    do = getattr(args, 'do', False)
    if do:
        # PROC-10: the "just do the easy ones" queue — no decision to settle.
        ordered = [p for p in candidates(reg, unlock, True)
                   if ready(p[1], state) and p[1].get('effort') in (EASY, 'easy')
                   and ci.weight(p[0], p[1])['class'] == 'direct']
        ordered.sort(key=lambda p: proc07_key(p, unlock))
    else:
        ordered = candidates(reg, unlock, args.all)
        if args.ready:
            ordered = [p for p in ordered if ready(p[1], state)]
    ts = reg.get('taskSet', {})
    print('%s — advisory, no state changes'
          % ('PROC-10 do queue: direct + easiest/easy, PROC-07 order' if do
             else 'PROC-07 order: unlock rank → effort → id' if args.all
             else 'Reviewed window: activeWindow.order'))
    print('live %s / archived %s · window %d · queued %d · shown %d'
          % (ts.get('live'), ts.get('archived'), len(win),
             len(candidates(reg, unlock, True)), min(args.n, len(ordered))))
    print('w=window position (00 = outside) · u=open-hito unlock · '
          'c=impact · READY/BLOCKED/SPEC')
    print()
    for rank, (m, t) in enumerate(ordered[:args.n], 1):
        wpos = win.index(t['id']) + 1 if t['id'] in win else 0
        crit = criterion(t)
        print('%2d. %-18s w%02d u=%d %-11s %-7s %-13s %s'
              % (rank, t['id'], wpos, unlock[m['id']], t.get('effort'),
                 t.get('stage'), ci.weight(m, t)['class'], m.get('en', '')[:46]))
        print('    %s%s' % (crit[:104], '…' if len(crit) > 104 else ''))
        print('    owner=%s  hito=%s  %s  %s'
              % (t.get('owner') or '(unset)', m['id'], status(t, state),
                 'WINDOW' if wpos else ''))
    return 0


def cmd_easy(args: argparse.Namespace) -> int:
    """Read-only inventory of easiest tasks, with directly-doable batches."""
    reg = load()
    unlock = unlocked_by(reg)
    state = states(reg)
    win = window(reg)
    ci = impact_index(reg)
    total = sum(1 for _, t in rows(reg) if t.get('effort') == EASY)
    pool = [(m, t) for m, t in candidates(reg, unlock, True)
            if t.get('effort') == EASY and ready(t, state)
            and not t['id'].endswith(BOOKKEEPING)]
    pool.sort(key=lambda p: proc07_key(p, unlock))
    adjacent = [(m, t) for m, t in candidates(reg, unlock, True)
                if t.get('effort') == 'easy' and ready(t, state)
                and ci.weight(m, t)['class'] == 'direct']
    print('effort ladder — 1 easiest · 2 easy · 3 medium · 4 hard · '
          '5 hardest (canonical English; Spanish only in the UI)')
    print('in register %d · ready now %d · in window %d · '
          'direct+easy queue %d'
          % (total, len(pool), sum(1 for _, t in pool if t['id'] in win),
             len(adjacent)))
    if not pool:
        print('no ready easiest task — `tasky.py next --do` queues direct+easy')
        return 0
    shown = pool[:args.n]
    for start in range(0, len(shown), args.batch):
        batch = shown[start:start + args.batch]
        print('\nbatch %d — %d task(s), PROC-07 order'
              % (start // args.batch + 1, len(batch)))
        for m, t in batch:
            print('   %-18s u=%d · %s'
                  % (t['id'], unlock[m['id']], criterion(t)[:72]))
    print('\nwork one batch with `tasky.py show <id>`; the state move is '
          'automatic once the pointer verifies')
    return 0


def cmd_pick(args: argparse.Namespace) -> int:
    reg = load()
    unlock = unlocked_by(reg)
    ci = impact_index(reg)
    state = states(reg)
    win = window(reg)
    skip = set(args.skip or [])
    ordered = [(m, t) for m, t in candidates(reg, unlock, args.all)
               if t['id'] not in skip
               and (args.include_bookkeeping
                    or not t['id'].endswith(BOOKKEEPING))]
    hit = next(((m, t) for m, t in ordered if ready(t, state)), None)
    if hit is None:
        print('no ready task in this queue — run `tasky.py audit` or `tasky.py next --all`')
        return 0
    m, t = hit
    wpos = win.index(t['id']) + 1 if t['id'] in win else 0
    print('pick    %s  [hito %s · %s · %s]'
          % (t['id'], m['id'], t.get('effort'), t.get('stage')))
    w = ci.weight(m, t)
    print('why     u=%d · w%02d · c=%s (%dq) · owner %s [exists: %s] · %s'
          % (unlock[m['id']], wpos, w['class'], w['depth'],
             t.get('owner'), 'yes' if owner_ok(t) else 'NO', status(t, state)))
    print('done    %s' % criterion(t)[:120])
    print('next    python3 tools/dev/tasks/tasky.py show %s' % t['id'])
    return 0


def cmd_questy(_args: argparse.Namespace) -> int:
    """Read-only question batch for a heavy shortlist (AGENTS 12.3 format)."""
    reg = load()
    unlock = unlocked_by(reg)
    state = states(reg)
    ordered = candidates(reg, unlock, False)
    blocked = [(m, t) for m, t in ordered if blockers(t, state)]
    vague = [(m, t) for m, t in ordered if is_generic(t)]
    hard = [(m, t) for m, t in ordered if ready(t, state)
            and t.get('effort') in ('hard', 'hardest')]
    easy = [(m, t) for m, t in ordered if ready(t, state)
            and t.get('effort') in (EASY, 'easy')]
    heavy = (len(blocked) + len(vague) > len(easy)) or (not easy and bool(hard))
    print('questy — read-only · window %d · ready-easy %d · blocked %d · '
          'vague %d · ready-hard %d · %s'
          % (len(window(reg)), len(easy), len(blocked), len(vague), len(hard),
             'HEAVY' if heavy else 'LIGHT'))
    if not heavy:
        print('shortlist is light — run `tasky.py pick` and work the winner')
        return 0
    n = 1
    if blocked:
        print('\n%d. Which blocked task should be unblocked first?' % n)
        k = 1
        for m, t in blocked[:3]:
            print('   %d.%d %s ← %s (u=%d)' %
                  (n, k, t['id'], ','.join(blockers(t, state)), unlock[m['id']]))
            k += 1
        print('   %d.%d none — leave blockers in place' % (n, k))
        n += 1
    if vague:
        print('\n%d. Which vague criterion should be specified first?' % n)
        k = 1
        for _, t in vague[:3]:
            print('   %d.%d %s — "%s"' % (n, k, t['id'], criterion(t)[:64]))
            k += 1
        print('   %d.%d none — keep criteria as they are' % (n, k))
        n += 1
    if hard:
        print('\n%d. Take a hard ready task now?' % n)
        k = 1
        for _, t in hard[:3]:
            print('   %d.%d %s (%s, w%02d)' % (n, k, t['id'], t.get('effort'),
                                               window(reg).index(t['id']) + 1))
            k += 1
        print('   %d.%d no — keep the window as is' % (n, k))
        n += 1
    print('\n%d. Re-rank the window instead?' % n)
    print('   %d.1 yes — run `tasky.py audit`, then re-rank activeWindow.order' % n)
    print('   %d.2 no' % n)
    print('\nreply with one option number per question, in order (AGENTS §12.3)')
    return 0


BOOKKEEPING = ('.3c', '.3b', '.3')


def cmd_rewindow(args: argparse.Namespace) -> int:
    """Print a read-only proposed window of genuine work for the owner to choose."""
    reg = load()
    unlock = unlocked_by(reg)
    state = states(reg)
    win = set(window(reg))
    pairs = [(m, t) for m, t in rows(reg)
             if m.get('state') != 'on' and t.get('state') in ('pendiente', 'parcial')
             and ready(t, state) and not t['id'].endswith(BOOKKEEPING)
             and t['id'] not in win]
    ci = impact_index(reg)
    use_impact = getattr(args, 'impact', False)
    if use_impact:
        # PROC-10 first: the decisions worth asking about rise to the top.
        pairs.sort(key=lambda p: (-projection.IMPACT_CLASSES.index(
            ci.weight(p[0], p[1])['class']), proc07_key(p, unlock)))
    else:
        pairs.sort(key=lambda p: proc07_key(p, unlock))
    show = pairs[:args.n]
    print('rewindow — read-only, changes nothing · ready non-bookkeeping outside window %d'
          % len(pairs))
    print('rank by %s · select by number; no register edit'
          % ('PROC-10 impact → PROC-07 (unlock → effort → id)' if use_impact
             else 'PROC-07 (unlock → effort → id)'))
    print()
    if args.survey:
        print('questy source — Q001 with %d options · answer 1-%d · '
              '`0` = all ★ · `-` = skip · questy batches in groups of 3'
              % (len(show), len(show)))
        print('c=impact: direct 0 · simple/branched 1 · '
              'complex/structuring 3 (questy-all batch)')
        print('next after answer: python3 tools/dev/tasks/tasky.py options <id>')
        print()
        print('Q001 Which task should I work?')
        for rank, (m, t) in enumerate(show, 1):
            star = ' (Recommended)' if rank == 1 else ''
            w = ci.weight(m, t)
            print('  %2d. %s%s — u=%d %s · c=%s (%dq) · owner %s'
                  % (rank, t['id'], star, unlock[m['id']], t.get('effort'),
                     w['class'], w['depth'], t.get('owner')))
            print('      Ref: hito %s · Affects: %s' % (m['id'], t.get('owner')))
            print('      done: %s' % criterion(t)[:96])
        print('\nanswer grammar: `3` = one · `0` = all ★ · `-` = skip · '
              '`python3 tools/dev/tasks/tasky.py options <id>` for A/B/C')
        return 0
    for rank, (m, t) in enumerate(show, 1):
        print('%2d. %-18s u=%d %-11s %-7s %-13s owner %s'
              % (rank, t['id'], unlock[m['id']], t.get('effort'), t.get('stage'),
                 ci.weight(m, t)['class'], t.get('owner')))
        print('    %s' % criterion(t)[:100])
        print('    hito %s — %s' % (m['id'], m.get('en', '')[:64]))
    print('\nto inspect: python3 tools/dev/tasks/tasky.py show <id>')
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    reg = load()
    hit = [(m, t) for m, t in rows(reg) if t['id'] == args.task_id]
    if not hit:
        print('unknown live task: ' + args.task_id, file=sys.stderr)
        return 1
    m, t = hit[0]
    state = states(reg)
    wgt = impact_index(reg).weight(m, t)
    wpos = window(reg).index(t['id']) + 1 if t['id'] in window(reg) else 0
    bl = blockers(t, state)
    print('task     %s  [%s / %s / %s]' % (t['id'], m['id'], t.get('stage'),
                                          t.get('effort')))
    print('title    %s' % t.get('en'))
    print('state    %s' % t.get('state'))
    print('owner    %s  [exists: %s]' % (t.get('owner'), 'yes' if owner_ok(t) else 'NO'))
    print('depends  %s  [%s]' % (', '.join(t.get('depends_on') or []) or 'none',
                                'BLOCKED:' + ','.join(bl) if bl else 'satisfied'))
    print('pointer  %s' % pointer(t))
    print('window   %s' % ('w%02d' % wpos if wpos else 'not in window'))
    print('impact   %s · score %d · %d question(s) · %s'
          % (wgt['class'], wgt['score'], wgt['depth'],
             ', '.join(wgt['reasons']) or 'no graph signal'))
    if wgt['override']:
        print('override %s — %s' % (wgt['override'], wgt['impact_reason']))
    print('done     %s' % criterion(t))
    print('hito     %s — %s' % (m['id'], m.get('en')))
    print('notes    %s' % (m.get('notes') or '').strip())
    print('source   %s' % m.get('source'))
    print('\napplicable procedures:')
    for p in procedures_source.load():
        if p['id'] in ('PROC-07', 'PROC-08', 'PROC-09', 'PROC-01') or \
                (args.task_id.endswith('.3') and p['id'] == 'PROC-03'):
            print('  %s  %s  [checker %s]' % (p['id'], p['title'], p.get('checker')))
    print('\nfull policy: python3 tools/dev/tasks/tasky.py procedure')
    return 0


def find_task(task_id: str) -> tuple[dict, dict] | None:
    reg = load()
    return next(((m, t) for m, t in rows(reg) if t['id'] == task_id), None)


def cmd_weight(args: argparse.Namespace) -> int:
    """PROC-10: how much should be asked before this task is worked."""
    hit = find_task(args.task_id)
    if hit is None:
        print('unknown live task: ' + args.task_id, file=sys.stderr)
        return 1
    m, t = hit
    w = impact_index(load()).weight(m, t)
    print('weight   %s  [hito %s · %s · %s]'
          % (t['id'], m['id'], t.get('stage'), t.get('effort')))
    print('class    %s · score %d · %d question(s)'
          % (w['class'], w['score'], w['depth']))
    print('signals  u=%d (hito unlock) · g=%d (deps generated) · '
          'fan-out=%d · owner=%s%s'
          % (w['unlock'], w['generated'], w['fanout'], t.get('owner') or '(unset)',
             ' · canonical ' + w['canonical'] if w['canonical'] else ''))
    print('why      %s' % (', '.join(w['reasons']) or 'no graph signal'))
    print('decision %s' % (w['decision'] or '(none in hito notes)'))
    if w['override']:
        print('override %s — %s' % (w['override'], w['impact_reason']))
    else:
        print('override none — set impact_override + impact_reason in %s to tune'
              % t['id'])
    print('next     python3 tools/dev/tasks/tasky.py options %s' % t['id'])
    return 0


def cmd_options(args: argparse.Namespace) -> int:
    """Offer default solutions, hard-dependency handling and user override."""
    hit = find_task(args.task_id)
    if hit is None:
        print('unknown live task: ' + args.task_id, file=sys.stderr)
        return 1
    m, t = hit
    w = impact_index(load()).weight(m, t)
    a, b = projection.decision_options(w['decision'])
    b = b or 'Do one case now; park the rest in tasks/pendings.md'
    print('options  %s · %s · %d question(s) — A/B/C; ★ states reason + con'
          % (t['id'], w['class'], w['depth']))
    print('  A ★ keep the declared graph and the owner default: %s'
          % (a or 'apply the hito Done-when as written'))
    print('      why: no register churn, owner default stands.')
    print('      con: an open Decision stays unresolved until recorded in the owner doc.')
    print('  B   take the alternative: %s' % b)
    print('      why: settles the open Decision in the owner doc.')
    print('      con: needs an owner-doc edit and a second verification pass.')
    print('  C   hard-register the chosen edge in depends_on with '
          'impact_reason; owner signs at review')
    print('      why: the dependency becomes machine-checkable in the graph.')
    print('      con: changes PROC-07 order; a wrong edge needs a review to undo.')
    if w['depth']:
        print()
        print('Q1 Which solution? 1=A ★ · 2=B · 3=C')
        print('   Ref: %s · Affects: %s' % (m['id'], t.get('owner')))
    if w['depth'] == 3:
        edges = [str(d) for d in (m.get('depends_on') or [])] + \
                [str(d) for d in (t.get('depends_on') or [])]
        print()
        print('Q2 Which dependencies are hard-registered?')
        for i, edge in enumerate(dict.fromkeys(edges), 1):
            print('   %d. %s' % (i, edge))
        print('   %d. none — keep the graph advisory (Recommended)' % (len(set(edges)) + 1))
        print()
        print('Q3 Who records the decision?')
        print('   1. %s (owner) ★' % (t.get('owner') or '(unset)'))
        print('   2. reviewer in activeWindow.reviewedBy')
        print('   3. tasks/pendings.md — no register change')
    if not w['depth']:
        print('\nno decision to settle — work it; `tasky.py next --do` queues these')
    print('\ntune: set impact_override + impact_reason in %s (milestones.json); '
          'the gate keeps your class' % t['id'])
    return 0


def cmd_procedure(args: argparse.Namespace) -> int:
    procs = procedures_source.load()
    for p in procs:
        if args.proc_id and p['id'] != args.proc_id:
            continue
        print('%s — %s' % (p['id'], p['title']))
        print('  standard : %s' % p.get('standard'))
        print('  checker  : %s' % p.get('checker'))
        print('  done     : %s' % p.get('definition_of_done'))
        print('  advice   : %s' % p.get('advice'))
        print('  inputs   : %s' % p.get('inputs'))
        print('  outputs  : %s' % p.get('outputs'))
        print('  gates    : %s' % p.get('gates'))
        print()
    if args.proc_id and not any(p['id'] == args.proc_id for p in procs):
        print('unknown procedure: ' + args.proc_id, file=sys.stderr)
        return 1
    return 0


def registered_c6() -> set[tuple[str, str]]:
    """Edges registered as C6 exceptions in tasks/measures.md (the one home)."""
    text = (ROOT / 'development/tasks/measures.md').read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.startswith('| C6 |'):
            return set(re.findall(r'`([\w-]+)`←`([\w-]+)`', line))
    return set()


def c6_inversions(reg: dict) -> set[tuple[str, str]]:
    """Hito edges whose dependiente is further along than its prerequisite."""
    hitos = [m for area in reg.get('sections', [])
             for box in area.get('subsections', [])
             for m in box.get('milestones', [])]
    state = {m['id']: m.get('state') for m in hitos}
    rank = {'todo': 0, 'part': 1, 'on': 2}
    return {(m['id'], dep) for m in hitos for dep in (m.get('depends_on') or [])
            if rank.get(m.get('state'), -1) > rank.get(state.get(dep), -1)}


def cmd_audit(_args: argparse.Namespace) -> int:
    reg = load()
    pairs = rows(reg)
    state = states(reg)
    archived = {a.get('id') for a in (reg.get('tasks_archive') or [])}
    stale = [t['id'] for _, t in pairs if is_generic(t)]
    missing = [t['id'] for _, t in pairs if not owner_ok(t)]
    closed = [(t['id'], d) for _, t in pairs
              for d in (t.get('depends_on') or []) if d in archived]
    print('audit — read-only window hygiene + registered C6 exceptions')
    print('generic criteria %d · missing owners %d · closed-hito deps %d'
          % (len(stale), len(missing), len(closed)))
    for label, items in (('spec', stale), ('owner', missing),
                         ('closed', ['%s→%s' % pair for pair in closed])):
        if items:
            print('%s: %s%s' % (label, ', '.join(items[:8]),
                                ' …' if len(items) > 8 else ''))
    print('window %d · reviewed %s by %s'
          % (len(window(reg)),
             (reg.get('taskSet', {}).get('activeWindow') or {}).get('reviewed'),
             (reg.get('taskSet', {}).get('activeWindow') or {}).get('reviewedBy')))
    # Q130/Q143: reported only here, on request. State inversions are advisory;
    # never a warning in --check and never a failed gate in tasky.
    inv, expect = c6_inversions(reg), registered_c6()
    fmt = lambda edges: ', '.join('%s←%s' % e for e in sorted(edges)) or 'none'
    print('C6: %d inversions · %d registered · advisory only'
          % (len(inv), len(expect)))
    if inv != expect:
        print('  new: %s' % fmt(inv - expect))
        print('  resolved: %s' % fmt(expect - inv))
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    """Load a profile's advanced bundle: questy-all tree + Plan/Work managers."""
    profile = PROFILES.get(args.profile)
    if profile is None:
        print('unknown profile %r — known: %s'
              % (args.profile, ', '.join(PROFILES)), file=sys.stderr)
        return 1
    print('context — profile %s · read-only · source of the survey ground'
          % args.profile)
    counts = {'OK': 0, 'missing': 0, 'N/A': 0}
    for group in ('tree', 'tabs'):
        for label, rel in profile[group]:
            state = 'N/A' if not rel else ('OK' if (ROOT / rel).exists() else 'missing')
            counts[state] += 1
            print('%s  %-20s %s' % (state, label, rel or 'not present in this profile'))
    print('loaded %d · missing %d · N/A %d'
          % (counts['OK'], counts['missing'], counts['N/A']))
    print('next  python3 tools/dev/tasks/tasky.py rewindow --survey')
    return 0


def cmd_card(_args: argparse.Namespace) -> int:
    print(CARD_TEXT, end='')
    return 0


def cmd_check(_args: argparse.Namespace) -> int:
    gates = [
        'tools/dev/tasks/build-work-tracker.py --check',
        'tools/dev/tasks/build-common.py --check',
        'tools/dev/checks/jsony.py --no-write',
        'tools/dev/tasks/check-restore.py',
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


def positive_int(value: str) -> int:
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError('must be > 0')
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--profile', default='flove',
                    help='context profile (default flove); selects the register')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('pick', help='one ready task with its rationale')
    p.add_argument('--all', action='store_true', help='rank the whole queue, not the window')
    p.add_argument('--skip', action='append', metavar='ID', default=[],
                   help='exclude an id (repeatable), e.g. an already-satisfied pick')
    p.add_argument('--include-bookkeeping', action='store_true',
                   help='include .3c/.3b/.3 scaffold tasks (skipped by default)')
    p.set_defaults(fn=cmd_pick)
    p = sub.add_parser('next', help='reviewed window or full PROC-07 order')
    p.add_argument('n', nargs='?', type=int, default=10)
    p.add_argument('--all', action='store_true', help='rank the whole queue')
    p.add_argument('--ready', action='store_true', help='hide blocked and vague tasks')
    p.add_argument('--do', action='store_true',
                   help='PROC-10 do queue: direct + easiest/easy, no decision')
    p.set_defaults(fn=cmd_next)
    p = sub.add_parser('easy', help='count easiest tasks and propose batches')
    p.add_argument('n', nargs='?', type=int, default=30)
    p.add_argument('--batch', type=positive_int, default=10,
                   help='tasks per proposed batch (default 10)')
    p.set_defaults(fn=cmd_easy)
    p = sub.add_parser('questy', help='question batch when the shortlist is heavy')
    p.set_defaults(fn=cmd_questy)
    p = sub.add_parser('rewindow', help='read-only proposed window of genuine work')
    p.add_argument('n', nargs='?', type=int, default=30)
    p.add_argument('--survey', action='store_true',
                   help='render candidates as questy source (Q001, 30 options)')
    p.add_argument('--impact', action='store_true',
                   help='rank by PROC-10 impact before PROC-07')
    p.set_defaults(fn=cmd_rewindow)
    p = sub.add_parser('context', help='load a profile bundle (default flove)')
    p.add_argument('profile', nargs='?', default='flove')
    p.set_defaults(fn=cmd_context)
    p = sub.add_parser('show', help='one task with proof of readiness')
    p.add_argument('task_id')
    p.set_defaults(fn=cmd_show)
    p = sub.add_parser('weight', help='PROC-10 class, score and question depth')
    p.add_argument('task_id')
    p.set_defaults(fn=cmd_weight)
    p = sub.add_parser('options', help='A/B/C solutions, hard deps and override')
    p.add_argument('task_id')
    p.set_defaults(fn=cmd_options)
    p = sub.add_parser('procedure', help='print a PROC block from AGENTS.md')
    p.add_argument('proc_id', nargs='?')
    p.set_defaults(fn=cmd_procedure)
    p = sub.add_parser('audit', help='read-only window hygiene report')
    p.set_defaults(fn=cmd_audit)
    p = sub.add_parser('card', help='print the short work card')
    p.set_defaults(fn=cmd_card)
    p = sub.add_parser('check', help='run the four register gates')
    p.set_defaults(fn=cmd_check)
    args = ap.parse_args()
    profile = PROFILES.get(args.profile)
    if profile is None:
        ap.error('unknown profile %r — known: %s'
                 % (args.profile, ', '.join(PROFILES)))
    globals()['REGISTER'] = ROOT / profile['register']
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
