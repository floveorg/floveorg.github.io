/* questy-html — RSS feed generator (reference tool).
   Reads a making-of.html, writes RSS 2.0 per category + an "all" feed into <root>/feeds/.
   Usage: node gen-feeds.js [floveRoot] [pageURL]
   Run this after appending a new interview entry to making-of.html. */
const fs = require("fs");
const ROOT = process.argv[2] || "/home/kdeneon/Documents/flove";
const PAGE = process.argv[3] || "https://flove.org/making-of.html";

const html = fs.readFileSync(ROOT + "/making-of.html", "utf8");
const _eStart = html.indexOf("const ENTRIES = [");
const slice = html.slice(_eStart, html.indexOf("/* ----------", _eStart));   // robust: first comment block after ENTRIES
let ENTRIES; eval(slice.replace("const ENTRIES", "ENTRIES"));

const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const rfc822 = d => new Date(d + "T00:00:00Z").toUTCString();

const items = [];
ENTRIES.forEach(e => e.qa.forEach((q, i) => {
  const qid = e.id + "_q" + (i + 1);
  const decided = (q.chosen || []).join(' · ') || q.answer || '—';
  const opts = (q.o || []).map(o => `• ${o.l} — ${o.d}`).join('\n');
  const desc = `${opts ? opts + '\n\n' : ''}★ decided: ${decided}` +
    (q.suggest && q.suggest.length ? ` · ◇ recommended: ${q.suggest.join(' · ')}` : '');
  items.push({ qid, title: q.q, cats: q.cats || [], date: e.date, desc });
}));

function feed(title, descr, list) {
  const xmlItems = list.map(it =>
`    <item>
      <title>${esc(it.title)}</title>
      <link>${PAGE}#${it.qid}</link>
      <guid isPermaLink="false">${it.qid}</guid>
${it.cats.map(c => `      <category>${esc(c)}</category>`).join('\n')}
      <pubDate>${rfc822(it.date)}</pubDate>
      <description>${esc(it.desc)}</description>
    </item>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${esc(title)}</title>
    <link>${PAGE}</link>
    <description>${esc(descr)}</description>
    <language>en</language>
${xmlItems}
  </channel>
</rss>
`;
}

fs.mkdirSync(ROOT + "/feeds", { recursive: true });
const allCats = [...new Set(items.flatMap(it => it.cats))].sort();
const written = [];
fs.writeFileSync(ROOT + "/feeds/all.xml", feed("flove making-of — all questions", "Every design question from flove interviews.", items));
written.push("all.xml (" + items.length + ")");
allCats.forEach(c => {
  const list = items.filter(it => it.cats.includes(c));
  fs.writeFileSync(ROOT + "/feeds/" + slug(c) + ".xml", feed("flove making-of — " + c + " questions", "New " + c + " design questions from flove interviews.", list));
  written.push(slug(c) + ".xml (" + list.length + ")");
});
console.log("wrote feeds/:\n  " + written.join("\n  "));
