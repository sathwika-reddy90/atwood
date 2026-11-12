// Atwood Dsigns — behaviour. Plain JavaScript, no dependencies.
// Content is never hidden waiting for a script: the only motion is the home hero's one fade, which waits at most
// 1.2s for the web fonts. Each feature below is a small function, started at the bottom of the file.
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const decoded = (img) => (img.decode ? img.decode().catch(() => {}) : Promise.resolve());
  const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 400));

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

  /* ---------- header: solid once the page moves (or past a dark opening), hidden on the way down ---------- */
  const header = () => {
    const h = $('.site-header');
    if (!h) return;
    const over = h.classList.contains('site-header--over');
    let last = window.scrollY, queued = false;
    const update = () => {
      queued = false;
      const y = window.scrollY;
      h.classList.toggle('is-solid', over ? y > window.innerHeight * 0.6 : y > 10);
      if (!root.classList.contains('is-locked')) {
        if (y > 500 && y > last + 4) h.classList.add('is-hidden');
        else if (y < last - 4 || y < 500) h.classList.remove('is-hidden');
      }
      last = y;
    };
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
    h.addEventListener('focusin', () => h.classList.remove('is-hidden'));
    update();
  };

  /* ---------- full-screen menu below 1000px ---------- */
  const menu = () => {
    const toggle = $('.menu-toggle');
    const panel = $('#menu-panel');
    const h = $('.site-header');
    if (!toggle || !panel) return;
    const label = $('.menu-toggle__label', toggle) || toggle;
    panel.inert = true;
    const set = (open) => {
      if (open === panel.classList.contains('is-open')) return;
      toggle.setAttribute('aria-expanded', String(open));
      label.textContent = open ? 'Close' : 'Menu';
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
    window.matchMedia('(min-width: 1000px)').addEventListener('change', (e) => e.matches && set(false));
  };

  /* ---------- the ten stages: a dotted path through the stage markers, drawn as the section is read ---------- */
  // The path is measured from where the markers really are, so it meets them at every width. Scrolling down draws it
  // (it never undraws), a marker travels along it, and each stage appears as the path reaches it. With reduced motion
  // the path is drawn in full and every stage is shown.
  const journey = () => {
    $$('[data-journey]').forEach((sec) => {
      const map = $('.journey__map', sec);
      const svg = $('.journey__svg', sec);
      const list = $('.journey__stages', sec);
      const track = $('.journey__track', sec);
      const path = $('.journey__path', sec);
      const reveal = $('.journey__reveal', sec);
      const mask = $('mask', sec);
      const dot = $('.journey__dot', sec);
      const stages = $$('.jstage', sec);
      const marks = stages.map((st) => $('.jstage__mark', st));
      if (!map || !svg || marks.some((m) => !m)) return;
      let total = 0, at = [], table = [], frac = 0, queued = false, current = -1;

      const update = () => {
        queued = false;
        if (!total) return;
        const animate = root.classList.contains('motion');
        if (!animate) frac = 1;
        else {
          const r = map.getBoundingClientRect();
          const vh = window.innerHeight;
          const start = vh * 0.85, span = r.height + vh * 0.15;   // from the map's top at 85% of the screen to its foot at 70%
          frac = Math.max(frac, Math.min(1, Math.max(0, (start - r.top) / span)));
        }
        const drawn = frac * total;
        reveal.style.strokeDashoffset = (total - drawn).toFixed(1);
        let last = -1;
        stages.forEach((st, i) => { const on = drawn >= at[i] - 1; st.classList.toggle('is-on', on); if (on) last = i; });
        if (!animate) last = -1;
        if (last !== current) {
          if (stages[current]) stages[current].classList.remove('is-current');
          if (stages[last]) stages[last].classList.add('is-current');
          current = last;
        }
        const moving = animate && drawn > 0 && drawn < total;
        sec.classList.toggle('is-drawing', moving);
        if (moving) { // the marker's place on the path, from the sampled table
          let lo = 0, hi = table.length - 1;
          while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (table[mid][2] < drawn) lo = mid; else hi = mid; }
          const [a, b] = [table[lo], table[hi]];
          const k = (drawn - a[2]) / ((b[2] - a[2]) || 1);
          dot.setAttribute('cx', (a[0] + (b[0] - a[0]) * k).toFixed(1));
          dot.setAttribute('cy', (a[1] + (b[1] - a[1]) * k).toFixed(1));
        }
      };

      const measure = () => {
        const mr = map.getBoundingClientRect();
        const W = mr.width, H = mr.height;
        if (!W) return;
        const vw = document.documentElement.clientWidth;
        const left = -mr.left, right = vw - mr.left;
        const pts = marks.map((m) => { const r = m.getBoundingClientRect(); return [r.left + r.width / 2 - mr.left, r.top + r.height / 2 - mr.top]; });
        const serp = getComputedStyle(list).gridTemplateColumns.split(' ').length > 1;
        // waypoints [x, y, stage or -1]: in from the page's edge, through every marker (and round the turn), out again
        const way = [];
        if (serp) {
          way.push([left, pts[0][1] + 120, -1]);
          pts.slice(0, 5).forEach((pt, i) => way.push([pt[0], pt[1], i]));
          // round the turn in the margin; where the space between the rows allows, the path curls into a loop there
          const bx = W + Math.max(12, Math.min(64, (right - W) * 0.55));
          const top = stages[4].getBoundingClientRect().bottom - mr.top + 24, foot = pts[5][1] - 40;
          const R = Math.min(64, (foot - top) / 2);
          way.push([bx, pts[4][1] + 40, -1]);
          if (R >= 40) {
            const cx = (pts[4][0] + W) / 2, cy = (top + foot) / 2;
            way.push([bx - 8, cy - R * 0.9, -1], [cx + R * 0.15, cy + R, -1], [cx - R, cy, -1], [cx, cy - R, -1], [cx + R * 1.05, cy + R * 0.25, -1]);
          }
          way.push([bx, pts[5][1] - 30, -1]);
          pts.slice(5).forEach((pt, i) => way.push([pt[0], pt[1], i + 5]));
          way.push([left, pts[9][1] + 90, -1]);
        } else {
          // in from just above the first stage and out just below the last, clear of the text around the list
          way.push([pts[0][0] + 22, -36, -1]);
          pts.forEach((pt, i) => way.push([pt[0], pt[1], i]));
          way.push([pts[9][0] + 16, H + 24, -1]);
        }
        // a smooth curve through the waypoints (Catmull-Rom, written as cubic Beziers). Its length is worked out here, by
        // sampling each curve, rather than asked of the browser, which can report a stale length just after a change.
        const P = (i) => way[Math.max(0, Math.min(way.length - 1, i))];
        const f = (n) => n.toFixed(1);
        let d = `M${f(way[0][0])} ${f(way[0][1])}`;
        let len = 0;
        at = new Array(marks.length).fill(0);
        table = [[way[0][0], way[0][1], 0]];
        for (let i = 0; i < way.length - 1; i++) {
          const [p0, p1, p2, p3] = [P(i - 1), P(i), P(i + 1), P(i + 2)];
          const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
          const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
          d += `C${f(c1[0])} ${f(c1[1])} ${f(c2[0])} ${f(c2[1])} ${f(p2[0])} ${f(p2[1])}`;
          let [px, py] = p1;
          for (let s = 1; s <= 24; s++) {
            const t = s / 24, u = 1 - t;
            const x = u * u * u * p1[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p2[0];
            const y = u * u * u * p1[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p2[1];
            len += Math.hypot(x - px, y - py);
            table.push([x, y, len]);
            [px, py] = [x, y];
          }
          if (p2[2] >= 0) at[p2[2]] = len;
        }
        total = len;
        svg.setAttribute('width', f(W));
        svg.setAttribute('height', f(H));
        svg.setAttribute('viewBox', `0 0 ${f(W)} ${f(H)}`);
        [track, path, reveal].forEach((el) => el.setAttribute('d', d));
        Object.entries({ x: left - 100, y: -400, width: right - left + 200, height: H + 800 }).forEach(([k, v]) => mask.setAttribute(k, f(v)));
        reveal.style.strokeDasharray = `${f(total)} ${f(total + 50)}`;
        update();
      };

      if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('in'); io.disconnect(); } }), { rootMargin: '0px 0px -12% 0px' });
        io.observe(sec);
      } else sec.classList.add('in');
      window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
      if ('ResizeObserver' in window) { let t = 0; new ResizeObserver(() => { clearTimeout(t); t = setTimeout(measure, 100); }).observe(map); }
      else window.addEventListener('resize', measure);
      if (document.fonts) document.fonts.ready.then(measure);
      window.addEventListener('load', measure);
      measure();
    });
  };

  /* ---------- portfolio: filtering, kept in the address, and a photograph viewer ---------- */
  const portfolio = () => {
    const gallery = $('.gallery');
    if (!gallery) return;
    const cards = $$('.card', gallery);
    const buttons = $$('[data-filter]');
    const status = $('#filter-status');
    const count = $('[data-count]');
    const names = Object.fromEntries(buttons.map((b) => [b.dataset.filter, b.firstChild.textContent.trim()]));
    const apply = (f) => {
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
      let n = 0;
      cards.forEach((c) => { const on = f === 'all' || c.dataset.cat === f; c.hidden = !on; if (on) n++; });
      if (count) count.textContent = n;
      status.textContent = `Showing ${n} ${f === 'all' ? 'rooms' : names[f].toLowerCase()}`;
      history.replaceState(null, '', f === 'all' ? location.pathname : `#${f}`);
    };
    buttons.forEach((b) => b.addEventListener('click', () => apply(b.dataset.filter)));
    const fromHash = () => { const f = location.hash.slice(1); if (f in names) apply(f); };
    fromHash();
    window.addEventListener('hashchange', fromHash);

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
      idle(() => [1, -1].forEach((d) => load(list[(idx + d + list.length) % list.length].src)));
    };
    const close = () => {
      if (!lb.classList.contains('is-open')) return;
      lb.classList.remove('is-open');
      lb.setAttribute('aria-hidden', 'true');
      lb.inert = true;
      overlay.close();
      const back = list[idx].card;
      back.focus({ preventScroll: true });
      back.scrollIntoView({ block: 'nearest', behavior: reduced() ? 'auto' : 'smooth' });
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
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) close();
    });
  };

  /* ---------- services: the section being read is marked in the jump links ---------- */
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
    // Restore an unsent draft, then let a "Plan your kitchen" link choose the project type.
    const draft = store.get();
    fields.forEach((n) => { if (draft[n] && !form.elements[n].value) form.elements[n].value = draft[n]; });
    const wanted = new URLSearchParams(location.search).get('type');
    if (wanted) {
      const opt = [...form.elements.type.options].find((o) => o.value.toLowerCase() === wanted.toLowerCase());
      if (opt) form.elements.type.value = opt.value;
    }
    let saveT = 0;
    const phoneOk = (v) => { const d = v.replace(/[^\d+]/g, ''); return /^(\+\d{10,14}|0?\d{10})$/.test(d); };
    const check = (el) => (el.name === 'phone' ? el.value.trim() !== '' && phoneOk(el.value) : el.checkValidity());
    form.addEventListener('input', (e) => {
      clearTimeout(saveT);
      saveT = setTimeout(() => store.set(Object.fromEntries(fields.map((n) => [n, form.elements[n].value]))), 300);
      const f = e.target.closest('.field');
      if (f && f.classList.contains('invalid') && check(e.target)) { f.classList.remove('invalid'); e.target.setAttribute('aria-invalid', 'false'); }
    });
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
    const report = (channel) => {
      statusBox.textContent = '';
      const p = document.createElement('p');
      p.textContent = channel === 'email'
        ? 'Your email app should now be open with your message ready to send. If nothing opened, copy the message and email it to atwood.dsigns@gmail.com.'
        : 'WhatsApp should now be open in a new tab with your message ready to send. If it did not open, copy the message and send it to +91 90001 81212.';
      const btn = document.createElement('button');
      btn.type = 'button';
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

  /* ================================================================ motion
     Applied only when motion is allowed: html.motion turns on the hidden start states in the stylesheet, so without
     this script, or with reduced motion, every element is simply visible. Only transform, opacity and clip-path move. */
  const motionOK = !reduced() && 'IntersectionObserver' in window;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Which elements reveal, and how. Reading text in articles is left still.
  const REVEALS = [
    ['main h1:not(.hero__title), main h2:not(.sr-only), .statement, .reel__end h3, .story-case__text h3, .pnext__text strong', 'words'],
    ['main .ph', 'img'],
    ['main .lead, main .shead p, main .kicker, .intro__label, .intro__lead, .intro__links, .intro__pic figcaption, .opener .crumbs, .svc .go, .reel__intro p, .reel__cap, .story-case__text p, .idea__text, .feature-post__text, .post-row__text, .pplan__text, .visit__card, .form, .faq-block__head p', 'up'],
    ['.pillars, .notes, .posts, .items, .next-steps, .routes, .faq, .chips, .stories, .intro__body', 'stagger'],
  ];
  const SKIP = '.hero, .phero, .loader, .menu-panel, .lightbox, .article__body, .journey__head, .journey__map, [data-r]';

  // Each word in its own mask; elements such as <em> keep their words inside them.
  const splitWords = (el) => {
    let i = 0;
    const walk = (node) => [...node.childNodes].forEach((n) => {
      if (n.nodeType === 3) {
        const parts = n.textContent.split(/(\s+)/);
        const frag = document.createDocumentFragment();
        parts.forEach((t) => {
          if (!t) return;
          if (/^\s+$/.test(t)) { frag.append(t); return; }
          const w = document.createElement('span'); w.className = 'w';
          const inner = document.createElement('span'); inner.textContent = t; inner.style.setProperty('--i', i++);
          w.append(inner); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && !n.classList.contains('w')) walk(n);
    });
    walk(el);
  };

  // Whole lines in masks, measured from where the words really break; <em> words stay emphasised. Re-measured when
  // the heading's width changes, so the masks always match the lines on screen.
  const splitLines = (el) => {
    if (!el._words) {
      el._words = [];
      const walk = (node, em) => [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) n.textContent.split(/[ \t\n\r\f]+/).filter(Boolean).forEach((t) => el._words.push({ t, em }));
        else if (n.nodeType === 1) walk(n, em || n.tagName === 'EM');
      });
      walk(el, false);
      el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    }
    el.textContent = '';
    const spans = el._words.map((w, i) => {
      const sp = document.createElement('span');
      sp.textContent = w.t;
      el.append(sp);
      if (i < el._words.length - 1) el.append(' ');
      return sp;
    });
    const lines = [];
    let top = null;
    spans.forEach((sp, i) => { if (sp.offsetTop !== top) { lines.push([]); top = sp.offsetTop; } lines[lines.length - 1].push(el._words[i]); });
    el.textContent = '';
    lines.forEach((words, l) => {
      const ln = document.createElement('span');
      ln.className = 'ln';
      ln.setAttribute('aria-hidden', 'true');
      const inner = document.createElement('span');
      inner.style.setProperty('--l', l);
      words.forEach((w, i) => {
        if (w.em) { const em = document.createElement('em'); em.textContent = w.t; inner.append(em); } else inner.append(w.t);
        if (i < words.length - 1) inner.append(' ');
      });
      ln.append(inner);
      el.append(ln);
    });
    el._w = el.clientWidth;
  };

  const reveals = () => {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    }), { rootMargin: '0px 0px -4% 0px' });
    $$('[data-gallery]').forEach((el) => { el.dataset.r = 'gallery'; io.observe(el); });
    $$('[data-cards]').forEach((el) => { el.dataset.r = 'cards'; io.observe(el); });
    const lined = $$('[data-lines]');
    lined.forEach((el) => { el.dataset.r = 'lines'; splitLines(el); io.observe(el); });
    // the first split may be measured in a fallback face; measure again once the web fonts have arrived
    if (lined.length && document.fonts) document.fonts.ready.then(() => lined.forEach(splitLines));
    if (lined.length && 'ResizeObserver' in window) {
      let t = 0;
      new ResizeObserver(() => {
        clearTimeout(t);
        t = setTimeout(() => lined.forEach((el) => { if (Math.abs(el.clientWidth - el._w) > 2) splitLines(el); }), 150);
      }).observe(document.body);
    }
    REVEALS.forEach(([sel, kind]) => $$(sel).forEach((el) => {
      if (el.closest(SKIP) && !el.matches('.phero h1')) return;
      if (el.dataset.r || el.closest('[data-r="stagger"]') && kind !== 'stagger') return;
      el.dataset.r = kind;
      if (kind === 'words') splitWords(el);
      if (kind === 'stagger') [...el.children].forEach((c, n) => c.style.setProperty('--i', Math.min(n, 12)));
      io.observe(el);
    }));
    // Should the visitor turn reduced motion on, everything is shown at once.
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => { if (e.matches) { root.classList.remove('motion'); } });
  };

  // A few photographs drift with depth as the page scrolls: desktop only, and only while on screen.
  const depth = () => {
    if (!window.matchMedia('(min-width: 900px)').matches) return;
    const items = [];
    $$('[data-depth]').forEach((el) => items.push({ el, d: +el.dataset.depth, move: el }));
    $$('.opener__pic .ph, .svc__pic .ph, .why__pic .ph, .ps--wide .ph, .story-case__main, .pnext .ph, .phero .ph').forEach((ph) => {
      ph.classList.add('px');
      const img = $('img', ph);
      if (img) items.push({ el: ph, d: 0.08, move: img });
    });
    $$('.g-tile .ph').forEach((ph) => { ph.classList.add('px'); items.push({ el: ph, d: 0.035, move: $('img', ph) }); });
    if (!items.length) return;
    const seen = new Set();
    const io = new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? seen.add(e.target) : seen.delete(e.target))), { rootMargin: '100px 0px' });
    items.forEach((it) => io.observe(it.el));
    let queued = false;
    const frame = () => {
      queued = false;
      const vh = window.innerHeight;
      items.forEach((it) => {
        if (!seen.has(it.el)) return;
        const r = it.el.getBoundingClientRect();
        const off = (r.top + r.height / 2 - vh / 2) * -it.d;
        it.move.style.translate = `0 ${off.toFixed(1)}px`;
      });
    };
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(frame); } }, { passive: true });
    frame();
  };

  // Selected work: from 1000px the section pins and vertical scrolling moves the reel sideways.
  const reel = () => {
    const sec = $('[data-reel]');
    if (!sec) return;
    const track = $('.reel__track', sec);
    const bar = $('.reel__progress', sec);
    const items = $$('.reel__item', sec);
    const mq = window.matchMedia('(min-width: 1000px)');
    let dist = 0, top = 0, on = false, queued = false;
    const measure = () => {
      on = mq.matches;
      sec.classList.toggle('is-pinned', on);
      if (!on) { sec.style.height = ''; track.style.transform = ''; return; }
      dist = Math.max(0, track.scrollWidth - window.innerWidth);
      sec.style.height = `${dist + window.innerHeight}px`;
      top = sec.getBoundingClientRect().top + window.scrollY;
      frame();
    };
    const frame = () => {
      queued = false;
      if (!on) return;
      const p = Math.min(1, Math.max(0, (window.scrollY - top) / (dist || 1)));
      track.style.transform = `translate3d(${(-p * dist).toFixed(1)}px, 0, 0)`;
      bar.style.setProperty('--p', p.toFixed(4));
      const vw = window.innerWidth;
      items.forEach((it) => { // depth inside each frame: the photograph moves a little against the reel
        const r = it.getBoundingClientRect();
        if (r.right < 0 || r.left > vw) return;
        const img = $('.ph img', it);
        const room = r.width * 0.065;   // .reel.is-pinned images are scaled 1.14: 7% of the width spare on each side
        if (img) img.style.translate = `${Math.max(-room, Math.min(room, (r.left + r.width / 2 - vw / 2) * -0.06)).toFixed(1)}px 0`;
      });
    };
    // A keyboard user tabbing into a project off to the side is scrolled to it.
    sec.addEventListener('focusin', (e) => {
      if (!on) return;
      const it = e.target.closest('.reel__item, .reel__end');
      if (!it) return;
      const x = it.offsetLeft - (window.innerWidth - it.offsetWidth) / 2;
      window.scrollTo({ top: top + Math.min(dist, Math.max(0, x)), behavior: 'auto' });
    });
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(frame); } }, { passive: true });
    window.addEventListener('resize', measure);
    mq.addEventListener('change', measure);
    if (document.fonts) document.fonts.ready.then(measure);
    window.addEventListener('load', measure);
    measure();
  };

  // A label that follows the pointer over projects; the real cursor stays.
  const cursor = () => {
    if (!finePointer) return;
    const c = document.createElement('div');
    c.className = 'cursor'; c.setAttribute('aria-hidden', 'true');
    document.body.append(c);
    let x = -200, y = -200, tx = x, ty = y, s = 0, ts = 0, raf = 0;
    const tick = () => {
      x += (tx - x) * 0.2; y += (ty - y) * 0.2; s += (ts - s) * 0.18;
      c.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0) scale(${s.toFixed(3)})`;
      raf = Math.abs(tx - x) + Math.abs(ty - y) + Math.abs(ts - s) > 0.1 ? requestAnimationFrame(tick) : 0;
    };
    const go = () => { if (!raf) raf = requestAnimationFrame(tick); };
    document.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX; ty = e.clientY;
      const t = e.target.closest && e.target.closest('[data-cursor]');
      ts = t ? 1 : 0;
      if (t && c.textContent !== t.dataset.cursor) c.textContent = t.dataset.cursor;
      go();
    }, { passive: true });
    document.addEventListener('pointerleave', () => { ts = 0; go(); });
  };

  // The home hero and project openings start once the fonts are in, after the loader when it shows.
  const opening = () => {
    if (!$('.hero, .phero')) return;
    const loader = $('.loader') && !root.classList.contains('seen');
    let done = false;
    const go = () => { if (!done) { done = true; root.classList.add('hero-go'); } };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(go, loader ? 900 : 60));
    setTimeout(go, loader ? 1800 : 1200);
  };

  /* ---------- start ---------- */
  root.classList.add('ready'); // the head script shows everything if this line never runs
  if (motionOK) {
    root.classList.add('motion');
    reveals();
    opening();
    depth();
    cursor();
    reel(); // with reduced motion the projects simply stack, one under another
  }
  header();
  menu();
  journey(); // drawn in full, at once, with reduced motion
  portfolio();
  jumpNav();
  enquiry();
  const y = $('#year');
  if (y) y.textContent = new Date().getFullYear();
})();
