#!/usr/bin/env python3
"""Builds 16ahead.com into ../public-16ahead (Firebase site `16ahead`).

The landing page is Claude Design's design_handoff_16ahead_landing, with the
universal menu (taliferro-ui's static build, copied into tt/) in place of the
design's Log in pill. /terms, /privacy and /privacy-rights carry the same
legal text as taliferro.tech, so they keep working once taliferro.tech
redirects here.

    python3 src/sixteen_ahead.py

css/16ahead.css and js/16ahead.js are hand-written; edit them directly.
"""
import hashlib
import json
import os
import shutil
from datetime import date
from html import escape
from pathlib import Path

from legal_pages import pages as legal_pages

SITE = "https://16ahead.com"
GA_ID = "G-RM39WFG83C"  # GA4 stream "16Ahead Home" in the taliferrotech property
APP_URL = "https://app.16ahead.com"
SIGN_IN_URL = f"{APP_URL}/login"
IO_URL = "https://16ahead.io"
# The mission box hands off to the General Assistant, which plans the next moves
# and points the visitor to the app to start in (it reads ?mission=).
ASSISTANT_URL = "https://assistant.16ahead.com/"
GROUP_URL = "https://taliferro.com"
OUT = Path(__file__).resolve().parent.parent / "public-16ahead"
UI = Path(os.environ.get("TALIFERRO_UI", Path.home() / "Dropbox/corporate/taliferro-ui"))
ADDRESS = "1424 11th Ave Ste 400, Seattle, WA 98122"
PHONE_DISPLAY = "+1 401.646.2662"
PHONE_TEL = "+14016462662"
EMAIL = "info@16ahead.com"
TAGLINE = "Stay sixteen moves ahead."
DESCRIPTION = "Tell 16Ahead your mission. It keeps your business moving toward it and shows you what's next."

MORNING = [
    ("6:00", "You wake up wondering what to do next.", "It's already working. It looks at everything in motion and plans the day's moves."),
    ("6:30", "You shower and get ready.", "It writes the follow-ups, posts and proposals that should go out today."),
    ("7:15", "You pour a coffee and log in.", "Your moves are lined up and waiting for a yes."),
]
# (slug, title, ask, by morning). A row shows its Claude Design video once it
# is at media/overnight-<slug>.mp4 with media/overnight-<slug>-poster.jpg.
OVERNIGHT = [
    ("business", "A business, overnight", "Start a candle business called Ember & Oak.",
     "Store is live with products. Image Creator has made the product photos and logo. Docs has written the terms and "
     "return policy. Email Signature and branded emails are set up, Social has the first posts scheduled, and SayIt "
     "has made a short brand jingle."),
    ("campaign", "A launch campaign, overnight", "Get our new product in front of 50 local boutiques.",
     "Find and Lead Vault have the 50 shops and their contacts. Email Creator and Image Creator have made a personal "
     "pitch and lookbook for each one. Outreach has sent them, and your morning report shows who opened and who replied."),
    ("answer", "An answer, overnight", "Find out why customers stopped buying.",
     "Pulse has surveyed your past customers and Docs has a report with the top three reasons. Marketing Assistant has "
     "a win-back campaign drafted and waiting for one tap to approve."),
]
MOVES = ["Follow up with Regina. It has been 41 days.", "Send the proposal that is due Friday.", "Post this week's update."]
LADDER = [("1", "Most people plan the next move."), ("3", "Good players plan a few more."), ("16", "You see the whole board.")]
PEOPLE = [
    ("Founders", "Follow up with the investor who went quiet."),
    ("Project managers", "Nudge the client before the deadline slips."),
    ("Business development directors", "Bid on the contract that opened overnight."),
    ("Retail business owners", "Tell your regulars the new stock is in."),
]


def asset_version(rel):
    return hashlib.sha256((OUT / rel).read_bytes()).hexdigest()[:10]


def sync_menu():
    """The universal menu's static build, styles and images, laid out as
    taliferro-ui/static/sync.sh does (styles/ next to menu-logos/ and menu-icons/)."""
    tt = OUT / "tt"
    shutil.rmtree(tt, ignore_errors=True)
    (tt / "styles").mkdir(parents=True)
    shutil.copy(UI / "static/dist/universal-menu.js", tt)
    shutil.copy(UI / "styles/universal-menu.css", tt / "styles")
    shutil.copytree(UI / "menu-logos", tt / "menu-logos", ignore=shutil.ignore_patterns(".*"))
    shutil.copytree(UI / "menu-icons", tt / "menu-icons", ignore=shutil.ignore_patterns(".*"))


def menu_config(on_home):
    here = "" if on_home else "/"
    items = [
        {"label": "Overnight", "icon": "bolt", "url": f"{here}#overnight", "keywords": "examples use cases business launch campaign"},
        {"label": "Your morning", "icon": "sun", "url": f"{here}#morning", "keywords": "how it works day approve"},
        {"label": "Why sixteen", "icon": "grid", "url": f"{here}#why", "keywords": "chess name"},
        {"label": "Who it's for", "icon": "users", "url": f"{here}#who", "keywords": "founders managers business development retail"},
        {"label": "What's your mission?", "icon": "target", "url": f"{here}#mission", "keywords": "start sign up"},
    ]
    secondary = [
        {"label": "How it's built", "icon": "bolt", "url": IO_URL, "external": True, "keywords": "technical api 16ahead.io"},
        {"label": "Terms", "icon": "file", "url": "/terms", "keywords": "legal"},
        {"label": "Privacy", "icon": "shield", "url": "/privacy", "keywords": "legal data"},
    ]
    return {"app": "todd", "name": "16Ahead", "items": items, "secondaryItems": secondary,
            "accountNote": "One 16Ahead account signs you in to every app.",
            "signInUrl": SIGN_IN_URL, "signInLabel": "Log in"}


ORG = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "16Ahead",
    "url": f"{SITE}/",
    "logo": f"{SITE}/img/16ahead-dial-1024.png",
    "slogan": TAGLINE,
    "description": DESCRIPTION,
    "email": EMAIL,
    "parentOrganization": {"@type": "Organization", "name": "Taliferro Tech, LLC", "url": "https://taliferro.tech",
                           "address": {"@type": "PostalAddress", "streetAddress": "1424 11th Ave Ste 400",
                                       "addressLocality": "Seattle", "addressRegion": "WA", "postalCode": "98122",
                                       "addressCountry": "US"}},
}


def page(path, title, description, body, extra_ld=None, robots="index,follow"):
    url = f"{SITE}{path}"
    graph = [ORG, {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": description,
                   "isPartOf": {"@id": f"{SITE}/#website"}, "publisher": {"@id": f"{SITE}/#organization"}}]
    graph += extra_ld or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)
    menu = json.dumps(menu_config(path == "/"), ensure_ascii=False)
    og_image = f"{SITE}/media/16ahead-story-poster.jpg"
    return f'''<!doctype html>
<html lang="en" class="light">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="16Ahead">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="720">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/tt/styles/universal-menu.css?v={asset_version("tt/styles/universal-menu.css")}">
<link rel="stylesheet" href="/css/16ahead.css?v={asset_version("css/16ahead.css")}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="/" aria-label="16Ahead home"><img src="/img/16ahead-dial-128.png" alt="" width="40" height="40"><span>16AHEAD</span></a>
    <div data-tt-menu></div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap ftr__in">
    <span class="ftr__brand"><img src="/img/16ahead-dial-128.png" alt="" width="28" height="28">16Ahead is a product of Taliferro Tech, LLC.</span>
    <nav aria-label="Footer"><a href="{IO_URL}">How it's built</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="{GROUP_URL}">taliferro.com</a></nav>
  </div>
</footer>
<script>window.TT_MENU = {menu};</script>
<script src="/tt/universal-menu.js?v={asset_version("tt/universal-menu.js")}" defer></script>
<script src="/js/16ahead.js?v={asset_version("js/16ahead.js")}" defer></script>
</body>
</html>
'''


def dial():
    """The 16Ahead logo (design_handoff_16ahead_logos svg/light/01-16ahead.svg)
    drawn inline so js/16ahead.js can move the highlight around the 16 ticks.
    Each tick is one app; tick 1 is 16Ahead itself, as in the logo."""
    ticks = "".join(
        f'<g transform="rotate({i * 22.5} 50 50)"><line class="dial__tick" x1="50" y1="7" x2="50" y2="16"/>'
        f'<line class="dial__lit{" is-on" if i == 1 else ""}" x1="50" y1="3" x2="50" y2="19"/></g>'
        for i in range(16))
    return (f'<svg class="dial" viewBox="0 0 100 100" width="460" height="460" role="img" aria-label="The 16Ahead dial">{ticks}'
            '<text x="50" y="62" text-anchor="middle" font-weight="800" font-size="31" letter-spacing="-1.5">16</text></svg>')


def home():
    times ="".join(
        f'<div class="time"><span class="time__at">{t}</span>'
        f'<div class="time__you"><span class="label">You</span><b>{escape(you)}</b></div>'
        f'<div class="time__it"><span class="label">16Ahead</span><span>{escape(it)}</span></div></div>'
        for t, you, it in MORNING)
    moves = "".join(f'<div class="today__row"><span>{escape(m)}</span><i aria-hidden="true">Approve</i></div>' for m in MOVES)
    videos = [o for o in OVERNIGHT if (OUT / f"media/overnight-{o[0]}.mp4").exists()]

    def clip(slug, name):
        if not (OUT / f"media/overnight-{slug}.mp4").exists():
            return ''
        poster = f'/media/overnight-{slug}-poster.jpg?v={asset_version(f"media/overnight-{slug}-poster.jpg")}'
        return (f'<button class="run__play" type="button" data-title="{escape(name)}" '
                f'data-video="/media/overnight-{slug}.mp4?v={asset_version(f"media/overnight-{slug}.mp4")}" data-poster="{poster}">'
                f'<img src="{poster}" alt="" width="1280" height="720" loading="lazy">'
                f'<span class="run__cta">Watch it happen · 1:00</span><span class="visually-hidden">Play: {escape(name)}</span></button>')
    overnight = "".join(
        f'<article class="run"><div class="run__copy"><span class="run__n">{n}</span><h3>{escape(name)}</h3>'
        f'<div class="run__ask"><span class="label">Tell it</span><q>{escape(ask)}</q></div>'
        f'<div class="run__done"><span class="label">By morning</span><span>{escape(done)}</span></div></div>{clip(slug, name)}</article>'
        for n, (slug, name, ask, done) in enumerate(OVERNIGHT, 1))
    ladder = "".join(f'<div><b>{n}</b><span>{escape(x)}</span></div>' for n, x in LADDER)
    people = "".join(
        f'<div class="person"><b>{escape(who)}</b><div><span class="label">Your next move</span><span>{escape(move)}</span></div></div>'
        for who, move in PEOPLE)
    poster = f"/media/16ahead-story-poster.jpg?v={asset_version('media/16ahead-story-poster.jpg')}"
    body = f'''<section class="wrap hero">
  <div class="hero__copy">
    <span class="eyebrow">One login.</span>
    <h1><span class="hero__big">Tell it what you want done.</span><span class="hero__sub"><em>Wake up to it done.</em></span></h1>
    <div class="hero__actions">
      <a class="pill pill--blue" href="#mission">What's your mission?</a>
      <a class="pill pill--surface" href="#overnight">Watch it work</a>
    </div>
  </div>
  <div class="hero__dial">{dial()}</div>
</section>
<section class="overnight" id="overnight">
  <div class="wrap overnight__in">
  <div class="overnight__head">
    <span class="eyebrow">Overnight</span>
    <h2 class="h2">Three requests. Three mornings.</h2>
    <p>Sixteen apps hand the work to each other while you sleep. Watch each one happen.</p>
  </div>
  {overnight}
  </div>
  <dialog class="watch" aria-label="Video">
    <div class="watch__bar"><b></b><button type="button" class="watch__close">Close</button></div>
    <video controls playsinline preload="none" autofocus></video>
  </dialog>
</section>
<section class="morning" id="morning">
  <div class="wrap morning__in">
    <div class="morning__head">
      <span class="eyebrow">Your morning</span>
      <h2 class="h2">It's done. So what's next?</h2>
      <p>You wake up wondering what to do next. 16Ahead already knows.</p>
    </div>
    <video class="story" controls playsinline preload="none" poster="{poster}" aria-label="A one-minute walk through a morning with 16Ahead">
      <source src="/media/16ahead-story.mp4" type="video/mp4">
    </video>
    <div class="times">{times}</div>
    <div class="approve">
      <div class="approve__copy">
        <b>All you have to do is approve.</b>
        <span>Nothing goes out without you. Change anything you like, skip what you don't want, and approve the rest.</span>
      </div>
      <div class="today" aria-label="Example: today's moves">
        <div class="today__head"><b>Today's moves</b><span>{len(MOVES)} ready</span></div>
        {moves}
      </div>
    </div>
  </div>
</section>
<section class="wrap why" id="why">
  <div class="why__copy">
    <span class="eyebrow">Why sixteen</span>
    <h2 class="h2">Good players think a few moves ahead. 16Ahead thinks sixteen.</h2>
    <p>In chess, the player who sees further wins. Your competition is busy reacting to today. You'll already know what comes after it.</p>
  </div>
  <div class="ladder">{ladder}</div>
</section>
<section class="who" id="who">
  <div class="wrap who__in">
    <div class="who__head">
      <span class="eyebrow">Who it's for</span>
      <h2 class="h2">For people who can't afford to miss the next move.</h2>
    </div>
    <div class="people">{people}</div>
  </div>
</section>
<section class="mission" id="mission">
  <div class="mission__panel">
    <h2>What's your mission?</h2>
    <p>{DESCRIPTION}</p>
    <form action="{ASSISTANT_URL}" method="get">
      <input name="mission" type="text" placeholder="Land three new contracts by June" aria-label="Your mission" autocomplete="off">
      <button type="submit">Start</button>
    </form>
    <span class="mission__login">Already have an account? <a href="{SIGN_IN_URL}">Log in</a></span>
  </div>
</section>'''
    website = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "16Ahead",
               "publisher": {"@id": f"{SITE}/#organization"}}
    video = {"@type": "VideoObject", "name": "A morning with 16Ahead", "description": DESCRIPTION,
             "thumbnailUrl": f"{SITE}/media/16ahead-story-poster.jpg", "contentUrl": f"{SITE}/media/16ahead-story.mp4",
             "uploadDate": "2026-10-27", "duration": "PT1M"}
    clips = [{"@type": "VideoObject", "name": name, "description": f"Tell it: “{ask}” By morning: {done}",
              "thumbnailUrl": f"{SITE}/media/overnight-{slug}-poster.jpg", "contentUrl": f"{SITE}/media/overnight-{slug}.mp4",
              "uploadDate": date.fromtimestamp((OUT / f"media/overnight-{slug}.mp4").stat().st_mtime).isoformat(),
              "duration": "PT1M"} for slug, name, ask, done in videos]
    return page("/", f"16Ahead · {TAGLINE}", DESCRIPTION, body, [website, video] + clips)


def not_found():
    body = '''<section class="wrap nf">
  <span class="eyebrow">Error 404</span>
  <h1>This move isn't on the board.</h1>
  <p>The page moved or never existed.</p>
  <a class="pill pill--blue" href="/">Go to 16Ahead</a>
</section>'''
    return page("/404", "Page not found · 16Ahead", "This page moved or never existed.", body, robots="noindex")


def main():
    sync_menu()
    pages = {"index.html": home(), "404.html": not_found()}
    legal = legal_pages(ADDRESS, PHONE_DISPLAY, PHONE_TEL)
    for path, out, title, desc, body in legal:
        pages[out] = page(path, title.replace("| Taliferro Tech", "· 16Ahead"), desc, f'<div class="wrap">{body}</div>')
    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")
    urls = [("/", "1.0")] + [(l[0], "0.3") for l in legal]
    sitemap = "".join(f"  <url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n" for p, pr in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("built", len(pages), "pages + sitemap.xml into", OUT.name)


if __name__ == "__main__":
    main()
