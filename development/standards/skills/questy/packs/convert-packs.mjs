#!/usr/bin/env node
/* Convert making-of sources into questy pack .js files.
   Usage: node convert-packs.mjs   (run from skills/questy/packs/)

   nety-spec: the feed's bullets are the options; the "★ decided" line is the
   made decision. The decided text is the SHORT form of the option (the part
   before " — "), and some decisions join several options with " · ". This
   converter matches decided → full option label(s) and emits them as `pre`
   so the dev page can pin the actual made decision on the card.
   Summary items (category "Notes") have no bullets — they get authored options
   from NETY_NOTES_OPTS, with the recap itself as the decided option.

   browsy-questions.md: the decisions table only records the made decision, so
   alternative options are authored here in BROWSY_ALTS (keyed by row id). Each
   question then renders as [decided, ...alternatives] with the decided answer
   as the loaded default. */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const HERE = dirname(new URL(import.meta.url).pathname);
const OUT = HERE + '/';
const FEEDS = resolve(HERE, '../../../debates/making-of/feeds/nety-spec.xml');
const BROWSY = resolve(HERE, '../../../debates/browsy/browsy-questions.md');
mkdirSync(OUT, { recursive: true });

/* ---------- hat heuristics (partial, first match wins) ---------- */
const HAT_MAP = [
  // facts — what we know, data, evidence
  [/^(content|state|memory|cache|data|compat|performance|perf|a11y|i18n|testing|test|log|analytics|documentation|docs|version|sync|schema|quota|metric|debug|storage|size|backward|bandwidth|protocol|settings|config|params|persistence|install|tech|stats|monitor|budget|cpu|memory|offline)/i, 'facts'],
  // heart — people, feelings, experience
  [/^(notif|ux|menu|badge|keyboard|onboard|first|dismiss|feedback|support|help|emotion|reaction|audio|voice|human|heritage|closest|friend|invites?)/i, 'heart'],
  // risk — threats, failure, security, moderation
  [/^(secur|privacy|encrypt|recover|revoc|vouch|trust|moder|abuse|resil|cras|conflict|error|rotat|permission|threat|fail|risk|sign|key|factor|identit|hierarchy|adjudic|grace|idle|revoke|claim|access)/i, 'risk'],
  // optimism — value, vision, benefits
  [/^(feature|strategy|multi|open source|release|growth|econom|benefit|vision|value|gain|monet|market|audience|engagement|ranking|telemetry|consent)/i, 'optimism'],
  // creative — design, wild ideas, aesthetics
  [/^(ui|design|theme|animat|overlay|visual|aesthetic|icon|creative|rainbow|vizy|viz|xr|game|playful|retro|maximal|kinetic|brand|slogan|name|naming|symbol|weight)/i, 'creative'],
  // make — structure, flow, connection, how it works
  [/^(integrat|plugin|manifest|api|lifecycle|messag|auth|publish|navigat|routing|frontend|backend|workflow|build|bridge|extension|architect|scope|structure|tier|loading|update|local-first|local|dev|side|popup|options|badge|timing|mechan|fork|standard|share|close|groups|social|circle|normal|super|advanced|mini|appy|browsy|p2p|agent|chat|dm|flow|hybrid|tab|panel|sync|storage|inject|demo|tree|scripts|format|brief|cross|oasis|native|notes)/i, 'make']
];
const hatFor = (cat) => {
  const c = String(cat).trim();
  for (const [re, h] of HAT_MAP) if (re.test(c)) return h;
  return '';
};

/* ---------- decided → full option label matching ---------- */
/* The feed records decisions in the option's SHORT form (before " — ") and
   joins multi-option decisions with " · ". Map back to the full labels. */
function shortOf(o) { return String(o).split(' — ')[0].trim(); }
function matchDecided(opts, decided) {
  if (!decided) return null;
  const whole = opts.find(o => o === decided || o.startsWith(decided + ' — ') || shortOf(o) === decided || shortOf(o).startsWith(decided));
  if (whole) return { labels: [whole] };
  const parts = decided.split('·').map(s => s.trim()).filter(Boolean);
  if (parts.length > 1) {
    const labels = [];
    const ok = parts.every(p => {
      const m = opts.find(o => o === p || o.startsWith(p + ' — ') || shortOf(o) === p || shortOf(o).startsWith(p));
      if (!m) return false;
      labels.push(m);
      return true;
    });
    if (ok) return { labels };
  }
  return null;
}

/* ---------- nety-spec.xml ---------- */
function parseFeed(file) {
  const xml = readFileSync(file, 'utf8');
  const items = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)];
  return items.map((m, i) => {
    const it = m[1];
    const title = (it.match(/<title>(.*?)<\/title>/s) || [])[1] || '';
    const cats = [...it.matchAll(/<category>(.*?)<\/category>/g)].map(c => c[1]);
    const desc = (it.match(/<description>(.*?)<\/description>/s) || [])[1] || '';
    const opts = desc.split('\n').map(l => l.trim()).filter(l => l.startsWith('• ')).map(l => l.slice(2).trim()).map(decode);
    const decidedM = desc.match(/★ decided: ([\s\S]*?)(?:<\/description>|$)/s);
    const decided = decidedM ? decode(decidedM[1].trim().replace(/<[^>]+>/g, '').trim()) : '';
    const sub = cats[1] || cats[0] || '';
    const match = matchDecided(opts, decided);
    return {
      id: (it.match(/<guid[^>]*>([\s\S]*?)<\/guid>/) || [])[1] || ('q' + (i + 1)),
      cat: sub, hat: hatFor(sub), q: decode(title.trim()), o: opts, a: decided,
      ...(match ? { pre: match.labels } : {})
    };
  });
}
function decode(s) { return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#039;/g, "'"); }

let netySpec = parseFeed(FEEDS);

/* Summary items (category "Notes") carry no bullets — author plausible options
   so they render as real questions, with the recap as the decided option. */
const NETY_NOTES_OPTS = {
  'nety-spec_q68': [
    'Two tiered domains, separate: nety = hardware quota ladder (compute/storage/AI/network), appy = software feature ladder (apps/data/profiles)',
    'One combined ladder covering hardware and software together',
    'nety (hardware) gates how high appy (software) can climb'
  ],
  'nety-spec_q69': [
    'Stages (newbie·known·homie·expert·legend) gate the tier ceiling; which tier you browse is your choice',
    'Each stage hard-locks you into its own tier',
    'Stages are cosmetic — no ceiling or gating at all'
  ],
  'nety-spec_q70': [
    'mini (nety) open — free client + contribute + web miniprofile; basic (appy) invite-gated for play & store',
    'Everything open and permissionless, including appy registration',
    'Everything invite-gated, even running the nety client'
  ],
  'nety-spec_q71': [
    'Four scoped facets: Personal=auth · Local=invite-net · Social=trusts · Global=contribs; Activity (presence) inside Global',
    'A single blended trust score instead of four facets',
    'Four facets plus Activity as a separate fifth stat'
  ],
  'nety-spec_q72': [
    'Identity rung weights low→high: social link (email-only) → social link (phone) → verified email → verified Telegram ✦ publish gate → verified phone → biometrics',
    'All identity rungs carry equal weight',
    'Weights stay hidden — only coarse tier badges are shown'
  ],
  'nety-spec_q73': [
    'Registration is invite-coded; publishing a static HTML page requires ≥ Telegram verification',
    'Open registration; publishing still requires ≥ Telegram verification',
    'Invite-coded registration but publishing needs no verification'
  ],
  'nety-spec_q74': [
    'Store integrates profily (extended profile) + puzzy/sety (settings) + wizy (agents)',
    'Store is apps-only; profile, settings and agents stay separate apps',
    'A single all-in-one account app replacing the three'
  ],
  'nety-spec_q75': [
    'MyNet spans both layers (f2f substrate in nety, custom circles in appy); MyWizy = your athen-ia finetuner, Wizy = the app',
    'MyNet lives only in the upper appy layer',
    'MyNet lives only in the lower nety infrastructure layer'
  ],
  'nety-spec_q76': [
    'Stages unlock more across both layers: further apps (upper) + further resources & donation directing (lower); donations can target a circle',
    'Stages unlock apps only — resources/donations stay flat',
    'Stages unlock resources only — apps stay open to everyone'
  ],
  'nety-spec_q77': [
    'Invites stay public/traceable for flagging, even though facet scores are owner-private',
    'Invites are private too; only scores are public',
    'Everything about a peer is public and traceable'
  ],
  'nety-spec_q78': [
    'flovenet apps INDEPENDENT — implemented natively, LEARNING oasis\'s good patterns; oasis is an optional add-on',
    'Build the apps layer on oasis/SSB as a hard dependency',
    'Fuse flovenet and oasis into a single stack'
  ],
  'nety-spec_q79': [
    'Bridge: one Ed25519 keypair → flovenet (lower) → GraphQL gateway (portable base) → upper layer; \'Circles\' is the user-facing name',
    'Separate keys per layer joined by a signed attestation',
    'Bridge at the app layer only — identities stay fully separate'
  ],
  'nety-spec_q80': [
    'MyWizy AI: flovenet-native local-first by default; oasis \'42\' an optional pluggable engine',
    'oasis \'42\' is the default inference engine',
    'A hosted cloud AI service powers MyWizy'
  ]
};
netySpec = netySpec.map(it => {
  const notesOpts = NETY_NOTES_OPTS[it.id];
  if (!notesOpts) return it;
  const o = [it.a, ...notesOpts];
  return { ...it, o, pre: [it.a] };
});

/* ---------- browsy-questions.md ---------- */
/* The decisions table only keeps the made decision; alternatives authored here
   (same voice, plausible paths the conversation could have taken). */
const BROWSY_ALTS = {
  'BD01': ['Reliability-first (never block the page)', 'Feature-complete regardless of speed'],
  'BD02': ['Menu item only', 'Toolbar button', 'No visible badge at all'],
  'BD03': ['Load on every page load', 'Defer to idle time', 'Load once at browser start'],
  'BD04': ['Simplicity-first', 'Feature-rich (more state)'],
  'BD05': ['Per-site limits', 'No limit (unbounded)', 'LRU eviction of old data'],
  'BD06': ['Custom context menu now', 'Keyboard shortcut only'],
  'BD07': ['Quick panel for frequent actions', 'Floating mini-bar on hover'],
  'BD08': ['Badge only', 'Notifications only', 'Neither — pull only'],
  'BD10': ['Trust changes only', 'Items only', 'None — you check manually'],
  'BD11': ['TTL-based expiry', 'Size-based eviction', 'No caching'],
  'BD12': ['Minimal permissions only', 'CSP only', 'Browser default protections only'],
  'BD13': ['Auto-update', 'Auto-update with visible changelog', 'Prompt before updating'],
  'BD14': ['Silent retry', 'Console only', 'Full error page'],
  'BD15': ['Local only (no encryption)', 'Encrypted and synced', 'Minimal data collection'],
  'BD16': ['Anonymous ID only', 'Account with email', 'Badges only'],
  'BD17': ['Minimal (content only)', 'Content + metadata', 'Per-site opt-in levels'],
  'BD18': ['Modern browsers only', 'Broad legacy support', 'Web-standards baseline'],
  'BD19': ['Lazy loading only', 'Cache only', 'Minimal (no extra machinery)'],
  'BD20': ['Keyboard only', 'ARIA only', 'Rely on browser defaults'],
  'BD21': ['English only', 'Auto-detect the browser language', 'All languages bundled'],
  'BD22': ['System theme only', 'Manual light/dark toggle', 'Custom user themes'],
  'BD23': ['No settings', 'Inline quick settings', 'Advanced config file'],
  'BD24': ['Storage only', 'Messaging only', 'No integration (isolated)'],
  'BD25': ['flove API only', 'Custom API only', 'No public API'],
  'BD26': ['User-managed (on/off)', 'Event-driven manual lifecycle'],
  'BD27': ['Unit tests only', 'Manual testing only', 'CI automation only'],
  'BD28': ['No logging', 'Log file export', 'Remote error reporting'],
  'BD29': ['No analytics', 'Minimal anonymous counters', 'Opt-out analytics'],
  'Q01': ['Keep minimal extraction (text only)', 'Keep full extraction', 'Defer the decision'],
  'Q02': ['Fixed threshold always', 'No threshold (fully open)', 'Threshold set by trust score'],
  'Q03': ['Storage + bandwidth only', 'Compute only', 'No P2P (cloud only)'],
  'Q04': ['Only the current tier visible', 'Locked tiers hidden entirely', 'Toggleable display'],
  'Q05': ['Dedicated P2P publish button', 'Auto-publish everything', 'Via the extension menu'],
  'Q06': ['Full agent control at all tiers', 'Preset agent personas', 'No agents at normal'],
  'Q07': ['Every page', 'Flove pages only', 'User-selected sites'],
  'Q08': ['Free for all tiers', 'Stays in normal', 'Super tier only'],
  'Q09': ['Keep the previous definition', 'Empty normal tier (placeholder)', 'Add more apps to normal'],
  'Q10': ['Online only', 'Cache visited pages only', 'Manual offline mode'],
  'Q11': ['Advanced = normal + data tools', 'Advanced = limited set', 'Super shares advanced\'s scope'],
  'Q12': ['Continuous live sync', 'Daily sync', 'Manual sync only'],
  'Q13': ['Full release notes in popup', 'Email alerts', 'No alerts'],
  'Q14': ['Design governance now', 'Minimal voting', 'Founder-only for now'],
  'Q15': ['Settings only', 'Alerts and settings in separate menus', 'Single combined menu'],
  'Q16': ['One agent', 'Full chat agent', 'No agents at normal'],
  'Q17': ['Chrome only', 'Chrome + Safari', 'All major browsers'],
  'Q18': ['Visualization only', 'Advanced features stay free', 'Super tier only'],
  'Q19': ['All pages', 'User-whitelisted sites', 'No injection (popup only)'],
  'Q20': ['No social identity at normal', 'Full MyNet at normal', 'Read-only social at normal'],
  'Q21': ['Feed only', 'Notifications only', 'No overlays at all'],
  'Q22': ['Vizy free for all', 'Vizy super only', 'No vizy'],
  'Q23': ['Mentions only', 'Trust changes only', 'No push — pull only'],
  'Q24': ['1 shape only', 'All shapes', '5 shapes'],
  'Q25': ['Auto-dismiss after a timeout', 'Dismiss on navigation', 'Dismiss on click outside'],
  'Q26': ['XR/VR later', 'No XR/VR', 'AR only'],
  'Q27': ['Floating popup window', 'Bottom sheet', 'Full-page overlay'],
  'Q28': ['No teasers', 'Live demos in mini', 'Teasers on all tiers'],
  'Q29': ['Soft cap with a warning', 'Hard cap (e.g. 100)', 'Cap set by the creator'],
  'Q30': ['One panel per overlay type', 'System-tray stacking', 'Always on top'],
  'Q31': ['All public content', 'Bookmarks only', 'User-defined sources'],
  'Q32': ['Remember the last state', 'Always start open', 'Auto-open on new content'],
  'Q33': ['Permanent forever', '7-day auto-delete', 'Manual deletion only'],
  'Q34': ['Plain text format', 'Native SSB post', 'Raw JSON blob'],
  'Q35': ['Settings toggle', 'Popup at first run', 'Per-agent buttons'],
  'Q36': ['Central verifies', 'Both client and central verify', 'No verification'],
  'Q37': ['Private / Public only', 'Private / Close / Public', 'Trust-tier based'],
  'Q38': ['Title-only index', 'Author/tags only', 'No indexing'],
  'Q39': ['Merge into one concept', 'Close = family; Related = friends', 'Tier-based'],
  'Q41': ['Group chat at normal', 'Group chat at advanced', 'No group chat'],
  'Q42': ['Recency-weighted', 'Engagement-weighted', 'Lexical only'],
  'Q43': ['No chat at normal', 'Full chat at normal', 'Chat at advanced'],
  'Q44': ['Local only', 'Central only', 'Peer-based only'],
  'Q45': ['Text only', 'Text + attachments', 'Everything in DMs'],
  'Q46': ['Identified pull (personalization)', 'No Central enrichment', 'Push your local data to Central'],
  'Q47': ['5 minutes', 'Until the recipient replies', 'No editing'],
  'Q48': ['Emoji grid only', 'Limited preset set', 'No reactions'],
  'Q49': ['Preset curated set', 'Typed text reactions', 'A small default set'],
  'Q50': ['Revisit later', 'Expand normal scope', 'Shrink normal scope'],
  'Q51': ['Single simple list', 'Two tabs', 'Collapsible sections'],
  'Q52': ['Side panel only', 'Both popup and side panel', 'Neither (full page)'],
  'Q53': ['Theme only', 'Permissions + theme', 'Minimal (no debug mode)'],
  'Q54': ['Everywhere', 'User-selected sites', 'No badge at all'],
  'Q55': ['Always inject', 'Inject automatically on flove.org', 'Inject automatically on whitelisted sites'],
  'Q56': ['Onboarding only', 'Just-in-time only', 'Ask once per install'],
  'Q57': ['Plain chrome.storage', 'Central-side sessions', 'No stored auth'],
  'Q58': ['Central only', 'Extension config only', 'Hardcoded'],
  'Q59': ['Built-in dev panel', 'Separate debug page', 'Log-only'],
  'Q60': ['Single retry', 'Infinite retry', 'Manual retry only'],
  'Q61': ['Notify and update on approval', 'Manual update only', 'Update with changelog'],
  'Q62': ['Common set (open, close, dismiss)', 'Full configurable set', 'System defaults'],
  'Q63': ['Single "open in browsy" item', 'Full context item menu', 'Selection-only menu'],
  'Q64': ['Central sync service', 'P2P sync', 'No multi-device support'],
  'Q65': ['Auth only', 'Overlay state only', 'Nothing (fresh start)'],
  'Q66': ['Single welcome page', 'Skip onboarding', 'Video tutorial'],
  'Q67': ['Hardcoded defaults', 'Per-site budgets', 'No budgets'],
  'Q68': ['All sites', 'flove.org only', 'Ask every time'],
  'Q69': ['No telemetry', 'Crash reports only', 'Opt-in anonymous usage'],
  'Q70': ['Schema migrations on update', 'Clear on major versions', 'Full re-import'],
  'Q93': ['Plain (no encryption)', 'App-level symmetric key', 'Per-recipient keys'],
  'Q93a': ['Random generated', 'Stored seed phrase', 'Central-issued'],
  'Q93b': ['Hidden entirely', 'Visible only to close circles', 'Shown as a trust score'],
  'Q93c': ['Telegram only', 'Password + email', 'Web3 wallet'],
  'Q93d': ['Full factors visible', 'Nothing visible', 'Factors visible to everyone'],
  'Q93e': ['Feature access only', 'Navigation bonuses only', 'No bonuses'],
  'Q93f': ['All factors equal', 'Trust vouches at the top', 'Email at the top'],
  'Q93g': ['Privacy-first browsing', 'Your identity, everywhere', 'No slogan'],
  'Q93h': ['Build from scratch', 'Fork oasis/SSB', 'Share a common library with nety'],
  'Q93i': ['Recovery code only', 'Contact support', 'No recovery'],
  'Q93j': ['Local-only vouches', 'Point-based scoring', 'Central approval'],
  'Q93k': ['Separate from the first circle', 'No first circle (empty)', 'Include all groups from day one'],
  'Q95': ['Fade in', 'Slide from the right', 'No animation'],
  'Q96': ['Auto-clear the oldest data', 'Hard stop', 'No warning'],
  'Q97': ['Design it now', 'No bonuses', 'Bonus = visibility only'],
  'Q98': ['Key gains only', 'Statement only', 'No chain'],
  'Q99': ['Full reveal by default', 'Nothing by default', 'Circle-dependent'],
  'Q100': ['Single master password', 'Support-mediated', 'No recovery'],
  'Q101': ['Pre-seeded with trusted contacts', 'Auto-added from vouches', 'Single list, no tabs'],
  'Q102': ['1 hop', '5 hops', 'Unlimited'],
  'Q103': ['Private accountability partners', 'Beneficiaries of assets', 'No heritage concept'],
  'Q104': ['Support desk only', 'Automated recovery codes', 'No recovery'],
  'Q105': ['6 months idle', '2 years idle', 'Never (no claim)'],
  'Q106': ['Capped at 5', 'Capped at 20', 'All open without approval'],
  'Q107': ['Outgoing only', 'Incoming only', 'Score summary only'],
  'Q108': ['Immediate (no approval)', 'Auto-approve close circle', 'Central approval'],
  'Q109': ['Names hidden, depth shown', 'Only direct vouchers', 'Fully private'],
  'Q110': ['Periodic automatic rotation', 'Rotation on risk events', 'No rotation'],
  'Q111': ['Vouches invalidated', 'Re-vouch required', 'Mixed handling'],
  'Q112': ['Max 3, threshold 2', 'Max 10, threshold 3', 'No limits'],
  'Q113': ['browsy notification only', 'Email only', 'No notification'],
  'Q114': ['User-configurable', 'Scales with contact count', 'Fixed at 3'],
  'Q115': ['No delay', '30 days', 'Immediate after idle'],
  'Q116': ['No revocation', 'Revoke within 30 days', 'Revoke with a penalty'],
  'Q117': ['Per-device keys', 'Key copied between devices', 'Central session'],
  'Q118': ['Any contact', 'Only the trusted tier', 'No requirement'],
  'Q119': ['Support verifies', 'Both parties confirm', 'No verification'],
  'Q120': ['No editing', 'Edit with approval', 'Edit your own only'],
  'Q121': ['3 hops', '5 hops', 'Direct only'],
  'Q122': ['Raw key export', 'No export', 'Encrypted export'],
  'Q123': ['QR code', 'Backup file', '24-word mnemonic'],
  'Q124': ['Anytime', 'When the primary factor is lost', 'Never (support only)'],
  'Q125': ['3 hops', 'Direct only', 'Owner decides'],
  'Q126': ['No timestamp', 'Adds a nonce', 'Adds a vector clock'],
  'Q127': ['Fixed enum', 'User-set per vouch', 'Score-derived'],
  'Q128': ['Set up the first circle first', 'Both at once', 'Skip straight to browsing'],
  'Q129': ['Flat circles only', 'Two-level max', 'No hierarchy'],
  'Q130': ['Heritage + Closest', 'Single unified group', 'Four groups'],
  'Q131': ['Keep the Circles name', 'MyNet separate from Trusts', 'Use both interchangeably'],
  'Q132': ['Single Close group', 'User-defined groups only', 'Friends + Others'],
  'Q133': ['Close → Groups → Social (3 tiers)', 'Private → Public (2 tiers)', 'Tierless (flat)'],
  'Q134': ['Groups always private', 'Groups always public', 'No groups tier'],
  'Q135': ['No sub-groups', 'Sub-groups in Groups only', 'User-defined tiers'],
  'Q136': ['Public posts only', 'Public profile only', 'No social tier'],
  'Q137': ['Interest only', 'Project only', 'User-defined only'],
  'Q138': ['Tier stays private', 'Visible to MyNet only', 'No tiers shown'],
  'Q139': ['Inner → Outer', 'Friends → Fans', 'Tier numbers'],
  'Q140': ['Automatic by activity', 'Suggestion + confirm', 'Fixed once set'],
  'Q141': ['Soft cap (e.g. 50 per tier)', 'Hard cap on Closest', 'Tiers gate features'],
  'Q142': ['Flat groups only', 'User categories only', 'No sub-structure'],
  'Q143': ['Interest, Project only', 'User-defined', 'No categories'],
  'Q144': ['Posts only', 'Profile + posts', 'Selected content only'],
  'Q145': ['Single Closest group', 'Closest + Recovery', 'User-defined tabs'],
  'Q146': ['Friends, Colleagues, Others', 'Friends + Others', 'User-defined'],
  'Q147': ['Automatic sync', 'No integration', 'Move MyFamily into Trusts directly'],
  'Q148': ['Temporary only', 'Uncategorized only', 'No Others group'],
  'Q149': ['Simple move everywhere', 'Approval for all moves', 'Automatic by trust score'],
  'Q150': ['Badge shows the tier', 'Badge per group activity', 'Badge = unread count'],
  'Q151': ['All local, nothing published', 'Everything published', 'Central-only storage'],
  'Q152': ['Consent after (at publish time)', 'Implicit consent', 'Always ask when publishing'],
  'Q153': ['Membership only', 'Nothing published', 'Consent-based'],
  'Q154': ['Full trust details', 'Trust + tier', 'Content references too'],
  'Q155': ['No revocation', 'Within 30 days', 'Revoke with a delay'],
  'Q156': ['Same concept', 'Heritage = family only', 'Trusts always public'],
  'Q157': ['Notify B', 'Notify with a consent option', 'Notify on high-tier trusts'],
  'Q158': ['Hidden', 'In the profile', 'No list'],
  'Q159': ['Recovery published with consent', 'Recovery shown to close', 'Partially public'],
  'Q160': ['Everything consent-based', 'All published', 'All private'],
  'Q161': ['All groups public', 'All groups private', 'Group type decides'],
  'Q162': ['Consent-based', 'User can make private', 'Semi-private'],
  'Q163': ['Per-trust inline toggle', 'Separate consent page', 'No UI (always ask)'],
  'Q164': ['Discovery via invites only', 'Search-based', 'No discovery'],
  'Q165': ['All-or-nothing consent', 'Per-peer granularity', 'Per-tier granularity'],
  'Q166': ['No limit', '1 group', 'Per-tier limit'],
  'Q167': ['5 max', 'Unlimited', '1 default only'],
  'Q168': ['People only', 'Rules only', 'Tier-based'],
  'Q169': ['Fixed names', 'Auto names', 'No names'],
  'Q170': ['Public + Private only', 'Single "Everyone" default', 'No defaults'],
  'Q171': ['Visible to members', 'Public list', 'Shared across devices'],
  'Q172': ['Single select', 'Tag input', 'Slider'],
  'Q173': ['Anyone can edit', 'Members can edit', 'No editing'],
  'Q174': ['System rules', 'Template rules', 'No rules'],
  'Q175': ['Inherit from Close', 'Nested groups', 'Global rules'],
  'Q176': ['Central storage', 'Synced by default', 'P2P storage'],
  'Q177': ['Content becomes public', 'Content is deleted', 'Members keep access'],
  'Q178': ['Auto-sync', 'Publish only', 'No sync'],
  'Q179': ['Prompt the user', 'Merge', 'Block sync'],
  'Q180': ['Publish, then select groups', 'One-tap to all groups', 'Central confirms first'],
  'Q181': ['Content only', 'Hash only', 'Timestamp only'],
  'Q182': ['browsy local only', 'Central only', 'GitHub only'],
  'Q183': ['No feedback', 'Confetti animation', 'Log entry'],
  'Q184': ['Save = publish', 'Separate explicit modes with a warning', 'Publish = share only'],
  'Q185': ['Posts only', 'Selected types', 'No publish'],
  'Q186': ['Private by default', 'Close only by default', 'User picks each time'],
  'Q187': ['Visible to members', 'Visible count only', 'Public'],
  'Q188': ['Members see all group content', 'Creator-only visibility', 'By role'],
  'Q189': ['Public', 'Close', 'Ask each time'],
  'Q190': ['Publish = share only', 'Save auto-publishes', 'No distinction'],
  'Q191': ['Standalone settings page', 'Per-content popup', 'Part of the profile'],
  'Q192': ['All apps', 'All tiers', 'Also super'],
  'Q193': ['Per-item only', 'Top bar only', 'Context menu only'],
  'Q194': ['Last-write-wins', 'Prompt with a copy of both', 'Merge automatically'],
  'Q195': ['Vector clocks everywhere', 'Server timestamps', 'Reject skews'],
  'Q196': ['Whole-object replace', 'Deep recursive merge', 'Version-numbered'],
  'Q197': ['Central authoritative', 'Last-writer-wins', 'Highest-trust wins'],
  'Q198': ['Browsy wins silently', 'Central wins silently', 'Skip (log only)'],
  'Q199': ['Block offline writes', 'Memory queue (lost on close)', 'Sync via service worker'],
  'Q200': ['Central pulls on demand', 'Push public + private', 'No push'],
  'Q201': ['browsy authoritative', 'Central decides', 'First-seen wins'],
  'Q202': ['Central log', 'Both sides log', 'No log'],
  'Q203': ['Reject unknown versions', 'Auto-migrate all', 'Version negotiation'],
  'Q204': ['Revoke via Central', 'No revocation', 'Recovery code resets'],
  'Q205': ['Timestamps del servidor', 'Vector clocks', 'Relojes lógicos'],
  'Q206': ['Por campo', 'Por bloque', 'Por revisión'],
  'Q207': ['Reintento lineal', 'Reintento infinito', 'Reintento manual'],
  'Q208': ['Aceptar y adaptar (coerce)', 'Rechazar en silencio', 'Sin validación'],
  'Q209': ['Snapshot completo cada vez', 'Sync completo por fragmentos', 'Por colección'],
  'Q210': ['Tiempo real para todo', 'Batches de 30 min', 'Solo bajo demanda'],
  'Q211': ['Inmediatamente', 'Resumen semanal', 'Nunca'],
  'Q212': ['3', '10', 'Sin límite'],
  'Q213': ['1MB por sync', '10MB por sync', 'Configurable por el usuario'],
  'Q214': ['3 días', '30 días', 'Sin umbral'],
  'Q215': ['1 hop', '5 hops', 'Completo sin límite'],
  'Q216': ['Totalmente automático', 'Totalmente manual', 'Solo al actualizar la app'],
  'Q217': ['Solo delta', 'Por campo', 'Solo al cambiar'],
  'Q218': ['Sin deshacer', '7 días', 'Deshacer ilimitado'],
  'Q219': ['7 días', '90 días', 'Para siempre'],
  'Q220': ['ID anónimo', 'Email de la cuenta', 'ID de hardware'],
  'Q221': ['Sin UI de estado', 'Página de estado detallada', 'Avisos toast'],
  'Q222': ['Descartar los cambios fallidos', 'Reintentar en silencio siempre', 'Bloquear la app hasta sincronizar'],
  'Q223': ['Sin compresión', 'Comprimido en todo', 'Compresión por tipo'],
  'Q224': ['Solo TLS', 'E2E para todo', 'Sin E2E'],
  'Q225': ['Auth solo', 'Publish bridge solo', 'Todas las features a la vez'],
  'Q226': ['Auth primero', 'Mynet primero', 'Prioridad igual'],
  'Q227': ['25MB / 50MB / 0.5%', '100MB / 200MB / 2%', 'Sin presupuesto explícito'],
  'Q228': ['chrome.storage.local', 'Memoria + periódico', 'Sin modo offline'],
  'Q229': ['Todo sincronizado', 'Todo local', 'Configurable por el usuario'],
  'Q230': ['Público por defecto', 'Mixto por contenido', 'Preguntar en el primer arranque'],
  'Q231': ['Móvil primero', 'Chrome solo', 'Todas las plataformas a la vez'],
  'Q232': ['<5MB (objetivo 3MB)', '<25MB', 'Sin objetivo de tamaño'],
  'Q233': ['Actualizaciones manuales', 'Auto-update silencioso', 'Rollout por etapas'],
  'Q234': ['Unit solo', 'E2E automatizado solo', 'Manual solo'],
  'Q235': ['README solo', 'Sitio de docs completo', 'Ayuda inline solo'],
  'Q236': ['Tour rápido de 3 pasos', 'Pantalla de bienvenida única', 'Sin onboarding'],
  'Q237': ['Consola solo', 'Telemetría remota completa', 'Sin reporte de errores'],
  'Q238': ['Contadores mínimos', 'Métricas críticas solo', 'Sin métricas'],
  'Q239': ['Antes del MVP', 'Continuo', 'Nunca (confiar en open source)'],
  'Q240': ['Monitorización fija', 'Sin monitorización', 'Solo en desarrollo'],
  'Q241': ['Solo GitHub issues', 'Feedback in-app solo', 'Solo email'],
  'Q242': ['Mensual', 'Semanal', 'Quincenal'],
  'Q243': ['Solo la última versión', 'Todas las versiones', 'Sin garantías'],
  'Q244': ['Source-available', 'Núcleo open source, plugins cerrados', 'Código cerrado']
};

/* ---------- browsy-questions.md ---------- */
const md = readFileSync(BROWSY, 'utf8');
const rows = [];
for (const line of md.split('\n')) {
  const m = line.match(/^\|\s*([A-Za-z0-9]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\*{2}([^*]*)\*{2}\s*\|/);
  if (!m) continue;
  const [, id, cat, q, dec] = m;
  if (/^[-]+$/.test(id)) continue;
  rows.push({ id, cat: cat.trim(), q: q.trim(), dec: dec.trim() });
}
const browsy = rows.map(r => ({
  id: 'B' + r.id, cat: r.cat, hat: hatFor(r.cat), q: r.q,
  o: [r.dec, ...(BROWSY_ALTS[r.id] || [])], a: r.dec
}));

/* ---------- emit ---------- */
const packBrowsy = {
  id: 'browsy', name: 'Browsy', src: 'making-of · browsy (nety+browsy decisions)',
  dot: '#3aa0ff', cat: 'making-of', a: browsy
};
const packNetySpec = {
  id: 'nety-spec', name: 'Nety spec', src: 'making-of · nety-spec interviews',
  dot: '#2f6bff', cat: 'making-of', a: netySpec
};
writeFileSync(OUT + "browsy.js", '/* questy pack — Browsy (nety + browsy decisions, Q01–Q244)\n   Source: development/standards/debates/browsy/browsy-questions.md\n   Generated by convert-packs.mjs — re-run to refresh. */\nwindow.QUESTY_PACKS = window.QUESTY_PACKS || [];\nwindow.QUESTY_PACKS.push(' + JSON.stringify(packBrowsy) + ');\n');
writeFileSync(OUT + "nety-spec.js", '/* questy pack — Nety spec (making-of interviews, 80q)\n   Source: development/standards/debates/making-of/feeds/nety-spec.xml\n   Generated by convert-packs.mjs — re-run to refresh. */\nwindow.QUESTY_PACKS = window.QUESTY_PACKS || [];\nwindow.QUESTY_PACKS.push(' + JSON.stringify(packNetySpec) + ');\n');

console.log('browsy questions:', browsy.length, '| nety-spec questions:', netySpec.length);
console.log('hat distribution browsy:', browsy.reduce((a, x) => { a[x.hat] = (a[x.hat] || 0) + 1; return a; }, {}));
console.log('hat distribution nety-spec:', netySpec.reduce((a, x) => { a[x.hat] = (a[x.hat] || 0) + 1; return a; }, {}));
console.log('wrote:', OUT + 'browsy.js', OUT + 'nety-spec.js');
