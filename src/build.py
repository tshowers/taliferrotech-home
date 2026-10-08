#!/usr/bin/env python3
"""Builds the static taliferro.tech pages into ../public.

Products, header, footer and the universal menu live here once and are
written into every page as plain HTML, so the site stays fully static
(crawlable, no framework) while each product is edited in one place.

    python3 src/build.py
"""
import hashlib
import json
import math
from html import escape
from pathlib import Path
from urllib.parse import quote

from affiliate_pages import pages as affiliate_pages
from company_pages import careers, investors
from product_pages import PAGES

SITE = "https://taliferro.tech"
OUT = Path(__file__).resolve().parent.parent / "public"
YEAR = 2026


def asset_version(rel):
    """Content hash for cache-busting: a changed file gets a new URL, so the
    7-day browser cache (firebase.json) never serves a stale stylesheet."""
    return hashlib.sha256((OUT / rel).read_bytes()).hexdigest()[:10]


GA_ID = "G-QMVLRLV5XN"  # GA4 stream "Taliferro Tech Home" in the taliferrotech property
EMAIL = "info@taliferro.tech"
PHONE_DISPLAY = "+1 401.646.2662"
PHONE_TEL = "+14016462662"
ADDRESS = "1424 11th Ave Ste 400, Seattle, WA 98122"
GROUP_URL = "https://taliferro.com"
TODD_URL = "https://todd.taliferro.tech"
SIGN_IN_URL = "https://todd.taliferro.tech/login"
PRIVACY_URL = "https://todd.taliferro.tech/privacy-policy"
TERMS_URL = "https://todd.taliferro.tech/terms-and-conditions"
FOUNDER_PROFILE = "https://taliferro.com/team/tyrone-showers/"
FOUNDER_LINKEDIN = "https://www.linkedin.com/in/tyroneshowers"
SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/company/taliferro-tech"),
    ("YouTube", "https://www.youtube.com/@TaliferroTechLLC"),
    ("Instagram", "https://www.instagram.com/taliferrotech/"),
]

CONSULT_BODY = (
    "Hi Taliferro Tech,\n\n"
    "Our business: \n"
    "Work we want off our plate: \n"
    "Tools we use today: \n"
)
CONSULT_MAILTO = f"mailto:{EMAIL}?subject=Consultation&body={quote(CONSULT_BODY)}"

# (name, tint, glyph file, url or None, one line). Order = universal menu order.
# url None = no confirmed address yet; the card renders without a link.
PRODUCTS = [
    ("Ask TODD", "green", "ask-todd.png", "https://ask.taliferro.tech", "Ask a business question and get the answer with the next move."),
    ("Find", "blue", "find.svg", "https://find.taliferro.tech", "Search that starts with what you remember and ends with an answer."),
    ("Maya", "green", "maya.png", "https://maya.taliferro.tech", "Your on-call AI Marketing Director for message, campaigns and audience."),
    ("Network", "violet", "network.png", "https://network.taliferro.tech", "See which relationships deserve your attention this week."),
    ("Moves", "blue", "moves.png", "https://moves.taliferro.tech", "The next best actions across your business, in priority order."),
    ("Outreach", "blue", "outreach.png", "https://outreach.taliferro.tech", "Personal outreach emails, drafted and ready for your approval."),
    ("Pulse", "pink", "pulse.png", "https://pulse.taliferro.tech", "A live read on how your business is doing."),
    ("Lead Vault", "yellow", "lead-vault.png", "https://lead-vault.taliferro.tech", "Validated business leads you can preview, unlock and contact."),
    ("Social", "cyan", "social.png", "https://social.taliferro.tech", "Social posts drafted for your channels."),
    ("SayIt", "pink", "sayit.png", "https://sayit.taliferro.tech", "A new type of social media."),
    ("Docs", "blue", "docs.png", "https://docs.taliferro.tech", "Business documents drafted from what TODD already knows."),
    ("Email Creator", "yellow", "email-creator.svg", "https://emails.taliferro.tech", "Describe an email and get finished HTML."),
    ("Email Signature", "violet", "email-signature.png", "https://signature.taliferro.tech", "A professional signature that pastes into any mail app."),
    ("Image Creator", "cyan", "image-creator.svg", "https://images.taliferro.tech", "Describe an image and download it as a PNG."),
    ("Music", "pink", "music.png", "https://music.taliferro.com", "Taliferro Music: jazz, R&B and downtempo, streaming live."),
]
P = {p[0]: p for p in PRODUCTS}

GROUPS = [
    ("Intelligence", "Ask, plan and decide", ["Ask TODD", "Find", "Maya", "Moves", "Pulse"]),
    ("Grow", "Relationships, leads and outreach", ["Network", "Lead Vault", "Outreach", "Social", "SayIt"]),
    ("Create", "Documents, email and images", ["Docs", "Email Creator", "Email Signature", "Image Creator"]),
    ("Listen", "From Taliferro Music", ["Music"]),
]

# Lucide paths, stroke 2.5, currentColor.
ICONS = {
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "ext": '<path d="M7 17 17 7M7 7h10v10"/>',
    "chev": '<path d="m9 18 6-6-6-6"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7l10-5Z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    "brief": '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
    "dollar": '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "undo": '<path d="M9 14 4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
}


def icon(name, size=18, cls="i"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def chip(name, size):
    tint, glyph = P[name][1], P[name][2]
    return (f'<span class="chip t-{tint}" style="--sz:{size}px" aria-hidden="true">'
            f'<span class="glyph" style="--g:url(/img/products/{glyph})"></span></span>')


def page_url(name):
    return f"/products/{PAGES[name]['slug']}"


def detail_link(name, cls, inner):
    return f'<a class="{cls}" href="{page_url(name)}">{inner}</a>'


def product_link(name, cls, inner):
    url = P[name][3]
    if url:
        return f'<a class="{cls}" href="{url}" data-search="{escape(name.lower())}">{inner}</a>'
    return f'<div class="{cls} is-pending" data-search="{escape(name.lower())}" title="Link coming soon">{inner}</div>'


# ---------------------------------------------------------------- chrome

AC = ' aria-current="page"'
NEWTAB = ' target="_blank" rel="noopener"'

NAV = [("Products", "/products"), ("About", "/about"), ("Contact", "/contact")]


def header(current):
    seg = "".join(
        f'<a href="{href}"{AC if label == current else ""}>{label}</a>' for label, href in NAV)
    return f'''<header class="hdr">
  <a class="brand" href="/" aria-label="Taliferro Tech home"><img src="/img/general/apple-touch-icon.png" alt="" width="36" height="36"><span>Taliferro Tech</span></a>
  <nav class="seg" aria-label="Site"><span class="seg__track">{seg}</span></nav>
  <a class="hdr__group" href="{GROUP_URL}" target="_blank" rel="noopener">Taliferro Group{icon("ext", 14)}</a>
  <button class="pill pill--surface theme-toggle" type="button" aria-label="Switch colour theme">{icon("moon", 16, "i i-moon")}{icon("sun", 16, "i i-sun")}<span class="theme-toggle__label"></span></button>
  <button class="pill pill--primary menu-open" type="button" aria-haspopup="dialog" aria-controls="menu">{icon("menu")}Menu</button>
</header>'''


def footer():
    links = [("Careers", "/careers"), ("Investors", "/investors"), ("Affiliates", "/affiliates"), ("Privacy", PRIVACY_URL), ("Terms", TERMS_URL)] + SOCIAL
    items = "".join(f'<a href="{u}"{NEWTAB if u.startswith("http") else ""}>{l}</a>' for l, u in links)
    return f'''<footer class="ftr">
  <b>Taliferro Tech, LLC</b><span>{ADDRESS}</span><span class="ftr__sp"></span>
  <span class="ftr__links">{items}</span><span>© {YEAR} Taliferro Tech, LLC</span>
</footer>'''


def menu(current):
    site = [("Home", "/", "home"), ("Products", "/products", "grid"), ("About", "/about", "info"), ("Contact", "/contact", "mail")]
    rows = "".join(
        f'<a class="mrow" href="{h}" data-search="{l.lower()} page"{AC if l == current else ""}>{icon(k)}<span>{l}</span></a>'
        for l, h, k in site)
    out = (f'<a class="mrow" href="{GROUP_URL}" target="_blank" rel="noopener" data-search="taliferro group consulting">{icon("brief")}<span>Taliferro Group</span>{icon("ext", 12, "i mrow__ext")}</a>'
           f'<a class="mrow" href="{TODD_URL}" data-search="todd intelligence layer">{icon("layers")}<span>TODD</span>{icon("ext", 12, "i mrow__ext")}</a>')
    tiles = "".join(product_link(n, "mtile", f'{chip(n, 56)}<span>{n}</span>') for n, *_ in PRODUCTS)
    return f'''<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="menu__bar">
    <a class="brand" href="/"><img src="/img/general/apple-touch-icon.png" alt="" width="32" height="32"><span>Taliferro Tech</span></a>
    <label class="menu__search">{icon("search")}<input type="search" placeholder="Search products and pages" aria-label="Search products and pages" autocomplete="off"><kbd>⌘K</kbd></label>
    <button class="pill pill--primary menu-close" type="button">{icon("x")}Close</button>
  </div>
  <div class="menu__body">
    <div class="menu__site">
      <span class="kicker">Taliferro Tech</span>
      {rows}
      <span class="menu__rule"></span>
      {out}
    </div>
    <div class="menu__products">
      <div class="menu__head"><span class="kicker">Products</span><span class="menu__note">Opens in this tab</span></div>
      <div class="mgrid">{tiles}</div>
      <p class="menu__empty" hidden>Nothing matches that search.</p>
    </div>
    <div class="menu__start">
      <span class="kicker">Get started</span>
      <div class="menu__card">
        <p>One TODD account signs you in to every product.</p>
        <a class="btn btn--primary btn--sm" href="{SIGN_IN_URL}">Sign in with TODD</a>
        <a class="btn btn--bg btn--sm" href="{CONSULT_MAILTO}">{icon("mail")}Book a consultation</a>
      </div>
    </div>
  </div>
  <div class="menu__strip">
    <b>TALIFERRO TECH, LLC</b><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><span>Seattle, Washington, USA</span>
    <span class="ftr__sp"></span><a href="{PRIVACY_URL}">Privacy</a><a href="{TERMS_URL}">Terms</a><span>© {YEAR} Taliferro Tech, LLC</span>
  </div>
</div>'''


ORG = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "Taliferro Tech, LLC",
    "alternateName": ["Taliferro Tech", "Taliferro Group"],
    "url": f"{SITE}/",
    "logo": f"{SITE}/img/general/apple-touch-icon.png",
    "description": "Taliferro Tech builds AI software products that draft, nudge, validate and route the work for you. Every product runs on TODD, the Taliferro intelligence layer.",
    "foundingDate": "2022",
    "founder": [{"@type": "Person", "name": "Vikki Owens"},
                {"@type": "Person", "name": "Tyrone Showers", "url": FOUNDER_PROFILE, "sameAs": [FOUNDER_LINKEDIN]}],
    "email": EMAIL,
    "telephone": PHONE_TEL,
    "address": {"@type": "PostalAddress", "streetAddress": "1424 11th Ave Ste 400", "addressLocality": "Seattle",
                "addressRegion": "WA", "postalCode": "98122", "addressCountry": "US"},
    "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "email": EMAIL, "telephone": PHONE_TEL,
                      "areaServed": "US", "availableLanguage": "English"}],
    "sameAs": [u for _, u in SOCIAL] + [GROUP_URL],
}


def page(path, title, description, current, body, extra_ld=None, robots="index,follow"):
    url = f"{SITE}{path}"
    graph = [ORG, {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": description,
                   "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#organization"}}]
    graph += extra_ld or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0e13" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Taliferro Tech">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og/taliferro-tech.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{SITE}/img/og/taliferro-tech.png">
<link rel="icon" href="/img/general/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/img/general/favicon-32x32.png">
<link rel="apple-touch-icon" href="/img/general/apple-touch-icon.png">
<link rel="manifest" href="/img/general/manifest.json">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/css/site.css?v={asset_version("css/site.css")}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
{menu(current or "Home")}
<script src="/js/site.js?v={asset_version("js/site.js")}" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- pages

def cta_consult(label="Book a consultation", cls="btn btn--primary"):
    return f'<a class="{cls}" href="{CONSULT_MAILTO}">{icon("mail")}{label}</a>'


def contact_rows():
    rows = [("Email", EMAIL, f"mailto:{EMAIL}", "mail"), ("Phone", PHONE_DISPLAY, f"tel:{PHONE_TEL}", "phone"),
            ("Office", ADDRESS, "https://maps.google.com/?q=" + quote(ADDRESS), "pin")]
    return "".join(
        f'<a class="crow" href="{h}"{NEWTAB if h.startswith("http") else ""}>'
        f'<span class="crow__icon">{icon(i)}</span><span><span class="kicker">{k}</span><span class="crow__v">{v}</span></span></a>'
        for k, v, h, i in rows)


def home():
    ring = [n for n, *_ in PRODUCTS if n != "Ask TODD"]
    orbit = ""
    for k, n in enumerate(ring):
        a = k / len(ring) * math.pi * 2 - math.pi / 2
        r = 158 if k % 2 else 200
        x, y = 260 + r * math.cos(a) - 30, 260 + r * math.sin(a) - 30
        orbit += f'<span class="orbit__tile" style="left:{x:.1f}px;top:{y:.1f}px">{chip(n, 60)}</span>'
    tiles = "".join(detail_link(n, "ptile", f'{chip(n, 56)}<span>{n}</span>') for n, *_ in PRODUCTS)
    pillars = [("It does the work", "Our products don't stop at an answer. They draft the email, stage the follow-up and check the data, then wait for your go-ahead.", "check"),
               ("One intelligence layer", "TODD sits under every product, so what one app learns, the others can use.", "layers"),
               ("Built in Seattle", "Designed, engineered and supported by Taliferro Tech, LLC on Capitol Hill.", "pin")]
    pill = "".join(f'<div class="pillar"><span class="pillar__icon">{icon(i, 22)}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d, i in pillars)
    body = f'''<section class="hero">
  <div class="hero__copy">
    <span class="tag t-cyan">Software products · Seattle, WA</span>
    <h1 class="display">Software that does the work.</h1>
    <p class="lede">Taliferro Tech builds AI products that draft, nudge, validate and route the work for you, so your business keeps moving. Every product runs on TODD, our intelligence layer.</p>
    <div class="actions">{cta_consult()}<a class="btn btn--surface" href="/products">Explore products{icon("arrow", 16)}</a></div>
    <p class="hero__contact"><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
  </div>
  <div class="orbit" aria-label="TODD at the centre of fourteen Taliferro Tech products" role="img">
    <span class="orbit__disc"></span>{orbit}
    <div class="orbit__core">{chip("Ask TODD", 112)}<b>TODD</b><span>Intelligence layer</span></div>
  </div>
</section>
<section class="band t-green">
  {chip("Ask TODD", 52)}
  <div class="band__copy"><h2>Every product runs on TODD.</h2><p>TODD turns scattered information into clear next moves, then works across the apps to get them done.</p></div>
  <a class="btn btn--bg btn--sm" href="{TODD_URL}">todd.taliferro.tech{icon("ext", 14)}</a>
</section>
<section class="section">
  <div class="section__head"><div><span class="kicker">Products</span><h2 class="h2">Fifteen products, one account.</h2></div><a class="btn btn--surface btn--sm" href="/products">All products{icon("arrow", 16)}</a></div>
  <div class="pgrid">{tiles}</div>
</section>
<section class="section pillars">{pill}</section>
<section class="panel">
  <div class="panel__copy"><h2>Have work that should run itself?</h2><p>Tell us what slows your team down. We'll show you what TODD can take on and which products fit.</p>{cta_consult()}</div>
  <div class="panel__rows">{contact_rows()}</div>
</section>'''
    website = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Taliferro Tech",
               "publisher": {"@id": f"{SITE}/#organization"}}
    return page("/", "Taliferro Tech | AI software that does the work",
                "Taliferro Tech builds AI software products that draft, nudge, validate and route the work for you. Fifteen products, one TODD account. Based in Seattle, WA.",
                "", body, [website])


def products():
    sections = ""
    for title, desc, names in GROUPS:
        cards = "".join(detail_link(n, "pcard",
                                    f'{chip(n, 56)}<span class="pcard__body"><b>{n}</b><span>{P[n][4]}</span>'
                                    f'<span class="pcard__open">Learn more{icon("arrow", 14)}</span></span>'
                                    f'{icon("chev", 16, "i pcard__chev")}') for n in names)
        sections += f'<section class="pgroup"><h2><span>{title}</span><small>{desc}</small></h2><div class="pcards">{cards}</div></section>'
    body = f'''<section class="pagehead">
  <div><h1 class="display display--md">Products</h1><p class="lede">Fifteen products, one intelligence layer. Sign in once with your TODD account and use any of them.</p></div>
  {cta_consult("Not sure where to start? Book a consultation", "btn btn--primary btn--sm pagehead__cta")}
</section>
<div class="pgroups">{sections}</div>'''
    items = [{"@type": "ListItem", "position": i + 1,
              "item": {"@type": "SoftwareApplication", "name": n, "description": d, "applicationCategory": "BusinessApplication",
                       "operatingSystem": "Web", **({"url": u} if u else {}), "publisher": {"@id": f"{SITE}/#organization"}}}
             for i, (n, _, _, u, d) in enumerate(PRODUCTS)]
    return page("/products", "Products | Taliferro Tech",
                "All fourteen Taliferro Tech products: Ask TODD, Maya, Network, Moves, Outreach, Pulse, Lead Vault, Social, SayIt, Docs, Email Creator, Email Signature, Image Creator and Music.",
                "Products", body, [{"@type": "ItemList", "name": "Taliferro Tech products", "itemListElement": items}])


def about():
    facts = [("Legal name", "Taliferro Tech, LLC"), ("Founded", "2022"), ("Headquarters", ADDRESS), ("Co-founders", "Vikki Owens · Tyrone Showers"),
             ("Brands", "Taliferro Tech (products) · Taliferro Group (consulting)")]
    fl = "".join(f'<div class="fact"><span class="kicker">{k}</span><span>{v}</span></div>' for k, v in facts)
    body = f'''<section class="about">
  <div class="about__copy">
    <span class="tag t-cyan">About Taliferro Tech</span>
    <h1 class="display display--md">AI answered the questions. Nobody was doing the work.</h1>
    <p class="lede">Taliferro Tech was founded in 2022 after we noticed a significant shortcoming in the AI space. AI was answering a lot of questions, but nothing was actually doing the work automatically. So Taliferro Tech set out to make software that does the work, instead of always pushing work onto the user.</p>
    <p class="quote t-cyan">That is our main goal: to lighten the load of every user by actually doing the work.</p>
  </div>
  <div class="facts">{fl}</div>
</section>
<section class="section section--narrow">
  <h2 class="h2 h2--sm">One company, two names</h2>
  <div class="brands">
    <div class="brandcard t-cyan"><span class="brandcard__head"><img src="/img/general/apple-touch-icon.png" alt="" width="40" height="40"><b>Taliferro Tech</b></span><span class="kicker kicker--tint">Software products · taliferro.tech</span><p>The products on this site, from Ask TODD to Music, all running on the TODD intelligence layer.</p></div>
    <div class="brandcard brandcard--surface"><span class="brandcard__head"><span class="brandcard__icon">{icon("brief", 20)}</span><b>Taliferro Group</b></span><span class="kicker">Consulting · taliferro.com</span><p>Consulting and engineering engagements for businesses that want hands-on help.</p><a class="brandcard__link" href="{GROUP_URL}" target="_blank" rel="noopener">Visit taliferro.com{icon("ext", 14)}</a></div>
  </div>
  <p class="note">Both are trade names of Taliferro Tech, LLC.</p>
</section>
<section class="section section--narrow founder">
  <img class="person__photo" src="/img/team/tyrone-showers-192.webp" alt="Sketch of Tyrone Showers" width="72" height="72">
  <div class="founder__name"><span class="kicker">Co-founder and Chairman</span><b>Tyrone Showers</b></div>
  <div class="founder__links"><a class="btn btn--surface btn--sm" href="{FOUNDER_PROFILE}" target="_blank" rel="noopener">Profile{icon("ext", 14)}</a><a class="btn btn--surface btn--sm" href="{FOUNDER_LINKEDIN}" target="_blank" rel="noopener">LinkedIn{icon("ext", 14)}</a></div>
</section>
<section class="panel panel--row">
  <div class="panel__copy"><h2 class="h2 h2--sm">Let's take some work off your plate.</h2><p>Email us and we'll set up a time to talk.</p></div>
  {cta_consult()}
</section>'''
    return page("/about", "About | Taliferro Tech",
                "Taliferro Tech, LLC was founded in Seattle in 2022 by Vikki Owens and Tyrone Showers to build software that does the work instead of pushing it onto the user.",
                "About", body, [{"@type": "AboutPage", "url": f"{SITE}/about", "mainEntity": {"@id": f"{SITE}/#organization"}}])


def contact():
    steps = [("What your business does", "A sentence or two is enough."), ("The work that eats your week", "Follow-ups, reporting, outreach, data entry."),
             ("The tools you use today", "Email, CRM, spreadsheets, anything else.")]
    sl = "".join(f'<li><span class="num">{i + 1}</span><span><b>{t}</b><span>{d}</span></span></li>' for i, (t, d) in enumerate(steps))
    body = f'''<section class="contact">
  <div class="contact__main">
    <h1 class="display display--md">Book a consultation</h1>
    <p class="lede">Email us a few lines about your business and the work you want off your plate. We'll reply to set up a time to talk.</p>
    <div class="actions">
      <a class="btn btn--primary btn--lg" href="{CONSULT_MAILTO}">{icon("mail")}<span class="only-wide">Email {EMAIL}</span><span class="only-narrow">Email us</span></a>
      <a class="btn btn--surface only-narrow" href="tel:{PHONE_TEL}">{icon("phone")}{PHONE_DISPLAY}</a>
    </div>
    <div class="contact__rows">{contact_rows()}</div>
  </div>
  <div class="contact__side">
    <div class="steps"><span class="kicker">What to put in the email</span><ol>{sl}</ol></div>
    <p class="aside t-cyan">{icon("brief", 20)}<span>Need a consulting engagement? That's Taliferro Group.</span><a href="{GROUP_URL}" target="_blank" rel="noopener">taliferro.com{icon("ext", 12)}</a></p>
  </div>
</section>'''
    return page("/contact", "Book a consultation | Taliferro Tech",
                "Book a consultation with Taliferro Tech. Email info@taliferro.tech or call +1 401.646.2662. Office at 1424 11th Ave, Seattle, WA.",
                "Contact", body, [{"@type": "ContactPage", "url": f"{SITE}/contact", "mainEntity": {"@id": f"{SITE}/#organization"}}])


def not_found():
    body = f'''<section class="nf">
  <div class="nf__copy">
    <span class="kicker">Error 404</span>
    <h1 class="display display--md">This page moved or never existed.</h1>
    <p class="lede">Try the products page or head home.</p>
    <div class="actions"><a class="btn btn--primary" href="/">Go home</a><a class="btn btn--surface" href="/products">See products{icon("arrow", 16)}</a></div>
  </div>
  <span class="nf__disc t-cyan" aria-hidden="true">404</span>
</section>'''
    return page("/404", "Page not found | Taliferro Tech", "This page moved or never existed.", "", body, robots="noindex")


def product_page(name):
    _, tint, _, url, line = P[name]
    d = PAGES[name]
    group = next(g for g in GROUPS if name in g[2])
    features = "".join(f'<div class="feat"><h3>{t}</h3><p>{x}</p></div>' for t, x in d["features"])
    steps = ""
    if d.get("steps"):
        items = "".join(f'<li><span class="num">{i + 1}</span><span><b>{t}</b><span>{x}</span></span></li>'
                        for i, (t, x) in enumerate(d["steps"]))
        steps = f'<section class="section section--narrow"><span class="kicker">How it works</span><ol class="howto">{items}</ol></section>'
    open_btn = (f'<a class="btn btn--primary" href="{url}">Open {name}{icon("ext", 14)}</a>' if url else "")
    app_btn = (f'<a class="btn btn--surface" href="{d["app_store"]}" target="_blank" rel="noopener">Get the iPhone app{icon("ext", 14)}</a>'
               if d.get("app_store") else "")
    platforms = "Web and iPhone" if d.get("ios") else "Web"
    fits = d.get("fits") or []
    fit_html = ""
    if fits:
        fit_cards = "".join(detail_link(n, "pcard pcard--sm", f'{chip(n, 48)}<span class="pcard__body"><b>{n}</b><span>{P[n][4]}</span></span>'
                                        f'{icon("chev", 16, "i pcard__chev pcard__chev--on")}') for n in fits)
        fit_html = f'<section class="section section--narrow"><h2 class="h2 h2--sm">Works well with</h2><div class="pcards">{fit_cards}</div></section>'
    faq = "".join(f'<details class="qa"><summary>{q}{icon("chev", 16, "i qa__chev")}</summary><p>{a}</p></details>' for q, a in d["faq"])
    body = f'''<nav class="crumbs" aria-label="Breadcrumb"><a href="/products">Products</a>{icon("chev", 14)}<span aria-current="page">{name}</span></nav>
<section class="phero">
  <div class="phero__copy">
    <span class="phero__name">{chip(name, 72)}<span><span class="kicker">{group[0]} · {platforms}</span><b>{name}</b></span></span>
    <h1 class="display display--md">{d["tagline"]}</h1>
    <p class="lede">{d["lede"]}</p>
    <div class="actions">{open_btn}{app_btn}{cta_consult("Book a consultation", "btn btn--surface")}</div>
  </div>
</section>
<section class="section section--narrow">
  <span class="kicker">What it does</span>
  <div class="feats">{features}</div>
</section>
{steps}
<section class="band t-green band--page">
  {chip("Ask TODD", 52)}
  <div class="band__copy"><h2>{"This is TODD." if name == "Ask TODD" else f"{name} runs on TODD."}</h2><p>TODD, the Taliferro Tech intelligence layer, sits under every product, so what {name} learns, the others can use. One TODD account signs you in to all of them.</p></div>
  <a class="btn btn--bg btn--sm" href="{TODD_URL}">todd.taliferro.tech{icon("ext", 14)}</a>
</section>
{fit_html}
<section class="section section--narrow">
  <h2 class="h2 h2--sm">Questions</h2>
  <div class="faq">{faq}</div>
</section>
<section class="panel panel--row">
  <div class="panel__copy"><h2 class="h2 h2--sm">Not sure {name} is the right fit?</h2><p>Tell us what slows your team down and we'll tell you which products fit.</p></div>
  {cta_consult()}
</section>'''
    path = page_url(name)
    app = {"@type": "SoftwareApplication", "@id": f"{SITE}{path}#app", "name": name, "description": d["lede"],
           "applicationCategory": "BusinessApplication", "operatingSystem": "Web, iOS" if d.get("ios") else "Web",
           "publisher": {"@id": f"{SITE}/#organization"}, "image": f"{SITE}/img/products/{P[name][2]}"}
    if url:
        app["url"] = url
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Products", "item": f"{SITE}/products"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"}]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    return page(path, f"{d['title']} | Taliferro Tech", d["lede"][:300], "Products", body, [app, crumbs, faq_ld])


def sitemap(paths):
    urls = "".join(f"  <url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n" for p, pr in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


def main():
    pages = {"index.html": home(), "products/index.html": products(), "about.html": about(), "contact.html": contact(), "404.html": not_found()}
    for n, *_ in PRODUCTS:
        pages[f"products/{PAGES[n]['slug']}.html"] = product_page(n)
    aff = affiliate_pages(icon, TODD_URL, PHONE_DISPLAY, PHONE_TEL)
    for path, out, title, desc, body in aff:
        pages[out] = page(path, title, desc, "", body)
    c_path, c_out, c_title, c_desc, c_body, c_ld = careers(icon, EMAIL, SITE)
    pages[c_out] = page(c_path, c_title, c_desc, "", c_body, c_ld)
    i_path, i_out, i_title, i_desc, i_body, i_ld = investors(icon, EMAIL, SITE)
    pages[i_out] = page(i_path, i_title, i_desc, "", i_body, i_ld)
    (OUT / "products").mkdir(exist_ok=True)
    (OUT / "affiliates").mkdir(exist_ok=True)
    (OUT / "products.html").unlink(missing_ok=True)
    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")
    urls = [("/", "1.0"), ("/products", "0.9")] + [(page_url(n), "0.8") for n, *_ in PRODUCTS] + [("/about", "0.6"), ("/contact", "0.7"), (c_path, "0.5"), (i_path, "0.4")] + [(a[0], "0.5") for a in aff]
    (OUT / "sitemap.xml").write_text(sitemap(urls), encoding="utf-8")
    print("built", len(pages), "pages + sitemap.xml")


if __name__ == "__main__":
    main()
