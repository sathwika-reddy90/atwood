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
          el.style.transform = `scale(${(1.08 - p * 0.08).toFixed(4)})`;
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
    const light = !h.classList.contains('site-header--over'); // no photograph behind it: solid as soon as the page moves
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

  /* ---------- home hero: the type follows once the photograph has decoded ---------- */
  const hero = () => {
    const sec = $('.hero');
    if (!sec) return;
    const imgs = $$('.hero__pic img', sec);
    const caption = $('.hero__room span:last-child', sec);
    const roomLink = $('.hero__room', sec);
    const count = $('.hero__count', sec);
    const bars = $$('.hero__bars i', sec);
    const toggle = $('.slide-toggle', sec);
    const label = toggle && $('.tlabel', toggle);

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
    if (bars[0]) bars[0].classList.add('is-on');
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
      if (roomLink && next.dataset.href) roomLink.href = next.dataset.href;
      if (count) count.textContent = `${String(n + 1).padStart(2, '0')} / ${String(imgs.length).padStart(2, '0')}`;
      bars.forEach((b, k) => b.classList.toggle('is-on', k === n));
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

  /* ---------- room by room: the studio's photographs, one room type at a time ---------- */
  const viewer = () => {
    const root = $('[data-viewer]');
    if (!root) return;
    const frame = $('.viewer__frame', root);
    const altEl = $('.viewer__alt', root);
    const countEl = $('.viewer__count', root);
    const thumbsEl = $('.viewer__thumbs', root);
    const more = $('.viewer__more', root);
    const rooms = $$('.viewer__rooms button', root);
    const pad = (n) => String(n).padStart(2, '0');
    let photos = [], idx = 0, ticket = 0;
    const parse = (b) => b.dataset.photos.split('|').map((p) => {
      const [src, alt, small, w] = p.split('::');
      return { src, alt, srcset: small ? `${small} 800w, ${src} ${w}w` : '' };
    });

    const show = async (n) => {
      idx = (n + photos.length) % photos.length;
      const { src, alt, srcset } = photos[idx], mine = ++ticket;
      countEl.textContent = `${pad(idx + 1)} / ${pad(photos.length)}`;
      $$('button', thumbsEl).forEach((t, i) => t.setAttribute('aria-pressed', String(i === idx)));
      const im = new Image();
      im.alt = alt; im.sizes = '(max-width: 960px) 100vw, 66vw';
      if (srcset) im.srcset = srcset;
      im.src = src;
      await decoded(im); // crossfade only to a photograph that has arrived
      if (mine !== ticket) return;
      const old = $('img.is-on', frame);
      frame.appendChild(im);
      requestAnimationFrame(() => requestAnimationFrame(() => { im.classList.add('is-on'); if (old) old.classList.remove('is-on'); }));
      setTimeout(() => { $$('img', frame).forEach((x) => { if (x !== im) x.remove(); }); }, motion.reduced ? 0 : 650);
      altEl.textContent = alt;
      const next = photos[(idx + 1) % photos.length];
      idle(() => { const p = new Image(); p.sizes = im.sizes; if (next.srcset) p.srcset = next.srcset; p.src = next.src; });
    };
    const choose = (b) => {
      rooms.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      photos = parse(b);
      const name = $('span', b).textContent;
      thumbsEl.textContent = '';
      photos.forEach((ph, i) => {
        const t = document.createElement('button');
        t.type = 'button';
        t.setAttribute('aria-label', `Photograph ${i + 1}: ${ph.alt}`);
        const ti = document.createElement('img');
        ti.alt = ''; ti.loading = 'lazy'; ti.decoding = 'async'; ti.sizes = '120px';
        if (ph.srcset) ti.srcset = ph.srcset;
        ti.src = ph.src;
        t.appendChild(ti);
        t.addEventListener('click', () => show(i));
        thumbsEl.appendChild(t);
      });
      more.href = `portfolio.html#${b.dataset.cat}`;
      more.setAttribute('aria-label', `See ${name.toLowerCase()} in the portfolio`);
      show(0);
    };
    // the first room is already in the page; wire its thumbnails rather than rebuilding them
    photos = parse(rooms[0]);
    $$('button', thumbsEl).forEach((t, i) => t.addEventListener('click', () => show(i)));
    rooms.forEach((b, i) => {
      b.addEventListener('click', () => { if (b.getAttribute('aria-pressed') !== 'true') choose(b); });
      b.addEventListener('keydown', (e) => {
        const to = { ArrowDown: i + 1, ArrowRight: i + 1, ArrowUp: i - 1, ArrowLeft: i - 1, Home: 0, End: rooms.length - 1 }[e.key];
        if (to === undefined) return;
        e.preventDefault();
        rooms[(to + rooms.length) % rooms.length].focus();
      });
    });
    $('.viewer__prev', root).addEventListener('click', () => show(idx - 1));
    $('.viewer__next', root).addEventListener('click', () => show(idx + 1));
    $('.viewer__stage', root).addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    });
    let sx = null;
    frame.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') sx = e.clientX; });
    frame.addEventListener('pointerup', (e) => {
      if (sx === null) return;
      const dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    });
  };

  /* ---------- the ten stages: drag with momentum, buttons, keys, progress ---------- */
  const timeline = (wrap) => {
    const row = $('.row', wrap);
    const items = $$('.moment', row);
    const bar = $('.progress span', wrap);
    const ticks = $$('.rail [data-goto]', wrap);
    const count = $('.moments__count b', wrap);
    const status = $('[data-row-status]', wrap);
    const prev = $('[data-dir="prev"]', wrap);
    const next = $('[data-dir="next"]', wrap);
    const pitch = () => (items[1] ? items[1].offsetLeft - items[0].offsetLeft : row.clientWidth);
    const range = () => {
      const first = clamp(Math.round(row.scrollLeft / pitch()), 0, items.length - 1);
      const shown = Math.max(1, Math.round(row.clientWidth / pitch()));
      return [first + 1, Math.min(items.length, first + shown)];
    };
    const update = () => {
      const max = row.scrollWidth - row.clientWidth;
      const p = max > 0 ? row.scrollLeft / max : 1;
      if (bar) bar.style.transform = `scaleX(${Math.max(0.06, p).toFixed(4)})`;
      if (prev) prev.disabled = row.scrollLeft < 4;
      if (next) next.disabled = row.scrollLeft > max - 4;
      const [a, b] = range();
      count.textContent = a === b ? `${a}` : `${a} to ${b}`;
      // the stages in view are active: full strength in the row, bronze on the rail
      items.forEach((it, i) => it.classList.toggle('is-active', i >= a - 1 && i <= b - 1));
      ticks.forEach((t, i) => {
        const on = i >= a - 1 && i <= b - 1;
        t.classList.toggle('is-active', on);
        if (i === a - 1) t.setAttribute('aria-current', 'step'); else t.removeAttribute('aria-current');
      });
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
    ticks.forEach((t) => t.addEventListener('click', () => goTo(+t.dataset.goto)));
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

  /* ---------- portfolio: animated filtering, kept in the address, and a photograph viewer ---------- */
  const portfolio = () => {
    const gallery = $('.gallery');
    if (!gallery) return;
    const cards = $$('.card', gallery);
    const buttons = $$('[data-filter]');
    const status = $('#filter-status');
    const count = $('[data-count]');
    const names = Object.fromEntries(buttons.map((b) => [b.dataset.filter, b.firstChild.textContent.trim()]));

    const apply = async (f, animate) => {
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
      const keep = new Set(cards.filter((c) => f === 'all' || c.dataset.cat === f));
      if (!animate || motion.reduced) {
        cards.forEach((c) => { c.hidden = !keep.has(c); });
      } else {
        // FLIP: note where every visible card is, let the leaving ones fade, re-flow, then glide the rest
        // from their old place to the new one while the newcomers settle in.
        const before = new Map(cards.filter((c) => !c.hidden).map((c) => [c, c.getBoundingClientRect()]));
        const leaving = cards.filter((c) => !c.hidden && !keep.has(c));
        leaving.forEach((c) => c.classList.add('is-leaving'));
        if (leaving.length) await wait(220);
        cards.forEach((c) => { c.hidden = !keep.has(c); c.classList.remove('is-leaving'); });
        const vh = window.innerHeight;
        let n = 0;
        keep.forEach((c) => {
          const now = c.getBoundingClientRect();
          if (now.bottom < -200 || now.top > vh + 200) return;
          const was = before.get(c);
          if (was) {
            const dx = was.left - now.left, dy = was.top - now.top;
            if (dx || dy) c.animate([{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }], { duration: 650, easing: 'cubic-bezier(.16,1,.3,1)' });
          } else {
            c.animate([{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }], { duration: 600, delay: Math.min(n++ * 40, 360), easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards' });
          }
        });
      }
      if (count) count.textContent = keep.size;
      status.textContent = `Showing ${keep.size} ${f === 'all' ? 'rooms' : names[f].toLowerCase()}`;
      history.replaceState(null, '', f === 'all' ? location.pathname : `#${f}`);
    };
    buttons.forEach((b) => b.addEventListener('click', () => apply(b.dataset.filter, true)));
    const fromHash = () => { const f = location.hash.slice(1); if (f in names && f !== 'all') apply(f, false); };
    fromHash();
    window.addEventListener('hashchange', fromHash);

    // Each card carries every photograph of its room; the viewer walks through all of them, room by room.
    const photosOf = (card) => card.dataset.photos.split('|').map((p) => { const [src, alt] = p.split('::'); return { src, alt, card }; });
    const lb = $('.lightbox');
    document.body.appendChild(lb); // a direct child of body, so everything else can be made inert while it is open
    const lbImg = $('img', lb);
    const lbCaption = $('.lb-caption', lb);
    const lbIndex = $('.lb-index', lb);
    lb.inert = true;
    let list = [], idx = 0, ticket = 0;
    const load = (src) => new Promise((res) => { const im = new Image(); im.onload = im.onerror = () => res(im); im.src = src; });
    const show = async (n) => {
      idx = (n + list.length) % list.length;
      const item = list[idx], mine = ++ticket;
      const room = $('h2', item.card).textContent;
      const inRoom = list.filter((x) => x.card === item.card);
      lbCaption.textContent = inRoom.length > 1 ? `${room}, photograph ${inRoom.indexOf(item) + 1} of ${inRoom.length}` : room;
      lbIndex.textContent = `${idx + 1} of ${list.length}`;
      lb.classList.add('is-loading');
      await load(item.src);
      if (mine !== ticket) return;
      lbImg.src = item.src;
      lbImg.alt = item.alt;
      lb.classList.remove('is-loading');
      idle(() => [1, -1].forEach((d) => load(list[(idx + d + list.length) % list.length].src))); // neighbours ready
    };
    const close = () => {
      if (!lb.classList.contains('is-open')) return;
      lb.classList.remove('is-open');
      lb.setAttribute('aria-hidden', 'true');
      lb.inert = true;
      overlay.close();
      const back = list[idx].card;
      back.focus({ preventScroll: true });
      back.scrollIntoView({ block: 'nearest', behavior: motion.reduced ? 'auto' : 'smooth' }); // the room last viewed
    };
    cards.forEach((card) => card.addEventListener('click', (e) => {
      e.preventDefault();
      list = cards.filter((c) => !c.hidden).flatMap(photosOf);
      lb.inert = false;
      lb.classList.add('is-open');
      lb.setAttribute('aria-hidden', 'false');
      overlay.open([lb], close);
      show(list.findIndex((x) => x.card === card));
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

  /* ---------- services list: hovering or focusing a service shows its photograph ---------- */
  const servicePreview = () => {
    const items = $$('[data-preview]');
    const imgs = $$('.svc-preview img');
    const caption = $('[data-preview-caption]');
    if (!items.length || !imgs.length) return;
    const set = (i) => {
      items.forEach((it, k) => it.classList.toggle('is-active', k === i));
      imgs.forEach((im, k) => im.classList.toggle('is-on', k === i));
      caption.textContent = imgs[i].dataset.caption;
      const idx = $('[data-preview-index]');
      if (idx) idx.textContent = imgs[i].dataset.index;
    };
    items.forEach((it, i) => { it.addEventListener('pointerenter', () => set(i)); it.addEventListener('focus', () => set(i)); });
    idle(() => imgs.forEach((im) => { im.loading = 'eager'; }));
  };

  /* ---------- in-page section links mark the section being read ---------- */
  const jumpNav = () => {
    const links = $$('.jump a');
    if (!links.length) return;
    const map = new Map(links.map((a) => [$(a.getAttribute('href')), a]).filter(([sec]) => sec));
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => { a.classList.remove('is-current'); a.removeAttribute('aria-current'); });
      const a = map.get(e.target);
      a.classList.add('is-current');
      a.setAttribute('aria-current', 'location');
    }), { rootMargin: '-45% 0px -50% 0px' });
    map.forEach((_, sec) => io.observe(sec));
  };

  /* ---------- enquiry form: email or WhatsApp with the details filled in ---------- */
  const enquiry = () => {
    const form = $('#enquiry');
    if (!form) return;
    const KEY = 'atwood-enquiry';
    const fields = ['name', 'phone', 'email', 'type', 'area', 'message'];
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
    const body = () => `Name: ${v('name')}\nPhone: ${v('phone')}\nEmail: ${v('email')}\nProject: ${v('type')}${v('area') ? `\nLocality: ${v('area')}` : ''}\n\n${v('message')}`;

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
  viewer();
  $$('[data-row]').forEach(timeline);
  quotes();
  portfolio();
  servicePreview();
  jumpNav();
  enquiry();
  const y = $('#year');
  if (y) y.textContent = new Date().getFullYear();
})();
