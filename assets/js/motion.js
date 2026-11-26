/* Atlantis Travel – hareket katmanı (v4). Bağımlılık yok. */
/* Fuar haritası: lejant ile pin eşleştirme (hareket tercihinden bağımsız) */
(function () {
  document.querySelectorAll('.fair-map').forEach(function (sec) {
    var pins = {};
    sec.querySelectorAll('.fm-pin').forEach(function (p) { pins[p.getAttribute('data-k')] = p; });
    sec.querySelectorAll('.fm-legend li').forEach(function (li) {
      var p = pins[li.getAttribute('data-k')];
      var on = function (v) { li.classList.toggle('on', v); if (p) p.classList.toggle('on', v); };
      li.addEventListener('mouseenter', function () { on(true); }); li.addEventListener('focus', function () { on(true); });
      li.addEventListener('mouseleave', function () { on(false); }); li.addEventListener('blur', function () { on(false); });
    });
  });
})();
(function () {
  'use strict';
  if (!window.matchMedia || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var root = document.documentElement;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  root.classList.add('motion');

  /* Sıralı geçiş gecikmesi */
  document.querySelectorAll('.who-grid,.svc-grid,.steps3,.reviews,.cards,.why-list,.kinds').forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, i) { c.style.setProperty('--d', (i * 90) + 'ms'); });
  });

  /* Görünmeyen öğeleri derinlikten getir (site.js'in eklediği .in sınıfını yeniden kurar) */
  if ('IntersectionObserver' in window) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rio.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -60px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top > innerHeight) { el.classList.remove('in'); rio.observe(el); }
    });
  }

  /* Hero parallax */
  var hero = document.querySelector('.hero2');
  var bg = hero && hero.querySelector('.bg img');
  var wrap = hero && hero.querySelector('.wrap');
  if (hero && bg) {
    var ticking = false;
    var paint = function () {
      ticking = false;
      var y = window.scrollY, h = hero.offsetHeight || 1;
      if (y > h * 1.2) return;
      bg.style.transform = 'translate3d(0,' + (y * 0.32).toFixed(1) + 'px,0) scale(1.08)';
      if (wrap) {
        wrap.style.transform = 'translate3d(0,' + (y * 0.12).toFixed(1) + 'px,0)';
        wrap.style.opacity = String(Math.max(0, 1 - (y / h) * 0.95));
      }
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }, { passive: true });
    paint();
  }

  /* Kartlarda 3D eğim (yalnızca fare/trackpad) */
  if (fine) {
    document.querySelectorAll('.svc,.who,.card').forEach(function (el) {
      el.classList.add('tilt');
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
        el.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg');
        el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      });
      el.addEventListener('pointerleave', function () {
        el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg');
      });
    });
  }

  /* Güven bandı sayaçları */
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target, d = el._at;
        var t0 = null;
        var step = function (t) {
          t0 = t0 || t;
          var k = Math.min(1, (t - t0) / 1500), ease = 1 - Math.pow(1 - k, 3);
          var v = (d.end * ease).toFixed(d.dec);
          if (d.sep) v = v.replace('.', d.sep);
          el.textContent = v + d.suf;
          if (k < 1) requestAnimationFrame(step); else el.textContent = d.txt;
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('.trust strong').forEach(function (el) {
      var txt = el.textContent, m = txt.match(/^(\d+)([.,]\d+)?(.*)$/);
      if (!m) return;
      el._at = { txt: txt, end: parseFloat(m[1] + (m[2] ? '.' + m[2].slice(1) : '')), dec: m[2] ? m[2].length - 1 : 0, sep: m[2] ? m[2][0] : '', suf: m[3] };
      el.textContent = (m[2] ? '0' + m[2][0] + '0' : '0') + m[3];
      cio.observe(el);
    });
  }
  /* 3D fuar haritası: girişte yerine oturma + fareyle eğim */
  document.querySelectorAll('.fair-map').forEach(function (sec) {
    var plane = sec.querySelector('.fm-plane'), stage = sec.querySelector('.fm-stage');
    if (!plane || !stage) return;
    var base = innerWidth <= 520 ? { rx: 40, rz: -8 } : { rx: 52, rz: -14 };
    var set = function (rx, rz) { plane.style.setProperty('--fm-rx', rx.toFixed(1) + 'deg'); plane.style.setProperty('--fm-rz', rz.toFixed(1) + 'deg'); };
    if ('IntersectionObserver' in window) {
      set(base.rx + 12, base.rz - 16);
      var mio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { mio.disconnect(); set(base.rx, base.rz); }
      }, { threshold: 0.35 });
      mio.observe(stage);
    }
    if (fine) {
      stage.addEventListener('pointermove', function (e) {
        var r = stage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        set(base.rx + y * 10, base.rz + x * 14);
      });
      stage.addEventListener('pointerleave', function () { set(base.rx, base.rz); });
    }
  });
})();
