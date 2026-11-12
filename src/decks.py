"""Investor decks, one source for both.

TEASER  -> public /deck (unlisted: noindex, not in the sitemap, linked from nowhere).
           Sent personally on first contact. No terms, financials, valuation or cap
           table, and no customer names (customers asked not to be named publicly).
FULL    -> the investor room only. Rendered to PNG slides + a PDF by
           tools/render_full_deck.sh into root/deck-private/ (never under public/),
           then uploaded to gs://taliferro-investor-room/docs/deck/.

Copy comes from investor-room-draft.md and the Oct 23, 2026 bank package (the
source of truth for numbers). Never describe customers by business size; say who
it's for. Slide sizes are in cqw so a slide scales to any width (1cqw = 16px at 1600).
"""
from html import escape as e

# ------------------------------------------------------------------ shared copy
# The story (founders, Nov 2026), same as 16ahead.com: one request, sixteen apps
# working as one, a complete result you approve, then the next move. Follow-up
# is the proof the engine works, not the headline.
PROBLEM = [
    ("Work falls between tools", "Every app does one piece. A person still carries the work from one to the next, and that's where it stalls."),
    ("One result takes many hands", "A launch, a proposal or a real answer needs research, writing, design and sending: several people or several tools."),
    ("Nobody knows what's next", "The next move lives in someone's head. When they're busy, it waits."),
]
PRODUCT = [
    ("One request, one plan", "Ask in plain words. 16Ahead turns the request into a plan of steps across its apps."),
    ("Sixteen apps, working as one", "The apps hand the work to each other: what Find discovers, Outreach uses, and Docs turns into a proposal."),
    ("A complete result, for your yes", "The work happens overnight. In the morning the result is ready to approve, and nothing goes out without a yes."),
    ("Always the next move", "Then it looks at everything in motion and lines up what should happen next."),
]
# The three requests on 16ahead.com (sixteen_ahead.py OVERNIGHT), shortened.
RUNS = [
    ("“Start a candle business called Ember & Oak.”", "Store live with products. Image Creator made the photos and logo, Docs wrote the terms, Social scheduled the first posts, SayIt made a brand jingle."),
    ("“Get our new product in front of 50 local boutiques.”", "Find and Lead Vault found the shops. Email Creator and Image Creator made a pitch and lookbook for each. Outreach sent them; the morning report shows who replied."),
    ("“Find out why customers stopped buying.”", "Pulse surveyed past customers, Docs wrote a report with the top three reasons, and Marketing Assistant drafted a win-back campaign for one-tap approval."),
]
PLANS = [
    ("Single app", "$4.99–$19.99 a month", "Anyone who wants one job done, such as outreach, social posts or documents. The low-cost way in."),
    ("16Ahead suite", "$99 a month", "Founders, owners and teams who want the work carried across every app. Where our customers are today."),
    ("Enterprise", "$5,000 a month", "A dedicated environment across departments, with roles, reports and its own data flows. Where we grow next."),
]
RESULTS = [
    ("+25%", "revenue with no new hires", "Seattle fireplace repair company"),
    ("−70%", "time spent on admin", "Same company"),
    ("+12%", "more bids won", "Commercial construction firm"),
    ("+40%", "vendor engagement from automated follow-ups", "Supplier-diversity consultancy"),
]
TEAM = [
    ("Tyrone Showers", "Co-founder and Chairman", "Decades leading data and systems work for AT&T, Accenture, Johnson & Johnson and public agencies."),
    ("Vikki Owens", "Co-founder and Strategic Advisor", "Certified Scrum Master and PMP who has delivered government and enterprise projects."),
    ("Ted Freeman", "President", ""),
    ("Booker Showers", "Chief Technical Advisor", ""),
]
MARKET = [
    ("$12.6B", "a year: every eligible US employer firm at our list prices"),
    ("1%", "our target share, about $126M a year in revenue"),
    ("6.4M", "US firms with 1–999 employees (Census Bureau, 2022)"),
]
COMPETE = [
    ("Chat assistants", "ChatGPT and others answer and draft. A person still carries the work into every other tool."),
    ("Automation tools", "Zapier, Make: connect apps, but someone has to design and maintain every workflow."),
    ("AI sales reps", "11x, Artisan, Regie.ai, AiSDR: one job, cold outreach for sales teams, from about $250 to $3,750+ a month."),
    ("16Ahead", "You ask in plain words. It plans the work, runs it across sixteen apps and brings back a complete result to approve. $99 a month."),
]
PROOF_TITLE = "The engine already does a job customers pay for"
PROOF_NOTE = ("Customers on the earlier version use it for prospecting and follow-ups: the same engine that now runs any request "
              "across sixteen apps. Every app exists because a paying customer asked for it.")
RISKS = [
    ("Revenue is early", "2026 revenue is $38,000 invoiced to three customers, and 74% of it comes from two of them."),
    ("Sales are founder-led", "We haven't yet shown a repeatable way to win customers without the founders selling."),
    ("A new category", "Customers understand a single app faster than sixteen working as one, so part of the job is education."),
    ("Focus", "Many apps compete for a small team's time. The raise is meant to fund that focus."),
    ("Key people", "The platform depends on its lead developer. A written succession plan names a successor and is being completed."),
]

# ------------------------------------------------------------------ the decks
# Each slide: (layout, data). Layouts are rendered by slide_html() below.
TEASER = [
    ("cover", {"kicker": "Investor overview · November 2026", "title": "16Ahead",
               "sub": "Tell it what you want done. Sixteen AI apps get it done.", "meta": "Taliferro Tech, LLC · Seattle, WA"}),
    ("cards", {"kicker": "The problem", "title": "Businesses have more tools than ever. The work still waits on people.", "cards": PROBLEM}),
    ("cards", {"kicker": "What 16Ahead does", "title": "One request. Sixteen AI apps. A result you approve.", "cards": PRODUCT}),
    ("compare", {"kicker": "See it work", "title": "Three requests, three complete results", "rows": RUNS,
                 "note": "Each one is a single request in plain words. Watch them run on 16ahead.com."}),
    ("stats", {"kicker": "Proof", "title": PROOF_TITLE, "stats": RESULTS, "note": PROOF_NOTE}),
    ("statement", {"kicker": "What we learned the hard way", "title": "A policy change nearly ended us. It showed us the engine is the product.",
                   "lede": "Our early customers were concentrated in supplier-diversity consulting. When federal programs were rolled back, most of them closed. The ones who stayed kept the engine running for them every day, so we rebuilt it to take any request, not any one industry's.",
                   "points": []}),
    ("stats", {"kicker": "Market", "title": "A $12.6B market, counted from the bottom up",
               "stats": [(v, l, "") for v, l in MARKET],
               "note": "US employer firms from the Census Bureau's Statistics of U.S. Businesses (2022) multiplied by our list prices. Not counted: businesses with no employees, firms with 1,000+ employees, and everything outside the US."}),
    ("compare", {"kicker": "Competition", "title": "Every other AI tool does one job. 16Ahead runs sixteen as one.", "rows": COMPETE}),
    ("plans", {"kicker": "Business model", "title": "Subscriptions in three plans that grow with the customer", "plans": PLANS,
               "note": "Add-ons such as extra contacts. Affiliates earn 15% of Enterprise payments, a referral channel for Enterprise."}),
    ("team", {"kicker": "Team", "title": "Operators who lived the problem", "people": TEAM}),
    ("close", {"kicker": "Next step", "title": "The investor room",
               "lede": "The terms, financials from our filed returns, the independent valuation and the cap table, behind a personal access code.",
               "cta": "Ask for access: info@taliferro.tech", "who": "Tyrone Showers, Co-founder and Chairman"}),
]

FULL = [
    ("ask", {"kicker": "01 · The ask", "title": "Raising $1.5M", "lede": "to take 16Ahead from working product to repeatable sales.",
             "tiles": [("Instrument", "SAFE"), ("Valuation cap", "$30M"), ("Minimum check", "$25,000"), ("Target close", "Dec 30, 2026")]}),
    ("cards", {"kicker": "02 · What 16Ahead does", "title": "One request. Sixteen AI apps. A result you approve.", "cards": PRODUCT}),
    ("compare", {"kicker": "03 · See it work", "title": "Three requests, three complete results", "rows": RUNS,
                 "note": "The videos of all three are on 16ahead.com."}),
    ("today", {"kicker": "04 · Where we are today", "title": "A working product, paid for without loans",
               "bars": [("2023", 60600, ""), ("2024", 81400, ""), ("2025", 0, "Building the platform"), ("2026 YTD", 38000, "Invoiced to Sept 30")],
               "stats": [("$0", "company debt"), ("$440,100", "contributed by the founders and 12 supporters, with no repayment terms"),
                         ("3", "customers invoiced in 2026, plus a $99/month suite subscriber")],
               "note": "2023–24: gross receipts, filed Form 1065. 2026: invoiced through September 30, internal records, unaudited."}),
    ("timeline", {"kicker": "05 · Customer history", "title": "Built to order, tested by a hard year",
                  "items": [("2023", "Customers paid us to build specific tools. We folded each one into a single codebase instead of handing it off."),
                            ("2024", "$81,400 in gross receipts, about $40,000 of it a Washington State consulting contract."),
                            ("2025", "Most of our supplier-diversity customers closed when federal programs were rolled back. The survivors kept the engine running, so we paused client work and rebuilt it to take any request."),
                            ("2026", "First product sales: $38,000 invoiced to three customers.")],
                  "note": "Customers who'll speak with you: a wealth manager for professional athletes, a flooring contractor, a supplier-diversity consultancy, a fireplace repair company and a commercial construction firm. Names on request."}),
    ("stats", {"kicker": "06 · Proof", "title": PROOF_TITLE, "stats": RESULTS,
               "note": "Results on the earlier version. Each of these customers has agreed to speak with investors."}),
    ("plans", {"kicker": "07 · Pricing and business model", "title": "Three plans that grow with the customer", "plans": PLANS,
               "note": "Add-ons such as extra contacts at $5 per 1,000 a month. Affiliates earn 15% of Enterprise payments."}),
    ("stats", {"kicker": "08 · Market", "title": "A $12.6B market, counted from the bottom up",
               "stats": [(v, l, "") for v, l in MARKET],
               "note": "Suite: 6,281,253 firms with 1–99 employees × $1,188 a year = $7.5B. Enterprise: 103,741 firms with 100–999 employees × $50,000 = $5.2B. Census Bureau SUSB 2022."}),
    ("cards", {"kicker": "09 · Product and roadmap", "title": "Sixteen apps on one engine",
               "cards": [("Live today", "General Assistant, Marketing Assistant, Find, Network, Moves, Outreach, Pulse, Docs, Social, Lead Vault, Email Creator, Email Signature, Image Creator and Store on the web. Find, Network, Outreach, Pulse and Docs on iOS."),
                         ("Next", "Move every current customer onto 16Ahead. iOS apps for Marketing Assistant and Moves (in development); SayIt and Social to follow."),
                         ("Why it compounds", "Every app runs on the same engine, so a new app doesn't need a new backend, every improvement reaches every app, and every request can use all sixteen.")]}),
    ("compare", {"kicker": "10 · Competition", "title": "Every other AI tool does one job. 16Ahead runs sixteen as one.", "rows": COMPETE,
                 "note": "AI sales rep pricing: 11x from about $3,750 a month (annual), Artisan around $2,000, Regie.ai $180–$499 per user, AiSDR about $250–$900. Vendor pages and reviews, November 2026."}),
    ("cards", {"kicker": "11 · Milestones", "title": "The next 90 days, and what the next round needs to see",
               "cards": [("Next 90 days", "Move every current customer onto 16Ahead. Measure each request from ask to approved result: results approved, time saved, replies and meetings. Convert free and lapsed accounts back to paid."),
                         ("Toward the next round", "Recurring revenue on a path to $1M a year, a repeatable way to win customers beyond founder sales, and requests that use more of the sixteen apps over time.")]}),
    ("table", {"kicker": "12 · Ownership and structure", "title": "Simple ownership, no debt",
               "head": ("Owner", "Role", "Ownership"),
               "rows": [("Tyrone Showers", "Co-founder", "49.39%"), ("Vikki Owens", "Co-founder", "49.39%"),
                        ("12 supporters", "Converted at an $18M valuation", "1.23%")],
               "note": "Taliferro Tech, LLC, Seattle. No loans, lines of credit or leases. Supporter conversion agreements are being signed. Independent indicative valuation: $18M–$30M (September 2026)."}),
    ("list", {"kicker": "13 · Risks", "title": "What could slow us down", "items": RISKS}),
]


def slide_title(slide):
    layout, d = slide
    return d.get("title", "")


def _cards(cards):
    return "".join(f'<div class="dk-card"><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in cards)


def slide_html(slide, n, total, confidential=False):
    layout, d = slide
    k = f'<span class="dk-kicker">{e(d["kicker"])}</span>' if d.get("kicker") else ""
    h = f'<h2 class="dk-title">{e(d["title"])}</h2>' if d.get("title") and layout not in ("cover", "ask", "close") else ""
    note = f'<p class="dk-note">{e(d["note"])}</p>' if d.get("note") else ""
    if layout == "cover":
        body = (f'{k}<h1 class="dk-hero">{e(d["title"])}</h1><p class="dk-sub">{e(d["sub"])}</p>'
                f'<p class="dk-meta">{e(d["meta"])}</p>')
    elif layout == "cards":
        body = f'{k}{h}<div class="dk-cards dk-cols-{len(d["cards"])}">{_cards(d["cards"])}</div>{note}'
    elif layout == "statement":
        pts = "".join(f"<li>{e(p)}</li>" for p in d.get("points", []))
        body = f'{k}<h2 class="dk-big">{e(d["title"])}</h2><p class="dk-lede">{e(d["lede"])}</p>' + (f'<ul class="dk-points">{pts}</ul>' if pts else "")
    elif layout == "stats":
        stats = "".join(f'<div class="dk-stat"><b>{e(v)}</b><span>{e(l)}</span>' + (f"<small>{e(s)}</small>" if s else "") + "</div>"
                        for v, l, s in d["stats"])
        body = f'{k}{h}<div class="dk-stats dk-cols-{len(d["stats"])}">{stats}</div>{note}'
    elif layout == "compare":
        rows = "".join(f'<div class="dk-row{" is-us" if t == "16Ahead" else ""}"><b>{e(t)}</b><span>{e(b)}</span></div>' for t, b in d["rows"])
        body = f'{k}{h}<div class="dk-rows">{rows}</div>{note}'
    elif layout == "plans":
        plans = "".join(f'<div class="dk-card"><span class="dk-kicker">{e(t)}</span><b class="dk-price">{e(p)}</b><p>{e(b)}</p></div>' for t, p, b in d["plans"])
        body = f'{k}{h}<div class="dk-cards dk-cols-3">{plans}</div>{note}'
    elif layout == "team":
        ppl = "".join(f'<div class="dk-card"><h3>{e(n_)}</h3><span class="dk-role">{e(r)}</span>' + (f"<p>{e(b)}</p>" if b else "") + "</div>"
                      for n_, r, b in d["people"])
        body = f'{k}{h}<div class="dk-cards dk-cols-4">{ppl}</div>'
    elif layout == "close":
        body = (f'{k}<h2 class="dk-big">{e(d["title"])}</h2><p class="dk-lede">{e(d["lede"])}</p>'
                f'<p class="dk-cta">{e(d["cta"])}</p><p class="dk-meta">{e(d["who"])}</p>')
    elif layout == "ask":
        tiles = "".join(f'<div class="dk-tile"><span class="dk-kicker">{e(a)}</span><b>{e(b)}</b></div>' for a, b in d["tiles"])
        body = f'{k}<h1 class="dk-hero dk-hero--ask">{e(d["title"])}</h1><p class="dk-sub">{e(d["lede"])}</p><div class="dk-tiles">{tiles}</div>'
    elif layout == "today":
        mx = max(v for _, v, _ in d["bars"]) or 1
        bars = "".join(f'<div class="dk-bar"><span class="dk-barval">${v:,}</span><i style="height:{(v / mx * 100) if v else 0:.0f}%"'
                       f'{" class=is-zero" if not v else ""}></i><b>{e(lab)}</b>' + (f"<small>{e(s)}</small>" if s else "") + "</div>"
                       for lab, v, s in d["bars"])
        stats = "".join(f'<div class="dk-stat dk-stat--row"><b>{e(v)}</b><span>{e(l)}</span></div>' for v, l in d["stats"])
        body = f'{k}{h}<div class="dk-split"><div class="dk-chart"><div class="dk-bars">{bars}</div></div><div class="dk-side">{stats}</div></div>{note}'
    elif layout == "timeline":
        items = "".join(f'<div class="dk-step"><b>{e(y)}</b><p>{e(t)}</p></div>' for y, t in d["items"])
        body = f'{k}{h}<div class="dk-steps">{items}</div>{note}'
    elif layout == "table":
        head = "".join(f"<th>{e(x)}</th>" for x in d["head"])
        rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in d["rows"])
        body = f'{k}{h}<table class="dk-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>{note}'
    elif layout == "list":
        items = "".join(f'<div class="dk-card dk-card--line"><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in d["items"])
        body = f'{k}{h}<div class="dk-cards dk-cols-{min(len(d["items"]), 3)} dk-wrap">{items}</div>{note}'
    else:
        raise ValueError(layout)
    foot = (f'<footer class="dk-foot"><span>16Ahead · Taliferro Tech{" · Confidential" if confidential else ""}</span>'
            f'<span>{n} / {total}</span></footer>')
    return f'<section class="dk-slide dk-{layout}" aria-label="Slide {n}: {e(slide_title(slide))}"><div class="dk-in">{body}</div>{foot}</section>'


def deck_html(slides, confidential=False):
    return "".join(slide_html(s, i + 1, len(slides), confidential) for i, s in enumerate(slides))


# ------------------------------------------------------------------ outputs
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEASER_PDF = "files/16ahead-investor-overview.pdf"


def teaser_page(icon, email, ver):
    """The public, unlisted /deck page (built by build.py, noindex, not in the sitemap)."""
    pdf = (ROOT / "public" / TEASER_PDF).exists()
    dl = (f'<a class="btn btn--surface" href="/{TEASER_PDF}" download>{icon("arrow")}Download PDF</a>' if pdf else "")
    body = f'''<link rel="stylesheet" href="/css/deck.css?v={ver}">
<div class="deck-page">
  <div class="deck-page__head">
    <div><span class="tag t-blue">Investor overview</span></div>
    <div class="actions">{dl}<a class="btn btn--primary" href="mailto:{email}?subject=Investor%20room%20access">{icon("mail")}Ask for room access</a></div>
  </div>
  {deck_html(TEASER)}
</div>'''
    return ("/deck", "deck.html", "16Ahead investor overview | Taliferro Tech",
            "16Ahead: sixteen apps working as one. An overview for investors.", body)


def write_private(out_dir):
    """Standalone HTML for headless Chrome: per-slide files for the room's PNGs, and
    print files for the PDFs. Lives outside public/, so it never deploys."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    css = (ROOT / "public" / "css" / "deck.css").read_text()
    shell = ('<!doctype html><html><head><meta charset="utf-8"><style>{css}'
             'html,body{{margin:0;background:#fff}}.dk-slide{{width:1600px;border-radius:0;box-shadow:none}}</style></head>'
             '<body class="deck-print">{body}</body></html>')
    for i, s in enumerate(FULL):
        (out / f"full-{i + 1:02d}.html").write_text(shell.format(css=css, body=slide_html(s, i + 1, len(FULL), True)))
    (out / "full-print.html").write_text(shell.format(css=css, body=deck_html(FULL, True)))
    (out / "teaser-print.html").write_text(shell.format(css=css, body=deck_html(TEASER)))
    return [slide_title(s) for s in FULL]


if __name__ == "__main__":
    import json, sys
    titles = write_private(sys.argv[1] if len(sys.argv) > 1 else ROOT / "deck-private")
    print(json.dumps(titles))
