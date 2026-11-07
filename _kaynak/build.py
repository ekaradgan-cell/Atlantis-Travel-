#!/usr/bin/env python3
"""Atlantis Travel statik site oluşturucu.

Kullanım (depo kök klasöründe):  python3 _kaynak/build.py
Tüm .html sayfalarını, sitemap.xml'i yeniden üretir. Metinleri bu dosyadan düzenleyin.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://atlantistravel.com.tr"
PHONE1 = "+90 507 397 87 94"
PHONE1_RAW = "+905073978794"
PHONE2 = "+90 554 135 36 40"
PHONE2_RAW = "+905541353640"
WA = "905073978794"
EMAIL = "info@atlantistraveltr.com"
INSTAGRAM = "https://www.instagram.com/atlantis.traveltr"
FACEBOOK = "https://www.facebook.com/atlantis.traveltr"
VERSION = "20261107"

e = html.escape

# ----------------------------------------------------------------- ikonlar
ICONS = {
    "hotel": '<path d="M3 21h18M5 21V5l7-2 7 2v16M9 8h1M14 8h1M9 12h1M14 12h1M9 16h1M14 16h1"/>',
    "car": '<path d="M3 16l1.6-5.2A2 2 0 0 1 6.5 9.4h11a2 2 0 0 1 1.9 1.4L21 16v3h-2.5M3 16v3h2.5M3 16h18"/><circle cx="7" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/>',
    "health": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M12 8v8M8 12h8"/>',
    "group": '<circle cx="8" cy="8" r="3"/><circle cx="16.5" cy="8.5" r="2.5"/><path d="M2.5 20c0-3.2 2.6-5.5 5.5-5.5s5.5 2.3 5.5 5.5M14 15c3.4-.8 7 1.2 7 5"/>',
    "fair": '<path d="M3 21V9l9-6 9 6v12M3 21h18M8 21v-6h8v6M9 11h6"/>',
    "ops": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
    "plane": '<path d="M2.5 13.5l7-1.5L14 4.5c.6-1 2-1.2 2.6-.4.4.5.3 1.1 0 1.6L13 12l7.5 1.5v2.2l-8-.7-2.7 4.4H8l1-4.8-6.5-.6z"/>',
    "shield": '<path d="M12 3l7.5 3v6c0 4.5-3.2 8-7.5 9-4.3-1-7.5-4.5-7.5-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "phone": '<path d="M5 3.5h3.5l1.7 4.3-2.2 1.6a11 11 0 0 0 6.6 6.6l1.6-2.2 4.3 1.7V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.1 1.5 1.5 0 0 1 5 3.5z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>',
    "wa": '<path d="M4 20l1.3-3.9A8.5 8.5 0 1 1 8.1 19z"/><path d="M9 8.5c0 3.5 2.6 6.5 6.5 6.8l1-1.6-2-1-1 .8a5 5 0 0 1-2.5-2.5l.8-1-1-2z"/>',
    "pin": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "ig": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.2" cy="6.8" r=".6"/>',
    "steth": '<path d="M6 3v6a4 4 0 0 0 8 0V3M6 3H4.5M14 3h1.5M10 13v2a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.5 5.5 3.5 8.5s-1 5.9-3.5 8.5c-2.5-2.6-3.5-5.5-3.5-8.5s1-5.9 3.5-8.5z"/>',
    "building": '<rect x="5" y="3.5" width="14" height="17" rx="1"/><path d="M9 7.5h2M13 7.5h2M9 11h2M13 11h2M9 14.5h2M13 14.5h2M10.5 20.5v-3h3v3"/>',
    "briefcase": '<rect x="3.5" y="7.5" width="17" height="12" rx="2"/><path d="M9 7.5V5.5a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 15 5.5v2M3.5 13h17"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "tag": '<path d="M3.5 12.5V4.5h8l9 9-8 8z"/><circle cx="8" cy="9" r="1.3"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "fb": '<path d="M14.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.6-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.3H9v3h2.5V21"/>',
    "handshake": '<path d="M2.5 11l4-4 3 1.5L12 7l3 1.5 3-1.5 3.5 4M6.5 13.5l3 3c.6.6 1.5.6 2 0l1-1M12 15l1.5 1.5c.6.6 1.5.6 2 0l3-3"/>',
}


def icon(name, cls=""):
    return (f'<svg{(" class=" + chr(34) + cls + chr(34)) if cls else ""} viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


# İstanbul silüeti: özgün, sade çizgi illüstrasyon (kullanım hakkı sorunu yoktur)
SKYLINE = (
    '<svg class="skyline" viewBox="0 0 800 140" fill="none" stroke="#D4AF37" stroke-width="1.4" aria-hidden="true">'
    '<path d="M0 130h800"/>'
    '<path d="M40 130V96h18v34M49 96V70M49 70l-3 6h6z"/>'
    '<path d="M90 130v-22a40 30 0 0 1 80 0v22M100 108a30 22 0 0 1 60 0M130 78v-8M120 130v-14h20v14"/>'
    '<path d="M182 130V64M178 64h8M182 64l-2-10h4zM182 54v-8"/>'
    '<path d="M60 130V62M56 62h8M60 62l-2-10h4z"/>'
    '<path d="M250 130V82h22v48M261 82V60l-6 4M261 60l6 4M255 94h12"/>'
    '<path d="M300 130c80-60 220-60 300 0M330 130V92M570 130V92M330 92h240M360 130v-22M400 130v-28M440 130v-30M480 130v-28M520 130v-22"/>'
    '<path d="M640 130V40l8-14 8 14v90M640 70h16M644 52h8"/>'
    '<path d="M690 130V100h40v30M700 100v-10h20v10M760 130V88h20v42"/>'
    '</svg>'
)

# ----------------------------------------------------------------- sayfalar
PAGES = {
    "home": ("/", "/en/"),
    "konaklama": ("/kurumsal-konaklama", "/en/corporate-accommodation"),
    "transfer": ("/vip-transfer", "/en/vip-transfer"),
    "saglik": ("/saglik-turizmi", "/en/medical-tourism"),
    "fuar": ("/fuar-konaklama", "/en/trade-fair-accommodation"),
    "cozumler": ("/services", "/en/services"),
    "about": ("/about", "/en/about"),
    "teklif": ("/teklif-al", "/en/request-a-quote"),
    "contact": ("/contact", "/en/contact"),
    "sss": ("/sss", "/en/faq"),
    "privacy": ("/privacy", "/en/privacy"),
    "terms": ("/terms", "/en/terms"),
    "thanks": ("/tesekkurler", "/en/thank-you"),
    "referans": ("/referanslar", "/en/references"),
}
NOINDEX = {"thanks"}


def url(key, lang):
    return PAGES[key][0 if lang == "tr" else 1]


def out_file(path):
    if path.endswith("/"):
        return os.path.join(ROOT, path.strip("/"), "index.html")
    return os.path.join(ROOT, path.strip("/") + ".html")


UI = {
    "tr": {
        "skip": "İçeriğe geç", "menu": "Menü", "quote": "Teklif Al", "support": "7/24 operasyon desteği · İstanbul",
        "nav": [("home", "Ana Sayfa"), ("about", "Hakkımızda"), ("cozumler", "Hizmetlerimiz"),
                ("konaklama", "Kurumsal Konaklama"), ("fuar", "Fuar Konaklama"), ("referans", "Referanslar"),
                ("contact", "İletişim")],
        "svc": [("konaklama", "Kurumsal Konaklama"), ("transfer", "VIP Transfer"), ("saglik", "Sağlık Turizmi"),
                ("fuar", "Fuar Konaklama"), ("cozumler", "Tüm Hizmetler")],
        "online": "7/24 Online", "bar_t": "Hemen Teklif Alın", "bar_s": "Profesyonel konaklama ve seyahat çözümleri",
        "f_services": "Hizmetler", "f_company": "Kurumsal", "f_contact": "İletişim",
        "f_about": "İstanbul'da şirketler, sağlık kuruluşları ve gruplar için otel konaklama, VIP havalimanı transferi ve operasyon yönetimi.",
        "f_note": "Uçak bileti, vize ve yurt dışı otel rezervasyonu hizmeti verilmemektedir.",
        "cookies": "Çerez tercihleri", "rights": "Tüm hakları saklıdır.",
        "cookie_text": "Sitemizin çalışması için zorunlu çerezler kullanılır. Ziyaret istatistikleri için Google Analytics çerezlerine izin verebilirsiniz. Ayrıntılar",
        "cookie_link": "Gizlilik ve Çerez Politikası", "accept": "Kabul et", "reject": "Yalnızca zorunlu",
        "call": "Ara", "wa": "WhatsApp", "wa_label": "WhatsApp ile yazın", "home": "Ana Sayfa",
    },
    "en": {
        "skip": "Skip to content", "menu": "Menu", "quote": "Get a Quote", "support": "24/7 operations support · Istanbul",
        "nav": [("home", "Home"), ("about", "About"), ("cozumler", "Services"),
                ("konaklama", "Corporate Stays"), ("fuar", "Trade Fair Stays"), ("referans", "References"),
                ("contact", "Contact")],
        "svc": [("konaklama", "Corporate Accommodation"), ("transfer", "VIP Transfer"), ("saglik", "Medical Tourism"),
                ("fuar", "Trade Fair Stays"), ("cozumler", "All Services")],
        "online": "24/7 Online", "bar_t": "Get a Quote Now", "bar_s": "Professional accommodation and travel solutions",
        "f_services": "Services", "f_company": "Company", "f_contact": "Contact",
        "f_about": "Hotel accommodation, VIP airport transfers and operations management in Istanbul for companies, healthcare providers and groups.",
        "f_note": "We do not provide flight ticketing, visa services or hotel bookings abroad.",
        "cookies": "Cookie settings", "rights": "All rights reserved.",
        "cookie_text": "We use essential cookies to run this site. You can allow Google Analytics cookies for visitor statistics. Details:",
        "cookie_link": "Privacy and Cookie Policy", "accept": "Accept", "reject": "Essential only",
        "call": "Call", "wa": "WhatsApp", "wa_label": "Message us on WhatsApp", "home": "Home",
    },
}


def head(lang, key, title, desc, schema=None):
    tr_u, en_u = PAGES[key]
    canonical = SITE + (tr_u if lang == "tr" else en_u)
    robots = '<meta name="robots" content="noindex, follow">' if key in NOINDEX else ""
    og_locale = "tr_TR" if lang == "tr" else "en_US"
    ld = ""
    if schema:
        for s in schema:
            ld += '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>\n"
    return f"""<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{SITE}{tr_u}">
<link rel="alternate" hreflang="en" href="{SITE}{en_u}">
<link rel="alternate" hreflang="x-default" href="{SITE}{tr_u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Atlantis Travel">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F7F5F0">
<meta name="google-site-verification" content="JcOyTdAoY7mSeTs01vLE8-iCf59M3JGKTG3oztYii7o">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" as="image" href="/assets/img/hero-lobby.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&amp;family=Inter:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
<script src="/assets/js/site.js?v={VERSION}" defer></script>
{ld}</head>
"""


def header(lang, key):
    u = UI[lang]
    items = ""
    for k, label in u["nav"]:
        cur = ' aria-current="page"' if k == key else ""
        items += f'<li><a href="{url(k, lang)}"{cur}>{e(label)}</a></li>'
    if key not in PAGES:
        key = "home"
    tr_cur = ' aria-current="true"' if lang == "tr" else ""
    en_cur = ' aria-current="true"' if lang == "en" else ""
    items += (f'<li class="extra"><a class="online" href="https://wa.me/{WA}" target="_blank" rel="noopener">'
              f'<span class="dot"></span>{u["online"]}</a></li>'
              f'<li class="extra lang"><a href="{url(key, "tr")}" hreflang="tr" lang="tr"{tr_cur}>TR</a>'
              f'<a href="{url(key, "en")}" hreflang="en" lang="en"{en_cur}>EN</a></li>')
    return f"""<body>
<a class="skip" href="#icerik">{u["skip"]}</a>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="{url("home", lang)}" aria-label="Atlantis Travel – {u["home"]}">
<img src="/assets/img/logo-horizontal.png" width="727" height="229" alt="Atlantis Travel"></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="{u["menu"]}">{icon("menu")}</button>
<nav aria-label="{u["menu"]}"><ul class="menu" id="menu">{items}</ul></nav>
</div></header>
<main id="icerik">
"""


def footer(lang):
    u = UI[lang]
    T = lang == "tr"
    svc = "".join(f'<li><a href="{url(k, lang)}">{e(l)}</a></li>' for k, l in u["svc"])
    company = [("about", "Hakkımızda" if T else "About"), ("referans", "Referanslar" if T else "References"),
               ("sss", "SSS" if T else "FAQ"), ("contact", "İletişim" if T else "Contact")]
    comp = "".join(f'<li><a href="{url(k, lang)}">{e(l)}</a></li>' for k, l in company)
    legal = [("privacy", "Gizlilik Politikası" if T else "Privacy Policy"), ("terms", "Kullanım Şartları" if T else "Terms of Use")]
    leg = "".join(f'<li><a href="{url(k, lang)}">{e(l)}</a></li>' for k, l in legal)
    leg += f'<li><a href="#" data-cookie-settings>{u["cookies"]}</a></li>'
    return f"""</main>
<footer class="site-footer">
<div class="wrap cols">
<div class="brand-col">
<img src="/assets/img/logo-horizontal.png" width="727" height="229" alt="Atlantis Travel" loading="lazy">
<p>{u["f_about"]}</p>
<div class="social"><a href="{INSTAGRAM}" rel="noopener" target="_blank" aria-label="Instagram">{icon("ig")}</a><a href="{FACEBOOK}" rel="noopener" target="_blank" aria-label="Facebook">{icon("fb")}</a></div>
</div>
<div><h2>{u["f_services"]}</h2><ul>{svc}</ul></div>
<div><h2>{u["f_company"]}</h2><ul>{comp}</ul></div>
<div><h2>{"Yasal" if T else "Legal"}</h2><ul>{leg}</ul></div>
<div><h2>{u["f_contact"]}</h2><ul>
<li><a href="tel:{PHONE1_RAW}">{PHONE1}</a> (WhatsApp)</li>
<li><a href="tel:{PHONE2_RAW}">{PHONE2}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul></div>
</div>
<div class="wrap legal"><span>© <span data-year>2026</span> Atlantis Travel. {u["rights"]}</span><span>{u["f_note"]}</span></div>
</footer>
<div class="float-btns"><a class="fb-call" href="tel:{PHONE1_RAW}" aria-label="{u["call"]}">{icon("phone")}</a>
<a class="fb-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="{u["wa_label"]}">{icon("wa")}</a></div>
<div class="cta-bar"><div class="wrap"><div class="txt"><strong>{u["bar_t"]}</strong><span>{u["bar_s"]}</span></div>
<div class="acts"><a class="q" href="{url("teklif", lang)}">{icon("mail")}{u["quote"]}</a><a class="c" href="tel:{PHONE1_RAW}">{icon("phone")}{u["call"]}</a></div></div></div>
<div class="cookie" role="dialog" aria-label="{u["cookies"]}">
<p>{u["cookie_text"]} <a href="{url("privacy", lang)}">{u["cookie_link"]}</a>.</p>
<div class="row"><button class="btn btn-gold" type="button" data-consent="all">{u["accept"]}</button>
<button class="btn btn-ghost" type="button" data-consent="essential">{u["reject"]}</button></div>
</div>
</body>
</html>
"""


# ----------------------------------------------------------------- bileşenler
def page_hero(lang, eyebrow, h1, lead, crumb_label, actions=True):
    u = UI[lang]
    acts = ""
    if actions:
        acts = (f'<div class="actions"><a class="btn btn-gold" href="{url("teklif", lang)}">{u["quote"]}</a>'
                f'<a class="btn btn-outline" href="https://wa.me/{WA}" target="_blank" rel="noopener">{icon("wa")}{u["wa"]}</a></div>')
    return f"""<section class="page-hero on-navy"><div class="wrap">
<nav class="crumbs" aria-label="breadcrumb"><a href="{url("home", lang)}">{u["home"]}</a> / {e(crumb_label)}</nav>
<p class="eyebrow">{e(eyebrow)}</p>
<h1>{e(h1)}</h1>
<p class="lead">{e(lead)}</p>
{acts}
</div></section>
"""


def cards(items, featured_first=False):
    out = '<div class="cards">'
    for i, it in enumerate(items):
        cls = "card reveal" + (" featured" if featured_first and i < 2 else "")
        more = f'<a class="more" href="{it["href"]}">{e(it["more"])} →</a>' if it.get("href") else ""
        lst = ""
        if it.get("list"):
            lst = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in it["list"]) + "</ul>"
        ico = f'<span class="ico">{icon(it["icon"])}</span>' if it.get("icon") else ""
        out += f'<article class="{cls}">{ico}<h3>{e(it["t"])}</h3><p>{e(it["d"])}</p>{lst}{more}</article>'
    return out + "</div>"


def section_head(eyebrow, h2, p=""):
    pp = f"<p>{e(p)}</p>" if p else ""
    return f'<div class="section-head"><div><p class="eyebrow">{e(eyebrow)}</p><h2>{e(h2)}</h2></div>{pp}</div>'


def steps(items):
    return '<ol class="steps">' + "".join(
        f'<li class="reveal"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in items) + "</ol>"


def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def panel(eyebrow, h2, items):
    body = "".join(f'<div class="item"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in items)
    return f'<div class="panel on-navy reveal"><p class="eyebrow">{e(eyebrow)}</p><h2>{e(h2)}</h2>{body}</div>'


def cta_band(lang, title):
    u = UI[lang]
    return f"""<section class="cta-band"><div class="wrap">
<h2>{e(title)}</h2>
<div class="actions"><a class="btn btn-gold" href="{url("teklif", lang)}">{u["quote"]}</a>
<a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{icon("wa")}WhatsApp</a>
<a class="btn btn-line" href="tel:{PHONE1_RAW}">{icon("phone")}{PHONE1}</a></div>
</div></section>
"""


SERVICE_OPTS = {
    "tr": [("kurumsal-konaklama", "Kurumsal otel konaklama"), ("vip-transfer", "VIP havalimanı transferi"),
           ("saglik-turizmi", "Sağlık turizmi konaklama / transfer"), ("fuar-konaklama", "Fuar konaklama"),
           ("grup-heyet", "Grup, heyet veya spor takımı"), ("diger", "Diğer")],
    "en": [("kurumsal-konaklama", "Corporate hotel accommodation"), ("vip-transfer", "VIP airport transfer"),
           ("saglik-turizmi", "Medical tourism accommodation / transfer"), ("fuar-konaklama", "Trade fair accommodation"),
           ("grup-heyet", "Group, delegation or sports team"), ("diger", "Other")],
}

FL = {
    "tr": {"company": "Şirket / kurum adı", "company_opt": "Firma adı", "name": "Yetkili kişi", "name_c": "Ad soyad",
           "email": "E-posta", "phone": "Telefon", "service": "Talep edilen hizmet", "choose": "Seçiniz",
           "ds": "Giriş / transfer tarihi", "de": "Çıkış tarihi", "guests": "Kişi sayısı", "rooms": "Oda sayısı",
           "fair": "Fuar adı", "subject": "Konu", "msg": "Açıklama", "msg_c": "Mesajınız",
           "consent": "Talebime yanıt verilmesi amacıyla iletişim bilgilerimin işlenmesine ilişkin <a href=\"/privacy\">aydınlatma metnini</a> okudum ve kabul ediyorum.",
           "send": "Talebi gönder", "send_c": "Mesajı gönder", "wa": "WhatsApp ile gönder",
           "note": "Zorunlu alanlar * ile işaretlidir. Kimlik, pasaport veya sağlık bilgisi paylaşmayın.",
           "hp": "Bu alanı boş bırakın"},
    "en": {"company": "Company / institution", "company_opt": "Company name", "name": "Contact person", "name_c": "Full name",
           "email": "Email", "phone": "Phone", "service": "Service requested", "choose": "Please select",
           "ds": "Check-in / transfer date", "de": "Check-out date", "guests": "Number of guests", "rooms": "Number of rooms",
           "fair": "Trade fair name", "subject": "Subject", "msg": "Details", "msg_c": "Your message",
           "consent": "I have read the <a href=\"/en/privacy\">privacy notice</a> and agree to my contact details being processed to respond to my request.",
           "send": "Send request", "send_c": "Send message", "wa": "Send via WhatsApp",
           "note": "Required fields are marked *. Please do not share ID, passport or health information.",
           "hp": "Leave this field empty"},
}


def field(fid, label, kind="text", req=False, full=False, opts=None, ac="", extra=""):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ""
    r = " required" if req else ""
    acs = f' autocomplete="{ac}"' if ac else ""
    cls = "field full" if full else "field"
    name = fid.split("-", 1)[1]
    if kind == "select":
        o = "".join(f'<option value="{v}">{e(t)}</option>' for v, t in opts)
        ctl = f'<select id="{fid}" name="{name}"{r}>{o}</select>'
    elif kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{name}" maxlength="3000"{r}></textarea>'
    else:
        ctl = f'<input id="{fid}" name="{name}" type="{kind}"{r}{acs}{extra}>'
    return f'<div class="{cls}"><label for="{fid}">{e(label)}{star}</label>{ctl}<span class="err" role="alert"></span></div>'


def qform(lang, ftype="teklif"):
    L = FL[lang]
    p = ftype[:1]
    num = ' min="1" max="5000" inputmode="numeric"'
    f = ""
    if ftype == "teklif":
        opts = [("", L["choose"])] + SERVICE_OPTS[lang]
        f += field(f"{p}-company", L["company"], req=True, ac="organization")
        f += field(f"{p}-name", L["name"], req=True, ac="name")
        f += field(f"{p}-email", L["email"], "email", True, ac="email")
        f += field(f"{p}-phone", L["phone"], "tel", True, ac="tel")
        f += field(f"{p}-service", L["service"], "select", True, True, opts)
        f += field(f"{p}-date_start", L["ds"], "date")
        f += field(f"{p}-date_end", L["de"], "date")
        f += field(f"{p}-guests", L["guests"], "number", extra=num)
        f += field(f"{p}-rooms", L["rooms"], "number", extra=num)
        f += field(f"{p}-message", L["msg"], "textarea", full=True)
        send = L["send"]
    elif ftype == "fuar":
        f += field(f"{p}-name", L["name_c"], req=True, ac="name")
        f += field(f"{p}-company", L["company_opt"], ac="organization")
        f += field(f"{p}-email", L["email"], "email", True, ac="email")
        f += field(f"{p}-phone", L["phone"], "tel", True, ac="tel")
        f += field(f"{p}-fair_name", L["fair"], req=True)
        f += field(f"{p}-guests", L["guests"], "number", True, extra=num)
        f += field(f"{p}-date_start", L["ds"].split(" /")[0], "date", True)
        f += field(f"{p}-date_end", L["de"], "date", True)
        f += field(f"{p}-message", L["msg"], "textarea", full=True)
        send = L["send"]
    else:
        f += field(f"{p}-name", L["name_c"], req=True, ac="name")
        f += field(f"{p}-email", L["email"], "email", True, ac="email")
        f += field(f"{p}-phone", L["phone"], "tel", ac="tel")
        f += field(f"{p}-subject", L["subject"])
        f += field(f"{p}-message", L["msg_c"], "textarea", True, True)
        send = L["send_c"]
    return f"""<form class="qform" action="/form.php" method="post" novalidate>
<input type="hidden" name="form_type" value="{ftype}"><input type="hidden" name="lang" value="{lang}"><input type="hidden" name="ts" value="">
<div class="hp" aria-hidden="true"><label for="{p}-website">{L["hp"]}</label><input id="{p}-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
{f}
<label class="consent full"><input type="checkbox" name="kvkk" value="1" required><span>{L["consent"]} <span class="req">*</span></span></label>
<div class="form-actions full"><button class="btn btn-gold" type="submit">{send}</button>
<button class="btn btn-wa" type="button" data-wa-send>{icon("wa")}{L["wa"]}</button></div>
<p class="full" style="font-size:.85rem;color:var(--muted)">{L["note"]}</p>
<div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def form_section(lang, title, lead, ftype="teklif", sid="teklif"):
    eyebrow = "Teklif Al" if lang == "tr" else "Request a quote"
    if ftype == "iletisim":
        eyebrow = "Mesaj" if lang == "tr" else "Message"
    wa_line = "WhatsApp" + (": " + PHONE1)
    return f"""<section class="section white" id="{sid}"><div class="wrap form-wrap">
<div class="form-aside">
<p class="eyebrow">{eyebrow}</p>
<h2>{e(title)}</h2>
<p class="lead">{e(lead)}</p>
<a class="btn btn-wa" style="align-self:flex-start" href="https://wa.me/{WA}" target="_blank" rel="noopener">{icon("wa")}{wa_line}</a>
<a class="btn btn-line" style="align-self:flex-start;color:var(--navy-700);border-color:var(--navy-700)" href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a>
</div>
{qform(lang, ftype)}
</div></section>
"""


def org_schema(lang):
    return {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": "Atlantis Travel",
        "url": SITE + "/",
        "logo": SITE + "/assets/img/logo-horizontal.png",
        "image": SITE + "/assets/img/og-image.jpg",
        "email": EMAIL,
        "telephone": [PHONE1_RAW, PHONE2_RAW],
        "address": {"@type": "PostalAddress", "addressLocality": "İstanbul", "addressCountry": "TR"},
        "areaServed": {"@type": "City", "name": "İstanbul"},
        "sameAs": [INSTAGRAM, FACEBOOK],
        "availableLanguage": ["tr", "en"],
        "description": ("İstanbul'da kurumsal otel konaklama, VIP havalimanı transferi ve sağlık turizmi organizasyonu."
                        if lang == "tr" else
                        "Corporate hotel accommodation, VIP airport transfers and medical tourism logistics in Istanbul."),
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE1_RAW, "contactType": "customer service",
                         "availableLanguage": ["Turkish", "English"], "hoursAvailable": "Mo-Su 00:00-23:59"},
    }


# ----------------------------------------------------------------- içerik
REVIEWS = [
    ("Zafer P.", "Atlantis Travel ile seyahat deneyimim mükemmeldi! Rezervasyon süreci hızlı ve sorunsuzdu, ekip her konuda yardımcı oldu. Kesinlikle tavsiye ederim!"),
    ("Sercan T.", "Tereddütlerimizin olduğu seyahatimizde aklımızdaki tüm soru işaretlerini giderdiler. Bir sorun yaşadığımızda geri dönüşleri çok hızlı oldu."),
    ("Emre Ş.", "Turizm sektöründe birlikte çalıştığımız bir acenta, oldukça iyi ve kaliteli hizmetlerinden dolayı çok memnunuz."),
    ("Can A.", "Müşteri memnuniyetini önde tutan bir firma, güvenilir, herkese tavsiye ederim."),
    ("Ekrem İ.", "Mükemmel bir servis, çok yetenekli ve güler yüzlü personeli ile sorunsuz bir yolculuk yaşamak istiyorsanız Atlantis Travel rehberiniz olsun."),
]
GREVIEW = "https://g.page/r/CUzJql2zq06IEBM/review"


def pic(name, alt, w=600, h=600, lazy=True, cls=""):
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="/assets/img/{name}.webp" type="image/webp">'
            f'<img{c} src="/assets/img/{name}.jpg" width="{w}" height="{h}" alt="{e(alt)}"{ld}></picture>')


def reviews_block(lang, n=3):
    T = lang == "tr"
    stars = "".join(icon("star") for _ in range(5))
    cards_html = "".join(
        f'<figure class="review reveal"><div class="stars" aria-label="5/5">{stars}</div>'
        f'<blockquote>“{e(t)}”</blockquote><figcaption>{e(nm)}</figcaption></figure>' for nm, t in REVIEWS[:n])
    return f"""<div class="reviews-head"><div class="stars big" aria-hidden="true">{stars}</div>
<strong>{"Google yorumlarımız" if T else "Our Google reviews"}</strong>
<a class="more" href="{GREVIEW}" target="_blank" rel="noopener">{"Tüm yorumlar" if T else "All reviews"} →</a></div>
<div class="reviews">{cards_html}</div>
<p class="review-note">{"Yorumlar Google İşletme profilimizden alınmıştır." if T else "Reviews are taken from our Google Business profile (originally in Turkish)."}</p>"""


def build_home(lang):
    T = lang == "tr"
    u = UI[lang]
    title = ("Atlantis Travel | Kurumsal Konaklama ve Operasyonel Seyahat Çözümleri" if T else
             "Atlantis Travel | Corporate Accommodation & Travel Operations in Istanbul")
    desc = ("İstanbul'da hastaneler, sağlık turizmi firmaları, fuar katılımcıları ve şirketler için kurumsal otel konaklama, transfer organizasyonu ve 7/24 operasyon desteği." if T else
            "Corporate hotel accommodation, transfer organisation and 24/7 operations support in Istanbul for hospitals, medical tourism companies, trade fair exhibitors and businesses.")
    h = head(lang, "home", title, desc, [org_schema(lang)]) + header(lang, "home")
    feats = ([("clock", "7/24 Destek"), ("pin", "Hastane ve fuar alanlarına yakın oteller"),
              ("car", "Transfer organizasyonu"), ("tag", "Kuruma özel fiyatlandırma")] if T else
             [("clock", "24/7 support"), ("pin", "Hotels near hospitals and expo centres"),
              ("car", "Transfer organisation"), ("tag", "Pricing tailored to your organisation")])
    fl = "".join(f'<li>{icon(i)}<span>{e(t)}</span></li>' for i, t in feats)
    h += f"""<section class="hero2">
<picture class="bg"><source srcset="/assets/img/hero-lobby.webp" type="image/webp"><img src="/assets/img/hero-lobby.jpg" width="1024" height="1024" alt="" fetchpriority="high"></picture>
<div class="wrap">
<p class="pill">{"Sağlık kurumları için kurumsal seyahat" if T else "Corporate travel for healthcare providers"}</p>
<h1>{"Kurumsal Konaklama ve Operasyonel Seyahat Çözümleri" if T else "Corporate Accommodation and Travel Operations"}</h1>
<p class="lead">{"Profesyonel operasyon yönetimi ile bütçeye uygun, hızlı ve sürdürülebilir hizmet" if T else "Budget-friendly, fast and sustainable service backed by professional operations management"}</p>
<div class="actions"><a class="btn btn-gold" href="#teklif">{"Hemen Teklif Al" if T else "Get a Quote"}</a>
<a class="btn btn-outline" href="https://wa.me/{WA}" target="_blank" rel="noopener">{"WhatsApp ile Yazın" if T else "Message us on WhatsApp"}</a></div>
<ul class="hero-feats">{fl}</ul>
<a class="scroll" href="#kimler" aria-label="{"Aşağı kaydır" if T else "Scroll down"}">{icon("chev")}</a>
</div></section>
"""
    who = ([("steth", "Hastaneler ve Klinikler", "Hasta yakını ve sağlık personeli konaklaması"),
            ("globe", "Sağlık Turizmi Firmaları", "Yurt dışından gelen hastalar için konaklama ve transfer"),
            ("building", "Fuar Katılımcıları", "İstanbul fuarları için fuar alanına yakın toplu konaklama"),
            ("briefcase", "Kurumsal Şirketler", "İş seyahati ve ekip konaklaması")] if T else
           [("steth", "Hospitals and Clinics", "Accommodation for patients' relatives and medical staff"),
            ("globe", "Medical Tourism Companies", "Accommodation and transfers for patients from abroad"),
            ("building", "Trade Fair Exhibitors", "Group stays close to Istanbul's expo centres"),
            ("briefcase", "Corporate Companies", "Business travel and team accommodation")])
    whoh = "".join(f'<article class="who reveal"><span class="gi">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in who)
    svc = ([("svc-konaklama", "hotel", "Yurt İçi Konaklama", "Talep edilen bölgelerde her segmentten otel seçeneği ve bütçeye uygun fiyat alternatifleri ile kaliteli konaklama hizmeti sunuyoruz.", "konaklama"),
            ("svc-transfer", "car", "Transfer Organizasyonu", "Profesyonel transfer hizmetleri ile hastalarınızın ve personellerinizin güvenli ve konforlu ulaşımını sağlıyoruz.", "transfer"),
            ("svc-operasyon", "ops", "Operasyonel Süreç Yönetimi", "Tüm operasyonel süreçleri profesyonel bir anlayışla yöneterek sağlık kurumlarınızın operasyonel yükünü azaltıyoruz.", "saglik"),
            ("svc-grup", "group", "Grup ve Futbol Takımı Konaklamaları", "Spor kulüpleri ve büyük gruplar için özel konaklama paketleri sunuyoruz. Futbol takımları, spor organizasyonları ve kurumsal gruplar için uygun fiyatlı, konforlu ve organize konaklama çözümleri sağlıyoruz.", "cozumler")] if T else
           [("svc-konaklama", "hotel", "Accommodation in Türkiye", "Hotels of every category in the areas you need, with budget-friendly alternatives and quality service.", "konaklama"),
            ("svc-transfer", "car", "Transfer Organisation", "Professional transfers for safe and comfortable travel of your patients and staff.", "transfer"),
            ("svc-operasyon", "ops", "Operations Management", "We manage every operational step professionally to lighten the workload of your organisation.", "saglik"),
            ("svc-grup", "group", "Group and Football Team Stays", "Tailored accommodation packages for sports clubs, football teams, sports events and corporate groups: affordable, comfortable and well organised.", "cozumler")])
    svch = "".join(f'<a class="svc reveal" href="{url(k, lang)}">{pic(img, t)}<div class="b"><span class="si">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div></a>' for img, i, t, d, k in svc)
    stp = ([("Talebinizi İletin", "Form, telefon veya WhatsApp üzerinden ihtiyaçlarınızı paylaşın."),
            ("Size Özel Teklif", "Tarih, konum ve bütçenize uygun otel ve transfer seçeneklerini hazırlayalım."),
            ("Organizasyon Bizde", "Konaklama ve transferiniz planlandığı gibi yürütülsün, 7/24 yanınızdayız.")] if T else
           [("Send Your Request", "Share your needs via the form, phone or WhatsApp."),
            ("Tailored Offer", "We prepare hotel and transfer options matched to your dates, location and budget."),
            ("We Handle the Rest", "Your stay and transfers run as planned, with 24/7 support.")])
    stph = "".join(f'<li class="reveal"><span class="num">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(stp))
    why = ([("Güvenilir İş Ortaklığı", "Sağlık sektörüne özel çözümlerimizle uzun vadeli iş ortaklıkları kuruyoruz."),
            ("Her Segmentten Otel Seçeneği", "Geniş otel ağımız sayesinde her bütçeye uygun kaliteli konaklama alternatifleri sunuyoruz."),
            ("Bütçeye Uygun Fiyatlar", "Anlaşmalı otellerimiz ile uygun fiyatlar ve şeffaf fiyatlandırma sunuyoruz.")] if T else
           [("Reliable Partnership", "We build long-term partnerships with solutions designed for the healthcare sector."),
            ("Hotels in Every Category", "Our wide hotel network offers quality options for every budget."),
            ("Budget-Friendly Prices", "Competitive rates with our partner hotels and transparent pricing.")])
    whyh = "".join(f'<li>{icon("check")}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for t, d in why)
    h += f"""<section class="section" id="kimler"><div class="wrap">
<h2 class="center-h">{"Kimlere Hizmet Veriyoruz?" if T else "Who We Serve"}</h2>
<div class="who-grid">{whoh}</div>
</div></section>
<section class="section pt0"><div class="wrap">
<h2 class="center-h">{"Hizmetlerimiz" if T else "Our Services"}</h2>
<p class="center-p">{"Sağlık kurumlarınız için kapsamlı konaklama ve seyahat çözümleri" if T else "Comprehensive accommodation and travel solutions for your organisation"}</p>
<div class="svc-grid">{svch}</div>
</div></section>
<section class="section pt0"><div class="wrap">
<h2 class="center-h">{"Nasıl Çalışır?" if T else "How It Works"}</h2>
<ol class="steps3">{stph}</ol>
</div></section>
<section class="why"><div class="wrap">
<div><h2>{"Neden Atlantis Travel?" if T else "Why Atlantis Travel?"}</h2>
<p class="sub">{"Güvenilir iş ortaklığı modeliyle hızlı, planlı ve sürdürülebilir hizmet" if T else "Fast, planned and sustainable service through a reliable partnership model"}</p>
<span class="rule"></span><ul class="why-list">{whyh}</ul></div>
<div class="why-img">{pic("is-ortakligi", "Kurumsal iş ortaklığı" if T else "Business partnership")}</div>
</div></section>
<section class="section"><div class="wrap">{reviews_block(lang)}</div></section>
"""
    h += quick_form(lang)
    h += f"""<section class="consult"><div class="wrap">
<h2>{"Kurumsal Seyahat Çözümleriniz İçin Bizimle İletişime Geçin" if T else "Contact Us for Your Corporate Travel Needs"}</h2>
<p>{"Operasyonel verimliliğinizi artırın, maliyetlerinizi optimize edin. Profesyonel ekibimiz size özel çözümler sunmak için hazır." if T else "Improve operational efficiency and optimise costs. Our team is ready to offer solutions tailored to you."}</p>
<a class="btn btn-gold" href="{url("contact", lang)}">{"Ücretsiz Danışmanlık Alın" if T else "Get Free Consultation"}</a>
</div></section>
"""
    h += footer(lang)
    return h


def quick_form(lang):
    T = lang == "tr"
    return f"""<section class="section qf" id="teklif"><div class="wrap">
<h2 class="center-h">{"Hızlı Teklif Alın" if T else "Get a Quick Quote"}</h2>
<p class="center-p">{"Bilgilerinizi paylaşın, size en uygun konaklama teklifini hemen gönderelim" if T else "Share your details and we will send you the most suitable accommodation offer"}</p>
<div class="qf-card"><div class="qf-head">{"Teklif Formu" if T else "Quote Form"}</div>
{qform(lang, "teklif")}</div>
</div></section>
"""


def build_referans(lang):
    T = lang == "tr"
    title = "Referanslarımız | Atlantis Travel" if T else "References | Atlantis Travel"
    desc = ("Atlantis Travel hakkında Google yorumları ve birlikte çalıştığımız kurum türleri." if T else
            "Google reviews about Atlantis Travel and the types of organisations we work with.")
    h = head(lang, "referans", title, desc, [org_schema(lang)]) + header(lang, "referans")
    h += page_hero(lang, "Güvenilir İş Ortaklığı" if T else "Reliable Partnership", "Referanslarımız" if T else "Our References",
                   "Sağlık kurumları ve kurumsal firmalarla yürüttüğümüz iş birlikleri" if T else
                   "Our collaborations with healthcare providers and corporate companies",
                   "Referanslar" if T else "References")
    stars = "".join(icon("star") for _ in range(5))
    allrev = "".join(f'<figure class="review reveal"><div class="stars">{stars}</div><blockquote>“{e(t)}”</blockquote><figcaption>{e(nm)}</figcaption></figure>' for nm, t in REVIEWS)
    kinds = (["Özel Sağlık Kurumları", "Hastane Zincirleri", "Klinik Grupları", "Medikal Merkezler", "Sağlık Turizmi Firmaları", "Kurumsal Şirketler"] if T else
             ["Private Healthcare Providers", "Hospital Groups", "Clinic Groups", "Medical Centres", "Medical Tourism Companies", "Corporate Companies"])
    kh = "".join(f'<li>{icon("check")}{e(k)}</li>' for k in kinds)
    h += f"""<section class="section"><div class="wrap">
<h2 class="center-h">{"Google'da Müşterilerimiz Ne Diyor?" if T else "What Our Clients Say on Google"}</h2>
<div class="reviews">{allrev}</div>
<div class="center-actions"><a class="btn btn-gold" href="{GREVIEW}" target="_blank" rel="noopener">{"Google'da tüm yorumları gör" if T else "See all reviews on Google"}</a>
<a class="btn btn-ghost" href="{GREVIEW}" target="_blank" rel="noopener">{"Siz de yorum bırakın" if T else "Leave a review"}</a></div>
</div></section>
<section class="section white"><div class="wrap">
<h2 class="center-h">{"İş Ortaklarımız" if T else "Who We Work With"}</h2>
<p class="center-p">{"Güvenilir kurumsal çözümler sunduğumuz sağlık kurumları ve firmalar" if T else "Healthcare providers and companies we offer reliable corporate solutions to"}</p>
<ul class="kinds">{kh}</ul>
</div></section>
<section class="consult"><div class="wrap">
<h2>{"Siz de İş Ortağımız Olun" if T else "Become Our Partner"}</h2>
<p>{"Kurumsal konaklama ve seyahat ihtiyaçlarınız için güvenilir çözümler sunuyoruz." if T else "We provide reliable solutions for your corporate accommodation and travel needs."}</p>
<a class="btn btn-gold" href="{url("contact", lang)}">{"İletişime Geçin" if T else "Contact Us"}</a>
</div></section>
"""
    h += footer(lang)
    return h


def service_page(lang, key, title, desc, eyebrow, h1, lead, crumb, intro_h, intro_p, bullets, cards_items, panel_items,
                 cta, schema_service=None, faq=None, extra=""):
    T = lang == "tr"
    schema = [org_schema(lang)]
    if schema_service:
        schema.append({"@context": "https://schema.org", "@type": "Service", "name": schema_service,
                       "provider": {"@type": "TravelAgency", "name": "Atlantis Travel", "url": SITE + "/"},
                       "areaServed": {"@type": "City", "name": "İstanbul"},
                       "url": SITE + url(key, lang)})
    h = head(lang, key, title, desc, schema) + header(lang, key)
    h += page_hero(lang, eyebrow, h1, lead, crumb)
    h += f"""<section class="section"><div class="wrap split">
<div class="reveal"><h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{e(intro_h)}</h2>
<p class="lead" style="margin-bottom:24px">{e(intro_p)}</p>
{checks(bullets)}</div>
{panel("Neden Atlantis Travel" if T else "Why Atlantis Travel", "Tek muhatap, 7/24 takip" if T else "One contact, 24/7 follow-up", panel_items)}
</div></section>
"""
    if cards_items:
        h += f"""<section class="section white"><div class="wrap">
{section_head("Hizmet kapsamı" if T else "Scope of service", "Neler organize ediyoruz?" if T else "What we organise")}
{cards(cards_items)}
</div></section>
"""
    h += extra
    if faq:
        h += f'<section class="section"><div class="wrap">{section_head("Sık sorulanlar" if T else "FAQ", "Merak edilenler" if T else "Common questions")}' + faq_html(faq) + "</div></section>"
    h += cta_band(lang, cta)
    h += footer(lang)
    return h


def faq_html(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items) + "</div>"


def build_konaklama(lang):
    T = lang == "tr"
    return service_page(
        lang, "konaklama",
        "Kurumsal Otel Konaklama İstanbul | Atlantis Travel" if T else "Corporate Hotel Accommodation in Istanbul | Atlantis Travel",
        "Şirketler, kamu kurumları, klinikler ve gruplar için İstanbul'da 200+ otelle kurumsal konaklama. Bütçeye uygun seçenekler, planlı rezervasyon ve 7/24 operasyon desteği." if T else
        "Corporate accommodation in Istanbul through 200+ hotels for companies, public institutions, clinics and groups. Budget-aligned options and 24/7 support.",
        "Kurumsal Konaklama" if T else "Corporate accommodation",
        "Kurumsal otel konaklama ve seyahat yönetimi" if T else "Corporate hotel accommodation and travel management",
        "Şirketler, kamu kurumları, özel klinik ve hastane grupları için bütçeye uygun, hızlı ve sürdürülebilir konaklama hizmeti." if T else
        "Budget-aligned, fast and sustainable accommodation for companies, public institutions and private clinic and hospital groups.",
        "Kurumsal Konaklama" if T else "Corporate Accommodation",
        "Her segmentten otel, tek muhatap" if T else "Every hotel category, one contact",
        "İstanbul'da 200'den fazla otelle çalışıyoruz. Talep edilen bölgede ekonomik, orta ve üst segment seçenekleri sunar; rezervasyondan çıkışa kadar tüm süreci kurumunuz adına yönetiriz. İstanbul dışındaki şehirler için de talep üzerine konaklama organize ediyoruz." if T else
        "We work with more than 200 hotels in Istanbul. We offer economy, mid-range and upscale options in the area you need and manage the whole process on your behalf. Stays in other Turkish cities can be arranged on request.",
        ["Talep edilen bölgede her bütçeye uygun otel alternatifleri", "Hastanelere, ofislere ve fuar alanlarına yakın konumlar",
         "Bireysel, ekip ve grup rezervasyonları", "Kurumsal faturalandırma ve tek noktadan takip", "Transfer ile birlikte planlama"] if T else
        ["Hotel options for every budget in the area you need", "Locations close to hospitals, offices and expo centres",
         "Individual, team and group bookings", "Corporate invoicing and single-point follow-up", "Planned together with transfers"],
        [{"icon": "hotel", "t": "Ekonomik segment" if T else "Economy", "d": "Temiz, konforlu ve bütçe dostu konaklama seçenekleri." if T else "Clean, comfortable and budget-friendly stays."},
         {"icon": "hotel", "t": "Orta segment" if T else "Mid-range", "d": "Kalite ve konforun buluştuğu modern oteller." if T else "Modern hotels balancing quality and comfort."},
         {"icon": "hotel", "t": "Üst segment" if T else "Upscale", "d": "Yönetici ve misafir ağırlamaları için prestijli konaklama." if T else "Prestigious stays for executives and VIP guests."},
         {"icon": "ops", "t": "Operasyonel süreç yönetimi" if T else "Operations management", "d": "Rezervasyon, giriş-çıkış ve değişiklik takibi tek muhatapla." if T else "Bookings, check-in/out and changes handled by one contact."}],
        [("Kurumlara özel çalışma modeli", "Uzun vadeli iş ortaklığı ve düzenli konaklama ihtiyaçları için planlı süreç."),
         ("Hızlı ve planlı hizmet", "Acil talepler dahil rezervasyonlarınızı hızla organize ederiz."),
         ("7/24 destek", "Konaklama boyunca ulaşabileceğiniz operasyon ekibi.")] if T else
        [("A model built for organisations", "Planned processes for long-term partnerships and recurring stays."),
         ("Fast, organised service", "We arrange bookings quickly, including urgent requests."),
         ("24/7 support", "An operations team you can reach throughout the stay.")],
        "Kurumunuz için konaklama teklifi alın" if T else "Get an accommodation quote for your organisation",
        "Kurumsal otel konaklama" if T else "Corporate hotel accommodation")


def build_transfer(lang):
    T = lang == "tr"
    return service_page(
        lang, "transfer",
        "VIP Havalimanı Transferi İstanbul – IST ve SAW | Atlantis Travel" if T else "VIP Airport Transfer Istanbul – IST & SAW | Atlantis Travel",
        "İstanbul Havalimanı ve Sabiha Gökçen'den Mercedes Vito ile VIP transfer ve özel karşılama. Kurumsal misafirler, hastalar ve gruplar için 7/24 planlı ulaşım." if T else
        "VIP transfers and meet & greet from Istanbul Airport and Sabiha Gökçen with Mercedes Vito. Planned 24/7 transport for corporate guests, patients and groups.",
        "VIP Transfer", "VIP havalimanı transferi ve özel karşılama" if T else "VIP airport transfers and meet & greet",
        "İstanbul Havalimanı (IST) ve Sabiha Gökçen (SAW) karşılamalarından otel, hastane ve fuar transferlerine kadar güvenli ve konforlu ulaşım." if T else
        "Safe, comfortable transport from Istanbul Airport (IST) and Sabiha Gökçen (SAW) arrivals to hotel, hospital and expo transfers.",
        "VIP Transfer",
        "Misafirleriniz havalimanında karşılanır" if T else "Your guests are met at the airport",
        "Misafirlerinizi isim tabelasıyla karşılar, Mercedes Vito araçlarla otele, hastaneye veya toplantıya ulaştırırız. Grup büyüklüğüne göre minibüs ve otobüs seçenekleri de planlanabilir." if T else
        "We welcome your guests with a name sign and take them to their hotel, hospital or meeting in Mercedes Vito vehicles. Minibuses and coaches can be arranged for larger groups.",
        ["İstanbul Havalimanı (IST) ve Sabiha Gökçen (SAW) karşılama", "Mercedes Vito ile VIP transfer",
         "Otel – hastane – fuar – toplantı arası şehir içi transferler", "Uçuş saatine göre planlanan karşılama",
         "Grup büyüklüğüne göre minibüs ve otobüs seçenekleri"] if T else
        ["Meet & greet at Istanbul Airport (IST) and Sabiha Gökçen (SAW)", "VIP transfers by Mercedes Vito",
         "City transfers between hotel, hospital, expo and meetings", "Pick-up planned around flight times",
         "Minibus and coach options for groups"],
        [{"icon": "plane", "t": "Havalimanı karşılama" if T else "Airport meet & greet", "d": "Varış salonunda isim tabelasıyla karşılama ve bagaj desteği." if T else "Welcome with a name sign in the arrivals hall and luggage assistance."},
         {"icon": "car", "t": "Mercedes Vito VIP" if T else "Mercedes Vito VIP", "d": "Bireysel misafirler ve küçük gruplar için konforlu VIP araç." if T else "A comfortable VIP vehicle for individuals and small groups."},
         {"icon": "group", "t": "Grup transferleri" if T else "Group transfers", "d": "Heyetler ve takımlar için minibüs ve otobüs planlaması." if T else "Minibus and coach planning for delegations and teams."},
         {"icon": "health", "t": "Hastane transferleri" if T else "Hospital transfers", "d": "Hasta ve refakatçiler için otel ile hastane arası planlı ulaşım." if T else "Scheduled hotel–hospital transport for patients and companions."}],
        [("Planlı karşılama", "Uçuş bilgisine göre zamanlanan karşılama ve transfer."),
         ("Konaklama ile birlikte", "Transfer ve otel tek planda, tek muhatapla."),
         ("7/24 ulaşılabilirlik", "Gece varışları dahil her saatte destek.")] if T else
        [("Planned pick-ups", "Meet & greet scheduled around flight details."),
         ("Combined with accommodation", "Transfer and hotel in one plan, with one contact."),
         ("Available 24/7", "Support at any hour, including late-night arrivals.")],
        "VIP transfer talebinizi iletin" if T else "Request a VIP transfer",
        "VIP havalimanı transferi" if T else "VIP airport transfer")


def build_saglik(lang):
    T = lang == "tr"
    note = ("Atlantis Travel tıbbi işlem, teşhis veya tedavi hizmeti vermez. Hizmetimiz; hasta, refakatçi ve sağlık personeli için konaklama, transfer ve operasyon organizasyonudur." if T else
            "Atlantis Travel does not provide medical procedures, diagnosis or treatment. Our service is accommodation, transfer and operations support for patients, companions and healthcare staff.")
    extra = f'<section class="section tight"><div class="wrap"><div class="panel on-navy" style="padding:28px 32px"><p style="color:var(--on-navy)"><strong style="color:var(--gold)">{"Önemli bilgi" if T else "Please note"}:</strong> {e(note)}</p></div></div></section>'
    return service_page(
        lang, "saglik",
        "Sağlık Turizmi Konaklama ve Transfer İstanbul | Atlantis Travel" if T else "Medical Tourism Accommodation & Transfers in Istanbul | Atlantis Travel",
        "Özel hastaneler, diş klinikleri ve uluslararası hastalar için İstanbul'da otel konaklama, havalimanı ve hastane transferleri. Kurumlara özel operasyon desteği." if T else
        "Hotel accommodation, airport and hospital transfers in Istanbul for private hospitals, dental clinics and international patients.",
        "Sağlık Turizmi" if T else "Medical tourism",
        "Hastaneler ve klinikler için konaklama ve transfer organizasyonu" if T else "Accommodation and transfers for hospitals and clinics",
        "Özel hastaneler, diş klinikleri ve uluslararası hastalarınız için otel konaklaması, havalimanı karşılaması ve hastane transferlerini kurumunuz adına yönetiyoruz." if T else
        "We manage hotel stays, airport meet & greet and hospital transfers on behalf of private hospitals, dental clinics and their international patients.",
        "Sağlık Turizmi" if T else "Medical Tourism",
        "Sağlık kuruluşlarının operasyon yükünü azaltıyoruz" if T else "Reducing the operational load on healthcare providers",
        "Hasta, hasta yakını ve personel konaklama süreçlerindeki operasyonel yükü üstleniyoruz. Tedavi planınıza göre hastaneye yakın oteller, havalimanı karşılaması ve hastane transferleri tek plan halinde yürütülür." if T else
        "We take over the operational work of patient, companion and staff accommodation. Hotels close to the hospital, airport meet & greet and hospital transfers run as a single plan built around the treatment schedule.",
        ["Hastaneye ve kliniğe yakın otel seçenekleri", "Hasta ve refakatçi konaklaması", "Havalimanı karşılama ve hastane transferleri",
         "Kurumla koordineli tarih ve randevu planı", "Uluslararası hastalar için İngilizce iletişim"] if T else
        ["Hotels close to the hospital or clinic", "Patient and companion accommodation", "Airport meet & greet and hospital transfers",
         "Dates coordinated with the provider", "English-language communication for international patients"],
        [{"icon": "health", "t": "Özel hastaneler" if T else "Private hospitals", "d": "Uluslararası hasta birimleri için düzenli konaklama ve transfer desteği." if T else "Recurring accommodation and transfer support for international patient departments."},
         {"icon": "health", "t": "Diş klinikleri" if T else "Dental clinics", "d": "Kısa ve tekrarlayan ziyaretlere uygun otel ve transfer planı." if T else "Hotel and transfer plans suited to short, repeat visits."},
         {"icon": "group", "t": "Hasta ve refakatçiler" if T else "Patients and companions", "d": "Konforlu konaklama ve günlük ulaşım organizasyonu." if T else "Comfortable stays and daily transport arrangements."}],
        [("Kuruma özel süreç", "Uluslararası hasta biriminizle koordineli çalışırız."),
         ("Tek muhatap", "Konaklama, transfer ve değişiklikler aynı ekiple."),
         ("7/24 destek", "Hasta ve refakatçiler için her saatte ulaşılabilir operasyon.")] if T else
        [("A process for each provider", "We coordinate with your international patient department."),
         ("One contact", "Accommodation, transfers and changes handled by one team."),
         ("24/7 support", "Operations reachable at any hour for patients and companions.")],
        "Sağlık kuruluşunuz için iş birliği teklifi alın" if T else "Get a partnership quote for your healthcare organisation",
        "Sağlık turizmi konaklama ve transfer" if T else "Medical tourism accommodation and transfer", extra=extra)


def build_fuar(lang):
    T = lang == "tr"
    extra = f"""<section class="section white"><div class="wrap">
{section_head("Fuar merkezleri" if T else "Expo centres", "Hizmet verdiğimiz fuar alanları" if T else "Expo centres we serve")}
{cards([
    {"icon": "fair", "t": "TÜYAP Beylikdüzü", "d": ("Avrupa yakasındaki fuar merkezine yakın konumda ekonomik, orta ve üst segment otel seçenekleri." if T else "Economy, mid-range and upscale hotels close to the expo centre on the European side."),
     "list": (["Fuar alanına yakın oteller", "Günlük otel – fuar transferi", "Grup rezervasyonları"] if T else ["Hotels close to the venue", "Daily hotel–expo transfers", "Group bookings"])},
    {"icon": "fair", "t": "İstanbul Fuar Merkezi (İFM)" if T else "Istanbul Expo Center (IFM)", "d": ("Yeşilköy'deki fuar merkezi için havalimanına ve fuar alanına yakın konaklama." if T else "Accommodation near Yeşilköy's expo centre and the airport."),
     "list": (["Fuar alanına ve havalimanına yakın oteller", "Havalimanı transferi", "Türkçe ve İngilizce destek"] if T else ["Hotels near the venue and airport", "Airport transfers", "Turkish and English support"])},
])}
</div></section>
"""
    extra += form_section(lang, "Fuar konaklama talebi oluşturun" if T else "Request trade fair accommodation",
                          "Fuar adını, tarihleri ve kişi sayısını paylaşın; size uygun otel seçeneklerini gönderelim." if T else
                          "Share the fair name, dates and number of guests and we will send suitable hotel options.", "fuar", "fuar-form")
    return service_page(
        lang, "fuar",
        "Fuar Konaklama İstanbul – TÜYAP ve İFM | Atlantis Travel" if T else "Trade Fair Accommodation Istanbul – TÜYAP & IFM | Atlantis Travel",
        "TÜYAP Beylikdüzü ve İstanbul Fuar Merkezi (İFM) için fuar alanlarına yakın otel konaklama, havalimanı ve fuar transferleri." if T else
        "Hotel accommodation near TÜYAP Beylikdüzü and Istanbul Expo Center (IFM), with airport and expo transfers.",
        "Fuar Konaklama" if T else "Trade fair accommodation",
        "Fuar katılımcıları için İstanbul'da konaklama" if T else "Accommodation in Istanbul for trade fair participants",
        "Yurt içinden ve yurt dışından İstanbul'daki fuarlara gelen katılımcı ve ziyaretçi firmalar için fuar alanlarına yakın, her bütçeye uygun konaklama." if T else
        "Accommodation for every budget close to the venues, for exhibitors and visitors coming to Istanbul's trade fairs.",
        "Fuar Konaklama" if T else "Trade Fair Accommodation",
        "Fuar dönemine özel planlama" if T else "Planning for the fair period",
        "Fuar dönemlerinde yoğunlaşan talepleri önceden planlar; konaklama, havalimanı karşılaması ve otel–fuar arası günlük transferleri tek noktadan organize ederiz." if T else
        "We plan ahead for peak fair periods and organise accommodation, airport pick-ups and daily hotel–expo transfers from a single point.",
        ["Fuar alanlarına yakın konumda oteller", "Ekonomik, orta ve üst segment seçenekler", "Havalimanı karşılama ve günlük fuar transferi",
         "Toplu rezervasyonlarda kurumsal fiyatlandırma", "Türkçe ve İngilizce destek"] if T else
        ["Hotels close to the venues", "Economy, mid-range and upscale options", "Airport pick-ups and daily expo transfers",
         "Corporate pricing for group bookings", "Turkish and English support"],
        [],
        [("Tek noktadan hizmet", "Konaklama, transfer ve organizasyon için tek muhatap."),
         ("Erken planlama", "Fuar takvimine göre önceden rezervasyon."),
         ("7/24 destek", "Fuar süresince ulaşılabilir operasyon ekibi.")] if T else
        [("One point of contact", "Accommodation, transfers and logistics in one place."),
         ("Early planning", "Bookings made ahead according to the fair calendar."),
         ("24/7 support", "An operations team you can reach throughout the fair.")],
        "Fuar dönemi için yerinizi önceden ayırın" if T else "Secure your stay for the fair period early",
        "Fuar konaklama" if T else "Trade fair accommodation", extra=extra)


def build_cozumler(lang):
    T = lang == "tr"
    return service_page(
        lang, "cozumler",
        "Kurumsal Çözümler – Heyet, Grup ve Takım Konaklaması | Atlantis Travel" if T else "Corporate Solutions – Delegation, Group & Team Stays | Atlantis Travel",
        "Heyetler, delegasyonlar, spor ve futbol takımları ile toplu konaklama organizasyonları için İstanbul'da otel, transfer ve operasyon yönetimi." if T else
        "Hotel, transfer and operations management in Istanbul for delegations, sports and football teams and group stays.",
        "Kurumsal Çözümler" if T else "Corporate solutions",
        "Heyetler, gruplar ve takımlar için kurumsal organizasyon" if T else "Corporate logistics for delegations, groups and teams",
        "Delegasyonlar, spor takımları ve toplu konaklamalar için otel, transfer ve operasyonu planlı biçimde yönetiyoruz." if T else
        "We plan and manage hotels, transfers and operations for delegations, sports teams and group stays.",
        "Kurumsal Çözümler" if T else "Corporate Solutions",
        "Kalabalık gruplar, tek plan" if T else "Large groups, one plan",
        "Grup büyüklüğüne, programa ve bütçeye göre otel bloğu, transfer araçları ve günlük operasyonu birlikte planlıyoruz. Spor kulüpleri ve büyük gruplar için uygun fiyatlı, konforlu ve organize konaklama çözümleri sunuyoruz." if T else
        "We plan hotel room blocks, transfer vehicles and daily operations together, based on group size, schedule and budget, with comfortable, organised and cost-effective options for sports clubs and large groups.",
        ["Heyet ve delegasyon ağırlama", "Spor ve futbol takımı konaklamaları", "Toplu oda blokları ve isim listesi yönetimi",
         "Grup transferleri (minibüs, otobüs, VIP)", "Kurumsal anlaşmalar ve düzenli konaklama planları"] if T else
        ["Hosting delegations", "Sports and football team stays", "Room blocks and rooming list management",
         "Group transfers (minibus, coach, VIP)", "Corporate agreements and recurring stay plans"],
        [{"icon": "group", "t": "Heyet ve delegasyonlar" if T else "Delegations", "d": "Resmî ve kurumsal ziyaretler için konaklama ve ulaşım planı." if T else "Accommodation and transport for official and corporate visits."},
         {"icon": "group", "t": "Spor takımları" if T else "Sports teams", "d": "Kamp ve maç programına uygun otel ve transfer organizasyonu." if T else "Hotels and transfers fitted to training and match schedules."},
         {"icon": "handshake", "t": "Kurumsal anlaşmalar" if T else "Corporate agreements", "d": "Düzenli konaklama ihtiyacı olan kurumlar için uzun vadeli çalışma modeli." if T else "A long-term model for organisations with recurring needs."},
         {"icon": "ops", "t": "Danışmanlık ve planlama" if T else "Consulting and planning", "d": "Seyahat ve konaklama süreçlerinizi sadeleştirmek için planlama desteği." if T else "Planning support to simplify your travel and accommodation processes."}],
        [("Tek muhatap", "Tüm grup operasyonu için tek iletişim noktası."),
         ("Esnek planlama", "Program değişikliklerine hızlı uyum."),
         ("7/24 destek", "Grup konaklaması boyunca operasyon takibi.")] if T else
        [("One contact", "A single point of contact for the whole group."),
         ("Flexible planning", "Quick adjustments to programme changes."),
         ("24/7 support", "Operational follow-up throughout the stay.")],
        "Grubunuz için teklif alın" if T else "Get a quote for your group",
        "Grup ve heyet konaklama organizasyonu" if T else "Group and delegation accommodation")


def build_about(lang):
    T = lang == "tr"
    title = "Hakkımızda | Atlantis Travel" if T else "About Us | Atlantis Travel"
    desc = ("Atlantis Travel; şirketler, sağlık kuruluşları ve gruplar için İstanbul'da otel konaklama, VIP transfer ve operasyon yönetimi sunan kurumsal çözüm ortağıdır." if T else
            "Atlantis Travel is a corporate partner providing hotel accommodation, VIP transfers and operations management in Istanbul for companies, healthcare providers and groups.")
    h = head(lang, "about", title, desc, [org_schema(lang)]) + header(lang, "about")
    h += page_hero(lang, "Hakkımızda" if T else "About us",
                   "Kurumların konaklama ve seyahat ihtiyaçlarında güvenilir iş ortağı" if T else "A reliable partner for organisations' accommodation and travel needs",
                   "Sağlık kuruluşlarının ve şirketlerin konaklama, transfer ve operasyon süreçlerini profesyonel biçimde yönetiyoruz." if T else
                   "We professionally manage accommodation, transfer and operations for healthcare providers and companies.",
                   "Hakkımızda" if T else "About")
    story = ("Atlantis Travel, sağlık sektörünün dinamik yapısını ve kurumsal ihtiyaçları anlayarak yola çıktı. Özel klinik ve hastane gruplarının hasta, hasta yakını ve personel konaklama süreçlerinde yaşadığı operasyonel zorlukları çözmek için kurulduk. Bugün şirketlere, kamu kurumlarına, gruplara ve fuar katılımcılarına da aynı anlayışla hizmet veriyoruz."
             if T else
             "Atlantis Travel was founded with a clear understanding of the healthcare sector and corporate needs. We set out to solve the operational challenges private clinics and hospital groups face in accommodating patients, companions and staff. Today we serve companies, public institutions, groups and trade fair participants with the same approach.")
    story2 = ("Her bütçeye uygun konaklama seçenekleri sunuyor, transfer organizasyonlarını yönetiyor ve operasyonel süreçleri kurumlarınız adına koordine ediyoruz. Hızlı, planlı ve sürdürülebilir hizmet anlayışımızla kurumların operasyon yükünü azaltıyoruz."
              if T else
              "We offer accommodation for every budget, manage transfers and coordinate operations on your behalf. Our fast, planned and sustainable approach reduces the operational load on organisations.")
    h += f"""<section class="section"><div class="wrap split">
<div class="reveal"><p class="eyebrow">{"Hikayemiz" if T else "Our story"}</p>
<h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{"Sağlık sektöründen doğan bir hizmet anlayışı" if T else "A service approach born in healthcare"}</h2>
<p class="lead" style="margin-bottom:16px">{e(story)}</p><p class="lead">{e(story2)}</p></div>
{panel("Değerlerimiz" if T else "Our values", "Nasıl çalışıyoruz" if T else "How we work",
       [("Misyonumuz", "Kurumlara bütçeye uygun, hızlı ve güvenilir konaklama çözümleri sunarak operasyonel süreçlerini kolaylaştırmak."),
        ("Değerlerimiz", "Güvenilirlik, şeffaflık, profesyonellik ve müşteri odaklı hizmet."),
        ("Ekibimiz", "Deneyimli seyahat ve konaklama uzmanlarından oluşan ekibimiz 7/24 hizmet verir."),
        ("Kalite odaklılık", "Her segmentten otel seçeneği ve özenle seçilen iş ortaklarıyla çalışırız.")] if T else
       [("Our mission", "To simplify organisations' operations with budget-aligned, fast and reliable accommodation solutions."),
        ("Our values", "Reliability, transparency, professionalism and customer focus."),
        ("Our team", "Experienced travel and accommodation specialists available 24/7."),
        ("Quality focus", "Hotels in every category and carefully selected partners.")])}
</div></section>
<section class="section white"><div class="wrap">
{section_head("Faaliyet alanlarımız" if T else "What we do", "Hizmet verdiğimiz alanlar" if T else "Our areas of service")}
{cards([
    {"icon": "hotel", "t": UI[lang]["nav"][0][1], "d": "İstanbul'da 200+ otelle kurumsal ve grup konaklamaları." if T else "Corporate and group stays through 200+ hotels in Istanbul.", "href": url("konaklama", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "car", "t": UI[lang]["nav"][1][1], "d": "IST ve SAW'dan VIP karşılama ve transfer." if T else "VIP meet & greet and transfers from IST and SAW.", "href": url("transfer", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "health", "t": UI[lang]["nav"][2][1], "d": "Özel hastane ve klinik organizasyonları." if T else "Logistics for private hospitals and clinics.", "href": url("saglik", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "ops", "t": "7/24 operasyon" if T else "24/7 operations", "d": "Konaklama süresince kesintisiz destek." if T else "Continuous support throughout every stay.", "href": url("contact", lang), "more": "İletişim" if T else "Contact"},
])}
</div></section>
"""
    h += cta_band(lang, "Kurumsal seyahat çözümleriniz için bizimle iletişime geçin" if T else "Contact us for your corporate travel solutions")
    h += footer(lang)
    return h


def build_teklif(lang):
    T = lang == "tr"
    title = "Teklif Al – Kurumsal Konaklama ve VIP Transfer | Atlantis Travel" if T else "Request a Quote – Corporate Accommodation & VIP Transfer | Atlantis Travel"
    desc = ("Kurumsal otel konaklama, VIP havalimanı transferi, sağlık turizmi ve grup organizasyonları için hızlı teklif formu." if T else
            "Quick quote form for corporate hotel accommodation, VIP airport transfers, medical tourism and group logistics.")
    h = head(lang, "teklif", title, desc) + header(lang, "teklif")
    h += page_hero(lang, "Teklif Al" if T else "Request a quote",
                   "Kurumunuza özel teklif alın" if T else "Get a quote tailored to your organisation",
                   "Talebinizi iletin; ekibimiz uygun otel ve transfer seçenekleriyle size dönüş yapsın." if T else
                   "Send your request and our team will reply with suitable hotel and transfer options.",
                   "Teklif Al" if T else "Request a quote", actions=False)
    h += form_section(lang, "Talep formu" if T else "Request form",
                      "Ne kadar ayrıntı paylaşırsanız teklifinizi o kadar hızlı hazırlarız. Dilerseniz aynı bilgileri tek tıkla WhatsApp'tan da gönderebilirsiniz." if T else
                      "The more detail you share, the faster we can prepare your quote. You can also send the same details via WhatsApp in one click.")
    h += footer(lang)
    return h


def build_contact(lang):
    T = lang == "tr"
    title = "İletişim | Atlantis Travel" if T else "Contact | Atlantis Travel"
    desc = ("Atlantis Travel ile iletişime geçin: info@atlantistraveltr.com, +90 507 397 87 94 (WhatsApp). Kurumsal konaklama ve VIP transfer için 7/24 destek." if T else
            "Contact Atlantis Travel: info@atlantistraveltr.com, +90 507 397 87 94 (WhatsApp). 24/7 support for corporate accommodation and VIP transfers.")
    h = head(lang, "contact", title, desc, [org_schema(lang)]) + header(lang, "contact")
    h += page_hero(lang, "İletişim" if T else "Contact", "Bize ulaşın" if T else "Get in touch",
                   "Kurumsal konaklama, VIP transfer ve fuar hizmetleri için 7/24 ulaşabilirsiniz." if T else
                   "Reach us 24/7 for corporate accommodation, VIP transfers and trade fair services.",
                   "İletişim" if T else "Contact", actions=False)
    h += f"""<section class="section"><div class="wrap split">
<div><ul class="contact-list">
<li>{icon("mail")}<div><small>{"E-posta" if T else "Email"}</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li>{icon("wa")}<div><small>WhatsApp</small><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE1}</a></div></li>
<li>{icon("phone")}<div><small>{"Telefon" if T else "Phone"}</small><a href="tel:{PHONE1_RAW}">{PHONE1}</a> · <a href="tel:{PHONE2_RAW}">{PHONE2}</a></div></li>
<li>{icon("pin")}<div><small>{"Konum" if T else "Location"}</small>{"İstanbul, Türkiye" if T else "Istanbul, Türkiye"}</div></li>
<li>{icon("ig")}<div><small>{"Sosyal medya" if T else "Social media"}</small><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a> · <a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></div></li>
</ul></div>
{panel("Hızlı yanıt" if T else "Fast response", "Nasıl ulaşmalısınız?" if T else "How to reach us",
       [("Teklif için", "Teklif formu en hızlı yoldur; tüm bilgiler ekibimize tek seferde ulaşır."),
        ("Acil durumlar için", "WhatsApp ve telefon hattımız 7/24 açıktır."),
        ("Kurumsal iş birlikleri için", "E-posta ile kurum adınız ve ihtiyacınızı iletebilirsiniz.")] if T else
       [("For quotes", "The quote form is fastest; all details reach our team at once."),
        ("For urgent matters", "Our WhatsApp and phone lines are open 24/7."),
        ("For partnerships", "Email us your organisation name and requirements.")])}
</div></section>
"""
    h += form_section(lang, "Bize mesaj gönderin" if T else "Send us a message",
                      "Sorularınızı yazın, en kısa sürede yanıtlayalım." if T else "Write to us and we will reply shortly.", "iletisim", "mesaj")
    h += footer(lang)
    return h


FAQ = {
    "tr": [
        ("Fiyat teklifi nasıl alınır?", "Teklif formunu doldurarak veya WhatsApp hattımızdan bize yazarak teklif alabilirsiniz. Misafir sayısı, tarih ve bölge bilgilerini paylaştığınızda size uygun seçenekleri sunarız."),
        ("İptal politikanız nedir?", "İptal koşulları rezervasyon tarihine ve otelin koşullarına göre değişir. Rezervasyon sırasında size özel iptal koşulları yazılı olarak bildirilir."),
        ("Transfer hizmetleri nasıl çalışır?", "İstanbul Havalimanı ve Sabiha Gökçen'de misafirlerinizi karşılar, otele, hastaneye veya fuar alanına ulaştırırız. Bireysel misafirler için Mercedes Vito; gruplar için minibüs veya otobüs planlanabilir."),
        ("Toplu rezervasyonlarda indirim var mı?", "Toplu ve düzenli rezervasyonlar için kurumsal fiyatlandırma sunuyoruz. Misafir sayısı ve konaklama süresine göre teklif hazırlanır."),
        ("Ödeme nasıl yapılır?", "Ödeme yöntemi ve koşulları rezervasyon sırasında kurumunuzla birlikte netleştirilir ve yazılı olarak iletilir."),
        ("Acil durumlarda nasıl ulaşabilirim?", "7/24 telefon ve WhatsApp hattımızdan her zaman bize ulaşabilirsiniz."),
        ("Fuar konaklama hizmetiniz nedir?", "TÜYAP Beylikdüzü ve İstanbul Fuar Merkezi'ne gelen katılımcılar için fuar alanlarına yakın konaklama ve transfer organize ediyoruz. Fuar takvimine göre erken planlama yapılmasını öneririz."),
        ("Uçak bileti veya vize hizmeti veriyor musunuz?", "Hayır. Hizmetlerimiz İstanbul'da otel konaklama, transfer ve operasyon organizasyonu ile sınırlıdır."),
    ],
    "en": [
        ("How do I get a quote?", "Fill in the quote form or message us on WhatsApp. Share the number of guests, dates and area, and we will send suitable options."),
        ("What is your cancellation policy?", "Cancellation terms depend on the booking date and the hotel's conditions. The terms that apply to you are confirmed in writing at the time of booking."),
        ("How do transfers work?", "We meet your guests at Istanbul Airport or Sabiha Gökçen and take them to the hotel, hospital or expo centre. Mercedes Vito for individuals; minibuses or coaches for groups."),
        ("Do you offer group discounts?", "We offer corporate pricing for group and recurring bookings, quoted according to the number of guests and length of stay."),
        ("How is payment made?", "Payment method and terms are agreed with your organisation at the time of booking and confirmed in writing."),
        ("How can I reach you in an emergency?", "Our phone and WhatsApp lines are available 24/7."),
        ("What is your trade fair accommodation service?", "We arrange accommodation and transfers near TÜYAP Beylikdüzü and Istanbul Expo Center for fair participants. We recommend planning early according to the fair calendar."),
        ("Do you provide flight tickets or visa services?", "No. Our services cover hotel accommodation, transfers and operations in Istanbul."),
    ],
}


def build_sss(lang):
    T = lang == "tr"
    title = "Sıkça Sorulan Sorular | Atlantis Travel" if T else "Frequently Asked Questions | Atlantis Travel"
    desc = ("Teklif, iptal, transfer, toplu rezervasyon, ödeme ve fuar konaklaması hakkında sık sorulan sorular." if T else
            "Answers about quotes, cancellations, transfers, group bookings, payment and trade fair accommodation.")
    schema = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]}]
    h = head(lang, "sss", title, desc, schema) + header(lang, "sss")
    h += page_hero(lang, "SSS" if T else "FAQ", "Sıkça sorulan sorular" if T else "Frequently asked questions",
                   "Aradığınız yanıtı bulamazsanız bize 7/24 ulaşabilirsiniz." if T else "If you can't find your answer, reach us 24/7.",
                   "SSS" if T else "FAQ", actions=False)
    h += f'<section class="section"><div class="wrap">{faq_html(FAQ[lang])}</div></section>'
    h += cta_band(lang, "Sorunuzun cevabını bulamadınız mı?" if T else "Didn't find your answer?")
    h += footer(lang)
    return h


def build_privacy(lang):
    T = lang == "tr"
    title = "Gizlilik, KVKK ve Çerez Politikası | Atlantis Travel" if T else "Privacy and Cookie Policy | Atlantis Travel"
    desc = "Kişisel verilerin işlenmesine ilişkin aydınlatma metni ve çerez politikası." if T else "Privacy notice and cookie policy."
    h = head(lang, "privacy", title, desc) + header(lang, "privacy")
    h += page_hero(lang, "Yasal" if T else "Legal", "Gizlilik, KVKK ve Çerez Politikası" if T else "Privacy and Cookie Policy",
                   "Kişisel verilerinizi yalnızca talebinize yanıt vermek için işleriz." if T else "We process your personal data only to respond to your request.",
                   "Gizlilik" if T else "Privacy", actions=False)
    if T:
        body = f"""<h2>Veri sorumlusu</h2><p>Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) kapsamında Atlantis Travel tarafından hazırlanmıştır. İletişim: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>İşlenen veriler</h2><p>Teklif, fuar ve iletişim formlarında paylaştığınız ad soyad, şirket/kurum adı, e-posta, telefon, talep edilen hizmet, tarih, kişi ve oda sayısı ile açıklama alanına yazdığınız bilgiler. Formlarda kimlik numarası, pasaport bilgisi veya sağlık verisi istenmez; lütfen bu tür bilgileri paylaşmayın.</p>
<h2>İşleme amacı ve hukuki sebep</h2><p>Veriler; talebinize yanıt vermek, teklif hazırlamak ve rezervasyon sürecini yürütmek amacıyla, KVKK m.5/2-c (sözleşmenin kurulması) ve m.5/2-f (meşru menfaat) hukuki sebeplerine dayanarak işlenir.</p>
<h2>Saklama ve aktarım</h2><p>Form verileri web sitesinde veritabanına kaydedilmez; yalnızca şirket e-posta adresimize iletilir. E-posta yazışmaları talebin gerektirdiği süre ve yasal saklama süreleri boyunca tutulur. Rezervasyon için gerekli bilgiler yalnızca ilgili otel ve transfer hizmeti sağlayıcılarıyla paylaşılır.</p>
<h2>Haklarınız</h2><p>KVKK m.11 kapsamında verilerinize erişme, düzeltilmesini veya silinmesini isteme ve işlemeye itiraz etme haklarına sahipsiniz. Taleplerinizi <a href="mailto:{EMAIL}">{EMAIL}</a> adresine iletebilirsiniz.</p>
<h2>Çerezler</h2><p>Site, çalışması için gerekli olan tercih kaydını (çerez onayınız) tarayıcınızda saklar. Google Analytics yalnızca çerez bildiriminde "Kabul et" seçeneğini işaretlemeniz halinde yüklenir ve ziyaret istatistikleri için kullanılır. Tercihinizi altbilgideki "Çerez tercihleri" bağlantısından değiştirebilirsiniz.</p>
<h2>Güvenlik</h2><p>Site HTTPS ile sunulur; formlar kötüye kullanıma karşı korunur ve IP adresiniz saklanmaz (yalnızca kötüye kullanım sınırı için geçici, geri döndürülemez bir özet kullanılır).</p>"""
    else:
        body = f"""<h2>Data controller</h2><p>This notice is provided by Atlantis Travel under Turkish Personal Data Protection Law No. 6698 (KVKK). Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Data we process</h2><p>The details you enter in our quote, trade fair and contact forms: name, company, email, phone, service requested, dates, number of guests and rooms, and your message. We do not ask for ID numbers, passport details or health data; please do not share them.</p>
<h2>Purpose and legal basis</h2><p>We process this data to respond to your request, prepare a quote and handle bookings, on the basis of contract formation and legitimate interest (KVKK Art. 5/2-c and 5/2-f).</p>
<h2>Storage and sharing</h2><p>Form data is not stored in a website database; it is sent only to our company email address. Correspondence is kept as long as the request requires and as required by law. Booking details are shared only with the relevant hotels and transfer providers.</p>
<h2>Your rights</h2><p>You may request access to, correction or deletion of your data, or object to its processing, by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Cookies</h2><p>The site stores your cookie choice in your browser. Google Analytics is loaded only if you select "Accept" in the cookie notice. You can change your choice via "Cookie settings" in the footer.</p>
<h2>Security</h2><p>The site is served over HTTPS; forms are protected against abuse and your IP address is not stored (only a temporary, irreversible hash is used for rate limiting).</p>"""
    h += f'<section class="section"><div class="wrap prose">{body}<p style="margin-top:28px"><em>{"Son güncelleme" if T else "Last updated"}: 06.11.2026</em></p></div></section>'
    h += footer(lang)
    return h


def build_terms(lang):
    T = lang == "tr"
    title = "Kullanım Şartları | Atlantis Travel" if T else "Terms of Use | Atlantis Travel"
    desc = "Atlantis Travel web sitesi kullanım şartları." if T else "Atlantis Travel website terms of use."
    h = head(lang, "terms", title, desc) + header(lang, "terms")
    h += page_hero(lang, "Yasal" if T else "Legal", "Kullanım Şartları" if T else "Terms of Use", "", "Kullanım Şartları" if T else "Terms", actions=False)
    if T:
        body = """<h2>Sitenin amacı</h2><p>Bu web sitesi Atlantis Travel'ın hizmetleri hakkında bilgi vermek ve teklif taleplerini almak amacıyla yayınlanmaktadır. Sitedeki bilgiler genel niteliktedir; fiyat, müsaitlik ve koşullar her talep için ayrıca yazılı olarak bildirilir.</p>
<h2>Teklif ve rezervasyon</h2><p>Form üzerinden gönderilen talepler rezervasyon anlamına gelmez. Rezervasyon, tarafınıza iletilen teklifin yazılı olarak onaylanmasıyla kesinleşir; iptal ve değişiklik koşulları teklif ile birlikte bildirilir.</p>
<h2>Hizmet kapsamı</h2><p>Atlantis Travel; İstanbul'da otel konaklama, transfer ve operasyon organizasyonu hizmeti verir. Uçak bileti, vize ve yurt dışı otel rezervasyonu hizmeti sunulmaz. Sağlık turizmi kapsamında tıbbi işlem, teşhis veya tedavi hizmeti verilmez.</p>
<h2>Fikrî haklar</h2><p>Atlantis Travel adı, logosu ve sitedeki içerikler izinsiz kopyalanamaz ve kullanılamaz.</p>
<h2>Dış bağlantılar</h2><p>Sitede yer alan WhatsApp ve sosyal medya bağlantıları ilgili platformların kendi koşullarına tabidir.</p>"""
    else:
        body = """<h2>Purpose of the site</h2><p>This website provides information about Atlantis Travel's services and collects quote requests. Information on the site is general; prices, availability and terms are confirmed separately in writing for each request.</p>
<h2>Quotes and bookings</h2><p>A request sent through a form is not a booking. A booking is confirmed when you approve the written quote we send; cancellation and change terms are stated with the quote.</p>
<h2>Scope of service</h2><p>Atlantis Travel provides hotel accommodation, transfer and operations services in Istanbul. We do not provide flight ticketing, visa services or hotel bookings abroad, and we do not provide medical procedures, diagnosis or treatment.</p>
<h2>Intellectual property</h2><p>The Atlantis Travel name, logo and site content may not be copied or used without permission.</p>
<h2>External links</h2><p>WhatsApp and social media links are subject to those platforms' own terms.</p>"""
    h += f'<section class="section"><div class="wrap prose">{body}</div></section>'
    h += footer(lang)
    return h


def build_thanks(lang):
    T = lang == "tr"
    h = head(lang, "thanks", "Teşekkürler | Atlantis Travel" if T else "Thank you | Atlantis Travel",
             "Talebiniz alındı." if T else "Your request has been received.") + header(lang, "thanks")
    h += page_hero(lang, "Teşekkürler" if T else "Thank you", "Talebiniz alındı" if T else "Your request has been received",
                   "Ekibimiz en kısa sürede size dönüş yapacak. Acil durumlar için WhatsApp hattımız 7/24 açıktır." if T else
                   "Our team will get back to you shortly. For urgent matters, our WhatsApp line is open 24/7.",
                   "Teşekkürler" if T else "Thank you")
    h += footer(lang)
    return h


def build_404():
    h = head("tr", "home", "Sayfa bulunamadı | Atlantis Travel", "Aradığınız sayfa bulunamadı.").replace(
        '<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    h += header("tr", "")
    h += f"""<section class="page-hero on-navy"><div class="wrap">
<p class="eyebrow">404</p><h1>Sayfa bulunamadı · Page not found</h1>
<p class="lead">Aradığınız sayfa taşınmış veya kaldırılmış olabilir. The page may have been moved or removed.</p>
<div class="actions"><a class="btn btn-gold" href="/">Ana Sayfa</a><a class="btn btn-line" href="/en/">Home (EN)</a></div>
</div></section>
"""
    h += footer("tr")
    return h


BUILDERS = {
    "home": build_home, "konaklama": build_konaklama, "transfer": build_transfer, "saglik": build_saglik,
    "fuar": build_fuar, "cozumler": build_cozumler, "about": build_about, "teklif": build_teklif,
    "contact": build_contact, "sss": build_sss, "privacy": build_privacy, "terms": build_terms, "thanks": build_thanks,
    "referans": build_referans,
}

PRIORITY = {"home": "1.0", "konaklama": "0.9", "transfer": "0.9", "saglik": "0.9", "fuar": "0.8", "cozumler": "0.8",
            "teklif": "0.8", "about": "0.6", "contact": "0.7", "sss": "0.5", "privacy": "0.2", "terms": "0.2", "referans": "0.6"}


def main():
    count = 0
    for key, fn in BUILDERS.items():
        for lang in ("tr", "en"):
            path = out_file(url(key, lang))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(fn(lang))
            count += 1
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(build_404())
    today = date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in BUILDERS:
        if key in NOINDEX:
            continue
        for lang in ("tr", "en"):
            sm.append(f"<url><loc>{SITE}{url(key, lang)}</loc><lastmod>{today}</lastmod><priority>{PRIORITY[key]}</priority>"
                      f'<xhtml:link rel="alternate" hreflang="tr" href="{SITE}{url(key, "tr")}"/>'
                      f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{url(key, "en")}"/></url>')
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sm) + "\n")
    print(f"{count} sayfa + 404 + sitemap.xml oluşturuldu.")


if __name__ == "__main__":
    main()
