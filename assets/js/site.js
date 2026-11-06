/* Atlantis Travel – site betikleri (bağımlılık yok) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var LANG = doc.lang === 'en' ? 'en' : 'tr';
  var WA_NUMBER = '905073978794';
  var GA_ID = 'G-E30LNGPJKR';

  var T = {
    tr: {
      sending: 'Gönderiliyor…',
      ok: 'Teşekkürler, talebiniz alındı. Ekibimiz en kısa sürede size dönüş yapacak.',
      fail: 'Talebiniz gönderilemedi. Lütfen tekrar deneyin veya WhatsApp üzerinden yazın.',
      invalid: 'Lütfen işaretli alanları kontrol edin.',
      required: 'Bu alan zorunludur.',
      email: 'Geçerli bir e-posta adresi girin.',
      phone: 'Geçerli bir telefon numarası girin.',
      dates: 'Çıkış tarihi giriş tarihinden önce olamaz.',
      waIntro: 'Merhaba Atlantis Travel, teklif almak istiyorum.'
    },
    en: {
      sending: 'Sending…',
      ok: 'Thank you, your request has been received. Our team will get back to you shortly.',
      fail: 'Your request could not be sent. Please try again or write to us on WhatsApp.',
      invalid: 'Please check the highlighted fields.',
      required: 'This field is required.',
      email: 'Please enter a valid email address.',
      phone: 'Please enter a valid phone number.',
      dates: 'Check-out date cannot be before check-in date.',
      waIntro: 'Hello Atlantis Travel, I would like to request a quote.'
    }
  }[LANG];

  /* Menü */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* Yıl */
  var y = document.querySelectorAll('[data-year]');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();

  /* Ölçülü animasyon */
  var rev = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -40px 0px' });
    rev.forEach(function (el) { io.observe(el); });
  } else {
    rev.forEach(function (el) { el.classList.add('in'); });
  }

  /* Formlar */
  function val(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }
  function setErr(field, msg) {
    var box = field.closest('.field');
    if (!box) return;
    box.classList.toggle('invalid', !!msg);
    var e = box.querySelector('.err');
    if (e) e.textContent = msg || '';
    field.setAttribute('aria-invalid', msg ? 'true' : 'false');
  }
  function validate(form) {
    var ok = true, first = null;
    var fields = form.querySelectorAll('input,select,textarea');
    fields.forEach(function (f) {
      if (f.type === 'hidden' || f.closest('.hp')) return;
      var v = f.type === 'checkbox' ? f.checked : String(f.value || '').trim();
      var msg = '';
      if (f.required && !v) msg = T.required;
      else if (f.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = T.email;
      else if (f.type === 'tel' && v && !/^[+0-9()\s-]{7,20}$/.test(v)) msg = T.phone;
      if (f.type === 'checkbox') {
        if (f.required && !v) { ok = false; first = first || f; f.closest('.consent').style.color = '#A4262C'; }
        else if (f.closest('.consent')) f.closest('.consent').style.color = '';
        return;
      }
      setErr(f, msg);
      if (msg) { ok = false; first = first || f; }
    });
    var a = form.elements.date_start, b = form.elements.date_end;
    if (a && b && a.value && b.value && b.value < a.value) {
      setErr(b, T.dates); ok = false; first = first || b;
    }
    if (first) first.focus();
    return ok;
  }
  function waText(form) {
    var labels = form.querySelectorAll('label[for]');
    var lines = [T.waIntro];
    labels.forEach(function (l) {
      var f = document.getElementById(l.htmlFor);
      if (!f || f.type === 'checkbox' || f.closest('.hp')) return;
      var v = String(f.value || '').trim();
      if (f.tagName === 'SELECT' && f.selectedIndex === 0) v = '';
      if (v) lines.push(l.textContent.replace('*', '').trim() + ': ' + v);
    });
    return lines.join('\n');
  }

  document.querySelectorAll('form.qform').forEach(function (form) {
    var ts = form.elements.ts;
    if (ts) ts.value = String(Date.now());

    /* ?hizmet= / ?service= ile hizmet ön seçimi */
    var params = new URLSearchParams(location.search);
    var pre = params.get('hizmet') || params.get('service');
    if (pre && form.elements.service) {
      var opt = form.elements.service.querySelector('option[value="' + pre.replace(/[^a-z-]/g, '') + '"]');
      if (opt) form.elements.service.value = opt.value;
    }

    /* Tarih alanlarında geçmiş günleri kapat */
    var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
    var iso = today.toISOString().slice(0, 10);
    form.querySelectorAll('input[type="date"]').forEach(function (d) { d.min = iso; });

    var waBtn = form.querySelector('[data-wa-send]');
    if (waBtn) {
      waBtn.addEventListener('click', function () {
        window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(waText(form)), '_blank', 'noopener');
      });
    }

    form.addEventListener('input', function (e) {
      if (e.target.closest('.field.invalid')) setErr(e.target, '');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      status.className = 'form-status';
      if (!validate(form)) {
        status.textContent = T.invalid; status.className = 'form-status fail'; return;
      }
      var btn = form.querySelector('button[type="submit"]');
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = T.sending;
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'fetch' }
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; });
      }).then(function (data) {
        if (data && data.ok) {
          status.textContent = T.ok; status.className = 'form-status ok';
          form.reset(); if (ts) ts.value = String(Date.now());
          if (window.gtag) window.gtag('event', 'generate_lead', { form_type: val(form, 'form_type') });
        } else {
          status.textContent = (data && data.message) || T.fail; status.className = 'form-status fail';
        }
      }).catch(function () {
        status.textContent = T.fail; status.className = 'form-status fail';
      }).then(function () {
        btn.disabled = false; btn.textContent = label;
        status.setAttribute('tabindex', '-1'); status.focus();
      });
    });
  });

  /* Çerez onayı: Google Analytics yalnızca kabul edilirse yüklenir */
  var KEY = 'at_cookie_consent';
  function getC() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setC(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function loadGA() {
    if (window.gtag || !GA_ID) return;
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }
  var banner = document.querySelector('.cookie');
  var c = getC();
  if (c === 'all') loadGA();
  else if (!c && banner) banner.classList.add('show');
  if (banner) {
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-consent]');
      if (!b) return;
      setC(b.getAttribute('data-consent'));
      banner.classList.remove('show');
      if (b.getAttribute('data-consent') === 'all') loadGA();
    });
  }
  document.querySelectorAll('[data-cookie-settings]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); if (banner) banner.classList.add('show'); });
  });
})();
