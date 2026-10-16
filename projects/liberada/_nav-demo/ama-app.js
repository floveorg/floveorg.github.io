/* ============================================================
   ama-app.js · ama/index funcionalidad abstraída con el MISMO
   driver que risa (FloveApp.init desde central/shared/code/js/flove-app.js): nube de
   etiquetas flotante, reproductor/playlists/hilos y bottom-nav
   central. Solo cambia el config (feed, paleta, bot, categorías).
   ============================================================ */
window.AmaApp = (function () {
  'use strict';

  function init() {
    var cfg = {
      app: 'Ama liberada',
      feedUrl: 'https://ama.liberada.net/ama.json',
      favKey: 'ama-liberada-favs',
      botUrl: 'https://t.me/AmaLiberadaBot',
      pageSize: 10,
      playlistEs: 'Amores de la gente 💗',
      playlistEn: 'People\u2019s loves 💗',
      shareText: 'Escucha este amor 💗',
      shareTitle: 'Ama liberada',
      clipsOf: function (data) {
        if (Array.isArray(data)) return data;
        return (data && Array.isArray(data.clips)) ? data.clips : [];
      },
      trackOpts: {
        defaultTags: 'amor libre',
        origLabel: 'licencia',
        origOf: function (c) { return 'https://creativecommons.org/licenses/by-sa/4.0/deed.es'; },
        byOf: function (c) { return (c.name || 'Anónimo') + ' · CC BY-SA 4.0'; }
      },
      nav: {
        home: { name: 'Ama', url: '#top', mark: '<svg viewBox="0 0 100 100"><path d="M50 88 C20 70 12 48 22 34 C30 23 44 26 50 36 C56 26 70 23 78 34 C88 48 80 70 50 88Z" fill="#f472b6"/></svg>' },
        apps: { name: 'apps', url: 'https://flove.org/apps' },
        categories: [
          { name: 'lib', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19V5a2 2 0 012-2h14v16H6a2 2 0 00-2 2zM20 21H6a2 2 0 01-2-2"/></svg>', apps: [
            { name: 'Ama', url: 'ama-app.html', mark: '💗' },
            { name: 'Risa', url: 'risa-app.html', mark: '😹' },
            { name: 'Maria', url: 'maria.html', mark: '👩' },
            { name: 'Maria-dev', url: 'maria-dev.html', mark: '🧪' },
            { name: 'Liberada', url: 'https://liberada.net', mark: '🌱' }
          ]},
          { name: 'flove', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>', apps: [
            { name: 'flove.org', url: 'https://flove.org', mark: '🌱' },
            { name: 'Apps', url: 'https://flove.org/apps', mark: '🧩' }
          ]}
        ]
      }
    };
    return window.FloveApp.init(cfg);
  }

  return { init: init };
})();
