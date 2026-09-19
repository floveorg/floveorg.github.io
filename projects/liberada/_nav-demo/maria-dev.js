/* ============================================================
   maria-dev.js · María Demostración — variante de desarrollo
   (maria-dev.liberada.net). Mismo esqueleto que maria.js sobre el
   shell central, MÁS las features en desarrollo: bio extendida y
   browsy (barra fija de navegación central, flove-bottom-nav).
   Uso:  maria-dev.html carga nav-shell.js + flove-bottom-nav.js +
   maria-dev.js, y llama a FloveShell.init + FloveNav.bottom.
   ============================================================ */
window.MariaDev = {
  config: {
    app: 'María Demostración',
    tagline: 'maria-dev · en desarrollo',
    accent: '#f472b6',
    accentDeep: '#e63946',
    accentSoft: '#fdeaf0',

    mark: '<svg class="flove-mark" viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="md-am" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9b5de5"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs><circle cx="50" cy="50" r="44" fill="url(#md-am)" stroke="#2a1810" stroke-width="6"/><path d="M36 62 q14 12 28 0" fill="none" stroke="#2a1810" stroke-width="5" stroke-linecap="round"/><path d="M34 42 q8 -10 16 0" fill="none" stroke="#2a1810" stroke-width="5" stroke-linecap="round"/><circle cx="62" cy="42" r="4" fill="#2a1810"/></svg>',

    hero: {
      logo: '<svg viewBox="0 0 200 200" role="img" aria-hidden="true"><defs><linearGradient id="md-ah" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9b5de5"/><stop offset="1" stop-color="#f472b6"/></linearGradient></defs><circle cx="100" cy="100" r="88" fill="url(#md-ah)" stroke="#2a1810" stroke-width="12"/><path d="M72 124 q28 24 56 0" fill="none" stroke="#2a1810" stroke-width="10" stroke-linecap="round"/><path d="M68 84 q16 -20 32 0" fill="none" stroke="#2a1810" stroke-width="10" stroke-linecap="round"/><circle cx="124" cy="84" r="8" fill="#2a1810"/></svg>',
      lead: {
        es: 'Bio extendida, juega y filtra: la actividad de tus apps en tu nuevo perfil. · maria-dev.liberada.net',
        en: 'Extended bio, play and filter: your apps\' activity in your new profile. · maria-dev.liberada.net'
      },
      actions: [
        { label: { es: 'Seguir', en: 'Follow' }, href: 'https://liberada.net/usa/maria/', primary: true },
        { label: { es: 'Compartir', en: 'Share' }, href: 'https://liberada.net/usa/maria/' }
      ]
    },

    sections: [
      {
        id: 'bio',
        label: { es: 'Bio', en: 'Bio' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>',
        title: { es: 'Bio extendida', en: 'Extended bio' },
        lead: { es: 'Más sobre mí, mis redes y lo que hago en liberada.', en: 'More about me, my socials and what I do on liberada.' },
        body:
          '<div class="demo-note">maria-dev · bio extendida (demo)</div>' +
          '<p>Profesora de yoga desde hace 9 años, coordino el club de la risa de mi barrio y grabo notas de voz con mi clase. Cariño, movimiento y carcajada: eso es lo mío. Risa, Ama y Fuga son mis apps; esta página agrega todo lo que suelto en ellas.</p>' +
          '<div class="tag-space">' +
            '<span class="tag-chip">📸 @maria.yoga</span><span class="tag-chip">✈ @maria_demo</span>' +
            '<span class="tag-chip">📧 maria@liberada.net</span>' +
          '</div>'
      },
      {
        id: 'yo',
        label: { es: 'Yo', en: 'Me' },
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>',
        title: { es: 'Mis risas y amores', en: 'My laughs and loves' },
        lead: { es: 'Con filtro por app (Risa · Lovy) y por formato (audio · vídeo).', en: 'Filtered by app (Risa · Lovy) and format (audio · video).' },
        body:
          '<div class="tag-space">' +
            '<span class="tag-chip active">Risa</span><span class="tag-chip">Lovy</span>' +
            '<span class="tag-chip">🎙 audio</span><span class="tag-chip">🎬 vídeo</span>' +
          '</div>' +
          '<ul class="tracklist">' +
            '<li class="trackitem"><span class="tr-emoji">🧘</span><div class="tr-body"><div class="tr-title">Yoga y risa</div><div class="tr-meta">La Risa Yoga · audio · hoy</div></div><span>▶</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">💗</span><div class="tr-body"><div class="tr-title">Besito de buenos días</div><div class="tr-meta">María · audio · hace 1sem</div></div><span>▶</span></li>' +
            '<li class="trackitem"><span class="tr-emoji">🎬</span><div class="tr-body"><div class="tr-title">Con las alumnas</div><div class="tr-meta">La Risa Yoga · vídeo · hace 2sem</div></div><span>▶</span></li>' +
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
            '<li class="trackitem"><span class="tr-emoji">🏃</span><div class="tr-body"><div class="tr-title">Pedro López</div><div class="tr-meta">Runner y risueño · te sigue</div></div><span>✓</span></li>' +
          '</ul>'
      }
    ],

    related: [
      { name: 'Maria', url: 'maria.html', mark: '👩' },
      { name: 'Risa', url: 'risa-app.html', mark: '😹' },
      { name: 'Ama', url: 'ama-app.html', mark: '💗' }
    ],
    menu: {
      about: { es: 'Sobre María', en: 'About María' }
    },
    profileUrl: '#bio',
    flove: { about: 'https://flove.org/about', apps: 'https://flove.org/apps', home: 'https://flove.org' }
  },

  /* browsy — la barra fija de navegación central (maria-adv PoC),
     servida por central/shared/code (flove-bottom-nav.js · FloveNav). */
  browsy: {
    home: { name: 'Maria-dev', url: '#top', mark: '🧪' },
    apps: { name: 'apps', url: 'https://flove.org/apps' },
    categories: [
      { name: 'lib', icon: '🌱', apps: [
        { name: 'Maria', url: 'maria.html', mark: '👩' },
        { name: 'Risa', url: 'risa-app.html', mark: '😹' },
        { name: 'Ama', url: 'ama-app.html', mark: '💗' }
      ]},
      { name: 'flove', icon: '🧩', apps: [
        { name: 'flove.org', url: 'https://flove.org', mark: '🌱' },
        { name: 'Apps', url: 'https://flove.org/apps', mark: '🧩' }
      ]}
    ]
  }
};
