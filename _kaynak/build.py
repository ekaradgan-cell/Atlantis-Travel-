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
VERSION = "20261107b"

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
<link rel="icon" type="image/jpeg" sizes="96x96" href="/assets/img/amblem-96.jpg">
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
<strong>{GRATING[lang]}</strong>
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
             [("clock", "24/7 Support"), ("pin", "Hotels near hospitals and exhibition centers"),
              ("car", "Transfer organization"), ("tag", "Corporate pricing")])
    fl = "".join(f'<li>{icon(i)}<span>{e(t)}</span></li>' for i, t in feats)
    h += f"""<section class="hero2">
<picture class="bg"><source srcset="/assets/img/hero-lobby.webp" type="image/webp"><img src="/assets/img/hero-lobby.jpg" width="1024" height="1024" alt="" fetchpriority="high"></picture>
<div class="wrap">
<p class="pill">{"Sağlık kurumları için kurumsal seyahat" if T else "Corporate travel for healthcare institutions"}</p>
<h1>{"Kurumsal Konaklama ve Operasyonel Seyahat Çözümleri" if T else "Corporate Accommodation and Travel Operations for Healthcare Institutions"}</h1>
<p class="lead">{"Profesyonel operasyon yönetimi ile bütçeye uygun, hızlı ve sürdürülebilir hizmet" if T else "Professional operation management with budget-friendly, fast and sustainable service"}</p>
<div class="actions"><a class="btn btn-gold" href="#teklif">{"Hemen Teklif Al" if T else "Get a Quote Now"}</a>
<a class="btn btn-outline" href="https://wa.me/{WA}" target="_blank" rel="noopener">{"WhatsApp ile Yazın" if T else "Contact via WhatsApp"}</a></div>
<ul class="hero-feats">{fl}</ul>
<a class="scroll" href="#kimler" aria-label="{"Aşağı kaydır" if T else "Scroll down"}">{icon("chev")}</a>
</div></section>
"""
    who = ([("steth", "Hastaneler ve Klinikler", "Hasta yakını ve sağlık personeli konaklaması"),
            ("globe", "Sağlık Turizmi Firmaları", "Yurt dışından gelen hastalar için konaklama ve transfer"),
            ("building", "Fuar Katılımcıları", "İstanbul fuarları için fuar alanına yakın toplu konaklama"),
            ("briefcase", "Kurumsal Şirketler", "İş seyahati ve ekip konaklaması")] if T else
           [("steth", "Hospitals and Clinics", "Accommodation for patient relatives and healthcare staff"),
            ("globe", "Health Tourism Companies", "Accommodation and transfer services for international patients"),
            ("building", "Exhibition Participants", "Group accommodation near exhibition centers in Istanbul"),
            ("briefcase", "Corporate Companies", "Business travel and team accommodation")])
    whoh = "".join(f'<article class="who reveal"><span class="gi">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in who)
    svc = ([("svc-konaklama", "hotel", "Yurt İçi Konaklama", "Talep edilen bölgelerde her segmentten otel seçeneği ve bütçeye uygun fiyat alternatifleri ile kaliteli konaklama hizmeti sunuyoruz.", "konaklama"),
            ("svc-transfer", "car", "Transfer Organizasyonu", "Profesyonel transfer hizmetleri ile hastalarınızın ve personellerinizin güvenli ve konforlu ulaşımını sağlıyoruz.", "transfer"),
            ("svc-operasyon", "ops", "Operasyonel Süreç Yönetimi", "Tüm operasyonel süreçleri profesyonel bir anlayışla yöneterek sağlık kurumlarınızın operasyonel yükünü azaltıyoruz.", "saglik"),
            ("svc-grup", "group", "Grup ve Futbol Takımı Konaklamaları", "Spor kulüpleri ve büyük gruplar için özel konaklama paketleri sunuyoruz. Futbol takımları, spor organizasyonları ve kurumsal gruplar için uygun fiyatlı, konforlu ve organize konaklama çözümleri sağlıyoruz.", "cozumler")] if T else
           [("svc-konaklama", "hotel", "Domestic Accommodation", "We provide quality accommodation services with hotel options from all segments and budget-friendly price alternatives in the requested regions.", "konaklama"),
            ("svc-transfer", "car", "Transfer Organization", "We ensure safe and comfortable transportation for your patients and staff with professional transfer services.", "transfer"),
            ("svc-operasyon", "ops", "Operational Process Management", "We reduce the operational burden of your healthcare institutions by managing all operational processes with a professional approach.", "saglik"),
            ("svc-grup", "group", "Group and Football Team Accommodations", "We offer special accommodation packages for sports clubs and large groups. We provide affordable, comfortable, and organized accommodation solutions for football teams, sports organizations, and corporate groups.", "cozumler")])
    svch = "".join(f'<a class="svc reveal" href="{url(k, lang)}">{pic(img, t)}<div class="b"><span class="si">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div></a>' for img, i, t, d, k in svc)
    stp = ([("Talebinizi İletin", "Form, telefon veya WhatsApp üzerinden ihtiyaçlarınızı paylaşın."),
            ("Size Özel Teklif", "Tarih, konum ve bütçenize uygun otel ve transfer seçeneklerini hazırlayalım."),
            ("Organizasyon Bizde", "Konaklama ve transferiniz planlandığı gibi yürütülsün, 7/24 yanınızdayız.")] if T else
           [("Submit Your Request", "Share your needs via form, phone, or WhatsApp."),
            ("Customized Proposal", "We'll prepare hotel and transfer options tailored to your dates, location, and budget."),
            ("We Handle Everything", "Your accommodation and transfers are executed as planned, we're here for you 24/7.")])
    stph = "".join(f'<li class="reveal"><span class="num">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(stp))
    why = ([("Güvenilir İş Ortaklığı", "Sağlık sektörüne özel çözümlerimizle uzun vadeli iş ortaklıkları kuruyoruz."),
            ("Her Segmentten Otel Seçeneği", "Geniş otel ağımız sayesinde her bütçeye uygun kaliteli konaklama alternatifleri sunuyoruz."),
            ("Bütçeye Uygun Fiyatlar", "Anlaşmalı otellerimiz ile en uygun fiyat garantisi ve şeffaf fiyatlandırma politikası")] if T else
           [("Reliable Partnership", "We establish long-term partnerships with our healthcare sector-specific solutions"),
            ("Hotel Options from All Segments", "Thanks to our extensive hotel network, we offer quality accommodation alternatives suitable for every budget"),
            ("Budget-Friendly Prices", "Best price guarantee and transparent pricing policy with our contracted hotels")])
    whyh = "".join(f'<li>{icon("check")}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for t, d in why)
    h += f"""<section class="section" id="kimler"><div class="wrap">
<h2 class="center-h">{"Kimlere Hizmet Veriyoruz?" if T else "Who We Serve?"}</h2>
<div class="who-grid">{whoh}</div>
</div></section>
<section class="section pt0"><div class="wrap">
<h2 class="center-h">{"Hizmetlerimiz" if T else "Our Services"}</h2>
<p class="center-p">{"Sağlık kurumlarınız için kapsamlı konaklama ve seyahat çözümleri" if T else "Comprehensive accommodation and travel solutions for your healthcare institutions"}</p>
<div class="svc-grid">{svch}</div>
</div></section>
<section class="section pt0"><div class="wrap">
<h2 class="center-h">{"Nasıl Çalışır?" if T else "How It Works?"}</h2>
<ol class="steps3">{stph}</ol>
</div></section>
<section class="why"><div class="wrap">
<div><h2>{"Neden Atlantis Travel?" if T else "Why Atlantis Travel?"}</h2>
<p class="sub">{"Güvenilir iş ortaklığı modeliyle hızlı, planlı ve sürdürülebilir hizmet" if T else "Fast, planned, and sustainable service with a reliable partnership model"}</p>
<span class="rule"></span><ul class="why-list">{whyh}</ul></div>
<div class="why-img">{pic("is-ortakligi", "Kurumsal iş ortaklığı" if T else "Business partnership")}</div>
</div></section>
<section class="section"><div class="wrap">{reviews_block(lang)}</div></section>
"""
    h += quick_form(lang)
    h += f"""<section class="consult"><div class="wrap">
<h2>{"Kurumsal Seyahat Çözümleriniz İçin Bizimle İletişime Geçin" if T else "Contact Us for Your Corporate Travel Solutions"}</h2>
<p>{"Operasyonel verimliliğinizi artırın, maliyetlerinizi optimize edin. Profesyonel ekibimiz size özel çözümler sunmak için hazır." if T else "Increase your operational efficiency, optimize your costs. Our professional team is ready to offer you customized solutions."}</p>
<a class="btn btn-gold" href="{url("contact", lang)}">{"Ücretsiz Danışmanlık Alın" if T else "Get Free Consultation"}</a>
</div></section>
"""
    h += footer(lang)
    return h


def quick_form(lang):
    T = lang == "tr"
    return f"""<section class="section qf" id="teklif"><div class="wrap">
<h2 class="center-h">{"Hızlı Teklif Alın" if T else "Get a Quick Quote"}</h2>
<p class="center-p">{"Bilgilerinizi paylaşın, size en uygun konaklama teklifini hemen gönderelim" if T else "Share your information and we'll send you the best accommodation proposal right away"}</p>
<div class="qf-card"><div class="qf-head">{"Teklif Formu" if T else "Quote Form"}</div>
{qform(lang, "teklif")}<p class="qf-note">{"Bilgileriniz yalnızca teklif hazırlamak için kullanılır." if T else "Your information is only used to prepare your quote."} <a href="{url("privacy", lang)}">{"Gizlilik Politikası" if T else "Privacy Policy"}</a></p></div>
</div></section>
"""


def build_referans(lang):
    T = lang == "tr"
    title = "Referanslarımız | Atlantis Travel" if T else "References | Atlantis Travel"
    desc = ("Atlantis Travel hakkında Google yorumları ve birlikte çalıştığımız kurum türleri." if T else
            "Google reviews about Atlantis Travel and the types of organisations we work with.")
    h = head(lang, "referans", title, desc, [org_schema(lang)]) + header(lang, "referans")
    h += page_hero(lang, "Güvenilir İş Ortaklığı" if T else "Trusted Business Partnership", "Referanslarımız" if T else "Our References",
                   "Sağlık kurumları ve kurumsal firmalarla yürüttüğümüz başarılı iş birlikleri" if T else
                   "Successful collaborations with healthcare institutions and corporate companies",
                   "Referanslar" if T else "References")
    stars = "".join(icon("star") for _ in range(5))
    allrev = "".join(f'<figure class="review reveal"><div class="stars">{stars}</div><blockquote>“{e(t)}”</blockquote><figcaption>{e(nm)}</figcaption></figure>' for nm, t in REVIEWS)
    kinds = (["Özel Sağlık Kurumları", "Hastane Zincirleri", "Klinik Grupları", "Medikal Merkezler", "Sağlık Turizmi Firmaları", "Kurumsal Şirketler"] if T else
             ["Private Healthcare Institutions", "Hospital Chains", "Clinic Groups", "Medical Centers", "Health Tourism Companies", "Corporate Companies"])
    kh = "".join(f'<li>{icon("check")}{e(k)}</li>' for k in kinds)
    h += f"""<section class="section"><div class="wrap">
<h2 class="center-h">{"Google'da Müşterilerimiz Ne Diyor?" if T else "What Do Our Customers Say on Google?"}</h2>
<p class="center-p rating-line"><strong>{GRATING[lang]}</strong></p>
<div class="reviews">{allrev}</div>
<div class="center-actions"><a class="btn btn-gold" href="{GREVIEW}" target="_blank" rel="noopener">{"Google'da tüm yorumları gör" if T else "View all reviews on Google"}</a>
<a class="btn btn-ghost" href="{GREVIEW}" target="_blank" rel="noopener">{"Siz de yorum bırakın" if T else "Leave a review"}</a></div>
</div></section>
<section class="section white"><div class="wrap">
<h2 class="center-h">{"İş Ortaklarımız" if T else "Our Business Partners"}</h2>
<p class="center-p">{"Güvenilir kurumsal çözümler sunduğumuz sağlık kurumları ve firmalar" if T else "Healthcare institutions and companies to which we provide reliable corporate solutions"}</p>
<ul class="kinds">{kh}</ul>
</div></section>
<section class="consult"><div class="wrap">
<h2>{"Siz de İş Ortağımız Olun" if T else "Become Our Business Partner"}</h2>
<p>{"Kurumsal konaklama ve seyahat ihtiyaçlarınız için güvenilir çözümler sunuyoruz." if T else "We offer reliable solutions for your corporate accommodation and travel needs."}</p>
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



# ===================================================== Promake içerik eşitlemesi (07.11.2026)
GRATING = {"tr": "Google'da 5,0 puan · 10 yorum", "en": "5.0 rating on Google · 10 reviews"}


def consult(title, text, btn, href):
    return f"""<section class="consult"><div class="wrap">
<h2>{e(title)}</h2>
<p>{e(text)}</p>
<a class="btn btn-gold" href="{href}">{e(btn)}</a>
</div></section>
"""


def service_schema(lang, key, name, area=None):
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "provider": {"@type": "TravelAgency", "name": "Atlantis Travel", "url": SITE + "/"},
            "areaServed": area or {"@type": "City", "name": "İstanbul"},
            "url": SITE + url(key, lang)}


def img_grid(rows, cls):
    return (f'<div class="svc-grid {cls}">' + "".join(
        f'<div class="svc reveal">{pic(img, t)}<div class="b"><h3>{e(t)}</h3><p>{e(d)}</p></div></div>'
        for img, t, d in rows) + "</div>")


# ----------------------------------------------------------------- Hizmetlerimiz (/services)
SVC = {
    "tr": {
        "title": "Hizmetlerimiz – Kurumsal Konaklama, Transfer ve Operasyon | Atlantis Travel",
        "desc": "Sağlık kurumlarına özel konaklama, transfer organizasyonu ve operasyonel seyahat yönetimi hizmetleri. Türkiye genelinde güvenilir ve profesyonel çözümler.",
        "badge": "Kurumsal Çözümler",
        "h1": "Kurumsal Konaklama ve Operasyonel Seyahat Çözümleri",
        "sub": "Profesyonel operasyon yönetimi ile bütçeye uygun, hızlı ve sürdürülebilir hizmet",
        "crumb": "Hizmetlerimiz",
        "svc_h": "Hizmetlerimiz",
        "svc_d": "Sağlık kurumlarının konaklama ve seyahat ihtiyaçlarına yönelik kapsamlı çözümler sunuyoruz. Her aşamada profesyonel destek ve güvenilir hizmet anlayışıyla yanınızdayız.",
        "svc": [
            ("hotel", "Yurt İçi Konaklama", "Türkiye'nin her bölgesinde, her segmentten otel seçenekleri ile hasta ve hasta yakınlarınız için konforlu konaklama çözümleri.",
             ["Her bütçeye uygun otel alternatifleri", "Hastanelere yakın lokasyonlar", "Özel anlaşmalı fiyatlar", "7/24 rezervasyon desteği"]),
            ("car", "Transfer Organizasyonu", "Havalimanı, hastane ve otel transferleri için güvenli, konforlu ve zamanında ulaşım hizmetleri.",
             ["VIP araç seçenekleri", "Deneyimli profesyonel şoförler", "Uçuş takip sistemi", "Engelli dostu araçlar"]),
            ("ops", "Operasyonel Süreç Yönetimi", "Rezervasyondan check-out'a kadar tüm süreçlerin profesyonel yönetimi ile kurumunuzun operasyonel yükünü azaltıyoruz.",
             ["Merkezi rezervasyon sistemi", "Anlık raporlama ve takip", "Fatura ve ödeme yönetimi", "Özel müşteri temsilcisi"]),
            ("handshake", "Kurumsal Anlaşmalar", "Sağlık kurumlarına özel hazırlanmış, uzun vadeli iş ortaklığı modelleri ve avantajlı fiyatlandırma.",
             ["Yıllık kontrat avantajları", "Esnek ödeme koşulları", "Özel indirim paketleri", "Öncelikli hizmet garantisi"]),
            ("pin", "Bölgesel Çözümler", "Türkiye'nin tüm bölgelerinde geniş otel ağımız ve yerel partnerlerimizle kesintisiz hizmet.",
             ["Türkiye genelinde hizmet ağı", "Bölgesel özel fiyatlandırma", "Yerel destek ekipleri", "Alternatif konaklama seçenekleri"]),
            ("briefcase", "Danışmanlık Hizmetleri", "Seyahat ve konaklama süreçlerinizi optimize etmek için profesyonel danışmanlık ve planlama desteği.",
             ["Maliyet optimizasyonu", "Süreç iyileştirme önerileri", "Performans raporları", "Stratejik planlama desteği"]),
        ],
        "gal_h": "Hizmet Galerisi",
        "gal_d": "Sunduğumuz konaklama seçenekleri ve transfer araçlarından örnekler. Her segmentten kaliteli hizmet anlayışımızı keşfedin.",
        "hot_t": "Otel Seçeneklerimiz",
        "hotels": [("seg-ekonomik", "Ekonomik Segment", "Temiz, konforlu ve bütçe dostu konaklama seçenekleri"),
                   ("seg-orta", "Orta Segment", "Kalite ve konforun buluştuğu modern otel odaları"),
                   ("seg-luks", "Lüks Segment", "Prestijli ve üst düzey konfor sunan premium konaklama")],
        "veh_t": "Transfer Araçlarımız",
        "vehicles": [("arac-sedan", "VIP Sedan", "Bireysel ve küçük grup transferleri için lüks araçlar"),
                     ("arac-minibus", "Minibüs", "Orta büyüklükte gruplar için konforlu transfer"),
                     ("arac-otobus", "Otobüs", "Büyük grup transferleri için modern ve geniş araçlar")],
        "hl_t": "Hizmet Öne Çıkanları",
        "highlights": [("havalimani-karsilama", "Havalimanı Karşılama", "Profesyonel karşılama hizmeti ile misafirleriniz güvende"),
                       ("otel-resepsiyon", "Otel Resepsiyon", "Modern ve konforlu otel lobilerinde sorunsuz check-in")],
        "reg_b": "Türkiye Geneli Hizmet",
        "reg_h": "Hizmet Bölgelerimiz",
        "reg_d": "Türkiye'nin 7 bölgesinde geniş anlaşmalı otel ağımızla kesintisiz hizmet sunuyoruz.",
        "regions": ["Marmara Bölgesi", "Ege Bölgesi", "Akdeniz Bölgesi", "İç Anadolu Bölgesi", "Karadeniz Bölgesi",
                    "Doğu Anadolu Bölgesi", "Güneydoğu Anadolu Bölgesi"],
        "why_h": "Neden Atlantis Travel?",
        "why_d": "Sağlık sektörüne özel çözümlerimiz ve deneyimimizle kurumunuzun güvenilir iş ortağıyız.",
        "why": [("Sektörel Uzmanlık", "Sağlık kurumlarının özel ihtiyaçlarını anlayan deneyimli ekibimizle 7/24 yanınızdayız."),
                ("Geniş Otel Ağı", "Türkiye genelinde geniş anlaşmalı otel ağımız ile her bütçeye uygun seçenekler sunuyoruz."),
                ("Hızlı ve Güvenilir", "Acil durumlar dahil tüm rezervasyonlarınızı hızlı ve güvenilir şekilde gerçekleştiriyoruz."),
                ("Şeffaf Fiyatlandırma", "Gizli maliyet yok, net ve rekabetçi fiyatlarla bütçenizi kontrol altında tutun."),
                ("Teknolojik Altyapı", "Modern rezervasyon sistemi ve raporlama araçlarıyla tüm süreçleri kolayca takip edin.")],
        "grp_e": "Heyetler, gruplar ve takımlar",
        "grp_h": "Kalabalık gruplar, tek plan",
        "grp_p": "Grup büyüklüğüne, programa ve bütçeye göre otel bloğu, transfer araçları ve günlük operasyonu birlikte planlıyoruz. Spor kulüpleri ve büyük gruplar için uygun fiyatlı, konforlu ve organize konaklama çözümleri sunuyoruz.",
        "grp_l": ["Heyet ve delegasyon ağırlama", "Spor ve futbol takımı konaklamaları", "Toplu oda blokları ve isim listesi yönetimi",
                  "Grup transferleri (minibüs, otobüs, VIP)", "Kurumsal anlaşmalar ve düzenli konaklama planları"],
        "grp_pe": "Grup operasyonu", "grp_ph": "Tek muhatap, 7/24 takip",
        "grp_pi": [("Tek muhatap", "Tüm grup operasyonu için tek iletişim noktası."),
                   ("Esnek planlama", "Program değişikliklerine hızlı uyum."),
                   ("7/24 destek", "Grup konaklaması boyunca operasyon takibi.")],
        "cta_h": "Kurumsal Seyahat Çözümleriniz İçin Bizimle İletişime Geçin",
        "cta_d": "Sağlık kurumunuza özel çözümler ve avantajlı fiyatlar için ücretsiz danışmanlık alın.",
        "cta_b": "Ücretsiz Teklif Alın",
    },
    "en": {
        "title": "Our Services – Corporate Accommodation, Transfers & Operations | Atlantis Travel",
        "desc": "Accommodation, transfer organization and operational travel management for healthcare institutions. Reliable, professional solutions throughout Türkiye.",
        "badge": "Corporate Solutions",
        "h1": "Corporate Accommodation and Operational Travel Solutions",
        "sub": "Professional operation management with budget-friendly, fast and sustainable service",
        "crumb": "Our Services",
        "svc_h": "Our Services",
        "svc_d": "We offer comprehensive solutions for the accommodation and travel needs of healthcare institutions. We are with you at every stage with professional support and reliable service approach.",
        "svc": [
            ("hotel", "Domestic Accommodation", "Comfortable accommodation solutions for patients and their relatives with hotel options from every segment in all regions of Türkiye.",
             ["Hotel alternatives for every budget", "Locations close to hospitals", "Special contracted prices", "24/7 reservation support"]),
            ("car", "Transfer Organization", "Safe, comfortable and timely transportation services for airport, hospital and hotel transfers.",
             ["VIP vehicle options", "Experienced professional drivers", "Flight tracking system", "Disabled-friendly vehicles"]),
            ("ops", "Operational Process Management", "We reduce your institution's operational burden with professional management of all processes from reservation to check-out.",
             ["Central reservation system", "Real-time reporting and tracking", "Invoice and payment management", "Dedicated customer representative"]),
            ("handshake", "Corporate Agreements", "Long-term business partnership models and advantageous pricing specially prepared for healthcare institutions.",
             ["Annual contract advantages", "Flexible payment terms", "Special discount packages", "Priority service guarantee"]),
            ("pin", "Regional Solutions", "Uninterrupted service with our wide hotel network and local partners in all regions of Türkiye.",
             ["Service network across Türkiye", "Regional special pricing", "Local support teams", "Alternative accommodation options"]),
            ("briefcase", "Consulting Services", "Professional consulting and planning support to optimize your travel and accommodation processes.",
             ["Cost optimization", "Process improvement suggestions", "Performance reports", "Strategic planning support"]),
        ],
        "gal_h": "Service Gallery",
        "gal_d": "Examples of our accommodation options and transfer vehicles. Discover our quality service approach from every segment.",
        "hot_t": "Our Hotel Options",
        "hotels": [("seg-ekonomik", "Economy Segment", "Clean, comfortable and budget-friendly accommodation options"),
                   ("seg-orta", "Mid-Range Segment", "Modern hotel rooms where quality and comfort meet"),
                   ("seg-luks", "Luxury Segment", "Prestigious and premium accommodation offering superior comfort")],
        "veh_t": "Our Transfer Vehicles",
        "vehicles": [("arac-sedan", "VIP Sedan", "Luxury vehicles for individual and small group transfers"),
                     ("arac-minibus", "Minibus", "Comfortable transfer for medium-sized groups"),
                     ("arac-otobus", "Bus", "Modern and spacious vehicles for large group transfers")],
        "hl_t": "Service Highlights",
        "highlights": [("havalimani-karsilama", "Airport Welcome", "Your guests are safe with professional welcome service"),
                       ("otel-resepsiyon", "Hotel Reception", "Smooth check-in at modern and comfortable hotel lobbies")],
        "reg_b": "Nationwide Service",
        "reg_h": "Our Service Regions",
        "reg_d": "We provide uninterrupted service with our extensive contracted hotel network across all 7 regions of Türkiye.",
        "regions": ["Marmara Region", "Aegean Region", "Mediterranean Region", "Central Anatolia Region", "Black Sea Region",
                    "Eastern Anatolia Region", "Southeastern Anatolia Region"],
        "why_h": "Why Atlantis Travel?",
        "why_d": "We are your institution's reliable business partner with our healthcare sector-specific solutions and experience.",
        "why": [("Sectoral Expertise", "We are with you 24/7 with our experienced team that understands the special needs of healthcare institutions."),
                ("Wide Hotel Network", "We offer options for every budget with our extensive contracted hotel network throughout Türkiye."),
                ("Fast and Reliable", "We carry out all your reservations quickly and reliably, including emergency situations."),
                ("Transparent Pricing", "No hidden costs, keep your budget under control with clear and competitive prices."),
                ("Technological Infrastructure", "Easily track all processes with modern reservation system and reporting tools.")],
        "grp_e": "Delegations, groups and teams",
        "grp_h": "Large groups, one plan",
        "grp_p": "We plan hotel room blocks, transfer vehicles and daily operations together, based on group size, schedule and budget, with comfortable, organised and cost-effective options for sports clubs and large groups.",
        "grp_l": ["Hosting delegations", "Sports and football team stays", "Room blocks and rooming list management",
                  "Group transfers (minibus, coach, VIP)", "Corporate agreements and recurring stay plans"],
        "grp_pe": "Group operations", "grp_ph": "One contact, 24/7 follow-up",
        "grp_pi": [("One contact", "A single point of contact for the whole group."),
                   ("Flexible planning", "Quick adjustments to programme changes."),
                   ("24/7 support", "Operational follow-up throughout the stay.")],
        "cta_h": "Contact Us for Your Corporate Travel Solutions",
        "cta_d": "Get free consultation for solutions tailored to your healthcare institution and advantageous prices.",
        "cta_b": "Get Free Quote",
    },
}


def build_cozumler(lang):
    S = SVC[lang]
    schema = [org_schema(lang), service_schema(lang, "cozumler", S["h1"], {"@type": "Country", "name": "Türkiye"})]
    h = head(lang, "cozumler", S["title"], S["desc"], schema) + header(lang, "cozumler")
    h += page_hero(lang, S["badge"], S["h1"], S["sub"], S["crumb"])
    items = [{"icon": ic, "t": t, "d": d, "list": l} for ic, t, d, l in S["svc"]]
    regs = "".join(f'<li>{icon("pin")}{e(r)}</li>' for r in S["regions"])
    h += f"""<section class="section"><div class="wrap">
{section_head(S["badge"], S["svc_h"], S["svc_d"])}
{cards(items)}
</div></section>
<section class="section white"><div class="wrap">
<h2 class="center-h">{e(S["gal_h"])}</h2>
<p class="center-p">{e(S["gal_d"])}</p>
<h3 class="gal-h">{e(S["hot_t"])}</h3>
{img_grid(S["hotels"], "g3")}
<h3 class="gal-h">{e(S["veh_t"])}</h3>
{img_grid(S["vehicles"], "g3")}
<h3 class="gal-h">{e(S["hl_t"])}</h3>
{img_grid(S["highlights"], "g2")}
</div></section>
<section class="section"><div class="wrap">
<p class="eyebrow center-e">{e(S["reg_b"])}</p>
<h2 class="center-h">{e(S["reg_h"])}</h2>
<p class="center-p">{e(S["reg_d"])}</p>
<ul class="kinds regions">{regs}</ul>
</div></section>
<section class="section white"><div class="wrap">
{section_head("Atlantis Travel", S["why_h"], S["why_d"])}
{cards([{"icon": "check", "t": t, "d": d} for t, d in S["why"]])}
</div></section>
<section class="section"><div class="wrap split">
<div class="reveal"><p class="eyebrow">{e(S["grp_e"])}</p>
<h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{e(S["grp_h"])}</h2>
<p class="lead" style="margin-bottom:24px">{e(S["grp_p"])}</p>
{checks(S["grp_l"])}</div>
{panel(S["grp_pe"], S["grp_ph"], S["grp_pi"])}
</div></section>
"""
    h += consult(S["cta_h"], S["cta_d"], S["cta_b"], url("teklif", lang))
    h += footer(lang)
    return h


# ----------------------------------------------------------------- Kurumsal Konaklama
KK = {
    "tr": {
        "title": "Kurumsal Otel Konaklama İstanbul | Atlantis Travel",
        "desc": "Şirketler, kamu kurumları, klinikler ve gruplar için İstanbul'da 200+ otelle kurumsal konaklama. Bütçeye uygun seçenekler, planlı rezervasyon ve 7/24 operasyon desteği.",
        "badge": "Sağlık Kurumları İçin Özel Çözümler",
        "h1": "Kurumsal Konaklama ve Seyahat Yönetimi",
        "sub": "Özel klinik ve hastane grupları için profesyonel operasyon yönetimi ile bütçeye uygun, hızlı ve sürdürülebilir hizmet",
        "crumb": "Kurumsal Konaklama",
        "adv_h": "Neden Atlantis Travel?",
        "adv_s": "Sağlık kurumlarının operasyonel yükünü azaltarak güvenilir iş ortaklığı sunuyoruz",
        "adv": [("handshake", "Güvenilir İş Ortaklığı", "Sağlık sektörüne özel çözümlerimizle uzun vadeli iş ortaklıkları kuruyoruz"),
                ("hotel", "Her Segmentten Otel Seçeneği", "Geniş anlaşmalı otel ağı ile her bütçeye uygun kaliteli konaklama alternatifleri"),
                ("tag", "Bütçeye Uygun Fiyatlar", "Anlaşmalı otellerimiz ile en uygun fiyat garantisi ve şeffaf fiyatlandırma"),
                ("clock", "Hızlı ve Planlı Hizmet", "Profesyonel ekibimiz ile hızlı rezervasyon ve operasyonel süreç yönetimi")],
        "svc_h": "Hizmet Kapsamımız",
        "svc_s": "Kapsamlı konaklama ve seyahat çözümleri",
        "svc": [("hotel", "Yurt İçi Konaklama", "Talep edilen bölgelerde her segmentten otel seçeneği ve bütçeye uygun fiyat alternatifleri ile kaliteli konaklama hizmeti sunuyoruz."),
                ("car", "Transfer Organizasyonu", "Profesyonel transfer hizmetleri ile hastalarınızın ve personellerinizin güvenli ve konforlu ulaşımını sağlıyoruz."),
                ("ops", "Operasyonel Süreç Yönetimi", "Tüm operasyonel süreçleri profesyonel bir anlayışla yöneterek sağlık kurumlarınızın operasyonel yükünü azaltıyoruz.")],
        "int_e": "İstanbul ve Türkiye geneli",
        "int_h": "Her segmentten otel, tek muhatap",
        "int_p": "İstanbul'da 200'den fazla otelle çalışıyoruz. Talep edilen bölgede ekonomik, orta ve üst segment seçenekleri sunar; rezervasyondan çıkışa kadar tüm süreci kurumunuz adına yönetiriz. İstanbul dışındaki şehirler için de talep üzerine konaklama organize ediyoruz.",
        "int_l": ["Talep edilen bölgede her bütçeye uygun otel alternatifleri", "Hastanelere, ofislere ve fuar alanlarına yakın konumlar",
                  "Bireysel, ekip ve grup rezervasyonları", "Kurumsal faturalandırma ve tek noktadan takip", "Transfer ile birlikte planlama"],
        "int_pe": "Kurumlara özel", "int_ph": "Tek muhatap, 7/24 takip",
        "int_pi": [("Kurumlara özel çalışma modeli", "Uzun vadeli iş ortaklığı ve düzenli konaklama ihtiyaçları için planlı süreç."),
                   ("Hızlı ve planlı hizmet", "Acil talepler dahil rezervasyonlarınızı hızla organize ederiz."),
                   ("7/24 destek", "Konaklama boyunca ulaşabileceğiniz operasyon ekibi.")],
        "proc_h": "Çalışma Sürecimiz",
        "proc_s": "Basit ve şeffaf 4 adımda kurumsal konaklama çözümünüz hazır",
        "steps": [("Teklif Talebi", "İhtiyaçlarınızı, tarih aralığını, bölge ve bütçe bilgilerinizi bizimle paylaşın"),
                  ("Özel Teklif Hazırlama", "24 saat içinde size özel otel seçenekleri ve fiyat teklifini sunuyoruz"),
                  ("Onay ve Rezervasyon", "Seçtiğiniz oteller için anında rezervasyon yapıyor, onay belgelerini iletiyoruz"),
                  ("Operasyon Yönetimi", "Check-in'den check-out'a kadar tüm süreci takip ediyor, raporluyoruz")],
        "pr_h": "Fiyat Avantajları",
        "pr_s": "Kurumsal anlaşmalarımız sayesinde önemli tasarruf sağlayın",
        "pr_head": ("Özellik", "Bireysel", "Kurumsal"),
        "pr_rows": [("Otel Seçenekleri", "Sınırlı", "Geniş Otel Ağı"),
                    ("Fiyat Avantajı", "Liste Fiyatı", "Anlaşmalı Fiyat"),
                    ("Transfer Hizmeti", "Ekstra Ücret", "Paket İçinde"),
                    ("Operasyonel Destek", "Yok", "7/24 Destek"),
                    ("Fatura ve Raporlama", "Manuel", "Otomatik Sistem")],
        "ref_h": "Referanslarımız",
        "ref_s": "Türkiye'nin önde gelen sağlık kurumlarına hizmet veriyoruz",
        "ref_d": "Referans listesi ve detaylı bilgi için bizimle iletişime geçin.",
        "ref_b": "Referansları Görüntüle",
        "cta_h": "Kurumunuz İçin Özel Teklif Alın",
        "cta_s": "Operasyonel yükünüzü azaltın, maliyetlerinizi optimize edin. Size özel çözümümüzü hemen öğrenin.",
        "cta_b": "Ücretsiz Teklif Talep Edin",
        "schema": "Kurumsal otel konaklama",
    },
    "en": {
        "title": "Corporate Hotel Accommodation in Istanbul | Atlantis Travel",
        "desc": "Corporate accommodation in Istanbul through 200+ hotels for companies, public institutions, clinics and groups. Budget-aligned options and 24/7 support.",
        "badge": "Special Solutions for Healthcare Institutions",
        "h1": "Corporate Accommodation and Travel Management",
        "sub": "Budget-friendly, fast and sustainable service with professional operations management for private clinic and hospital groups",
        "crumb": "Corporate Accommodation",
        "adv_h": "Why Atlantis Travel?",
        "adv_s": "We offer a reliable partnership that reduces the operational burden of healthcare institutions",
        "adv": [("handshake", "Reliable Partnership", "We establish long-term partnerships with our healthcare-specific solutions"),
                ("hotel", "Hotels from Every Segment", "Quality accommodation alternatives for every budget with extensive contracted hotel network"),
                ("tag", "Budget-Friendly Prices", "Best price guarantee and transparent pricing with our contracted hotels"),
                ("clock", "Fast and Planned Service", "Quick reservations and operational process management with our professional team")],
        "svc_h": "Our Service Scope",
        "svc_s": "Comprehensive accommodation and travel solutions",
        "svc": [("hotel", "Domestic Accommodation", "We offer quality accommodation services with hotel options from every segment and budget-friendly price alternatives in requested regions."),
                ("car", "Transfer Organization", "We ensure safe and comfortable transportation for your patients and staff with professional transfer services."),
                ("ops", "Operational Process Management", "We reduce the operational burden of your healthcare institutions by managing all operational processes with a professional approach.")],
        "int_e": "Istanbul and across Türkiye",
        "int_h": "Every hotel category, one contact",
        "int_p": "We work with more than 200 hotels in Istanbul. We offer economy, mid-range and upscale options in the area you need and manage the whole process on your behalf. Stays in other Turkish cities can be arranged on request.",
        "int_l": ["Hotel options for every budget in the area you need", "Locations close to hospitals, offices and expo centres",
                  "Individual, team and group bookings", "Corporate invoicing and single-point follow-up", "Planned together with transfers"],
        "int_pe": "Built for organisations", "int_ph": "One contact, 24/7 follow-up",
        "int_pi": [("A model built for organisations", "Planned processes for long-term partnerships and recurring stays."),
                   ("Fast, organised service", "We arrange bookings quickly, including urgent requests."),
                   ("24/7 support", "An operations team you can reach throughout the stay.")],
        "proc_h": "Our Working Process",
        "proc_s": "Your corporate accommodation solution in 4 simple and transparent steps",
        "steps": [("Quote Request", "Share your needs, date range, region and budget with us"),
                  ("Tailored Quote", "We present hotel options and a price quote tailored to you within 24 hours"),
                  ("Approval and Reservation", "We book your chosen hotels immediately and send the confirmations"),
                  ("Operations Management", "We follow and report the whole process from check-in to check-out")],
        "pr_h": "Price Advantages",
        "pr_s": "Achieve significant savings through our corporate agreements",
        "pr_head": ("Feature", "Individual", "Corporate"),
        "pr_rows": [("Hotel Options", "Limited", "Extensive Hotel Network"),
                    ("Price Advantage", "List Price", "Contracted Price"),
                    ("Transfer Service", "Extra Fee", "Included in Package"),
                    ("Operational Support", "None", "24/7 Support"),
                    ("Invoicing and Reporting", "Manual", "Automated System")],
        "ref_h": "Our References",
        "ref_s": "We serve Türkiye's leading healthcare institutions",
        "ref_d": "Contact us for reference list and detailed information.",
        "ref_b": "View References",
        "cta_h": "Get a Custom Quote for Your Institution",
        "cta_s": "Reduce your operational burden and optimise your costs. Find out about our tailored solution now.",
        "cta_b": "Request a Free Quote",
        "schema": "Corporate hotel accommodation",
    },
}


def build_konaklama(lang):
    K = KK[lang]
    schema = [org_schema(lang), service_schema(lang, "konaklama", K["schema"])]
    h = head(lang, "konaklama", K["title"], K["desc"], schema) + header(lang, "konaklama")
    h += page_hero(lang, K["badge"], K["h1"], K["sub"], K["crumb"])
    hd, rows = K["pr_head"], K["pr_rows"]
    table = ('<div class="cmp-wrap reveal"><table class="cmp"><thead><tr>' + "".join(f"<th scope=\"col\">{e(x)}</th>" for x in hd)
             + "</tr></thead><tbody>" + "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in rows)
             + "</tbody></table></div>")
    h += f"""<section class="section white"><div class="wrap">
{section_head("Atlantis Travel", K["adv_h"], K["adv_s"])}
{cards([{"icon": i, "t": t, "d": d} for i, t, d in K["adv"]])}
</div></section>
<section class="section"><div class="wrap">
{section_head(K["crumb"], K["svc_h"], K["svc_s"])}
{cards([{"icon": i, "t": t, "d": d} for i, t, d in K["svc"]])}
</div></section>
<section class="section white"><div class="wrap split">
<div class="reveal"><p class="eyebrow">{e(K["int_e"])}</p>
<h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{e(K["int_h"])}</h2>
<p class="lead" style="margin-bottom:24px">{e(K["int_p"])}</p>
{checks(K["int_l"])}</div>
{panel(K["int_pe"], K["int_ph"], K["int_pi"])}
</div></section>
<section class="section"><div class="wrap">
{section_head(K["crumb"], K["proc_h"], K["proc_s"])}
{steps(K["steps"])}
</div></section>
<section class="section white"><div class="wrap">
{section_head(K["crumb"], K["pr_h"], K["pr_s"])}
{table}
</div></section>
<section class="section"><div class="wrap">
<h2 class="center-h">{e(K["ref_h"])}</h2>
<p class="center-p">{e(K["ref_s"])}</p>
<p class="center-p">{e(K["ref_d"])}</p>
<div class="center-actions"><a class="btn btn-gold" href="{url("referans", lang)}">{e(K["ref_b"])}</a></div>
</div></section>
"""
    h += consult(K["cta_h"], K["cta_s"], K["cta_b"], url("teklif", lang))
    h += footer(lang)
    return h


# ----------------------------------------------------------------- Fuar Konaklama
FAIR = {
    "tr": {
        "title": "Fuar Konaklama İstanbul – TÜYAP ve İFM | Atlantis Travel",
        "desc": "Beylikdüzü (TÜYAP) ve İstanbul Fuar Merkezi (İFM) için özel konaklama paketleri. Fuar alanlarına yakın, her bütçeye uygun otel seçenekleri ve transfer hizmetleri.",
        "eyebrow": "Fuar Konaklama",
        "h1": "Fuar Konaklama Çözümleri",
        "sub": "Beylikdüzü Fuar Merkezi ve İstanbul Fuar Merkezi (İFM) için özel konaklama hizmetleri",
        "crumb": "Fuar Konaklama",
        "int_h": "Uluslararası Fuar Katılımcıları İçin Özel Çözümler",
        "int_p": "Yurt dışından İstanbul'daki fuarlara gelen katılımcı ve ziyaretçi firmalar için fuar alanlarına yakın konumda, her bütçeye uygun konaklama seçeneklerimizle hizmetinizdeyiz.",
        "int_l": ["Fuar alanlarına yakın konumda oteller", "Ekonomik, orta ve üst segment seçenekler", "Havalimanı karşılama ve günlük fuar transferi",
                  "Toplu rezervasyonlarda kurumsal fiyatlandırma", "Türkçe ve İngilizce destek"],
        "ben_h": "Neden Atlantis Travel?",
        "ben": [("Fuar Deneyimi", "Yıllardır uluslararası fuar katılımcılarına hizmet veren deneyimli ekibimiz"),
                ("Geniş Otel Ağı", "Her segmentten 100+ otel seçeneği ile esnek rezervasyon imkanı"),
                ("Rekabetçi Fiyatlar", "Toplu rezervasyon avantajlarımızla bütçenize uygun en iyi fiyatlar"),
                ("Tek Noktadan Hizmet", "Konaklama, transfer ve tüm organizasyon ihtiyaçlarınız için tek muhatap")],
        "fc_h": "Hizmet Verdiğimiz Fuar Merkezleri",
        "fc": [("Beylikdüzü Fuar Merkezi", "Avrupa yakasının en büyük fuar merkezi olan Beylikdüzü Fuar Merkezi'ne yakın konumda, ekonomik ve lüks segment otel seçenekleri sunuyoruz.",
                ["Fuar alanına 5-15 dakika mesafede oteller", "Ekonomik, orta ve lüks segment seçenekler", "Günlük fuar transfer hizmeti", "Grup rezervasyonlarında özel indirimler"]),
               ("İstanbul Fuar Merkezi (İFM)", "Yeşilköy'de bulunan İstanbul Fuar Merkezi için havalimanına ve fuar alanına yakın stratejik konumlarda konaklama çözümleri sağlıyoruz.",
                ["Havalimanına 10-20 dakika mesafede", "Fuar alanına yürüme mesafesinde oteller", "7/24 havalimanı transfer hizmeti", "Çok dilli destek ekibi"])],
        "sv_h": "Fuar Konaklama Hizmetlerimiz",
        "sv": [("hotel", "Her Bütçeye Uygun Konaklama", "Ekonomik otellerden 5 yıldızlı lüks konaklama seçeneklerine kadar geniş portföyümüzle her bütçeye uygun çözümler sunuyoruz."),
               ("pin", "Stratejik Konum Avantajı", "Fuar alanlarına yakın konumdaki otellerimizle zaman ve ulaşım maliyetlerinden tasarruf edin."),
               ("car", "Fuar Transfer Organizasyonu", "Havalimanı karşılama, otel-fuar arası günlük transferler ve özel araç hizmetleri ile tam destek."),
               ("clock", "Profesyonel Destek", "Rezervasyondan check-out'a kadar tüm süreçte Türkçe, İngilizce ve diğer dillerde 7/24 destek.")],
        "form_h": "Rezervasyon Talebi Oluşturun",
        "form_d": "Fuar konaklama ihtiyaçlarınız için formu doldurun, en kısa sürede size özel teklifimizi gönderelim.",
        "submit": "Rezervasyon Talebi Gönder",
        "cta": "Fuar Konaklamanız İçin Hemen Teklif Alın",
        "schema": "Fuar konaklama",
    },
    "en": {
        "title": "Trade Fair Accommodation Istanbul – TÜYAP & IFM | Atlantis Travel",
        "desc": "Special accommodation packages for Beylikdüzü (TÜYAP) and Istanbul Fair Center (IFM). Hotels close to the venues for every budget, with transfer services.",
        "eyebrow": "Trade fair accommodation",
        "h1": "Fair Accommodation Solutions",
        "sub": "Special accommodation services for Beylikdüzü Fair Center and Istanbul Fair Center (IFM)",
        "crumb": "Trade Fair Accommodation",
        "int_h": "Special Solutions for International Fair Participants",
        "int_p": "We are at your service with accommodation options close to fair venues and suitable for every budget for participating and visiting companies coming from abroad to fairs in Istanbul.",
        "int_l": ["Hotels close to the venues", "Economy, mid-range and upscale options", "Airport pick-ups and daily expo transfers",
                  "Corporate pricing for group bookings", "Turkish and English support"],
        "ben_h": "Why Atlantis Travel?",
        "ben": [("Fair Experience", "Our experienced team that has been serving international fair participants for years"),
                ("Wide Hotel Network", "Flexible reservation opportunity with 100+ hotel options from every segment"),
                ("Competitive Prices", "Best prices suitable for your budget with our bulk reservation advantages"),
                ("One-Stop Service", "Single point of contact for accommodation, transfer and all your organizational needs")],
        "fc_h": "Fair Centers We Serve",
        "fc": [("Beylikdüzü Fair Center", "We offer economical and luxury segment hotel options close to Beylikdüzü Fair Center, the largest fair center on the European side.",
                ["Hotels 5-15 minutes away from the fair area", "Economical, mid-range and luxury segment options", "Daily fair transfer service", "Special discounts for group reservations"]),
               ("Istanbul Fair Center (IFM)", "We provide accommodation solutions in strategic locations close to the airport and fair area for Istanbul Fair Center located in Yeşilköy.",
                ["10-20 minutes away from the airport", "Hotels within walking distance to the fair area", "24/7 airport transfer service", "Multilingual support team"])],
        "sv_h": "Our Fair Accommodation Services",
        "sv": [("hotel", "Accommodation for Every Budget", "We offer solutions suitable for every budget with our wide portfolio from economical hotels to 5-star luxury accommodation options."),
               ("pin", "Strategic Location Advantage", "Save on time and transportation costs with our hotels close to fair venues."),
               ("car", "Fair Transfer Organization", "Full support with airport pickup, daily hotel-fair transfers and private vehicle services."),
               ("clock", "Professional Support", "24/7 support in Turkish, English and other languages throughout the entire process from reservation to check-out.")],
        "form_h": "Create a Reservation Request",
        "form_d": "Fill out the form for your fair accommodation needs, and we'll send you our special offer as soon as possible.",
        "submit": "Send Reservation Request",
        "cta": "Get a Quote for Your Fair Accommodation Now",
        "schema": "Trade fair accommodation",
    },
}


def build_fuar(lang):
    F = FAIR[lang]
    schema = [org_schema(lang), service_schema(lang, "fuar", F["schema"])]
    h = head(lang, "fuar", F["title"], F["desc"], schema) + header(lang, "fuar")
    h += page_hero(lang, F["eyebrow"], F["h1"], F["sub"], F["crumb"])
    fc = [{"icon": "fair", "t": t, "d": d, "list": l} for t, d, l in F["fc"]]
    h += f"""<section class="section"><div class="wrap split">
<div class="reveal"><h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{e(F["int_h"])}</h2>
<p class="lead" style="margin-bottom:24px">{e(F["int_p"])}</p>
{checks(F["int_l"])}</div>
{panel("Atlantis Travel", F["ben_h"], F["ben"])}
</div></section>
<section class="section white"><div class="wrap">
{section_head(F["crumb"], F["fc_h"])}
{cards(fc)}
</div></section>
<section class="section"><div class="wrap">
{section_head(F["crumb"], F["sv_h"])}
{cards([{"icon": i, "t": t, "d": d} for i, t, d in F["sv"]])}
</div></section>
"""
    form = form_section(lang, F["form_h"], F["form_d"], "fuar", "fuar-form")
    h += form.replace(">" + FL[lang]["send"] + "</button>", ">" + e(F["submit"]) + "</button>", 1)
    h += cta_band(lang, F["cta"])
    h += footer(lang)
    return h


# ----------------------------------------------------------------- Hakkımızda
ABOUT = {
    "tr": {
        "title": "Hakkımızda | Atlantis Travel",
        "desc": "Sağlık kurumlarına özel konaklama ve seyahat çözümleri sunan Atlantis Travel. Geniş anlaşmalı otel ağı ile güvenilir iş ortağınız.",
        "h1": "Hakkımızda",
        "sub": "Sağlık kurumlarının konaklama ve seyahat ihtiyaçlarına profesyonel çözümler sunan güvenilir iş ortağınız.",
        "story_h": "Hikayemiz",
        "p1": "Atlantis Travel, sağlık sektörünün dinamik yapısını ve kurumsal ihtiyaçları derinlemesine anlayarak yola çıktı. Özel klinik ve hastane gruplarının hasta, hasta yakını ve personel konaklama süreçlerinde yaşadığı operasyonel zorlukları çözmek için kurulduk. Bugün, Türkiye genelinde geniş otel ağımız ve profesyonel ekibimizle sağlık kurumlarının en güvenilir seyahat çözüm ortağıyız.",
        "p2": "Yılların deneyimi ve sektörel uzmanlığımızla, her bütçeye uygun konaklama seçenekleri sunuyor, transfer organizasyonlarını kusursuz yönetiyor ve tüm operasyonel süreçleri kurumlarınız adına koordine ediyoruz. Hızlı, planlı ve sürdürülebilir hizmet anlayışımızla sağlık kurumlarının operasyonel yükünü azaltıyor, hasta memnuniyetini artırıyoruz.",
        "pan_e": "Atlantis Travel", "pan_h": "Misyon ve değerlerimiz",
        "pan": [("Misyonumuz", "Sağlık kurumlarına bütçeye uygun, hızlı ve güvenilir konaklama çözümleri sunarak operasyonel süreçlerini kolaylaştırmak."),
                ("Değerlerimiz", "Güvenilirlik, şeffaflık, profesyonellik ve müşteri odaklı hizmet anlayışı temel değerlerimizdir."),
                ("Ekibimiz", "Deneyimli seyahat ve konaklama uzmanlarından oluşan ekibimiz, 7/24 kesintisiz hizmet sunmaktadır."),
                ("Kalite Odaklı", "Her segmentten otel seçeneği ve titizlikle seçilmiş iş ortaklarıyla en yüksek hizmet kalitesini garanti ediyoruz.")],
        "cta_h": "Kurumsal Seyahat Çözümleriniz İçin Bizimle İletişime Geçin",
        "cta_d": "Bütçenize uygun konaklama seçenekleri ve profesyonel operasyon yönetimi için ücretsiz danışmanlık alın.",
        "cta_b": "Ücretsiz Danışmanlık Alın",
    },
    "en": {
        "title": "About Us | Atlantis Travel",
        "desc": "Atlantis Travel provides specialized accommodation and travel solutions for healthcare institutions. Your trusted business partner with an extensive contracted hotel network.",
        "h1": "About Us",
        "sub": "Your trusted business partner providing professional solutions for the accommodation and travel needs of healthcare institutions.",
        "story_h": "Our Story",
        "p1": "Atlantis Travel was founded with a deep understanding of the dynamic nature of the healthcare sector and corporate needs. We were established to solve the operational challenges experienced by private clinics and hospital groups in the accommodation processes of patients, patient relatives, and staff. Today, we are the most trusted travel solution partner for healthcare institutions with our extensive hotel network throughout Türkiye and professional team.",
        "p2": "With years of experience and sectoral expertise, we offer accommodation options suitable for every budget, manage transfer organizations flawlessly, and coordinate all operational processes on behalf of your institutions. With our fast, planned, and sustainable service approach, we reduce the operational burden of healthcare institutions and increase patient satisfaction.",
        "pan_e": "Atlantis Travel", "pan_h": "Our mission and values",
        "pan": [("Our Mission", "To facilitate operational processes by providing budget-friendly, fast, and reliable accommodation solutions to healthcare institutions."),
                ("Our Values", "Reliability, transparency, professionalism, and customer-focused service approach are our core values."),
                ("Our Team", "Our team of experienced travel and accommodation specialists provides uninterrupted service 24/7."),
                ("Quality Focused", "We guarantee the highest service quality with hotel options from every segment and carefully selected business partners.")],
        "cta_h": "Contact Us for Your Corporate Travel Solutions",
        "cta_d": "Get free consultation for accommodation options suitable for your budget and professional operation management.",
        "cta_b": "Get Free Consultation",
    },
}


def build_about(lang):
    T = lang == "tr"
    A = ABOUT[lang]
    h = head(lang, "about", A["title"], A["desc"], [org_schema(lang)]) + header(lang, "about")
    h += page_hero(lang, "Atlantis Travel", A["h1"], A["sub"], A["h1"])
    h += f"""<section class="section"><div class="wrap split">
<div class="reveal"><p class="eyebrow">Atlantis Travel</p>
<h2 style="font-size:clamp(1.8rem,3vw,2.4rem);margin-bottom:18px">{e(A["story_h"])}</h2>
<p class="lead" style="margin-bottom:16px">{e(A["p1"])}</p><p class="lead">{e(A["p2"])}</p></div>
{panel(A["pan_e"], A["pan_h"], A["pan"])}
</div></section>
<section class="section white"><div class="wrap">
{section_head("Faaliyet alanlarımız" if T else "What we do", "Hizmet verdiğimiz alanlar" if T else "Our areas of service")}
{cards([
    {"icon": "hotel", "t": "Kurumsal Konaklama" if T else "Corporate Accommodation", "d": "İstanbul'da 200+ otelle kurumsal ve grup konaklamaları." if T else "Corporate and group stays through 200+ hotels in Istanbul.", "href": url("konaklama", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "car", "t": "VIP Transfer", "d": "IST ve SAW'dan VIP karşılama ve transfer." if T else "VIP meet & greet and transfers from IST and SAW.", "href": url("transfer", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "health", "t": "Sağlık Turizmi" if T else "Medical Tourism", "d": "Özel hastane ve klinik organizasyonları." if T else "Logistics for private hospitals and clinics.", "href": url("saglik", lang), "more": "Ayrıntılar" if T else "Learn more"},
    {"icon": "ops", "t": "7/24 operasyon" if T else "24/7 operations", "d": "Konaklama süresince kesintisiz destek." if T else "Continuous support throughout every stay.", "href": url("contact", lang), "more": "İletişim" if T else "Contact"},
])}
</div></section>
"""
    h += consult(A["cta_h"], A["cta_d"], A["cta_b"], url("contact", lang))
    h += footer(lang)
    return h


# ----------------------------------------------------------------- İletişim
def build_contact(lang):
    T = lang == "tr"
    title = "İletişim | Atlantis Travel" if T else "Contact | Atlantis Travel"
    desc = ("Atlantis Travel ile iletişime geçin. Kurumsal konaklama, transfer organizasyonu ve fuar hizmetleri için 7/24 destek. Ücretsiz danışmanlık ve teklif alın." if T else
            "Contact Atlantis Travel. 24/7 support for corporate accommodation, transfer organisation and trade fair services. Get free consultation and a quote.")
    h = head(lang, "contact", title, desc, [org_schema(lang)]) + header(lang, "contact")
    h += page_hero(lang, "Atlantis Travel", "İletişim" if T else "Contact Us", desc, "İletişim" if T else "Contact", actions=False)
    h += f"""<section class="section"><div class="wrap split">
<div><ul class="contact-list">
<li>{icon("mail")}<div><small>{"E-posta" if T else "Email"}</small><a href="mailto:{EMAIL}">{EMAIL}</a><span class="note">{"Genellikle 24 saat içinde yanıt veririz" if T else "We typically respond within 24 hours"}</span></div></li>
<li>{icon("wa")}<div><small>WhatsApp</small><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE1}</a></div></li>
<li>{icon("phone")}<div><small>{"Telefon" if T else "Phone"}</small><a href="tel:{PHONE1_RAW}">{PHONE1}</a> · <a href="tel:{PHONE2_RAW}">{PHONE2}</a></div></li>
<li>{icon("pin")}<div><small>{"Adres" if T else "Address"}</small>{"İstanbul, Türkiye" if T else "Istanbul, Türkiye"}</div></li>
<li>{icon("ig")}<div><small>{"Bizi Takip Edin" if T else "Follow Us"}</small><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a> · <a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></div></li>
</ul>
<div class="support-box"><h3>{"Desteğe İhtiyacınız mı Var?" if T else "Need Support?"}</h3>
<p>{"Teknik destek veya sipariş sorularınız için özel destek ekibimizle iletişime geçin:" if T else "For technical support or general inquiries, contact our dedicated support team:"}</p>
<p><strong>{"Destek E-postası" if T else "Support Email"}:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div>
{panel("Hızlı yanıt" if T else "Fast response", "Nasıl ulaşmalısınız?" if T else "How to reach us",
       [("Teklif için", "Teklif formu en hızlı yoldur; tüm bilgiler ekibimize tek seferde ulaşır."),
        ("Acil durumlar için", "WhatsApp ve telefon hattımız 7/24 açıktır."),
        ("Kurumsal iş birlikleri için", "E-posta ile kurum adınız ve ihtiyacınızı iletebilirsiniz.")] if T else
       [("For quotes", "The quote form is fastest; all details reach our team at once."),
        ("For urgent matters", "Our WhatsApp and phone lines are open 24/7."),
        ("For partnerships", "Email us your organisation name and requirements.")])}
</div></section>
"""
    h += form_section(lang, "Bize Mesaj Gönderin" if T else "Send us a Message",
                      "Sorularınızı yazın, en kısa sürede yanıtlayalım." if T else "Write to us and we will reply shortly.", "iletisim", "mesaj")
    h += footer(lang)
    return h


# ----------------------------------------------------------------- SSS
FAQ = {
    "tr": [
        ("Fiyat teklifleri nasıl alınır?", "İletişim sayfamızdan veya WhatsApp hattımızdan bizimle iletişime geçerek detaylı fiyat teklifi alabilirsiniz. Misafir sayısı, tarih ve bölge bilgilerini paylaştığınızda en uygun fiyatları size sunuyoruz."),
        ("İptal politikanız nedir?", "İptal koşulları otel ve tarihe göre değişir, teklifinizde ayrıca belirtilir."),
        ("Transfer hizmetleri nasıl çalışır?", "Havalimanı, otogar veya istasyon karşılama hizmetleri sunuyoruz. Profesyonel sürücülerimiz ve konforlu araçlarımızla misafirlerinizin güvenli transferini sağlıyoruz. Grup büyüklüğüne göre sedan, minibüs veya otobüs seçenekleri mevcuttur."),
        ("Toplu rezervasyonlarda indirim var mı?", "Evet, toplu rezervasyonlarda özel indirimler sunuyoruz. Misafir sayısı ve konaklama süresine göre avantajlı fiyatlar için bizimle iletişime geçebilirsiniz."),
        ("Ödeme nasıl yapılır?", "Ödeme koşulları, teklifimizle birlikte size özel olarak bildirilir."),
        ("Acil durumlarda nasıl ulaşabilirim?", "7/24 destek hattımız ve WhatsApp iletişim hattımız üzerinden her zaman bize ulaşabilirsiniz. Acil durumlarda anında çözüm üretiyoruz."),
        ("Fuar konaklama hizmetiniz nedir?", "Fuar dönemlerinde yoğun talep gören bölgelerde özel konaklama paketleri sunuyoruz. Fuar takvimini takip ederek erken rezervasyon avantajları sağlıyoruz."),
        ("Uçak bileti veya vize hizmeti veriyor musunuz?", "Hayır. Hizmetlerimiz İstanbul'da otel konaklama, transfer ve operasyon organizasyonu ile sınırlıdır."),
    ],
    "en": [
        ("How do I get price quotes?", "You can get a detailed price quote by contacting us through our contact page or WhatsApp line. When you share the number of guests, date, and region information, we offer you the most suitable prices."),
        ("What is your cancellation policy?", "Cancellation conditions vary depending on the hotel and date, and are specified separately in your quote."),
        ("How do transfer services work?", "We offer airport, bus station, or train station pickup services. We ensure safe transfer of your guests with our professional drivers and comfortable vehicles. Sedan, minibus, or bus options are available depending on group size."),
        ("Are there discounts for group reservations?", "Yes, we offer special discounts for group reservations. You can contact us for advantageous prices based on the number of guests and accommodation duration."),
        ("How is payment made?", "Payment terms are communicated to you specifically with our quote."),
        ("How can I reach you in emergencies?", "You can always reach us through our 24/7 support line and WhatsApp communication line. We provide immediate solutions in emergency situations."),
        ("What is your fair accommodation service?", "We offer special accommodation packages in regions with high demand during fair periods. We provide early reservation advantages by following the fair calendar."),
        ("Do you provide flight tickets or visa services?", "No. Our services cover hotel accommodation, transfers and operations in Istanbul."),
    ],
}


def build_sss(lang):
    T = lang == "tr"
    title = "Sıkça Sorulan Sorular | Atlantis Travel" if T else "Frequently Asked Questions | Atlantis Travel"
    desc = ("Kurumsal konaklama, transfer organizasyonu ve fuar hizmetleri hakkında merak ettikleriniz. Atlantis Travel ile ilgili tüm sorularınızın cevapları burada." if T else
            "Everything you wonder about corporate accommodation, transfer organization, and fair services. Answers to all your questions about Atlantis Travel are here.")
    schema = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]}]
    h = head(lang, "sss", title, desc, schema) + header(lang, "sss")
    h += page_hero(lang, "SSS" if T else "FAQ", "Sıkça Sorulan Sorular" if T else "Frequently Asked Questions", desc,
                   "SSS" if T else "FAQ", actions=False)
    h += f'<section class="section"><div class="wrap">{faq_html(FAQ[lang])}</div></section>\n'
    h += consult("Sorunuzun cevabını bulamadınız mı?" if T else "Couldn't find the answer to your question?",
                 "Bizimle iletişime geçin, size yardımcı olmaktan mutluluk duyarız" if T else "Contact us, we'll be happy to help you",
                 "İletişime Geçin" if T else "Contact Us", url("contact", lang))
    h += footer(lang)
    return h


# ----------------------------------------------------------------- Gizlilik
def build_privacy(lang):
    T = lang == "tr"
    title = "Gizlilik Politikası ve KVKK Aydınlatma Metni | Atlantis Travel" if T else "Privacy Policy and Personal Data Protection Notice (KVKK) | Atlantis Travel"
    desc = "Kişisel verilerin işlenmesine ilişkin aydınlatma metni ve çerez politikası." if T else "Privacy notice and cookie policy."
    h = head(lang, "privacy", title, desc) + header(lang, "privacy")
    h += page_hero(lang, "Yasal" if T else "Legal",
                   "Gizlilik Politikası ve KVKK Aydınlatma Metni" if T else "Privacy Policy and Personal Data Protection Notice (KVKK)",
                   "Kişisel verilerinizi yalnızca talebinize yanıt vermek için işleriz." if T else "We process your personal data only to respond to your request.",
                   "Gizlilik" if T else "Privacy", actions=False)
    m = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    if T:
        body = f"""<h2>Veri Sorumlusu</h2><p>6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) uyarınca, kişisel verilerinizin veri sorumlusu Atlantis Travel'dır. İletişim bilgilerimiz: {m}</p>
<h2>Toplanan Kişisel Veriler ve Toplama Yöntemi</h2><p>Web sitemiz üzerinden sunulan iletişim ve teklif formları aracılığıyla aşağıdaki kişisel verileriniz toplanmaktadır:</p>
<ul><li>Ad Soyad</li><li>E-posta adresi</li><li>Telefon numarası</li><li>Misafir sayısı ve konaklama tarihleri (teklif formlarında)</li></ul>
<p>Formlarda ayrıca şirket/kurum adı, talep edilen hizmet, oda sayısı ve açıklama alanına yazdığınız bilgiler alınabilir. Formlarda kimlik numarası, pasaport bilgisi veya sağlık verisi istenmez; lütfen bu tür bilgileri paylaşmayın.</p>
<h2>Kişisel Verilerin İşlenme Amacı</h2><p>Toplanan kişisel verileriniz yalnızca size özel konaklama ve seyahat teklifleri hazırlamak, talebinize en uygun çözümleri sunmak ve sizinle iletişim kurmak amacıyla işlenmektedir. Verileriniz pazarlama, reklam veya başka amaçlarla kullanılmamaktadır.</p>
<h2>Hukuki Sebep</h2><p>Veriler KVKK m.5/2-c (sözleşmenin kurulması) ve m.5/2-f (meşru menfaat) hukuki sebeplerine dayanarak işlenir.</p>
<h2>KVKK Kapsamındaki Haklarınız</h2><p>6698 sayılı KVKK'nın 11. maddesi uyarınca aşağıdaki haklara sahipsiniz:</p>
<ul><li>Kişisel verilerinizin işlenip işlenmediğini öğrenme</li><li>Kişisel verileriniz işlenmişse buna ilişkin bilgi talep etme</li><li>Kişisel verilerin işlenme amacını ve bunların amacına uygun kullanılıp kullanılmadığını öğrenme</li><li>Yurt içinde veya yurt dışında kişisel verilerin aktarıldığı üçüncü kişileri bilme</li><li>Kişisel verilerin eksik veya yanlış işlenmiş olması hâlinde bunların düzeltilmesini isteme</li><li>KVKK'da öngörülen şartlar çerçevesinde kişisel verilerin silinmesini veya yok edilmesini isteme</li><li>Düzeltme, silme veya yok edilme taleplerinin kişisel verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme</li><li>İşlenen verilerin münhasıran otomatik sistemler vasıtasıyla analiz edilmesi suretiyle aleyhinize bir sonucun ortaya çıkmasına itiraz etme</li></ul>
<h2>Kişisel Verilerin Paylaşımı</h2><p>Kişisel verileriniz üçüncü kişilere satılmamaktadır. Ancak, size hizmet sunabilmek için gerekli olduğunda (örneğin otel rezervasyonu veya transfer organizasyonu için) anlaşmalı otel ve transfer firmalarıyla paylaşılabilir. Bu paylaşım yalnızca hizmetin yerine getirilmesi amacıyla ve gerekli güvenlik önlemleri alınarak yapılmaktadır.</p>
<h2>Saklama</h2><p>Form verileri web sitesinde veritabanına kaydedilmez; yalnızca şirket e-posta adresimize iletilir. E-posta yazışmaları talebin gerektirdiği süre ve yasal saklama süreleri boyunca tutulur.</p>
<h2>Çerezler</h2><p>Site, çalışması için gerekli olan tercih kaydını (çerez onayınız) tarayıcınızda saklar. Google Analytics yalnızca çerez bildiriminde "Kabul et" seçeneğini işaretlemeniz halinde yüklenir ve ziyaret istatistikleri için kullanılır. Tercihinizi altbilgideki "Çerez tercihleri" bağlantısından değiştirebilirsiniz.</p>
<h2>Güvenlik</h2><p>Site HTTPS ile sunulur; formlar kötüye kullanıma karşı korunur ve IP adresiniz saklanmaz (yalnızca kötüye kullanım sınırı için geçici, geri döndürülemez bir özet kullanılır).</p>
<h2>İletişim</h2><p>KVKK kapsamındaki haklarınızı kullanmak veya kişisel verilerinizle ilgili sorularınız için bizimle iletişime geçebilirsiniz:</p><p>E-posta: {m}</p>"""
    else:
        body = f"""<h2>Data Controller</h2><p>In accordance with the Personal Data Protection Law No. 6698 (KVKK), the data controller of your personal data is Atlantis Travel. Our contact information: {m}</p>
<h2>Personal Data Collected and Collection Method</h2><p>The following personal data is collected through the contact and quote forms provided on our website:</p>
<ul><li>Full Name</li><li>Email address</li><li>Phone number</li><li>Number of guests and accommodation dates (in quote forms)</li></ul>
<p>The forms may also collect your company name, the service requested, the number of rooms and your message. We do not ask for ID numbers, passport details or health data; please do not share them.</p>
<h2>Purpose of Processing Personal Data</h2><p>Your collected personal data is processed only for the purpose of preparing special accommodation and travel offers for you, providing the most suitable solutions to your request, and communicating with you. Your data is not used for marketing, advertising, or other purposes.</p>
<h2>Legal Basis</h2><p>We process this data on the basis of contract formation and legitimate interest (KVKK Art. 5/2-c and 5/2-f).</p>
<h2>Your Rights Under the KVKK</h2><p>In accordance with Article 11 of Law No. 6698, you have the following rights:</p>
<ul><li>To learn whether your personal data is being processed</li><li>To request information if your personal data has been processed</li><li>To learn the purpose of processing personal data and whether they are used in accordance with their purpose</li><li>To know the third parties to whom personal data is transferred domestically or abroad</li><li>To request correction of personal data if it is incomplete or incorrectly processed</li><li>To request deletion or destruction of personal data within the framework of the conditions stipulated in the KVKK</li><li>To request notification of correction, deletion, or destruction requests to third parties to whom personal data has been transferred</li><li>To object to the emergence of a result against you through the analysis of processed data exclusively by automated systems</li></ul>
<h2>Sharing of Personal Data</h2><p>Your personal data is not sold to third parties. However, when necessary to provide you with service (for example, for hotel reservations or transfer organization), it may be shared with contracted hotels and transfer companies. This sharing is done only for the purpose of fulfilling the service and with necessary security measures taken.</p>
<h2>Storage</h2><p>Form data is not stored in a website database; it is sent only to our company email address. Correspondence is kept as long as the request requires and as required by law.</p>
<h2>Cookies</h2><p>The site stores your cookie choice in your browser. Google Analytics is loaded only if you select "Accept" in the cookie notice. You can change your choice via "Cookie settings" in the footer.</p>
<h2>Security</h2><p>The site is served over HTTPS; forms are protected against abuse and your IP address is not stored (only a temporary, irreversible hash is used for rate limiting).</p>
<h2>Contact</h2><p>To exercise your rights under the KVKK or for questions about your personal data, you can contact us:</p><p>Email: {m}</p>"""
    h += f'<section class="section"><div class="wrap prose">{body}<p style="margin-top:28px"><em>{"Son güncelleme" if T else "Last updated"}: 07.11.2026</em></p></div></section>'
    h += footer(lang)
    return h


# ----------------------------------------------------------------- Kullanım şartları
def build_terms(lang):
    T = lang == "tr"
    title = "Kullanım Şartları | Atlantis Travel" if T else "Terms of Use | Atlantis Travel"
    desc = "Atlantis Travel web sitesi kullanım şartları." if T else "Atlantis Travel website terms of use."
    h = head(lang, "terms", title, desc) + header(lang, "terms")
    h += page_hero(lang, "Yasal" if T else "Legal", "Kullanım Şartları" if T else "Terms of Use", "", "Kullanım Şartları" if T else "Terms", actions=False)
    m = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    if T:
        body = f"""<h2>Genel Bilgilendirme</h2><p>Bu web sitesinde yer alan tüm bilgiler genel bilgilendirme amaçlıdır. Atlantis Travel, sitede yer alan bilgilerin doğruluğunu ve güncelliğini sağlamak için çaba göstermekle birlikte, bilgilerde değişiklik yapma hakkını saklı tutar. Sitede yer alan fiyat ve müsaitlik bilgileri teklif aşamasında kesinleşir.</p>
<h2>Hizmet Koşulları</h2><p>Atlantis Travel tarafından sunulan konaklama, transfer ve seyahat organizasyonu hizmetleri, müşteri ile yapılacak yazılı veya elektronik sözleşme ile belirlenir. Fiyatlar, iptal koşulları ve ödeme şartları her teklif için ayrı ayrı belirtilir ve müşteriye özel olarak bildirilir.</p>
<h2>Teklif ve Rezervasyon</h2><p>Form üzerinden gönderilen talepler rezervasyon anlamına gelmez. Rezervasyon, tarafınıza iletilen teklifin yazılı olarak onaylanmasıyla kesinleşir; iptal ve değişiklik koşulları teklif ile birlikte bildirilir.</p>
<h2>Hizmet Kapsamı</h2><p>Atlantis Travel; İstanbul'da otel konaklama, transfer ve operasyon organizasyonu hizmeti verir. Uçak bileti, vize ve yurt dışı otel rezervasyonu hizmeti sunulmaz. Sağlık turizmi kapsamında tıbbi işlem, teşhis veya tedavi hizmeti verilmez.</p>
<h2>Fikri Mülkiyet Hakları</h2><p>Bu web sitesinde yer alan tüm içerikler (metin, görsel, logo, tasarım vb.) Atlantis Travel'a aittir ve telif hakları ile korunmaktadır. İçeriklerin izinsiz kopyalanması, çoğaltılması, dağıtılması veya ticari amaçla kullanılması yasaktır.</p>
<h2>Sorumluluk Sınırlaması</h2><p>Atlantis Travel, web sitesinin kesintisiz ve hatasız çalışacağını garanti etmez. Sitede yer alan bilgilerin kullanımından doğabilecek doğrudan veya dolaylı zararlardan sorumlu tutulamaz. Üçüncü taraf web sitelerine verilen linklerden Atlantis Travel sorumlu değildir. WhatsApp ve sosyal medya bağlantıları ilgili platformların kendi koşullarına tabidir.</p>
<h2>Uygulanacak Hukuk ve Yetki</h2><p>Bu kullanım şartları Türkiye Cumhuriyeti kanunlarına tabidir. Bu şartlardan veya web sitesinin kullanımından doğabilecek her türlü uyuşmazlıkta İstanbul Mahkemeleri ve İcra Daireleri yetkilidir.</p>
<h2>İletişim</h2><p>Kullanım şartları hakkında sorularınız için bizimle iletişime geçebilirsiniz:</p><p>E-posta: {m}</p>"""
    else:
        body = f"""<h2>General Information</h2><p>All information on this website is for general information purposes. Atlantis Travel makes efforts to ensure the accuracy and timeliness of the information on the site, but reserves the right to make changes to the information. Price and availability information on the site is finalized at the quote stage.</p>
<h2>Service Terms</h2><p>Accommodation, transfer, and travel organization services provided by Atlantis Travel are determined by a written or electronic contract to be made with the customer. Prices, cancellation conditions, and payment terms are specified separately for each quote and communicated specifically to the customer.</p>
<h2>Quotes and Bookings</h2><p>A request sent through a form is not a booking. A booking is confirmed when you approve the written quote we send; cancellation and change terms are stated with the quote.</p>
<h2>Scope of Service</h2><p>Atlantis Travel provides hotel accommodation, transfer and operations services in Istanbul. We do not provide flight ticketing, visa services or hotel bookings abroad, and we do not provide medical procedures, diagnosis or treatment.</p>
<h2>Intellectual Property Rights</h2><p>All content on this website (text, images, logos, design, etc.) belongs to Atlantis Travel and is protected by copyright. Unauthorized copying, reproduction, distribution, or commercial use of the content is prohibited.</p>
<h2>Limitation of Liability</h2><p>Atlantis Travel does not guarantee that the website will operate uninterrupted and error-free. It cannot be held responsible for direct or indirect damages that may arise from the use of information on the site. Atlantis Travel is not responsible for links to third-party websites. WhatsApp and social media links are subject to those platforms' own terms.</p>
<h2>Applicable Law and Jurisdiction</h2><p>These terms of use are subject to the laws of the Republic of Türkiye. Istanbul Courts and Enforcement Offices have jurisdiction in all disputes that may arise from these terms or the use of the website.</p>
<h2>Contact</h2><p>For questions about the terms of use, you can contact us:</p><p>Email: {m}</p>"""
    h += f'<section class="section"><div class="wrap prose">{body}</div></section>'
    h += footer(lang)
    return h


# ----------------------------------------------------------------- 404 (canonical/hreflang olmadan)
def build_404():
    h = head("tr", "home", "Sayfa bulunamadı | Atlantis Travel", "Aradığınız sayfa bulunamadı.")
    h = "\n".join(l for l in h.split("\n") if not l.startswith('<link rel="canonical"') and not l.startswith('<link rel="alternate"')
                  and not l.startswith('<meta property="og:url"'))
    h = h.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
    h += header("tr", "")
    h += """<section class="page-hero on-navy"><div class="wrap">
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
