/* 법률사무소 차민 — main.js
   Progressive enhancement only. Every behaviour here has a working static
   fallback in style.css, so the site stays readable if this file never runs. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------- header */
  var hdr = document.querySelector('[data-header]');
  var quick = document.querySelector('[data-quick]');

  function onScroll() {
    var y = window.pageYOffset || root.scrollTop;
    if (hdr && !hdr.classList.contains('is-solid')) {
      hdr.classList.toggle('is-stuck', y > 24);
    }
    if (quick) quick.classList.toggle('is-on', y > 640);
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { onScroll(); ticking = false; });
  }, { passive: true });
  onScroll();

  /* ------------------------------------------------------ mobile nav */
  var burger = document.querySelector('[data-burger]');
  var nav = document.querySelector('[data-nav]');

  function closeNav() {
    document.body.classList.remove('nav-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
  }

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 980) closeNav();
    });
  }

  /* ------------------------------------------- hero intro (home only) */
  var hero = document.querySelector('[data-hero]');
  if (hero) {
    // one frame's grace so the champagne gradient has painted before it fades in
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { hero.classList.add('is-live'); });
    });
  }

  /* ------------------------------------------------- reveal on scroll */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length && !reduced && 'IntersectionObserver' in window) {
    root.classList.add('reveal-ready');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(reveals, function (el) { io.observe(el); });
  }

  /* -------------------------------------------------------- FAQ list */
  Array.prototype.forEach.call(document.querySelectorAll('[data-faq]'), function (item) {
    var btn = item.querySelector('.faq__q');
    var panel = item.querySelector('.faq__a');
    if (!btn || !panel) return;

    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');

      if (open) {
        panel.style.height = panel.scrollHeight + 'px';
        window.requestAnimationFrame(function () { panel.style.height = '0px'; });
      } else {
        panel.style.height = panel.scrollHeight + 'px';
        panel.addEventListener('transitionend', function once(e) {
          if (e.propertyName !== 'height') return;
          panel.removeEventListener('transitionend', once);
          // a fast second click can close the panel before this fires; only
          // release the height if the panel is still meant to be open
          if (btn.getAttribute('aria-expanded') === 'true') panel.style.height = 'auto';
        });
      }
    });

    // keep an open panel correct when the text reflows
    window.addEventListener('resize', function () {
      if (btn.getAttribute('aria-expanded') === 'true') panel.style.height = 'auto';
    });
  });

  /* ------------------------------------------- 성공사례 분야 거르기 */
  var filters = document.querySelectorAll('[data-filter]');
  if (filters.length) {
    var cases = document.querySelectorAll('.case');
    var empty = document.querySelector('.cases-empty');

    Array.prototype.forEach.call(filters, function (btn) {
      btn.addEventListener('click', function () {
        var pick = btn.getAttribute('data-filter');
        var shown = 0;

        Array.prototype.forEach.call(filters, function (b) {
          b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
        });
        Array.prototype.forEach.call(cases, function (c) {
          var hit = pick === 'all' || c.getAttribute('data-cat') === pick;
          c.hidden = !hit;
          if (hit) shown++;
        });

        // the empty state doubles as "no cases in this category yet"
        if (empty) empty.hidden = cases.length > 0 && shown > 0;
      });
    });

    // nothing published yet — the filter row would only lead to blank screens
    if (!cases.length) {
      var row = filters[0].closest('.filters');
      if (row) row.hidden = true;
    }
  }

  /* -------------------------------------------------- copy address */
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'), function (btn) {
    var label = btn.querySelector('[data-copy-label]');
    if (!label) return;
    var idle = label.textContent;
    var timer;

    function legacyCopy(text) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      return ok;
    }

    function done(ok) {
      label.textContent = ok ? '복사했습니다' : '복사에 실패했습니다';
      btn.classList.toggle('is-done', ok);
      window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        label.textContent = idle;
        btn.classList.remove('is-done');
      }, 2200);
    }

    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      // navigator.clipboard needs a secure context; plain http falls back
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done(true); },
                                                 function () { done(legacyCopy(text)); });
      } else {
        done(legacyCopy(text));
      }
    });
  });

  /* --------------------------------------------------- footer year */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();

/* ===================================================================
   상담 전환 추적 (Google Analytics)
   전화·카카오톡·지도·칼럼 등 주요 링크 클릭을 이벤트로 보낸다.
   gtag 가 없으면(차단·오프라인) 아무 일도 하지 않는다.
   =================================================================== */
(function () {
  if (typeof window.gtag !== 'function') return;

  function send(name, link) {
    try {
      window.gtag('event', name, {
        from_page: document.title,
        link_text: (link.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 50)
      });
    } catch (e) { /* 집계 실패가 링크 동작을 막지 않도록 */ }
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var a = t.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';

    if (href.indexOf('tel:') === 0) send('tel_click', a);
    else if (href.indexOf('pf.kakao.com') > -1) send('kakao_click', a);
    else if (href.indexOf('map.naver.com') > -1 || href.indexOf('naver.me') > -1 ||
             href.indexOf('map.kakao.com') > -1 || href.indexOf('place.map.kakao.com') > -1 ||
             href.indexOf('maps.google.com') > -1) send('map_click', a);
    else if (href.indexOf('mailto:') === 0) send('email_click', a);
    else if (/booking\.html(\?|#|$)/.test(href)) send('booking_page_click', a);
    else if (/(^|\/)blog\/|^\d{8}-/.test(href)) send('column_click', a);
    else if (href.indexOf('blog.naver.com') > -1) send('naverblog_click', a);
    else if (href.indexOf('instagram.com') > -1) send('instagram_click', a);
  }, true);
})();

/* 법률 칼럼 분야 필터 + 검색
   - 분야: 카드 분야 태그의 첫 단어로 형사·민사·행정·가사를 나눈다
   - 검색: blog/search-index.json(본문 전체)을 처음 검색할 때 불러온다. 못 불러오면 카드 글자만으로 찾는다 */
(function () {
  var nav = document.querySelector('[data-post-filter]');
  var list = document.querySelector('[data-posts]');
  if (!nav || !list) return;
  var form = document.querySelector('[data-post-search]');
  var input = form && form.querySelector('input');
  var clear = form && form.querySelector('.psearch__x');
  var status = document.querySelector('[data-post-status]');
  var map = { '형사': '형사', '민사': '민사', '행정': '행정', '학교폭력': '행정', '노동': '행정', '이혼': '가사', '가사': '가사' };
  var norm = function (t) { return (t || '').toLowerCase().replace(/\s+/g, ' '); };
  var esc = function (t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var cards = [].slice.call(list.querySelectorAll('.post'));
  var order = cards.slice();
  var counts = { all: cards.length };
  cards.forEach(function (c) {
    var t = c.querySelector('.post__tag');
    var k = t ? t.textContent.trim().split(/[\s·]+/)[0] : '';
    var cat = map[k] || '';
    c.setAttribute('data-cat', cat);
    counts[cat] = (counts[cat] || 0) + 1;
    c._title = norm((c.querySelector('.post__h') || {}).textContent);
    c._card = norm(c.textContent);
    c._body = '';
    c._raw = '';
  });
  var empty = document.createElement('p');
  empty.className = 'posts-empty'; empty.hidden = true;
  list.parentNode.insertBefore(empty, list.nextSibling);

  var btns = [].slice.call(nav.querySelectorAll('[data-cat]'));
  var state = { cat: 'all', q: '', page: 1 };
  var PER = 10;
  var pager = document.createElement('nav');
  pager.className = 'pager'; pager.setAttribute('aria-label', '칼럼 페이지');
  list.parentNode.insertBefore(pager, list.nextSibling);

  function snippet(raw, terms) {
    var low = raw.toLowerCase(), at = -1, len = 0;
    terms.forEach(function (t) { var i = low.indexOf(t); if (i > -1 && (at < 0 || i < at)) { at = i; len = t.length; } });
    if (at < 0) return '';
    var a = Math.max(0, at - 38), b = Math.min(raw.length, at + len + 62);
    var part = esc(raw.slice(a, b));
    terms.forEach(function (t) {
      var re = new RegExp('(' + esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      part = part.replace(re, '<mark>$1</mark>');
    });
    return (a > 0 ? '… ' : '') + part + (b < raw.length ? ' …' : '');
  }

  function render(track) {
    var terms = norm(state.q).trim().split(' ').filter(Boolean);
    var shown = 0, catCounts = { all: 0 };
    var scored = [];
    order.forEach(function (c) {
      var score = 0;
      if (terms.length) {
        var hay = c._card + ' ' + c._body;
        var ok = terms.every(function (t) { return hay.indexOf(t) > -1; });
        if (ok) terms.forEach(function (t) { score += (c._title.indexOf(t) > -1 ? 10 : 0) + (c._card.indexOf(t) > -1 ? 3 : 0) + 1; });
        else score = -1;
      }
      if (score >= 0) { catCounts.all++; catCounts[c.getAttribute('data-cat')] = (catCounts[c.getAttribute('data-cat')] || 0) + 1; }
      var vis = score >= 0 && (state.cat === 'all' || c.getAttribute('data-cat') === state.cat);
      c.hidden = !vis;
      var hit = c.querySelector('.post__hit');
      if (vis && terms.length && c._raw && !terms.every(function (t) { return c._card.indexOf(t) > -1; })) {
        if (!hit) { hit = document.createElement('p'); hit.className = 'post__hit'; c.appendChild(hit); }
        hit.innerHTML = snippet(c._raw, terms);
      } else if (hit) { hit.parentNode.removeChild(hit); }
      if (vis) { shown++; scored.push([score, c]); }
    });
    // 검색어가 있으면 제목에 걸린 글을 위로, 없으면 원래 날짜순
    var seq = terms.length ? scored.slice().sort(function (x, y) { return y[0] - x[0] || order.indexOf(x[1]) - order.indexOf(y[1]); }).map(function (x) { return x[1]; }) : order;
    seq.forEach(function (c) { list.appendChild(c); });

    // 페이지 나누기: 보이는 글을 10개씩
    var vis = seq.filter(function (c) { return !c.hidden; });
    var pages = Math.max(1, Math.ceil(vis.length / PER));
    if (state.page > pages) state.page = pages;
    if (state.page < 1) state.page = 1;
    vis.forEach(function (c, i) { if (Math.floor(i / PER) + 1 !== state.page) c.hidden = true; });
    var ph = '';
    if (pages > 1) {
      var mk = function (n, label, cls, dis) {
        return '<button type="button" class="pager__b' + (cls ? ' ' + cls : '') + '" data-page="' + n + '"' +
          (dis ? ' disabled' : '') + (n === state.page && !cls ? ' aria-current="page"' : '') +
          (label !== String(n) ? ' aria-label="' + (cls === 'pager__prev' ? '이전 페이지' : '다음 페이지') + '"' : ' aria-label="' + n + '페이지"') + '>' + label + '</button>';
      };
      ph += mk(state.page - 1, '‹', 'pager__prev', state.page === 1);
      for (var n = 1; n <= pages; n++) ph += mk(n, String(n), '', false);
      ph += mk(state.page + 1, '›', 'pager__next', state.page === pages);
    }
    pager.innerHTML = ph;
    pager.hidden = pages <= 1;

    btns.forEach(function (b) {
      var k = b.getAttribute('data-cat'), on = k === state.cat;
      b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var n = b.querySelector('.pfilter__n'); if (n) n.textContent = (terms.length ? catCounts : counts)[k] || 0;
    });
    if (status) status.textContent = terms.length ? '‘' + state.q.trim() + '’ 검색 결과 ' + shown + '건' : '';
    empty.hidden = shown > 0;
    empty.textContent = terms.length ? '검색 결과가 없습니다. 다른 낱말로 찾아보시거나 063-452-9075로 문의해 주세요.' : '이 분야의 칼럼이 아직 없습니다.';
    if (clear) clear.hidden = !state.q;
    list.classList.add('is-in');
    if (track && window.gtag && terms.length) window.gtag('event', 'column_search', { search_term: state.q.trim(), results: shown });
  }

  function syncUrl() {
    try {
      var u = location.pathname;
      if (state.q.trim()) u += '?q=' + encodeURIComponent(state.q.trim());
      if (state.page > 1) u += (u.indexOf('?') > -1 ? '&' : '?') + 'page=' + state.page;
      if (state.cat !== 'all') u += '#' + encodeURIComponent(state.cat);
      history.replaceState(null, '', u);
    } catch (err) {}
  }

  var loading = null;
  function loadIndex() {
    if (loading || !window.fetch) return loading;
    loading = fetch('search-index.json').then(function (r) { return r.json(); }).then(function (rows) {
      var byUrl = {};
      rows.forEach(function (r) { byUrl[r.u] = r; });
      cards.forEach(function (c) {
        var r = byUrl[c.getAttribute('href')];
        if (r) { c._raw = r.x; c._body = norm(r.x); }
      });
      render(false);
    }).catch(function () {});
    return loading;
  }

  nav.addEventListener('click', function (e) {
    var b = e.target.closest('[data-cat]'); if (!b) return;
    state.cat = b.getAttribute('data-cat'); state.page = 1;
    render(false); syncUrl();
    if (window.gtag) window.gtag('event', 'column_filter', { category: state.cat });
  });
  if (input) {
    var timer, gaTimer;
    input.addEventListener('focus', loadIndex);
    input.addEventListener('input', function () {
      loadIndex();
      state.q = input.value; state.page = 1;
      clearTimeout(timer); clearTimeout(gaTimer);
      timer = setTimeout(function () { render(false); syncUrl(); }, 120);
      gaTimer = setTimeout(function () { render(true); }, 1500);
    });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); input.blur(); } });
    clear.addEventListener('click', function () { input.value = ''; state.q = ''; state.page = 1; render(false); syncUrl(); input.focus(); });
  }

  pager.addEventListener('click', function (e) {
    var b = e.target.closest('[data-page]'); if (!b || b.disabled) return;
    state.page = parseInt(b.getAttribute('data-page'), 10) || 1;
    render(false); syncUrl();
    var top = (form || nav).getBoundingClientRect().top + window.pageYOffset - 110;
    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
  });

  var h = ''; try { h = decodeURIComponent(location.hash.slice(1)); } catch (err) {}
  try { state.page = parseInt(new URLSearchParams(location.search).get('page'), 10) || 1; } catch (err) {}
  if (h && counts[h]) state.cat = h;
  var q = ''; try { q = new URLSearchParams(location.search).get('q') || ''; } catch (err) {}
  if (q && input) { input.value = q; state.q = q; loadIndex(); }
  render(false);
})();
