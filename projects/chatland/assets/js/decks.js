/* ============================================================
   CHATLAND · diapositivas (secciones 02–07)
   Controlador genérico para cualquier [data-deck].
   ============================================================ */
(() => {
  'use strict';

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const pad = (n) => String(n).padStart(2, '0');

  $$('[data-deck]').forEach((deck) => {
    const slides = $$('.deck-slide', deck);
    if (!slides.length) return;

    const dotsBox = $('.deck-dots', deck);
    const count = $('.deck-count', deck);
    const prev = $('[data-deck-prev]', deck);
    const next = $('[data-deck-next]', deck);
    const stage = $('.deck-stage', deck);
    let i = 0;

    if (dotsBox) {
      dotsBox.innerHTML = slides
        .map((_, k) => `<button type="button" class="deck-dot" role="tab"
          aria-label="Diapositiva ${k + 1} de ${slides.length}"
          aria-selected="${k === 0}"></button>`)
        .join('');
    }
    const dots = $$('.deck-dot', deck);

    const show = (n) => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => {
        const on = k === i;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
        if (on) s.removeAttribute('inert');
        else s.setAttribute('inert', '');
      });
      dots.forEach((d, k) => d.setAttribute('aria-selected', String(k === i)));
      if (count) count.textContent = pad(i + 1) + ' / ' + pad(slides.length);
    };

    if (prev) prev.addEventListener('click', () => show(i - 1));
    if (next) next.addEventListener('click', () => show(i + 1));
    dots.forEach((d, k) => d.addEventListener('click', () => show(k)));

    /* teclado: solo cuando el foco está dentro de esta baraja */
    deck.addEventListener('keydown', (e) => {
      if (!deck.contains(document.activeElement)) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); show(i + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(i - 1); }
    });

    /* deslizar en táctil */
    if (stage) {
      let x0 = null;
      let y0 = null;
      stage.addEventListener('pointerdown', (e) => {
        if (e.pointerType === 'mouse') return;
        x0 = e.clientX; y0 = e.clientY;
      });
      stage.addEventListener('pointerup', (e) => {
        if (x0 === null) return;
        const dx = e.clientX - x0;
        const dy = e.clientY - y0;
        if (Math.abs(dx) > 46 && Math.abs(dx) > Math.abs(dy)) show(i + (dx < 0 ? 1 : -1));
        x0 = null; y0 = null;
      });
      stage.addEventListener('pointercancel', () => { x0 = null; y0 = null; });
    }

    show(0);
  });
})();
