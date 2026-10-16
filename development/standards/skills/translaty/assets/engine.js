// translaty engine — switches the page language and translates the bits CSS
// can't (<option> text, placeholders, aria-labels), remembers the choice, and
// keeps <html lang> in sync. Inline this in the app's <script> (or add one).
// Works for any number of languages: the active language is the code after
// "lang-" in the checked radio's id (lang-en -> en, lang-fr -> fr).
(function(){
  // Family-wide default (§13.2): ONE shared, app-agnostic key — not app-scoped —
  // so a choice in any flove app is the default everywhere (per-origin). LS_OLD
  // is the pre-standard key, read once for migration, then only LS is written.
  const LS = 'flove:lang', LS_OLD = 'translaty-lang';
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);            // es -> Es
  const radios = () => Array.from(document.querySelectorAll('input[name="lang"]'));
  const curLang = () => { const r = radios().find(x => x.checked); return r ? r.id.replace('lang-', '') : 'en'; };
  const stored = () => { try { return localStorage.getItem(LS) || localStorage.getItem(LS_OLD); } catch (_) { return null; } };
  // ?lang=<code> handoff — carries the default between apps on file:// too,
  // where per-file storage is isolated. Precedence: URL param > stored > 'en'.
  const urlLang = () => { try { return new URLSearchParams(location.search).get('lang'); } catch (_) { return null; } };
  function applyLang(){
    const li = curLang();
    document.documentElement.lang = li;
    // attributes/text the .en/.es span swap can't reach — carried on data-<lang>
    document.querySelectorAll('option[data-en]').forEach(o => { if (o.dataset[li] != null) o.textContent = o.dataset[li]; });
    document.querySelectorAll('[data-ph-en]').forEach(el => { const v = el.dataset['ph' + cap(li)]; if (v != null) el.placeholder = v; });
    document.querySelectorAll('[data-aria-en]').forEach(el => { const v = el.dataset['aria' + cap(li)]; if (v != null) el.setAttribute('aria-label', v); });
    try { localStorage.setItem(LS, li); } catch (_) {}     // always the shared key
  }
  function init(){
    // URL param wins (cross-app handoff), then the shared/old stored key.
    const want = urlLang() || stored();
    if (want){ const r = document.getElementById('lang-' + want); if (r) r.checked = true; }
    radios().forEach(r => r.addEventListener('change', () => {
      applyLang();
      const d = document.querySelector('details.lang'); if (d) d.open = false;   // close the worldball after a pick
    }));
    applyLang();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
