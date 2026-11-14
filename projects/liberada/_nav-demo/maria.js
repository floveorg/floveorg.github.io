/* ============================================================
   maria.js · María Demostración — perfil de usuaria, esqueleto
   abstraído en su propio fichero. El MISMO shell (central/shared/
   code/js/nav-shell.js · FloveShell) que risa/ama, solo cambia el
   config: paleta, avatar, bio y secciones (Yo · Favoritos ·
   Cadenas · Siguiendo) del perfil real usa/maria.
   Uso:  maria.html carga nav-shell.js + maria.js y llama a
   FloveShell.init(window.MariaApp.config).
   ============================================================ */
window.MariaApp = {
  config: {
    app: 'María Demostración',
    tagline: 'liberada.net',
    accent: '#f472b6',
    accentDeep: '#e63946',
    accentSoft: '#fdeaf0',

    mark: '<svg class="flove-mark" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="m-am" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb020"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs><circle cx="50" cy="50" r="44" fill="url(#m-am)" stroke="#2a1810" stroke-width="6"/><path d="M36 62 q14 12 28 0" fill="none" stroke="#2a1810" stroke-width="5" stroke-linecap="round"/><path d="M34 42 q8 -10 16 0" fill="none" stroke="#2a1810" stroke-width="5" stroke-linecap="round"/><circle cx="62" cy="42" r="4" fill="#2a1810"/></svg>',

    hero: {
      logo: '<svg viewBox="0 0 200 200" role="img" aria-hidden="true"><defs><linearGradient id="m-ah" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb020"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs><circle cx="100" cy="100" r="88" fill="url(#m-ah)" stroke="#2a1810" stroke-width="12"/><path d="M72 124 q28 24 56 0" fill="none" stroke="#2a1810" stroke-width="10" stroke-linecap="round"/><path d="M68 84 q16 -20 32 0" fill="none" stroke="#2a1810" stroke-width="10" stroke-linecap="round"/><circle cx="124" cy="84" r="8" fill="#2a1810"/></svg>',
      lead: {
        es: 'Profesora de yoga, amante de las risas espontáneas. Si no me río, no fue bueno. · maria.liberada.net',
        en: 'Yoga teacher, lover of spontaneous laughs. If I didn\'t laugh, it wasn\'t good. · maria.liberada.net'
      },
      actions: [
        { label: { es: 'Seguir', en: 'Follow' }, href: 'https://liberada.net/usa/maria/', primary: true },
        { label: { es: 'Compartir', en: 'Share' }, href: 'https://liberada.net/usa/maria/' }
      ]
    },

    sections: [
      {
        id: 'yo',
        label: { es: 'Yo', en: 'Me' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>',
        title: { es: 'Mis risas y amores', en: 'My laughs and loves' },
        lead: { es: 'Clips por alias: pulsa un chip para filtrar (demo).', en: 'Clips per alias: tap a chip to filter (demo).' },
        body:
          '<div class="demo-note">maria · perfil con risa y ama (demo)</div>' +
          '<div class="tag-space">' +
            '<span class="tag-chip active">María</span><span class="tag-chip">La Risa Yoga</span>' +
            '<span class="tag-chip">Contagiosa</span><span class="tag-chip">Carcajada</span>' +
            '<span class="tag-chip">privi</span>' +
          '</div>' +
          '<ul class="tracklist">' +
            '<li class="trackitem"><span class="tr-emoji">🧘</span><div class="tr-body"><div class="tr-title">Yoga y risa</div><div class="tr-meta">La Risa Yoga · audio · hoy</div></div><span>▶</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🤣</span><div class="tr-body"><div class="tr-title">La que no para</div><div class="tr-meta">Contagiosa · audio · hace 5d</div></div><span>▶</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">💗</span><div class="tr-body"><div class="tr-title">Besito de buenos días</div><div class="tr-meta">María · audio · hace 1sem</div></div><span>▶</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">👶</span><div class="tr-body"><div class="tr-title">Risa de bebé (Francia)</div><div class="tr-meta">privi · audio · hace 1d</div></div><span>▶</span></li>' +
          '</ul>'
      },
      {
        id: 'favoritos',
        label: { es: 'Favoritos', en: 'Favourites' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.4l6.1-.9z"/></svg>',
        title: { es: 'Mis favoritas', en: 'My favourites' },
        lead: { es: 'Risas y amores que guardé con la estrella.', en: 'Laughs and loves I starred.' },
        body:
          '<ul class="tracklist">' +
            '<li class="trackitem"><span class="tr-emoji">🤪</span><div class="tr-body"><div class="tr-title">Risa épica</div><div class="tr-meta">Loko Puro · audio · hace 4d</div></div><span>⭐</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">💻</span><div class="tr-body"><div class="tr-title">Código y risas</div><div class="tr-meta">Marc · audio · hace 8d</div></div><span>⭐</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">💗</span><div class="tr-body"><div class="tr-title">Amor de domingo</div><div class="tr-meta">Ana · audio · hace 2sem</div></div><span>⭐</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🎉</span><div class="tr-body"><div class="tr-title">Noche de risas</div><div class="tr-meta">Laura · audio · hace 3sem</div></div><span>⭐</span></li>' +
          '</ul>'
      },
      {
        id: 'cadenas',
        label: { es: 'Cadenas', en: 'Threads' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h12M4 12h8M4 17h4"/><path d="m19 15 2 2-2 2M19 9l2 2-2 2"/></svg>',
        title: { es: 'Cadenas de risa', en: 'Laugh threads' },
        lead: { es: 'Respuestas encadenadas bajo un clip (demo).', en: 'Replies threaded under a clip (demo).' },
        body:
          '<ul class="tracklist">' +
            '<li class="trackitem"><span class="tr-emoji">🤣</span><div class="tr-body"><div class="tr-title">La que no para</div><div class="tr-meta">Contagiosa · hoy</div></div><span>▶</span></li>' +
            '<li class="trackitem" style="margin-left:22px"><span class="tr-emoji">😂</span><div class="tr-body"><div class="tr-title">↳ Jajaja, contagiosa</div><div class="tr-meta">Marc · responde</div></div><span>▶</span></li>' +
            '<li class="trackitem" style="margin-left:44px"><span class="tr-emoji">🧘</span><div class="tr-body"><div class="tr-title">↳ Se la pongo a mi clase de yoga</div><div class="tr-meta">María · responde</div></div><span>▶</span></li>' +
          '</ul>'
      },
      {
        id: 'siguiendo',
        label: { es: 'Siguiendo', en: 'Following' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.4 3.6-5 6.5-5s5.5 1.6 6.5 5"/><path d="M16 9h5M18.5 6.5v5"/></svg>',
        title: { es: 'Sigo y me siguen', en: 'Following & followers' },
        lead: { es: 'La gente de mi círculo en liberada.', en: 'The people of my liberada circle.' },
        body:
          '<ul class="tracklist">' +
            '<li class="trackitem"><span class="tr-emoji">🧔</span><div class="tr-body"><div class="tr-title">Marc</div><div class="tr-meta">Creador de Risa · 3 risas</div></div><span>✓</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🤪</span><div class="tr-body"><div class="tr-title">Loko Puro</div><div class="tr-meta">Risas sin filtro · 4 risas</div></div><span>✓</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🧘</span><div class="tr-body"><div class="tr-title">Ana Pérez</div><div class="tr-meta">Yoga y risa · 2 risas</div></div><span>✓</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🏃</span><div class="tr-body"><div class="tr-title">Pedro López</div><div class="tr-meta">Runner y risueño · te sigue</div></div><span>✓</span></li>' +
          '</ul>'
      }
    ],

    related: [
      { name: 'Risa', url: 'risa-app.html', mark: '😹' },
      { name: 'Ama', url: 'ama-app.html', mark: '💗' },
      { name: 'Maria-dev', url: 'maria-dev.html', mark: '🧪' }
    ],
    menu: {
      about: { es: 'Sobre María', en: 'About María' }
    },
    profileUrl: '#yo',
    flove: { about: 'https://flove.org/about', apps: 'https://flove.org/apps', home: 'https://flove.org' }
  }
};
