/* ============================================================
   shell-config.js · shared app configs for the nav-shell demo
   (risa clone + ama). The shell is config-driven: same shell code,
   different config per app. Used by risa-clone.html, ama.html and
   the central-code tests (test-central.html, test-loader.html).
   ============================================================ */
window.NAV_CONFIG = window.NAV_CONFIG || {};

window.NAV_CONFIG.risa = {
  app: 'Risa liberada',
  tagline: 'respira, escucha, disfruta',
  accent: '#e2560f',
  accentDeep: '#b5450a',
  accentSoft: '#fde8d9',

  mark: '<svg class="flove-mark" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="42" fill="#ffb020" stroke="#2a1810" stroke-width="6"/><path d="M34 42 q6 -9 14 0" fill="none" stroke="#2a1810" stroke-width="6" stroke-linecap="round"/><circle cx="62" cy="42" r="5" fill="#2a1810"/><path d="M34 62 q16 14 32 0" fill="none" stroke="#2a1810" stroke-width="6" stroke-linecap="round"/></svg>',

  hero: {
    logo: '<svg viewBox="0 0 200 200" role="img" aria-hidden="true"><circle cx="100" cy="100" r="86" fill="#ffb020" stroke="#2a1810" stroke-width="10"/><path d="M70 86 q12 -18 28 0" fill="none" stroke="#2a1810" stroke-width="11" stroke-linecap="round"/><circle cx="124" cy="86" r="10" fill="#2a1810"/><path d="M70 126 q30 28 60 0" fill="none" stroke="#2a1810" stroke-width="11" stroke-linecap="round"/></svg>',
    lead: { es: 'La risa no se explica: se comparte. Manda una nota de voz y ríe con el círculo.', en: 'Laughter is not explained: it is shared. Send a voice note and laugh with the circle.' },
    actions: [
      { label: { es: 'Publicar risa', en: 'Share a laugh' }, href: 'https://t.me/RisaLiberadaBot', primary: true },
      { label: { es: 'Porque', en: 'Because' }, action: 'scroll-first' }
    ]
  },

  sections: [
    {
      id: 'inicio',
      label: { es: 'Inicio', en: 'Home' },
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12 12 4l9 8M5 10v10h14V10"/></svg>',
      title: { es: 'Risas de la gente', en: 'People\'s laughs' },
      lead: { es: 'La playlist del círculo: escucha, filtra por etiquetas y guarda favoritas.', en: 'The circle playlist: listen, filter by tags and save favourites.' },
      body:
        '<div class="demo-note">demo · clon de la 1ª sección de risa/index</div>' +
        '<input class="fake-input" type="search" placeholder="Título, tags, usuario…" value="" disabled>' +
        '<div class="tag-space">' +
          '<span class="tag-chip">libre</span><span class="tag-chip">perrete</span><span class="tag-chip">flamenca</span>' +
          '<span class="tag-chip">telele</span><span class="tag-chip">cachonda</span><span class="tag-chip">ronca</span>' +
        '</div>' +
        '<ul class="tracklist">' +
          '<li class="trackitem"><span class="tr-emoji">😹</span><div class="tr-body"><div class="tr-title">La risa del claxon</div><div class="tr-meta">· libre · hoy</div></div><span>▶</span></li>' +
          '<li class="trackitem"><span class="tr-emoji">🦁</span><div class="tr-body"><div class="tr-title">Risa del león</div><div class="tr-meta">· libre · ayer</div></div><span>▶</span></li>' +
          '<li class="trackitem"><span class="tr-emoji">🥤</span><div class="tr-body"><div class="tr-title">Risa del batido</div><div class="tr-meta">· libre · hace 2d</div></div><span>▶</span></li>' +
        '</ul>'
    },
    {
      id: 'ejercicios',
      label: { es: 'Ejercicios', en: 'Exercises' },
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c4 4 4 8 0 12s-8 4-8 0M12 3c-4 4-4 8 0 12s8 4 8 0M12 21v0"/></svg>',
      title: { es: 'Técnicas para reír', en: 'Techniques to laugh' },
      lead: { es: 'Pausas guiadas que ríen contigo.', en: 'Guided pauses that laugh with you.' },
      body:
        '<div class="tag-space">' +
          '<span class="tag-chip">😮‍💨 Riespira</span><span class="tag-chip">🦁 Risa del león</span>' +
          '<span class="tag-chip">🚗 Risa del claxon</span><span class="tag-chip">🥤 Risa del batido</span>' +
        '</div>'
    },
    {
      id: 'tech',
      label: { es: 'Tech', en: 'Tech' },
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="13" height="12" rx="2"/><path d="m15 10 7-4v12l-7-4"/></svg>',
      title: { es: 'Cómo está hecha', en: 'How it is built' },
      lead: { es: 'Abierta, sin servidor y sin coste: risa.json como feed, R2 como almacén.', en: 'Open, serverless and free: risa.json as the feed, R2 as storage.' },
      body:
        '<div class="tag-space">' +
          '<span class="tag-chip">Cloudflare R2 · D1 · SW</span><span class="tag-chip">GitHub Pages · Actions</span>' +
          '<span class="tag-chip">Node.js + Telegram Bot API</span>' +
        '</div>'
    },
    {
      id: 'entrar',
      label: { es: 'Entrar', en: 'Sign in' },
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.4 3.6-5 6.5-5s5.5 1.6 6.5 5"/><path d="M16 9h5M18.5 6.5v5"/></svg>',
      title: { es: 'Tu perfil', en: 'Your profile' },
      lead: { es: 'Reclama tu palabra y enlaza todas tus risas en tu subdominio.', en: 'Claim your word and link all your laughs on your subdomain.' },
      body:
        '<div class="tag-space">' +
          '<span class="tag-chip">🔑 Reclamar tu palabra</span><span class="tag-chip">🌐 &lt;user&gt;.liberada.net</span>' +
          '<span class="tag-chip">✏️ Editar perfil</span>' +
        '</div>'
    }
  ],

  related: [
    { name: 'Maria', url: 'maria.html', mark: '👩' },
    { name: 'Maria-dev', url: 'maria-dev.html', mark: '🧪' },
    { name: 'Ama', url: 'ama.html', mark: '💗' }
  ],
  menu: {
    about: { es: 'Sobre nos', en: 'About us' }
  },
  profileUrl: '#entrar',
  flove: { about: 'https://flove.org/about', apps: 'https://flove.org/apps', home: 'https://flove.org' }
};
