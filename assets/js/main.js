// Atwood Dsigns — behaviour and motion.
// Plain JavaScript, no dependencies. Each feature is a small function at the bottom of the file; the
// shared services above them (motion preference, scroll loop, overlays, reveals) are used by several.
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const docOrder = (a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);
  const fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
  const decoded = (img) => (img.decode ? img.decode().catch(() => {}) : Promise.resolve());
  const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 400));
  const srcsetFor = (src) => `${src.replace(/\.jpg$/, '-800.jpg')} 800w, ${src} 1500w`;

  /* ---------- motion preference, followed live ---------- */
  // Read once at load was not enough: people switch the setting while a page is open.
  const motion = (() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const subs = new Set();
    const api = { reduced: mq.matches, on: (fn) => subs.add(fn) };
    mq.addEventListener('change', (e) => { api.reduced = e.matches; subs.forEach((fn) => fn(e.matches)); });
    return api;
  })();

  /* ---------- one scroll loop for every scroll-driven feature ---------- */
  const scroll = (() => {
    const subs = new Set();
    let queued = false;
    const run = () => { queued = false; const y = window.scrollY; subs.forEach((fn) => fn(y)); };
    const queue = () => { if (!queued) { queued = true; requestAnimationFrame(run); } };
    window.addEventListener('scroll', queue, { passive: true });
    window.addEventListener('resize', queue);
    return { add: (fn) => { subs.add(fn); fn(window.scrollY); } };
  })();

  /* ---------- overlays: focus stays inside, the page behind is inert, scrolling is locked ---------- */
  const overlay = (() => {
    let scope = [], restore = null, shut = null;
    const focusables = () => scope.flatMap((el) => $$('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])', el))
      .filter((el) => el.getClientRects().length);
    const onKey = (e) => {
      if (e.key === 'Escape' && shut) { e.preventDefault(); shut(); return; }
      if (e.key !== 'Tab') return;
      const f = focusables();
      if (!f.length) return;
      const i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    };
    return {
      open(containers, onEscape) {
        scope = containers; restore = document.activeElement; shut = onEscape;
        [...document.body.children].forEach((el) => { if (!containers.includes(el) && el.tagName !== 'SCRIPT') el.inert = true; });
        root.classList.add('is-locked');
        document.addEventListener('keydown', onKey);
      },
      close() {
        [...document.body.children].forEach((el) => { el.inert = false; });
        root.classList.remove('is-locked');
        document.removeEventListener('keydown', onKey);
        const r = restore;
        scope = []; restore = null; shut = null;
        return r;
      },
    };
  })();

  /* ---------- headings split into lines that rise out of a mask ---------- */
  // Built with text nodes (never innerHTML), and re-split when the heading's width changes so the
  // masked lines always match the real line breaks after a resize or a phone rotation.
  const splitLines = (el) => {
    const text = el.dataset.text || (el.dataset.text = el.textContent.trim().replace(/\s+/g, ' '));
    el.setAttribute('aria-label', text);
    el.textContent = '';
    const words = text.split(' ').map((w, i, all) => {
      const s = document.createElement('span');
      s.textContent = w;
      el.append(s);
      if (i < all.length - 1) el.append(' ');
      return s;
    });
    const lines = [];
    let top = null;
    words.forEach((w) => { if (w.offsetTop !== top) { lines.push([]); top = w.offsetTop; } lines[lines.length - 1].push(w.textContent); });
    el.textContent = '';
    lines.forEach((words, i) => {
      const line = document.createElement('span');
      line.className = 'line';
      line.setAttribute('aria-hidden', 'true');
      line.style.setProperty('--l', i);
      const inner = document.createElement('span');
      inner.textContent = words.join(' ');
      line.append(inner);
      el.append(line);
    });
    el.dataset.w = el.clientWidth;
  };

  /* ---------- reveals: once, in reading order, choreographed per section ---------- */
  const reveal = (() => {
    const groups = new Map();
    let io = null;
    const show = (el, delay = 0) => {
      el.style.setProperty('--d', `${delay}ms`);
      if (el.hasAttribute('data-stagger')) [...el.children].forEach((c, i) => c.style.setProperty('--i', i));
      el.classList.add('is-in');
    };
    const onEnter = (entries) => {
      // Delays restart in every section, and cap at 450ms, so a late arrival never waits on another section.
      const bySection = new Map();
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        (groups.get(e.target) || []).forEach((el) => {
          const sec = el.closest('section, article, figure, .head-pic, .pano') || document.body;
          if (!bySection.has(sec)) bySection.set(sec, []);
          bySection.get(sec).push(el);
        });
      });
      bySection.forEach((list) => list.sort(docOrder).forEach((el, i) => show(el, Math.min(i * 90, 450))));
    };
    const init = () => {
      const all = $$('[data-rise], [data-open], [data-lines], [data-stagger]').filter((el) => !el.closest('.hero'));
      if (!('IntersectionObserver' in window) || motion.reduced) { all.forEach((el) => show(el)); return; }
      io = new IntersectionObserver(onEnter, { rootMargin: '0px 0px -8% 0px' });
      all.forEach((el) => {
        // A picture that opens from a clip-path is fully clipped at rest, and Chrome then never reports it
        // as intersecting, so pictures are watched through their parent.
        const t = el.hasAttribute('data-open') ? el.parentElement : el;
        if (!groups.has(t)) { groups.set(t, []); io.observe(t); }
        groups.get(t).push(el);
      });
      motion.on((reduced) => { if (reduced) all.forEach((el) => show(el)); });
    };
    return { init, show };
  })();

  /* ---------- scroll-linked pictures: slow scale and drift ---------- */
  // Browsers with scroll-driven animations run these in CSS, off the main thread. Elsewhere one rAF
  // loop updates only the pictures that are on screen.
  const parallax = () => {
    const els = $$('[data-scale], [data-drift]');
    if (!els.length) return;
    els.forEach((el) => { if (el.dataset.drift) el.style.setProperty('--drift', el.dataset.drift); });
    if (window.CSS && CSS.supports('animation-timeline: view()')) { root.classList.add('sda'); return; }
    const target = new Map(els.map((el) => [el.hasAttribute('data-scale') ? el.parentElement : el, el]));
    const visible = new Set();
    const io = new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target))), { rootMargin: '120px 0px' });
    target.forEach((_, t) => io.observe(t));
    const reset = () => els.forEach((el) => { el.style.transform = ''; el.style.translate = ''; });
    motion.on((r) => r && reset());
    scroll.add((y) => {
      if (motion.reduced) return;
      const vh = window.innerHeight;
      visible.forEach((t) => {
        const el = target.get(t);
        if (el.hasAttribute('data-scale')) {
          const r = t.getBoundingClientRect();
          const p = clamp((vh - r.top) / (vh + r.height), 0, 1);
          el.style.transform = `scale(${(1.18 - p * 0.18).toFixed(4)})`;
        } else {
          el.style.translate = `0 ${(Math.min(y, vh) * parseFloat(el.dataset.drift)).toFixed(1)}px`;
        }
      });
    });
  };

  /* ---------- header: solid after the first screen, hides on the way down ---------- */
  const header = () => {
    const h = $('.site-header');
    if (!h) return;
    const light = h.classList.contains('site-header--light');
    let last = window.scrollY;
    scroll.add((y) => {
      h.classList.toggle('is-solid', light ? y > 10 : y > window.innerHeight * 0.6);
      if (!root.classList.contains('is-locked')) {
        if (y > 500 && y > last + 4) h.classList.add('is-hidden');
        else if (y < last - 4 || y < 500) h.classList.remove('is-hidden');
      }
      last = y;
    });
    h.addEventListener('focusin', () => h.classList.remove('is-hidden'));
  };

  /* ---------- full-screen menu ---------- */
  const menu = () => {
    const toggle = $('.menu-toggle');
    const panel = $('#menu-panel');
    const h = $('.site-header');
    if (!toggle || !panel) return;
    panel.inert = true;
    const set = (open) => {
      if (open === panel.classList.contains('is-open')) return;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
      panel.classList.toggle('is-open', open);
      panel.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('menu-open', open);
      if (open) {
        overlay.open([h, panel], () => set(false));
        panel.inert = false;
        $('a', panel).focus();
      } else {
        const back = overlay.close();
        panel.inert = true;
        (back && back !== document.body ? back : toggle).focus();
      }
    };
    toggle.addEventListener('click', () => set(!panel.classList.contains('is-open')));
    window.matchMedia('(min-width: 1101px)').addEventListener('change', (e) => e.matches && set(false));
  };

  /* ---------- home hero: an opening sequence, then light shifting across the main print ---------- */
  const hero = () => {
    const sec = $('.hero');
    if (!sec) return;
    const imgs = $$('.hero__big img', sec);
    const caption = $('.hero__room span', sec);
    const toggle = $('.slide-toggle', sec);
    const label = toggle && $('.label', toggle);

    // The shutter waits for the type and the first picture, so it never opens on an empty frame.
    const open = () => {
      if (sec.classList.contains('is-ready')) return;
      sec.classList.add('is-ready');
      $$('[data-lines]', sec).forEach((el) => reveal.show(el, motion.reduced ? 0 : 450));
      $$('[data-rise]', sec).forEach((el) => reveal.show(el, motion.reduced ? 0 : 800));
    };
    Promise.all([fontsReady, decoded(imgs[0])]).then(() => requestAnimationFrame(open));
    setTimeout(open, 2500);

    if (imgs.length < 2 || !toggle) return;
    let i = 0, timer = 0, paused = motion.reduced, inView = true;
    const playing = () => !paused && inView && !document.hidden;
    const go = async (n) => {
      const next = imgs[n];
      next.loading = 'eager';
      await decoded(next); // never fade to a picture that has not arrived
      imgs[i].classList.remove('is-on');
      next.classList.add('is-on');
      i = n;
      caption.classList.add('is-swapping');
      setTimeout(() => { caption.textContent = next.dataset.name; caption.classList.remove('is-swapping'); }, 300);
      const after = imgs[(n + 1) % imgs.length];
      idle(() => { after.loading = 'eager'; });
    };
    const sync = () => {
      clearInterval(timer);
      if (playing()) timer = setInterval(() => go((i + 1) % imgs.length), 6000);
      toggle.setAttribute('aria-pressed', String(paused));
      label.textContent = paused ? 'Play' : 'Pause';
    };
    toggle.addEventListener('click', () => { paused = !paused; sync(); });
    new IntersectionObserver(([e]) => { inView = e.isIntersecting; sync(); }).observe(sec);
    document.addEventListener('visibilitychange', sync);
    motion.on((r) => { if (r) { paused = true; sync(); } });
    sync();
  };

  /* ---------- drawn, then built: comparison slider and room selector ---------- */
  const compare = () => {
    const box = $('.compare');
    if (!box) return;
    const range = $('input', box);
    const name = $('.compare__name', box);
    let built = $('.compare__built', box);
    let drawn = $('.compare__drawn', box);
    let pos = 50, anim = 0;

    const set = (v) => {
      pos = clamp(v, 0, 100);
      box.style.setProperty('--pos', `${pos}%`);
      box.style.setProperty('--p', pos);
      range.value = Math.round(pos);
      range.setAttribute('aria-valuetext', `${Math.round(pos)}% drawing, ${100 - Math.round(pos)}% built`);
    };
    const animateTo = (to, dur = 600) => {
      cancelAnimationFrame(anim);
      if (motion.reduced) { set(to); return; }
      const from = pos, t0 = performance.now();
      const step = (t) => {
        const k = Math.min(1, (t - t0) / dur);
        set(from + (to - from) * (1 - Math.pow(1 - k, 4)));
        if (k < 1) anim = requestAnimationFrame(step);
      };
      anim = requestAnimationFrame(step);
    };
    range.addEventListener('input', () => { cancelAnimationFrame(anim); set(+range.value); });

    // Pointer: grab anywhere on the picture. A touch only takes over once it is clearly horizontal,
    // so a vertical swipe over the picture still scrolls the page.
    const at = (e) => { const r = box.getBoundingClientRect(); return ((e.clientX - r.left) / r.width) * 100; };
    let drag = null;
    box.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;
      cancelAnimationFrame(anim);
      drag = { x: e.clientX, y: e.clientY, id: e.pointerId, live: e.pointerType === 'mouse' };
      if (drag.live) { box.setPointerCapture(e.pointerId); box.classList.add('is-dragging'); set(at(e)); }
    });
    box.addEventListener('pointermove', (e) => {
      if (!drag || e.pointerId !== drag.id) return;
      if (!drag.live) {
        const dx = Math.abs(e.clientX - drag.x), dy = Math.abs(e.clientY - drag.y);
        if (dy > 10 && dy > dx) { drag = null; return; }
        if (dx < 8) return;
        drag.live = true;
        box.setPointerCapture(e.pointerId);
        box.classList.add('is-dragging');
      }
      set(at(e));
    });
    const end = (e) => {
      if (!drag) return;
      if (!drag.live && e.type === 'pointerup') animateTo(at(e), 500); // a tap moves the divider there
      drag = null;
      box.classList.remove('is-dragging');
    };
    box.addEventListener('pointerup', end);
    box.addEventListener('pointercancel', end);

    // The first time it is seen, the divider sweeps across once to show that it moves.
    set(motion.reduced ? 50 : 96);
    new IntersectionObserver(([e], o) => {
      if (!e.isIntersecting) return;
      o.disconnect();
      animateTo(50, 1800);
      idle(() => $$('.rooms button').forEach((b) => ['built', 'drawn'].forEach((k) => {
        const im = new Image();
        im.sizes = built.sizes; im.srcset = srcsetFor(b.dataset[k]); im.src = b.dataset[k];
      })));
    }, { threshold: 0.4 }).observe(box.parentElement);

    // Rooms crossfade on a second layer instead of blanking the frame, and keep the divider where it is.
    const buttons = $$('.rooms button');
    let token = 0;
    const swap = async (b) => {
      const mine = ++token;
      const nb = built.cloneNode(), nd = drawn.cloneNode();
      [[nb, b.dataset.built], [nd, b.dataset.drawn]].forEach(([im, src]) => {
        im.removeAttribute('fetchpriority'); im.loading = 'eager';
        im.srcset = srcsetFor(src); im.src = src; im.classList.add('is-entering');
      });
      nb.alt = b.dataset.alt;
      await Promise.all([decoded(nb), decoded(nd)]);
      if (mine !== token) return;
      built.after(nb); drawn.after(nd);
      requestAnimationFrame(() => requestAnimationFrame(() => { nb.classList.remove('is-entering'); nd.classList.remove('is-entering'); }));
      const oldB = built, oldD = drawn;
      built = nb; drawn = nd;
      name.textContent = b.textContent;
      setTimeout(() => { oldB.remove(); oldD.remove(); }, motion.reduced ? 0 : 650);
    };
    buttons.forEach((b, i) => {
      b.addEventListener('click', () => {
        if (b.getAttribute('aria-pressed') === 'true') return;
        buttons.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        swap(b);
      });
      b.addEventListener('keydown', (e) => {
        const to = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: buttons.length - 1 }[e.key];
        if (to === undefined) return;
        e.preventDefault();
        buttons[(to + buttons.length) % buttons.length].focus();
      });
    });
  };

  /* ---------- the ten stages: drag with momentum, buttons, keys, progress ---------- */
  const timeline = (wrap) => {
    const row = $('.row', wrap);
    const items = $$('.moment', row);
    const bar = $('.progress span', wrap);
    const count = $('.moments__count b', wrap);
    const status = $('[data-row-status]', wrap);
    const prev = $('[data-dir="prev"]', wrap);
    const next = $('[data-dir="next"]', wrap);
    const pitch = () => (items[1] ? items[1].offsetLeft - items[0].offsetLeft : row.clientWidth);
    const range = () => {
      const first = clamp(Math.round(row.scrollLeft / pitch()), 0, items.length - 1);
      const shown = Math.max(1, Math.floor((row.clientWidth + 8) / pitch()));
      return [first + 1, Math.min(items.length, first + shown)];
    };
    const update = () => {
      const max = row.scrollWidth - row.clientWidth;
      const p = max > 0 ? row.scrollLeft / max : 1;
      bar.style.transform = `scaleX(${Math.max(0.06, p).toFixed(4)})`;
      if (prev) prev.disabled = row.scrollLeft < 4;
      if (next) next.disabled = row.scrollLeft > max - 4;
      const [a, b] = range();
      count.textContent = a === b ? `${a}` : `${a} to ${b}`;
    };
    let queued = false;
    row.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; update(); }); } }, { passive: true });
    window.addEventListener('resize', update);
    update();

    const announce = () => setTimeout(() => { const [a, b] = range(); status.textContent = `Showing stages ${a} to ${b} of ${items.length}: ${$('h3', items[a - 1]).textContent}`; }, 450);
    const goTo = (index) => {
      row.scrollTo({ left: clamp(index, 0, items.length - 1) * pitch(), behavior: motion.reduced ? 'auto' : 'smooth' });
      announce();
    };
    const page = (dir) => { const [a, b] = range(); goTo(a - 1 + dir * Math.max(1, b - a + 1)); };
    prev && prev.addEventListener('click', () => page(-1));
    next && next.addEventListener('click', () => page(1));
    row.addEventListener('keydown', (e) => {
      const [a] = range();
      const to = { ArrowRight: a, ArrowLeft: a - 2, Home: 0, End: items.length - 1 }[e.key];
      if (to === undefined) return;
      e.preventDefault();
      goTo(to);
    });

    // Mouse drag with momentum; touch keeps the browser's own scrolling and snapping.
    let drag = null, glide = 0;
    const settle = () => {
      row.classList.remove('is-dragging');
      row.scrollTo({ left: Math.round(row.scrollLeft / pitch()) * pitch(), behavior: motion.reduced ? 'auto' : 'smooth' });
    };
    row.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      cancelAnimationFrame(glide);
      drag = { x: e.clientX, s: row.scrollLeft, v: 0, t: performance.now(), lx: e.clientX, moved: false };
    });
    window.addEventListener('pointermove', (e) => {
      if (!drag) return;
      const dx = e.clientX - drag.x;
      if (!drag.moved && Math.abs(dx) > 5) { drag.moved = true; row.classList.add('is-dragging'); }
      if (!drag.moved) return;
      const now = performance.now();
      drag.v = (drag.lx - e.clientX) / Math.max(1, now - drag.t); // px per ms
      drag.t = now; drag.lx = e.clientX;
      row.scrollLeft = drag.s - dx;
    });
    window.addEventListener('pointerup', () => {
      if (!drag) return;
      const { moved } = drag;
      let v = drag.v * 16; // px per frame
      drag = null;
      if (!moved) return;
      if (motion.reduced || Math.abs(v) < 1) { settle(); return; }
      const step = () => {
        row.scrollLeft += v;
        v *= 0.92;
        if (Math.abs(v) > 0.6) glide = requestAnimationFrame(step); else settle();
      };
      glide = requestAnimationFrame(step);
    });
  };

  /* ---------- quotations over a photograph ---------- */
  const quotes = () => {
    const qs = $('.quote-sec');
    if (!qs) return;
    const box = $('.quotes', qs);
    const figs = $$('figure', box);
    const imgs = $$('.slides img', qs);
    const count = $('.count', qs);
    const toggle = $('.slide-toggle', qs);
    const paired = imgs.length === figs.length;
    let i = 0, timer = 0, paused = motion.reduced, held = false, inView = false;
    const show = (n, manual) => {
      figs[i].classList.remove('is-on'); if (paired) imgs[i].classList.remove('is-on');
      i = (n + figs.length) % figs.length;
      figs[i].classList.add('is-on'); if (paired) imgs[i].classList.add('is-on');
      count.textContent = `${i + 1} of ${figs.length}`;
      // Only a quotation the visitor asked for is read out; automatic changes stay silent.
      box.setAttribute('aria-live', manual ? 'polite' : 'off');
    };
    const sync = () => {
      clearInterval(timer);
      if (!paused && !held && inView && !document.hidden) timer = setInterval(() => show(i + 1, false), 7500);
      toggle.setAttribute('aria-pressed', String(paused));
      toggle.setAttribute('aria-label', paused ? 'Play quotations' : 'Pause quotations');
    };
    $('[data-q="prev"]', qs).addEventListener('click', () => { show(i - 1, true); sync(); });
    $('[data-q="next"]', qs).addEventListener('click', () => { show(i + 1, true); sync(); });
    toggle.addEventListener('click', () => { paused = !paused; sync(); });
    qs.addEventListener('mouseenter', () => { held = true; sync(); });
    qs.addEventListener('mouseleave', () => { held = false; sync(); });
    qs.addEventListener('focusin', () => { held = true; sync(); });
    qs.addEventListener('focusout', (e) => { if (!qs.contains(e.relatedTarget)) { held = false; sync(); } });
    let sx = null;
    qs.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') sx = e.clientX; });
    qs.addEventListener('pointerup', (e) => {
      if (sx === null) return;
      const dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 50) { show(i + (dx < 0 ? 1 : -1), true); sync(); }
    });
    new IntersectionObserver(([e]) => { inView = e.isIntersecting; sync(); }, { threshold: 0.3 }).observe(qs);
    document.addEventListener('visibilitychange', sync);
    motion.on((r) => { if (r) { paused = true; sync(); } });
    sync();
  };

  /* ---------- cursor label over pictures that open the portfolio ---------- */
  const cursor = () => {
    const targets = $$('[data-cursor]');
    if (!targets.length || !window.matchMedia('(pointer: fine)').matches) return;
    const c = document.createElement('div');
    c.className = 'cursor';
    c.setAttribute('aria-hidden', 'true');
    document.body.appendChild(c);
    let x = -200, y = -200, cx = x, cy = y, raf = 0, on = false;
    const loop = () => {
      cx += (x - cx) * 0.22; cy += (y - cy) * 0.22;
      c.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      raf = on || Math.abs(x - cx) > 0.5 ? requestAnimationFrame(loop) : 0;
    };
    window.addEventListener('pointermove', (e) => { x = e.clientX; y = e.clientY; if (on && !raf) raf = requestAnimationFrame(loop); }, { passive: true });
    targets.forEach((t) => {
      t.addEventListener('pointerenter', (e) => {
        if (motion.reduced || e.pointerType !== 'mouse') return;
        c.textContent = t.dataset.cursor; on = true; cx = x; cy = y;
        c.classList.add('is-on');
        if (!raf) raf = requestAnimationFrame(loop);
      });
      t.addEventListener('pointerleave', () => { on = false; c.classList.remove('is-on', 'is-down'); });
      t.addEventListener('pointerdown', () => c.classList.add('is-down'));
      t.addEventListener('pointerup', () => c.classList.remove('is-down'));
    });
  };

  /* ---------- moving between pages ---------- */
  // Browsers with cross-document view transitions animate the change in CSS and keep the header in place;
  // the page is prefetched on hover by the speculation rules in the head. Other browsers get a short fade
  // and a hover prefetch from here.
  const pageTransitions = () => {
    const internal = (a) => {
      if (!a || a.target || a.hasAttribute('download')) return null;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || !/\.html$|\/$/.test(url.pathname)) return null;
      if (url.pathname === location.pathname) return null;
      return url;
    };
    if (!(HTMLScriptElement.supports && HTMLScriptElement.supports('speculationrules')) && location.protocol !== 'file:') {
      const done = new Set();
      const prefetch = (e) => {
        const url = internal(e.target.closest && e.target.closest('a'));
        if (!url || done.has(url.pathname)) return;
        done.add(url.pathname);
        const l = document.createElement('link');
        l.rel = 'prefetch'; l.href = url.href;
        document.head.appendChild(l);
      };
      document.addEventListener('pointerover', prefetch, { passive: true });
      document.addEventListener('focusin', prefetch);
    }
    if (root.classList.contains('vt')) return;
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a');
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || motion.reduced) return;
      if (!internal(a) || a.closest('.gallery')) return;
      e.preventDefault();
      document.body.classList.add('is-leaving');
      setTimeout(() => { location.href = a.href; }, 200);
    });
    window.addEventListener('pageshow', (e) => { if (e.persisted) document.body.classList.remove('is-leaving'); });
  };

  /* ---------- portfolio: animated filtering, kept in the address, and a lightbox ---------- */
  const portfolio = () => {
    const gallery = $('.gallery');
    if (!gallery) return;
    const items = $$('a', gallery);
    const buttons = $$('[data-filter]');
    const status = $('#filter-status');
    const names = { all: '', residential: 'residential ', commercial: 'commercial ' };

    const apply = async (f, animate) => {
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
      const keep = new Set(items.filter((a) => f === 'all' || a.dataset.cat === f));
      if (!animate || motion.reduced) {
        items.forEach((a) => { a.hidden = !keep.has(a); });
      } else {
        // FLIP: note where every visible picture is, let the leaving ones fade, re-flow, then glide the
        // rest from their old place to the new one while the newcomers settle in.
        const before = new Map(items.filter((a) => !a.hidden).map((a) => [a, a.getBoundingClientRect()]));
        const leaving = items.filter((a) => !a.hidden && !keep.has(a));
        leaving.forEach((a) => a.classList.add('is-leaving'));
        if (leaving.length) await wait(220);
        items.forEach((a) => { a.hidden = !keep.has(a); a.classList.remove('is-leaving'); });
        const vh = window.innerHeight;
        let n = 0;
        keep.forEach((a) => {
          const now = a.getBoundingClientRect();
          if (now.bottom < -200 || now.top > vh + 200) return;
          const was = before.get(a);
          if (was) {
            const dx = was.left - now.left, dy = was.top - now.top;
            if (dx || dy) a.animate([{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }], { duration: 650, easing: 'cubic-bezier(.16,1,.3,1)' });
          } else {
            a.animate([{ opacity: 0, transform: 'scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: 550, delay: Math.min(n++ * 35, 400), easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards' });
          }
        });
      }
      status.textContent = `Showing ${keep.size} ${names[f]}projects`;
      history.replaceState(null, '', f === 'all' ? location.pathname : `#${f}`);
    };
    buttons.forEach((b) => b.addEventListener('click', () => apply(b.dataset.filter, true)));
    const fromHash = () => { const f = location.hash.slice(1); if (f in names && f !== 'all') apply(f, false); };
    fromHash();
    window.addEventListener('hashchange', fromHash);

    const lb = $('.lightbox');
    document.body.appendChild(lb); // a direct child of body, so everything else can be made inert while it is open
    const lbImg = $('img', lb);
    const lbCaption = $('.lb-caption', lb);
    const lbIndex = $('.lb-index', lb);
    lb.inert = true;
    let list = [], idx = 0, ticket = 0;
    const load = (a) => new Promise((res) => { const im = new Image(); im.onload = im.onerror = () => res(im); im.src = a.href; });
    const show = async (n) => {
      idx = (n + list.length) % list.length;
      const a = list[idx], mine = ++ticket;
      lbCaption.textContent = $('img', a).alt;
      lbIndex.textContent = `${idx + 1} of ${list.length}`;
      lb.classList.add('is-loading');
      await load(a);
      if (mine !== ticket) return;
      lbImg.src = a.href;
      lbImg.alt = $('img', a).alt;
      lb.classList.remove('is-loading');
      idle(() => [1, -1].forEach((d) => load(list[(idx + d + list.length) % list.length]))); // neighbours ready
    };
    const close = () => {
      if (!lb.classList.contains('is-open')) return;
      lb.classList.remove('is-open');
      lb.setAttribute('aria-hidden', 'true');
      lb.inert = true;
      overlay.close();
      const back = list[idx];
      back.focus({ preventScroll: true });
      back.scrollIntoView({ block: 'nearest', behavior: motion.reduced ? 'auto' : 'smooth' }); // the photo last viewed
    };
    items.forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      list = items.filter((x) => !x.hidden);
      lb.inert = false;
      lb.classList.add('is-open');
      lb.setAttribute('aria-hidden', 'false');
      overlay.open([lb], close);
      show(list.indexOf(a));
      $('.lb-close', lb).focus();
    }));
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    lb.addEventListener('keydown', (e) => {
      const to = { ArrowRight: idx + 1, ArrowLeft: idx - 1, Home: 0, End: list.length - 1 }[e.key];
      if (to === undefined) return;
      e.preventDefault();
      show(to);
    });
    let sx = null, sy = 0;
    lb.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') { sx = e.clientX; sy = e.clientY; } });
    lb.addEventListener('pointerup', (e) => {
      if (sx === null) return;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      sx = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) close(); // swipe down to close
    });
  };

  /* ---------- enquiry form: email or WhatsApp with the details filled in ---------- */
  const enquiry = () => {
    const form = $('#enquiry');
    if (!form) return;
    const KEY = 'atwood-enquiry';
    const fields = ['name', 'phone', 'email', 'type', 'message'];
    const required = ['name', 'phone', 'email', 'message'];
    const statusBox = $('.form-status', form);
    const store = {
      get() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } },
      set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* storage unavailable */ } },
      clear() { try { localStorage.removeItem(KEY); } catch { /* storage unavailable */ } },
    };

    // Restore an unsent draft, then let a "Plan your kitchen with us" link choose the project type.
    const draft = store.get();
    fields.forEach((n) => { if (draft[n] && !form.elements[n].value) form.elements[n].value = draft[n]; });
    const wanted = new URLSearchParams(location.search).get('type');
    if (wanted) {
      const opt = [...form.elements.type.options].find((o) => o.value.toLowerCase() === wanted.toLowerCase());
      if (opt) form.elements.type.value = opt.value;
    }
    let saveT = 0;
    form.addEventListener('input', (e) => {
      clearTimeout(saveT);
      saveT = setTimeout(() => store.set(Object.fromEntries(fields.map((n) => [n, form.elements[n].value]))), 300);
      const f = e.target.closest('.field');
      if (f && f.classList.contains('invalid') && check(e.target)) { f.classList.remove('invalid'); e.target.setAttribute('aria-invalid', 'false'); }
    });

    // Phone numbers are accepted with spaces, dashes or brackets; 10 digits, or a +country code.
    const phoneOk = (v) => { const d = v.replace(/[^\d+]/g, ''); return /^(\+\d{10,14}|0?\d{10})$/.test(d); };
    const check = (el) => (el.name === 'phone' ? el.value.trim() !== '' && phoneOk(el.value) : el.checkValidity());
    const validate = () => {
      let first = null;
      required.forEach((n) => {
        const el = form.elements[n];
        const ok = check(el);
        el.closest('.field').classList.toggle('invalid', !ok);
        el.setAttribute('aria-invalid', String(!ok));
        if (!ok && !first) first = el;
      });
      if (first) first.focus();
      return !first;
    };
    const v = (n) => form.elements[n].value.trim();
    const body = () => `Name: ${v('name')}\nPhone: ${v('phone')}\nEmail: ${v('email')}\nProject: ${v('type')}\n\n${v('message')}`;

    // After sending, say what should have happened and offer a way out if it did not.
    const report = (channel) => {
      statusBox.textContent = '';
      const p = document.createElement('p');
      p.textContent = channel === 'email'
        ? 'Your email app should now be open with your message ready to send. If nothing opened, copy the message and email it to atwood.dsigns@gmail.com.'
        : 'WhatsApp should now be open in a new tab with your message ready to send. If it did not open, copy the message and send it to +91 90001 81212.';
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'link link--accent';
      btn.textContent = 'Copy message';
      btn.addEventListener('click', async () => {
        try { await navigator.clipboard.writeText(body()); btn.textContent = 'Message copied'; }
        catch { btn.textContent = 'Select and copy the fields above'; }
      });
      statusBox.append(p, btn);
      statusBox.classList.add('is-on');
      clearTimeout(saveT); // a save still waiting from the last keystroke must not bring the draft back
      store.clear();
    };
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!validate()) return;
      const subject = `Consultation request: ${v('type')}`;
      window.location.href = `mailto:atwood.dsigns@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body())}`;
      report('email');
    });
    $('[data-whatsapp]', form).addEventListener('click', () => {
      if (!validate()) return;
      window.open(`https://wa.me/919000181212?text=${encodeURIComponent(body())}`, '_blank', 'noopener');
      report('whatsapp');
    });
  };

  /* ---------- start ---------- */
  root.classList.add('ready'); // the head script reveals everything if this line never runs
  header();
  menu();
  parallax();
  pageTransitions();
  fontsReady.then(() => {
    const heads = $$('[data-lines]');
    heads.forEach(splitLines);
    if ('ResizeObserver' in window) {
      let t = 0;
      const pending = new Set();
      const ro = new ResizeObserver((entries) => {
        entries.forEach((en) => { if (Math.abs(en.target.clientWidth - en.target.dataset.w) > 2) pending.add(en.target); });
        clearTimeout(t);
        t = setTimeout(() => { pending.forEach(splitLines); pending.clear(); }, 150);
      });
      heads.forEach((el) => ro.observe(el));
    }
    reveal.init();
    hero();
  });
  compare();
  $$('[data-row]').forEach(timeline);
  quotes();
  cursor();
  portfolio();
  enquiry();
  const y = $('#year');
  if (y) y.textContent = new Date().getFullYear();
})();
