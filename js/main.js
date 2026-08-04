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
