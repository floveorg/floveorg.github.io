(() => {
  'use strict';

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const pad = (n) => String(n).padStart(2, '0');
  const plain = (html) => html.replace(/<[^>]+>/g, '');

  const BUBBLE = 'M42 14 H78 A24 24 0 0 1 102 38 V62 A24 24 0 0 1 78 86 H52 L26 106 L31 86 H42 A24 24 0 0 1 18 62 V38 A24 24 0 0 1 42 14 Z';
  const HILL1 = 'M14 78 C28 58 48 66 66 68 C84 70 96 58 106 64 V92 H14 Z';
  const HILL2 = 'M14 86 C34 70 50 78 68 80 C84 82 96 72 106 78 V92 H14 Z';

  /* ---------- progress ---------- */
  const bar = $('#progressBar');
  const updateProgress = () => {
    if (!bar) return;
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };

  /* ---------- step tracking ---------- */
  const steps = $$('[data-step]');
  const railLinks = $$('[data-rail]');
  const stepbar = $('#stepbar');
  const stepNow = $('#stepNow');
  const stepName = $('#stepName');
  const prevBtn = $('#stepPrev');
  const nextBtn = $('#stepNext');
  let current = 0;

  const setCurrent = (i) => {
    current = Math.max(0, Math.min(steps.length - 1, i));
    const sec = steps[current];
    if (!sec) return;
    const n = sec.dataset.step || pad(current + 1);
    const name = sec.dataset.stepName || '';
    if (stepNow) stepNow.textContent = n + ' / ' + pad(steps.length);
    if (stepName) stepName.textContent = name;
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === steps.length - 1;
    railLinks.forEach((a) => {
      if (a.dataset.rail === sec.id) a.setAttribute('aria-current', 'step');
      else a.removeAttribute('aria-current');
    });
  };

  const go = (i) => {
    if (!steps[i]) return;
    steps[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  if (prevBtn) prevBtn.addEventListener('click', () => go(current - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => go(current + 1));

  const spy = new IntersectionObserver(
    (entries) => {
      const v = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (v) setCurrent(steps.indexOf(v.target));
    },
    { rootMargin: '-30% 0px -55% 0px', threshold: [0.05, 0.2, 0.5] }
  );
  steps.forEach((s) => spy.observe(s));

  const hero = $('#paso-0');
  if (hero && stepbar) {
    new IntersectionObserver(
      ([e]) => stepbar.classList.toggle('on', !e.isIntersecting),
      { threshold: 0.15 }
    ).observe(hero);
  }

  /* ---------- reveal ---------- */
  const reveals = $$('.reveal');
  const revObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          revObs.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
  );
  reveals.forEach((el) => revObs.observe(el));

  /* ---------- hero parallax ---------- */
  const corridor = $('#corridor');
  const onScroll = () => {
    const y = window.scrollY || 0;
    const vh = window.innerHeight || 1;
    if (corridor) {
      const m = Math.min(1, y / (vh * 1.1));
      corridor.style.transform = `translateY(${y * 0.18}px)`;
      corridor.style.opacity = String(1 - m * 0.55);
    }
    updateProgress();
  };

  if (corridor) {
    window.addEventListener(
      'pointermove',
      (e) => {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        const mx = (e.clientX / window.innerWidth - 0.5).toFixed(3);
        const my = (e.clientY / window.innerHeight - 0.5).toFixed(3);
        corridor.style.setProperty('--mx', mx);
        corridor.style.setProperty('--my', my);
      },
      { passive: true }
    );
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  setCurrent(0);

  /* ---------- dust canvas ---------- */
  const dust = $('#dust');
  if (dust && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const ctx = dust.getContext('2d');
    let w = 0, h = 0, pts = [];
    const resize = () => {
      w = dust.width = dust.offsetWidth;
      h = dust.height = dust.offsetHeight;
      pts = Array.from({ length: Math.min(42, Math.floor(w / 28)) }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.3 + 0.3,
        v: Math.random() * 0.18 + 0.04,
        a: Math.random() * 0.4 + 0.1,
      }));
    };
    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#F7C86A';
      pts.forEach((p) => {
        p.y -= p.v;
        p.x += Math.sin(p.y * 0.01) * 0.12;
        if (p.y < -10) {
          p.y = h + 10;
          p.x = Math.random() * w;
        }
        ctx.globalAlpha = p.a;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1;
      requestAnimationFrame(tick);
    };
    new ResizeObserver(resize).observe(dust);
    resize();
    tick();
  }

  /* ---------- lands (paletas de las escenas) ---------- */
  const LANDS = [
    { n: '01', name: 'La Taberna', wall: '#1E3A2C', wall2: '#12211A', floor1: '#2B4A38', floor2: '#0F1A14', sky1: '#8FD9A8', sky2: '#2E6B4A', sunC: '#F0B03C', hill1: '#1E6B49', hill2: '#2E9E6B', glow: 'rgba(240,176,60,.20)', glow2: 'rgba(247,200,106,.35)', lamp: '#F7C86A', table: '#2E4A38', sunx: '62%', suny: '62%' },
    { n: '02', name: 'La Oficina', wall: '#1C2A33', wall2: '#0D161C', floor1: '#22323C', floor2: '#0E161B', sky1: '#9CC8E8', sky2: '#2F4C68', sunC: '#A9D8F2', hill1: '#1C4A46', hill2: '#2E7A6B', glow: 'rgba(89,187,214,.18)', glow2: 'rgba(169,216,242,.30)', lamp: '#DCEFFF', table: '#2A3A44', sunx: '58%', suny: '58%' },
    { n: '03', name: 'El Taller', wall: '#33301C', wall2: '#1D1B10', floor1: '#3E3822', floor2: '#17140C', sky1: '#E0C866', sky2: '#6A5A23', sunC: '#FFD980', hill1: '#4A421C', hill2: '#6B5F2E', glow: 'rgba(224,200,102,.18)', glow2: 'rgba(255,217,128,.30)', lamp: '#FFE08A', table: '#3E3822', sunx: '66%', suny: '60%' },
    { n: '04', name: 'La Biblioteca', wall: '#2E2A1E', wall2: '#191710', floor1: '#3A3324', floor2: '#15130C', sky1: '#D1B98A', sky2: '#5C4E2E', sunC: '#F4DCA2', hill1: '#3A3A1E', hill2: '#5E5E2E', glow: 'rgba(209,185,106,.16)', glow2: 'rgba(244,220,162,.26)', lamp: '#F0DCA0', table: '#3A3324', sunx: '55%', suny: '60%' },
    { n: '05', name: 'El Patio', wall: '#1C2A1E', wall2: '#0C140D', floor1: '#28402A', floor2: '#101A10', sky1: '#BFDFF2', sky2: '#4B7A6A', sunC: '#FFF4D8', hill1: '#1E4A2C', hill2: '#2E7A48', glow: 'rgba(191,223,242,.18)', glow2: 'rgba(255,244,216,.30)', lamp: '#FFF0D0', table: '#2B3A2C', sunx: '50%', suny: '52%' },
    { n: '06', name: 'La Terraza', wall: '#33223A', wall2: '#1A121D', floor1: '#3A2E3E', floor2: '#170F18', sky1: '#F2A1A8', sky2: '#5A2E55', sunC: '#FFC2A6', hill1: '#4A2440', hill2: '#7A3A5E', glow: 'rgba(242,161,168,.18)', glow2: 'rgba(255,194,166,.30)', lamp: '#FFCFB8', table: '#3A2E3E', sunx: '70%', suny: '66%' },
    { n: '07', name: 'El Salón de juegos', wall: '#262A3A', wall2: '#14161C', floor1: '#2C3044', floor2: '#12141A', sky1: '#C8A8F2', sky2: '#4A3A6A', sunC: '#E8DEFF', hill1: '#2A2A4A', hill2: '#423A6A', glow: 'rgba(182,168,242,.18)', glow2: 'rgba(232,222,255,.28)', lamp: '#E2D6FF', table: '#2E3444', sunx: '60%', suny: '58%' },
    { n: '08', name: 'La Sala de música', wall: '#1A2A32', wall2: '#0C1418', floor1: '#213840', floor2: '#0F181C', sky1: '#8FD3D8', sky2: '#244C5A', sunC: '#D6FBFF', hill1: '#1C3A3A', hill2: '#2E5E5E', glow: 'rgba(143,211,216,.16)', glow2: 'rgba(214,251,255,.26)', lamp: '#CFF8FF', table: '#25343A', sunx: '54%', suny: '56%' },
    { n: '09', name: 'El Jardín', wall: '#162A1E', wall2: '#0A140D', floor1: '#20382A', floor2: '#0E1A12', sky1: '#BFE8A8', sky2: '#3A6A3E', sunC: '#FFF2C8', hill1: '#1E4A2E', hill2: '#2E7A48', glow: 'rgba(191,232,168,.16)', glow2: 'rgba(255,242,200,.26)', lamp: '#FFF0C0', table: '#24362A', sunx: '52%', suny: '54%' },
    { n: '10', name: 'La Cocina', wall: '#33281A', wall2: '#1A140D', floor1: '#3E3020', floor2: '#17120B', sky1: '#F0C08A', sky2: '#7A4A28', sunC: '#FFE0B0', hill1: '#4A3A1C', hill2: '#6B5A2E', glow: 'rgba(240,192,138,.18)', glow2: 'rgba(255,224,176,.30)', lamp: '#FFD8A8', table: '#3C291C', sunx: '64%', suny: '60%' },
    { n: '11', name: 'El Estudio', wall: '#242A33', wall2: '#12161C', floor1: '#2A323C', floor2: '#101419', sky1: '#A6B8D8', sky2: '#334560', sunC: '#E8F0FF', hill1: '#22304A', hill2: '#3A4A6A', glow: 'rgba(166,184,216,.15)', glow2: 'rgba(232,240,255,.24)', lamp: '#E0ECFF', table: '#262A34', sunx: '56%', suny: '56%' },
    { n: '12', name: 'La Azotea', wall: '#1C2630', wall2: '#0D1218', floor1: '#26323C', floor2: '#111820', sky1: '#8EC8F2', sky2: '#2C5070', sunC: '#FFF8E8', hill1: '#1C3A4A', hill2: '#2E5A6B', glow: 'rgba(142,200,242,.18)', glow2: 'rgba(255,248,232,.30)', lamp: '#FFF4D8', table: '#2A3240', sunx: '50%', suny: '48%' },
    { n: '13', name: 'El Cine', wall: '#1E1A2A', wall2: '#0C0A12', floor1: '#241E34', floor2: '#0F0C18', sky1: '#9A8AC8', sky2: '#2A1E44', sunC: '#D8C8FF', hill1: '#2A1E4A', hill2: '#42306A', glow: 'rgba(122,106,168,.14)', glow2: 'rgba(216,200,255,.22)', lamp: '#D0BFFF', table: '#221E2C', sunx: '58%', suny: '56%' },
    { n: '14', name: 'El Mercado', wall: '#33281C', wall2: '#1A150E', floor1: '#3E3224', floor2: '#17120C', sky1: '#E8C48A', sky2: '#6A4A28', sunC: '#FFE8B8', hill1: '#4A3A1E', hill2: '#6B5A2E', glow: 'rgba(232,196,138,.18)', glow2: 'rgba(255,232,184,.28)', lamp: '#FFE0A8', table: '#382C1E', sunx: '62%', suny: '60%' },
    { n: '15', name: 'El Umbral', wall: '#2A2420', wall2: '#141110', floor1: '#342C28', floor2: '#131110', sky1: '#F0D0A8', sky2: '#6A4A38', sunC: '#FFF0D8', hill1: '#3A3020', hill2: '#5A4A30', glow: 'rgba(240,208,168,.20)', glow2: 'rgba(255,240,216,.30)', lamp: '#FFE8C8', table: '#302824', sunx: '50%', suny: '64%' },
  ];

  const roomVars = (l) =>
    `--wall:${l.wall};--wall2:${l.wall2};--floor1:${l.floor1};--floor2:${l.floor2};` +
    `--sky1:${l.sky1};--sky2:${l.sky2};--sunC:${l.sunC};--hill1:${l.hill1};--hill2:${l.hill2};` +
    `--glow:${l.glow};--glow2:${l.glow2};--lamp:${l.lamp};--table:${l.table};` +
    `--sunx:${l.sunx};--suny:${l.suny}`;

  const roomHTML = (l) =>
    `<div class="room" style="${roomVars(l)}">
      <div class="r-sky"></div>
      <div class="r-beam"></div>
      <div class="r-arch"><div class="r-sun"></div><div class="r-hills"></div><div class="r-horizon"></div></div>
      <div class="r-side l"></div><div class="r-side r"></div>
      <div class="r-floor"></div>
      <div class="r-table"></div>
      <div class="r-lamp a"></div><div class="r-lamp b"></div>
      <div class="r-mote" style="left:22%;top:60%;animation-delay:0s"></div>
      <div class="r-mote" style="left:34%;top:72%;animation-delay:-2s"></div>
      <div class="r-mote" style="left:48%;top:54%;animation-delay:-4s"></div>
      <div class="r-mote" style="left:60%;top:68%;animation-delay:-6s"></div>
      <div class="r-mote" style="left:72%;top:58%;animation-delay:-8s"></div>
      <div class="r-mote" style="left:82%;top:74%;animation-delay:-10s"></div>
      <div class="r-vig"></div>
      <div class="r-grain"></div>
    </div>`;

  /* ---------- contenido del tour ---------- */
  const MOTIVES = [
    { li: 0, k: 'Pertenencia', title: 'Un sitio donde <em>quedar.</em>', body: 'Un mensaje se lee; una presencia se siente. Verte ahí, sentado en la misma sala, dice más que veinte mensajes.', tag: 'Un sitio con tu nombre y tu mesa.' },
    { li: 1, k: 'Lo que cambia', title: 'Más que una app. <em>Es un sitio.</em>', body: 'No hay feed ni notificaciones persiguiéndote. Hay un lugar, y tú estás o no estás.', tag: 'El formato, no el contenido.' },
    { li: 2, k: 'Sin cámara', title: 'Cerca, <em>sin cámara.</em>', body: 'Hay días en los que quieres compañía y no cara. Chatland te da presencia sin obligarte a enseñar la habitación.', tag: 'Presencia sin videollamada.' },
    { li: 3, k: 'Baja presión', title: 'El chat que <em>se habita.</em>', body: 'Puedes estar callado en una land. No pasa nada. No hay «¿sigues ahí?».', tag: 'El silencio también es compañía.' },
    { li: 4, k: 'La idea madre', title: 'La conversación es <em>la singularidad.</em>', body: 'Comuniquémonos entre nosotros como en el siglo 21: con más sitio y menos ruido. No con más mensajes: con más lugar.', tag: 'Conversación y lugar en una sola forma.' },
    { li: 5, k: 'Los gestos', title: 'Los gestos dicen lo que <em>cuesta escribir.</em>', body: 'Saludar, sentarse, bailar, esperar. Diecinueve formas de decir algo sin teclear.', tag: '19 animaciones por residente.' },
    { li: 6, k: 'El silencio', title: 'El silencio también <em>es compañía.</em>', body: 'Estar sin hablar no es no estar. El recinto no te pide que llenes el aire.', tag: 'Ritual · la costumbre de volver.' },
    { li: 7, k: 'La presencia', title: 'Estar es distinto de <em>escribir.</em>', body: 'La diferencia es la misma que entre escribir «quedamos» y quedar. Un mensaje se lee; una presencia se siente.', tag: 'Presencia · lo que no cabe en un texto.' },
    { li: 8, k: 'La costumbre', title: 'Un sitio fijo <em>crea costumbre.</em>', body: 'Volver al mismo bar, a la misma mesa, a la misma hora. La gente no se hace amiga de una app; se hace amiga de un lugar.', tag: 'Ritual · la costumbre de volver.' },
    { li: 9, k: 'El control', title: 'Un avatar te deja ser <em>sin exponerte.</em>', body: 'Eliges cómo te ves y cuánto muestras. Es una capa fina entre tú y el mundo, no una máscara.', tag: 'Control · tú decides cuánto enseñas.' },
    { li: 10, k: 'Sin espejo', title: 'No todo el mundo quiere <em>una videollamada.</em>', body: 'Hay días en los que quieres compañía y no cara. Compañía sin espejo, sin arreglarte, sin enseñar la habitación.', tag: 'Presencia sin cámara.' },
    { li: 11, k: 'El rendimiento', title: 'Va fluido en un móvil <em>de 2020.</em>', body: '60 fotogramas por segundo en un Redmi Note 9S. No necesitas lo último para entrar en un sitio cálido.', tag: 'Rendimiento · 60 fotogramas por segundo.' },
    { li: 12, k: 'La autonomía', title: 'Va <em>dentro del móvil.</em>', body: 'El recinto entero, sin cobertura, sin cargar mundos que se desmontan al salir. El sitio viaja contigo.', tag: 'Autonomía · funciona sin cobertura.' },
    { li: 13, k: 'Lo nativo', title: 'No es <em>otra pestaña.</em>', body: 'No es una web disfrazada: habla directo con la tarjeta gráfica del teléfono. Sin Unity, sin Godot, sin navegador.', tag: '3D nativo de verdad.' },
    { li: 14, k: 'La entrada', title: 'Entrar <em>es barato.</em>', body: 'Descargas, eliges land, eliges quién eres, entras. Sin teatro. La verja está abierta.', tag: 'Entrada libre · la verja está abierta.' },
  ];

  const PERSONAS = [
    { li: 13, sub: 'Nuevo perfil', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><circle cx="18.6" cy="22" r="1.8" fill="#14211C"/><circle cx="29.4" cy="22" r="1.8" fill="#14211C"/><path d="M19 29.5q5 4.5 10 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M38 6.5l1.1 4.2 4.2 1.1-4.2 1.1-1.1 4.2-1.1-4.2-4.2-1.1 4.2-1.1z" fill="#BFE06A" stroke="#14211C" stroke-width="1.2" stroke-linejoin="round"/></svg>`, title: 'El recién llegado', body: 'Acabas de mudarte y no conoces a nadie. Aquí hay un sitio al que entrar sin invitación, con aforo pequeño y caras que se repiten.', tag: 'La ciudad sin red.' },
    { li: 9, sub: 'Nuevo perfil', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><path d="M15.5 22q2.6-2.6 5.2 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M27.3 22q2.6-2.6 5.2 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M19 29q5 4 10 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M39.5 7.5c-1.3-2-4.2-1-3.8 1.3.3 1.5 3.8 3.6 3.8 3.6s3.5-2.1 3.8-3.6c.4-2.3-2.5-3.3-3.8-1.3z" fill="#D9663F" stroke="#14211C" stroke-width="1.2" stroke-linejoin="round"/></svg>`, title: 'El que cuida', body: 'No puedes salir de casa, pero puedes entrar un rato. Un sitio al que asomarse cuando el día deja un hueco.', tag: 'Cuidar también cansa.' },
    { li: 3, sub: 'Nuevo perfil', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><path d="M9.2 22C10.5 11.5 17 7.6 24 7.6S37.5 11.5 38.8 22C36 17.5 31 16.4 24 16.4S12 17.5 9.2 22z" fill="#F4F3E7" stroke="#14211C" stroke-width="1.8" stroke-linejoin="round"/><circle cx="18.4" cy="24.5" r="3.3" fill="none" stroke="#14211C" stroke-width="1.8"/><circle cx="29.6" cy="24.5" r="3.3" fill="none" stroke="#14211C" stroke-width="1.8"/><line x1="21.7" y1="24.5" x2="26.3" y2="24.5" stroke="#14211C" stroke-width="1.8"/><path d="M20 32q4 2.6 8 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><circle cx="15.6" cy="30" r="1.6" fill="#D9663F" opacity=".7"/><circle cx="32.4" cy="30" r="1.6" fill="#D9663F" opacity=".7"/></svg>`, title: 'La persona mayor que vive sola', body: 'Entrar es simple y visual: «estoy en el patio» se entiende mejor que un hilo de mensajes.', tag: 'Un sitio que se entiende sin manual.' },
    { li: 1, sub: 'De siempre', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><path d="M15.5 21q2.7-2.4 5.4 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M27.1 21q2.7-2.4 5.4 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><ellipse cx="24" cy="31" rx="4.4" ry="5.4" fill="#14211C"/><path d="M22 33q2 1.6 4 0" fill="none" stroke="#D9663F" stroke-width="1.4" stroke-linecap="round"/><path d="M38 8h4.4l-4.4 5h4.4" fill="none" stroke="#59BBD6" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>`, title: 'El cansado del chat plano', body: 'Cien conversaciones que no llegan a ningún sitio. Aquí no persigues mensajes: entras donde está la gente.', tag: 'Menos mensajes, más sitio.' },
    { li: 0, sub: 'De siempre', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><circle cx="19" cy="23" r="1.8" fill="#14211C"/><circle cx="29" cy="23" r="1.8" fill="#14211C"/><path d="M14.5 19.5l5-1.4" stroke="#14211C" stroke-width="1.8" stroke-linecap="round"/><path d="M33.5 19.5l-5-1.4" stroke="#14211C" stroke-width="1.8" stroke-linecap="round"/><path d="M18.5 31q2.75-2 5.5 0t5.5 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><path d="M26.5 39.5c-1.6 1.8-1.8 3.6.2 5.2 1.8-1.6 1.6-3.4-.2-5.2z" fill="#D9663F" stroke="#14211C" stroke-width="1.2" stroke-linejoin="round"/></svg>`, title: 'El grupo que ya no queda', body: 'El grupo de WhatsApp muerto. Dadle una mesa fija y un día fijo, y vuelve a haber sitio.', tag: 'Vuelve a haber sitio.' },
    { li: 10, sub: 'De siempre', face: `<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="25" r="15.5" fill="#F0B03C" stroke="#14211C" stroke-width="2.2"/><circle cx="18.4" cy="23" r="3.4" fill="none" stroke="#14211C" stroke-width="1.9"/><circle cx="29.6" cy="23" r="3.4" fill="none" stroke="#14211C" stroke-width="1.9"/><line x1="21.8" y1="23" x2="26.2" y2="23" stroke="#14211C" stroke-width="1.9"/><path d="M19.5 31q4.5 3.2 9 0" fill="none" stroke="#14211C" stroke-width="2" stroke-linecap="round"/><line x1="24" y1="9" x2="24" y2="4.5" stroke="#14211C" stroke-width="1.8" stroke-linecap="round"/><circle cx="24" cy="3.6" r="1.8" fill="#59BBD6" stroke="#14211C" stroke-width="1.2"/></svg>`, title: 'El curioso tecnológico', body: 'Motor propio sobre Filament, 60 FPS en un móvil de 2020. Artesanía, no plantilla.', tag: 'Artesanía, no plantilla.' },
  ];

  const ITEMS = MOTIVES.map((s) => ({ ...s, kind: 'motivo' }))
    .concat(PERSONAS.map((s) => ({ ...s, kind: 'persona' })));

  let mCount = 0, pCount = 0;
  ITEMS.forEach((s) => {
    if (s.kind === 'persona') {
      pCount++;
      s.badge = 'P' + pCount;
      s.idx = `Perfil ${pad(pCount)} / 06`;
      s.kicker = 'Para quién · ' + s.sub;
    } else {
      mCount++;
      s.badge = pad(mCount);
      s.idx = `Motivo ${pad(mCount)} / 15`;
      s.kicker = s.k;
    }
  });

  const stage = $('#tourStage');
  const track = $('#tourTrack');
  const tourNow = $('#tourNow');
  const tourPlay = $('#tourPlay');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ti = 0;
  let playing = false;
  let timer = null;

  if (track) {
    track.innerHTML = ITEMS.map((s, i) => {
      const l = LANDS[s.li];
      return `<article class="tour-slide" aria-hidden="${i === 0 ? 'false' : 'true'}" data-i="${i}" aria-label="${plain(s.title)}">
        <div class="tour-scene">${roomHTML(l)}</div>
        <div class="tour-body">
          ${s.kind === 'persona' ? `<span class="face tour-face" aria-hidden="true">${s.face}</span>` : ''}
          <span class="tour-k">${s.kicker}</span>
          <h3>${s.title}</h3>
          <p>${s.body}</p>
          <span class="tour-tag">${s.tag}</span>
          <span class="tour-index">${s.idx}</span>
        </div>
      </article>`;
    }).join('');
  }

  function updatePlay() {
    if (!tourPlay) return;
    tourPlay.setAttribute('aria-pressed', playing ? 'true' : 'false');
    tourPlay.textContent = playing ? 'Pausa' : 'Reproducir';
  }

  function stopTimer() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  function startTimer() {
    stopTimer();
    if (!playing) return;
    timer = setInterval(() => goTour(ti + 1), 8500);
  }

  function pauseTour() {
    playing = false;
    stopTimer();
    updatePlay();
  }

  function playTour() {
    playing = true;
    startTimer();
    updatePlay();
  }

  function goTour(i, manual = false) {
    if (!ITEMS.length) return;
    ti = ((i % ITEMS.length) + ITEMS.length) % ITEMS.length;
    if (track) {
      track.style.transform = `translateX(${-ti * 100}%)`;
      $$('.tour-slide', track).forEach((el, j) =>
        el.setAttribute('aria-hidden', j === ti ? 'false' : 'true')
      );
    }
    const s = ITEMS[ti];
    const l = LANDS[s.li];
    if (tourNow) {
      tourNow.innerHTML = s.kind === 'persona'
        ? `<b>Para quién</b> · ${plain(s.title)}`
        : `<b>Land ${l.n}</b> · ${l.name}`;
    }
    if (manual) pauseTour();
    else if (playing) startTimer();
  }

  if (tourPlay) tourPlay.addEventListener('click', () => (playing ? pauseTour() : playTour()));
  const tourOpen = $('#tourOpen');
  if (tourOpen) tourOpen.addEventListener('click', () => openModal(ti));
  const tourPrev = $('#tourPrev');
  const tourNext = $('#tourNext');
  if (tourPrev) tourPrev.addEventListener('click', () => goTour(ti - 1, true));
  if (tourNext) tourNext.addEventListener('click', () => goTour(ti + 1, true));

  if (stage) {
    stage.addEventListener('mouseenter', stopTimer);
    stage.addEventListener('mouseleave', () => { if (playing) startTimer(); });
    stage.addEventListener('focusin', stopTimer);
    stage.addEventListener('focusout', () => { if (playing) startTimer(); });

    let sx = null;
    stage.addEventListener('pointerdown', (e) => { sx = e.clientX; });
    stage.addEventListener('pointerup', (e) => {
      if (sx === null) return;
      const dx = e.clientX - sx;
      if (Math.abs(dx) > 46) goTour(ti + (dx < 0 ? 1 : -1), true);
      sx = null;
    });
    stage.addEventListener('pointercancel', () => { sx = null; });
  }

  let tourInView = false;
  const tourSection = $('#paso-1');
  if (tourSection) {
    new IntersectionObserver(
      ([e]) => {
        tourInView = e.isIntersecting;
        if (!tourInView) stopTimer();
        else if (playing && !timer) startTimer();
      },
      { threshold: 0.25 }
    ).observe(tourSection);
  }

  /* ---------- modal ---------- */
  const modal = $('#tmodal');
  const modalScene = $('#tmodalScene');
  const modalClose = $('#tmodalClose');
  let lastFocus = null;

  function openModal(i) {
    const s = ITEMS[i];
    if (!s || !modal) return;
    const l = LANDS[s.li];
    if (modalScene) modalScene.innerHTML = roomHTML(l);
    const face = $('#tmodalFace');
    const k = $('#tmodalK');
    const title = $('#tmodalTitle');
    const desc = $('#tmodalDesc');
    const tag = $('#tmodalTag');
    const idx = $('#tmodalIndex');
    if (face) {
      const isP = s.kind === 'persona';
      face.innerHTML = isP ? s.face : '';
      face.hidden = !isP;
    }
    if (k) k.textContent = s.kicker;
    if (title) title.innerHTML = s.title;
    if (desc) desc.textContent = s.body;
    if (tag) tag.textContent = s.tag;
    if (idx) idx.textContent = s.idx;
    lastFocus = document.activeElement;
    goTour(i, true);
    modal.hidden = false;
    void modal.offsetWidth;
    modal.classList.add('open');
    document.body.classList.add('modal-open');
    if (modalClose) modalClose.focus();
  }

  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.classList.remove('open');
    document.body.classList.remove('modal-open');
    window.setTimeout(() => {
      modal.hidden = true;
      if (modalScene) modalScene.innerHTML = '';
    }, 560);
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target && e.target.dataset && e.target.dataset.close) closeModal();
    });
  }
  if (modalClose) modalClose.addEventListener('click', closeModal);

  document.addEventListener('keydown', (e) => {
    if (modal && !modal.hidden) {
      if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
      if (e.key === 'Tab') {
        const focusables = $$('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])', modal)
          .filter((el) => !el.disabled && el.offsetParent !== null);
        if (!focusables.length) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
      return;
    }
    if (!tourInView) return;
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
    if (e.key === 'ArrowRight') { e.preventDefault(); goTour(ti + 1, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTour(ti - 1, true); }
  });

  goTour(0);
  updatePlay();
  if (playing) startTimer();

  /* ---------- residents ---------- */
  const RESIDENTS = [
    { id: 'R-01', name: 'Brasa', eye: '#F0B03C', tags: ['Cálido', 'Presente'] },
    { id: 'R-02', name: 'Ámbar', eye: '#F2C25A', tags: ['Curioso', 'Rápido'] },
    { id: 'R-03', name: 'Cobre', eye: '#D9663F', tags: ['Sereno', 'Leal'] },
    { id: 'R-04', name: 'Sombra', eye: '#59BBD6', tags: ['Observa', 'Pausado'] },
    { id: 'R-05', name: 'Ceniza', eye: '#BFE06A', tags: ['Suave', 'Atenta'] },
    { id: 'R-06', name: 'Musgo', eye: '#2E9E6B', tags: ['Reservado', 'Constante'] },
    { id: 'R-07', name: 'Brisa', eye: '#8EC8F2', tags: ['Ligera', 'Atenta'] },
  ];

  const residentBox = $('#residents');
  if (residentBox) {
    residentBox.innerHTML = RESIDENTS.map((r) => `
      <article class="resident">
        <span class="rid">${r.id}</span>
        <svg class="rmark mark" viewBox="0 0 120 120" aria-hidden="true">
          <path class="m-body" d="${BUBBLE}"/>
          <g clip-path="url(#cl-horizon)">
            <circle class="m-sun" cx="78" cy="41" r="9.5" style="fill:${r.eye}"/>
            <circle class="m-pupil" cx="81" cy="41" r="4.2"/>
            <circle class="m-glint" cx="82.6" cy="39.6" r="1.5"/>
            <path class="m-hill1" d="${HILL1}"/>
            <path class="m-hill2" d="${HILL2}"/>
          </g>
          <path class="m-line" d="${BUBBLE}"/>
        </svg>
        <h3>${r.id} · ${r.name}</h3>
        <div class="rtags">${r.tags.map((t) => `<span>${t}</span>`).join('')}</div>
      </article>`).join('');
  }

  $$('.chip[data-anim]').forEach((chip) => {
    chip.addEventListener('click', () => {
      const anim = chip.dataset.anim;
      $$('.chip[data-anim]').forEach((c) => c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'));
      if (residentBox) residentBox.dataset.anim = anim;
    });
  });

  /* ---------- light toggle ---------- */
  const lightDemo = $('#lightDemo');
  const lightToggle = $('#lightToggle');
  if (lightToggle && lightDemo) {
    lightToggle.addEventListener('click', () => {
      const on = lightDemo.classList.toggle('wire');
      lightToggle.setAttribute('aria-pressed', on ? 'true' : 'false');
      const lbl = lightToggle.querySelector('span');
      if (lbl) lbl.textContent = on ? 'Ver luz' : 'Ver malla';
    });
  }

  /* ---------- spec switch ---------- */
  const viewPlain = $('#viewPlain');
  const viewTech = $('#viewTech');
  const plainBox = $('#plainGrid');
  const spec = $('#specTable');
  if (viewPlain && viewTech) {
    const setView = (tech) => {
      viewPlain.setAttribute('aria-pressed', tech ? 'false' : 'true');
      viewTech.setAttribute('aria-pressed', tech ? 'true' : 'false');
      if (plainBox) plainBox.classList.toggle('off', tech);
      if (spec) spec.classList.toggle('on', tech);
    };
    viewPlain.addEventListener('click', () => setView(false));
    viewTech.addEventListener('click', () => setView(true));
  }
})();
