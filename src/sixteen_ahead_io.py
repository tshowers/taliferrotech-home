#!/usr/bin/env python3
"""Builds 16ahead.io into ../public-16ahead-io (Firebase site `16ahead-io`).

One technical page: how a request becomes a Mission (the gate, the plan, the
capability catalog, the watchdog, the approval gate and the report). It is
Claude Design's design_handoff_16ahead_io, with the universal menu in the
header as on 16ahead.com. Copy is verbatim from the handoff; the engine it
describes is todd-backend/functions/orchestrator/.

    python3 src/sixteen_ahead_io.py

css/16ahead-io.css and js/16ahead-io.js are hand-written; edit them directly.
"""
import hashlib
import json
import shutil
from html import escape

from sixteen_ahead import (APP_URL, DESCRIPTION as HOME_DESCRIPTION, GROUP_URL, OUT as HOME_OUT, SIGN_IN_URL, UI)

SITE = "https://16ahead.io"
HOME = "https://16ahead.com"
GA_ID = "G-RM39WFG83C"  # same "16Ahead Home" stream as 16ahead.com; GA4 streams accept any domain
OUT = HOME_OUT.parent / "public-16ahead-io"
TITLE = "16Ahead · How it works"
DESCRIPTION = ("How 16Ahead turns every request into a Mission: a gate, a plan with an owner for every step, "
               "a watchdog that keeps work from sticking, an approval gate, and a report.")

ICONS = {
    "hub": ("01-16ahead", "16Ahead"), "ga": ("02-general-assistant", "General Assistant"),
    "ma": ("03-marketing-assistant", "Marketing Assistant"), "network": ("04-network", "Network"),
    "outreach": ("05-outreach", "Outreach"), "moves": ("06-moves", "Moves"), "docs": ("07-docs", "Docs"),
    "pulse": ("08-pulse", "Pulse"), "social": ("09-social", "Social"), "lv": ("10-lead-vault", "Lead Vault"),
    "find": ("11-find", "Find"), "sayit": ("12-sayit", "SayIt"), "ec": ("13-email-creator", "Email Creator"),
    "ic": ("14-image-creator", "Image Creator"), "sig": ("15-email-signature", "Email Signature"),
    "store": ("16-store", "Store"),
}
OWNERS = {"you": ("You", "you"), "ma": ("Marketing Assistant", "ma"), "hub": ("16Ahead", "hub")}

RULES = [
    ("1", "No work without a plan.", "Every Mission carries ordered steps, and each step says who does it."),
    ("2", "Nothing is ever stuck.", "Every step has a rule for when it counts as stuck and what happens next. When a step can't be done by software, it becomes a person's step with the reason. It never just fails."),
    ("3", "Every finished Move has a report.", "What was done, who did each step, when it happened and what came out of it."),
]
INPUTS = ["Contacts", "Documents", "Mail", "Surveys", "Signals"]
ENGINE = [
    ("Events", "A reply, an open, a signature, a new record."),
    ("Scheduled jobs", "Planning runs and the 30-minute watchdog."),
    ("LLM reasoning", "The gate, the planner and the drafts."),
    ("The approval gate", "Every send waits for your yes."),
]
KDD = [
    ("Knows", "your business", ["network", "lv", "docs", "find"]),
    ("Decides", "what's next", ["hub", "ga", "ma"]),
    ("Does it", "with your approval", ["outreach", "social", "moves", "pulse", "ec", "ic", "sig", "sayit", "store"]),
]
SIGNALS = [
    ("More than one product is involved", '"Prepare a proposal" needs Find, Network and Docs'),
    ("One step's output is the next step's input", "Research → who to contact → what to say"),
    ("A person has to do or approve part of it", "Approve a send, price a proposal, attend the meeting"),
    ("It waits on the world", "A reply, registrations, a signature, a date"),
    ("Success is an outcome, not an artifact", '"Get a meeting," "build next quarter\'s pipeline"'),
    ("Facts have to be gathered before deciding", '"What should I address this week?"'),
    ("No product can do part of it", "Analysing invoices: a person step plus a capability gap"),
]
DIRECTS = ["Make an image of a lighthouse", "What's this contact's email?", "Open my outbox"]
KINDS = [
    ("tool", "16Ahead or the Marketing Assistant runs a registered tool."),
    ("task", "A person does it. Done when they mark it, or when evidence shows up, like the document being uploaded."),
    ("approval", "A person says yes or no to something that was prepared for them."),
    ("wait", "Waits for an event, with a timeout. The output says which happened: replied, no reply, bounced."),
    ("decision", 'The plan needs one answer from a person, such as "Which Regina?"'),
]
STEP_CODE = '''{
  id: "route1",
  title: "Find Regina's best contact route",
  owner: "16ahead",        // "person" | "marketing" | "16ahead"
  kind: "tool",            // tool | task | approval | wait | decision
  tool: "network.findContactRoute",
  input: { person: "$step:who1.person" },
  dependsOn: ["who1"],
  when: "",                // e.g. "$step:watch1.outcome == 'no_reply'"
  doneWhen: "A verified email or a warm-intro path",
  stuckAfter: "P2D",       // ISO duration once runnable
  onStuck: "escalate",     // remind | replan | reassign | escalate
  whyNotMe: "",            // set when handed to a person
  status: "pending",       // pending | running | waiting | done | skipped | failed
  resultSummary: "",       // one line for the report
  finishedBy: null         // who actually did it
}'''
TOOL_CODE = '''{
  name: "network.findContactRoute",
  product: "network",
  lane: "16ahead",         // which assistant may run it
  does: "Finds a verified email or warm-intro path for a person",
  inputs: {...}, outputs: {...},   // typed, so $step: references are checked
  effect: "read",          // read | create | send | wait | change
  access: "direct",        // direct | approval | never
  counts: {...},           // allowance and cost counters
  wraps: ["GET /network/..."]      // the documented API operations it uses
}'''
PACKS = [
    ("network", "Who someone is, relationship history, enrichment, validation, warm-intro paths"),
    ("lv", "New people and companies to reach, verified emails"),
    ("find", "Research, news, watching for a change"),
    ("outreach", "Sending, follow-ups, reply, open and bounce tracking"),
    ("ec", "Designed HTML emails"),
    ("ic", "Images, reused from the library or generated"),
    ("ma", "Strategy, positioning, copy, the marketing plan as the referee"),
    ("social", "Posts, scheduling, engagement numbers"),
    ("docs", "Proposals, RFP work, reports, filing outputs"),
    ("pulse", "Surveys, client sentiment, the trigger for case studies or recovery"),
    ("moves", "Person steps: assignment, due dates, the project view"),
    ("ga", "The front door: where people ask, and where the plan comes back"),
    ("sayit", "Another channel to publish to, alongside Social"),
    ("sig", "Sender identity and branding on every send"),
]
# (n, owner, kind, title, done, branch)
STEPS = [
    ("1", "hub", "tool", "Work out which Regina Okafor", "One confident match. If ambiguous, step 1b.", False),
    ("1b", "you", "decision", '"Did you mean Regina Okafor at Brightline or at Coastal Health?"', "Only when step 1 was ambiguous.", True),
    ("2", "hub", "tool", "Find a contact route: Network, Lead Vault, warm intros", "A verified email or an intro path. If neither, step 2b.", False),
    ("2b", "you", "task", '"I couldn\'t find a deliverable address. Do you have one, or who could introduce you?"', "Only when there's no route.", True),
    ("3", "ma", "tool", "Strategy: why her, why now, the angle, the ask, the tone", "A one-paragraph strategy you can read.", False),
    ("4", "ma", "tool", "Header image", "A library image reused, or a new one generated.", False),
    ("5", "ma", "tool", "HTML email from the strategy and image", "Designed email saved to Docs.", False),
    ("6", "you", "approval", "Approve the email", "Approve, edit or reject. A rejection gets one revision with your note.", False),
    ("7", "hub", "tool", "Send", "The mail provider accepted it.", False),
    ("8", "hub", "wait", "Watch for a reply for 5 business days", "Replied, no reply or bounced, plus the real open and click data.", False),
    ("9a", "ma", "tool", "Draft a reply to her response", "When replied. Then approve and send.", True),
    ("9b", "ma", "tool", "Follow-up using the real open and click data", "When no reply. Then approve, send, watch again. At most 2 follow-ups.", True),
    ("9c", "hub", "replan", "That address bounced. Back to step 2 without it", "When bounced.", True),
    ("10", "hub", "report", "Report", "Always last.", False),
]
WATCH = [
    ("Person task overdue", "remind", "One nudge to the assignee. On the second miss, escalate to the project lead."),
    ("Tool step failed twice", "replan", "The remaining steps are rewritten around the failure: a different contact route, or a person step."),
    ("Wait step timed out", "branch", 'Not stuck. The timeout is an outcome, and the plan takes the "no reply" branch.'),
    ("Assignee gone", "reassign", "Removed or on leave: the step goes to the project lead, who is told why."),
    ("Waiting on an answer for 2+ days", "escalate", "Ask again once, then escalate."),
]
REPORT = [
    ("1", "Identified Regina Okafor (Brightline)", "16Ahead", "Oct 17 09:02"),
    ("2", "Contact route: verified email", "16Ahead", "Oct 17 09:03"),
    ("3", "Strategy written", "Marketing Assistant", "Oct 17 09:04"),
    ("5", "Email designed", "Marketing Assistant", "Oct 17 09:06"),
    ("6", "Approved with one edit", "You", "Oct 17 11:40"),
    ("8", "Opened Oct 18, no reply after 5 days", "16Ahead", "Oct 24"),
    ("9b", "Follow-up sent", "Marketing Assistant + You", "Oct 24"),
    ("8'", "Replied", "16Ahead", "Oct 26"),
]
LOOP = ["Observe a business condition or signal.", "Interpret what it means.", "Choose a course of action.",
        "Execute it safely.", "Measure the outcome.", "Adapt using the result."]


def e(text):
    return escape(text, quote=True)


def asset_version(rel):
    return hashlib.sha256((OUT / rel).read_bytes()).hexdigest()[:10]


def sync_menu():
    """The universal menu's static build, laid out as taliferro-ui/static/sync.sh does."""
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
        {"label": "The system", "icon": "grid", "url": f"{here}#system", "keywords": "inputs engine outputs"},
        {"label": "The gate", "icon": "target", "url": f"{here}#gate", "keywords": "orchestrate direct signals"},
        {"label": "The plan", "icon": "list", "url": f"{here}#plan", "keywords": "steps kinds owner"},
        {"label": "Capability catalog", "icon": "bolt", "url": f"{here}#catalog", "keywords": "tools products"},
        {"label": "Worked example", "icon": "mail", "url": f"{here}#example", "keywords": "regina email"},
        {"label": "Watchdog", "icon": "activity", "url": f"{here}#watchdog", "keywords": "stuck remind escalate"},
        {"label": "Approval gate", "icon": "shield", "url": f"{here}#approval", "keywords": "approve send"},
        {"label": "The report", "icon": "file", "url": f"{here}#report", "keywords": "receipt"},
    ]
    secondary = [
        {"label": "16ahead.com", "icon": "home", "url": HOME, "external": True, "keywords": "home landing"},
        {"label": "Terms", "icon": "file", "url": f"{HOME}/terms", "external": True, "keywords": "legal"},
        {"label": "Privacy", "icon": "shield", "url": f"{HOME}/privacy", "external": True, "keywords": "legal data"},
    ]
    return {"app": "todd", "name": "16Ahead", "items": items, "secondaryItems": secondary,
            "accountNote": "One 16Ahead account signs you in to every app.",
            "signInUrl": SIGN_IN_URL, "signInLabel": "Log in"}


def shell(path, title, description, body, extra_ld=None, robots="index,follow"):
    url = f"{SITE}{path}"
    org = {"@type": "Organization", "@id": f"{HOME}/#organization", "name": "16Ahead", "url": f"{HOME}/",
           "logo": f"{HOME}/img/16ahead-dial-1024.png", "description": HOME_DESCRIPTION,
           "parentOrganization": {"@type": "Organization", "name": "Taliferro Tech, LLC", "url": "https://taliferro.tech"}}
    graph = [org, {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": description,
                   "publisher": {"@id": f"{HOME}/#organization"}}] + (extra_ld or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)
    menu = json.dumps(menu_config(path == "/"), ensure_ascii=False)
    og_image = f"{SITE}/media/16ahead-io-poster.jpg"
    home_link = "#top" if path == "/" else "/"
    return f'''<!doctype html>
<html lang="en" class="light">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="16Ahead">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="720">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/tt/styles/universal-menu.css?v={asset_version("tt/styles/universal-menu.css")}">
<link rel="stylesheet" href="/css/16ahead-io.css?v={asset_version("css/16ahead-io.css")}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="{home_link}" aria-label="16Ahead.io home"><img src="/img/16ahead-dial-128.png" alt="" width="40" height="40"><span class="brand__name">16AHEAD</span><span class="brand__tld">.io</span></a>
    <nav class="hdr__nav" aria-label="Sections"><a href="/#system">System</a><a href="/#plan">Plan</a><a href="/#example">Example</a><a href="/#watchdog">Watchdog</a></nav>
    <div data-tt-menu></div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap ftr__in">
    <span class="ftr__brand"><img src="/img/16ahead-dial-128.png" alt="" width="28" height="28">16Ahead is a product of Taliferro Tech, LLC.</span>
    <nav aria-label="Footer"><a href="{HOME}">16ahead.com</a><a href="{HOME}/terms">Terms</a><a href="{HOME}/privacy">Privacy</a><a href="{GROUP_URL}">taliferro.com</a></nav>
  </div>
</footer>
<script>window.TT_MENU = {menu};</script>
<script src="/tt/universal-menu.js?v={asset_version("tt/universal-menu.js")}" defer></script>
<script src="/js/16ahead-io.js?v={asset_version("js/16ahead-io.js")}" defer></script>
</body>
</html>
'''


def icon(key):
    f, name = ICONS[key]
    return f'<img src="/img/products/{f}.svg" alt="{e(name)}" title="{e(name)}" width="28" height="28" loading="lazy">'


def tile(key):
    return f'<span class="tile">{icon(key)}</span>'


def owner_pill(key):
    label, cls = OWNERS[key]
    return f'<span class="owner owner--{cls}">{e(label)}</span>'


def home():
    rules = "".join(f'<div class="rule"><span class="rule__n">{n}</span><b>{e(t)}</b><span>{e(x)}</span></div>' for n, t, x in RULES)
    inputs = "".join(f'<span class="chip">{e(i)}</span>' for i in INPUTS)
    engine = "".join(f'<div class="engine__row"><b>{e(n)}</b><span>{e(x)}</span></div>' for n, x in ENGINE)
    kdd = "".join(
        f'<div class="kdd"><span class="kdd__head">{e(v)} <span>{e(w)}</span></span>'
        f'<div class="kdd__icons">{"".join(tile(k) for k in keys)}</div></div>'
        for v, w, keys in KDD)
    signals = "".join(f'<div class="signal"><b>{e(s)}</b><span>{e(x)}</span></div>' for s, x in SIGNALS)
    directs = "".join(f'<span class="chip chip--light">{e(d)}</span>' for d in DIRECTS)
    kinds = "".join(f'<div class="kind"><span class="kpill kpill--{k}">{k}</span><span>{e(x)}</span></div>' for k, x in KINDS)
    packs = "".join(
        f'<div class="pack"><span class="tile tile--lg">{icon(k)}</span><span class="pack__text"><b>{e(ICONS[k][1])}</b><span>{e(g)}</span></span></div>'
        for k, g in PACKS)
    legend = "".join(f'<span class="legend__item"><span class="dot dot--{cls}"></span>{e(label)}</span>' for label, cls in OWNERS.values())
    steps = "".join(
        f'<div class="step{" step--branch" if branch else ""}"><span class="step__n">{e(n)}</span>'
        f'<span class="step__main"><b>{e(title)}</b><span class="step__pills">{owner_pill(o)}<span class="kpill kpill--dark">{e(kind)}</span></span></span>'
        f'<span class="step__done">{e(done)}</span></div>'
        for n, o, kind, title, done, branch in STEPS)
    watch = "".join(f'<div class="watch"><b>{e(s)}</b><span class="watch__action">{e(a)}</span><span>{e(x)}</span></div>' for s, a, x in WATCH)
    report = "".join(
        f'<div class="rrow"><span class="rrow__n">{e(n)}</span><span>{e(t)}</span><span class="rrow__who">{e(w)} · {e(when)}</span></div>'
        for n, t, w, when in REPORT)
    loop = "".join(f'<div class="loop"><span class="loop__n">{i:02d}</span><b>{e(x)}</b></div>' for i, x in enumerate(LOOP, 1))
    mono = '<code class="inline">'
    poster = f"/media/16ahead-io-poster.jpg?v={asset_version('media/16ahead-io-poster.jpg')}"
    body = f'''<div id="top"></div>
<section class="wrap hero">
  <div class="hero__copy">
    <span class="eyebrow eyebrow--lg">How it works</span>
    <h1>Orchestration and context.</h1>
    <p>Every request to 16Ahead becomes a <strong>Mission</strong>: a plan of ordered steps. Each step says who does it: a person, the Marketing Assistant or 16Ahead. This page walks through how a Mission is planned, run, watched and reported.</p>
  </div>
  <div class="rules">{rules}</div>
</section>
<section class="wrap film" aria-label="Video: one Mission, start to finish">
  <video class="film__video" muted loop playsinline preload="metadata" poster="{poster}" aria-label="A one-minute walk through one Mission, from request to report" data-autoplay>
    <source src="/media/16ahead-io.mp4" type="video/mp4">
  </video>
</section>
<section id="system" class="band band--dark">
  <div class="wrap band__in">
    <div class="head">
      <span class="eyebrow eyebrow--dark">01 · The system</span>
      <h2 class="h2">Inputs, one engine, sixteen products.</h2>
      <p>16Ahead reads what is already happening in your business, decides what should happen next, and does it through the products, with your approval.</p>
    </div>
    <div class="grid grid--300 system">
      <div class="card card--dark"><span class="cap">Inputs</span><div class="chips">{inputs}</div></div>
      <div class="card card--panel"><span class="cap cap--blue">The engine</span><div class="engine">{engine}</div></div>
      <div class="card card--dark"><span class="cap">Outputs</span><div class="kdds">{kdd}</div></div>
    </div>
  </div>
</section>
<section id="gate" class="wrap band__in">
  <div class="head">
    <span class="eyebrow">02 · The gate</span>
    <h2 class="h2">Every request passes one gate.</h2>
    <p>A request can be typed to an assistant, made by creating a Move, or come from a signal or a schedule. One assessment call works out the outcome you want, then whether reaching it needs a plan. It does if any of these is true.</p>
  </div>
  <div class="grid grid--420 grid--start">
    <div class="list">{signals}</div>
    <div class="stack">
      <div class="callout"><b>When unsure, orchestrate.</b><span>A wrong "orchestrate" costs one planning call and produces a short plan. A wrong "direct" leaves work stuck at the first step one tool can't do.</span></div>
      <div class="card card--surface"><span class="cap">If none apply, it's direct</span><span class="muted-text">One tool, done now, no Mission.</span><div class="chips">{directs}</div></div>
    </div>
  </div>
  <div class="grid grid--340">
    <div class="tint tint--green"><span class="cap">Action Missions</span><b>End with something done in the world: an email sent, a meeting booked, a proposal submitted.</b></div>
    <div class="tint tint--violet"><span class="cap">Insight Missions</span><b>End with an answer, and the next Missions already planned. Each one starts with one click.</b></div>
  </div>
  <div class="note">
    <b>Not only requests.</b>
    <span>The same gate runs on things 16Ahead notices without being asked: a stuck step, an unhappy survey answer, a reply that comes in, a funding announcement Find is watching for. Some Missions start before anyone asks.</span>
  </div>
</section>
<section id="plan" class="band band--surface">
  <div class="wrap band__in">
    <div class="head">
      <span class="eyebrow">03 · The plan</span>
      <h2 class="h2">Every step has an owner and a rule for when it's stuck.</h2>
      <p>A plan is an ordered set of steps with dependencies. Each step is one of five kinds. A {mono}when</code> condition on earlier outputs makes branches possible: if they reply, do this; if not, follow up.</p>
    </div>
    <div class="grid grid--210 kinds">{kinds}</div>
    <div class="grid grid--420 grid--start">
      <pre class="code" aria-label="The shape of a step">{e(STEP_CODE)}</pre>
      <div class="notes">
        <div class="note"><b>One source of truth.</b><span>The Mission record holds the steps, outputs, its origin and who it's for. Every surface reads the same Mission through one shared plan strip. Records that start a Mission keep a small summary so lists never need a second read.</span></div>
        <div class="note"><b>Never planless.</b><span>A Mission starts in {mono}planning</code>. If planning fails or times out, it gets a one-step fallback: a task for the requester, "Plan this," with the reason attached. An outage can't block work.</span></div>
        <div class="note"><b>You can edit it.</b><span>Reorder, reassign an owner or delete a step. The plan is re-validated and the edit is recorded.</span></div>
      </div>
    </div>
  </div>
</section>
<section id="catalog" class="wrap band__in">
  <div class="grid grid--420 grid--start">
    <div class="head">
      <span class="eyebrow">04 · The capability catalog</span>
      <h2 class="h2">Plans are built from every product's tools.</h2>
      <p>Every tool in every product declares what it does, its typed inputs and outputs, its effect and its access level. A Move created in Moves can use Network, Find, Docs and Pulse in one plan. Adding a tool to any product makes it available to every Mission at once.</p>
      <p>The planner is given the two or three closest past plans as references and adapts them. When a Mission finishes well and nobody had to rework the plan much, it is saved as a new example for that business.</p>
    </div>
    <pre class="code" aria-label="The shape of a tool">{e(TOOL_CODE)}</pre>
  </div>
  <div class="packs">{packs}</div>
  <div class="cant">
    <div class="cant__copy">
      <span class="cap">Knowing when it can't</span>
      <b>It never invents a tool and never drops a step.</b>
      <span>When no tool can do a step, the step goes to a person with the reason written down. Each reason is counted, and the most frequent ones become the build list.</span>
    </div>
    <div class="cant__card">
      <div class="cant__meta">{owner_pill("you")}<code>task · whyNotMe</code></div>
      <b>"I can't sign documents. Send it through DocuSign and upload the signed copy."</b>
    </div>
  </div>
</section>
<section id="example" class="band band--dark">
  <div class="wrap band__in">
    <div class="head head--wide">
      <span class="eyebrow eyebrow--dark">05 · Worked example</span>
      <h2 class="h2">"Create an email I can send to Regina Okafor."</h2>
      <p>One sentence becomes a ten-step plan across Network, Find, the Marketing Assistant, Image Creator, Email Creator, Outreach and Docs. Two of the steps are yours.</p>
    </div>
    <div class="legend">{legend}</div>
    <div class="steps">{steps}</div>
    <p class="after">Step 9b drafts the follow-up from the real open and click data the wait step recorded. A follow-up never claims engagement that didn't happen.</p>
  </div>
</section>
<section id="watchdog" class="wrap band__in">
  <div class="grid grid--420 grid--end">
    <div class="head">
      <span class="eyebrow">06 · The watchdog</span>
      <h2 class="h2">Nothing stays stuck.</h2>
      <p>Every 30 minutes a scheduled job reads the Missions that are due for a check and acts on every step past its time limit.</p>
    </div>
    <div class="gauge"><span class="gauge__n">0</span><span class="gauge__text"><b>Stuck count</b><span>The watchdog's job is to keep this at zero. It's the gauge on the Moves cockpit.</span></span></div>
  </div>
  <div class="list">{watch}</div>
  <div class="note note--wide">
    <b>Waiting on a person is a state, not stuck.</b>
    <span>Signing a contract, attending a meeting or logging into a bid portal belongs to a person. That's fine as long as a named person has it, knows why, and the watchdog is tracking it. Work is stuck only when its current step has no owner, no next action, or is past due with nobody told. Every step is either a tool from one of the products or a named person with a reason. There is no third option.</span>
  </div>
</section>
<section id="approval" class="approval-wrap">
  <div class="approval">
    <div class="head">
      <span class="eyebrow eyebrow--onblue">07 · The approval gate</span>
      <h2 class="h2">Nothing goes out without you.</h2>
      <p>Every send is an approval step until you decide auto-send is ready. That is your call. Routine, reversible work happens on its own; approvals are for exceptions, risk, spend and policy limits.</p>
    </div>
    <div class="acard" aria-label="Example approval card">
      <div class="acard__top"><span class="cap">Step 6 · Waiting on you</span><span class="kpill kpill--approval">approval</span></div>
      <b>Approve the email to Regina Okafor</b>
      <div class="acard__btns" aria-hidden="true"><span class="fake fake--dark">Approve</span><span class="fake">Edit</span><span class="fake">Reject with a note</span></div>
      <span class="acard__note">A rejection sends it back for one revision with your note.</span>
    </div>
  </div>
</section>
<section id="report" class="wrap band__in">
  <div class="grid grid--420 grid--center report">
  <div class="head">
    <span class="eyebrow">08 · The report</span>
    <h2 class="h2">Every finished Move has a report.</h2>
    <p>When the last step finishes, the report lists what was done, who did each step, when, and what came out of it. The last line says how much was done for you and how little of your time it took.</p>
  </div>
  <div class="receipt">
    <div class="receipt__head"><b>Reach Regina Okafor · done in 9 days</b><span>Outcome: replied, meeting booked for Oct 30</span></div>
    <div class="receipt__rows">{report}</div>
    <b class="receipt__split">Split: 7 steps by 16Ahead and the Marketing Assistant, 2 by you. Your time: about 4 minutes.</b>
  </div>
  </div>
</section>
<section id="standard" class="band band--dark">
  <div class="wrap band__in">
    <div class="head head--wide">
      <span class="eyebrow eyebrow--dark">09 · The standard</span>
      <h2 class="h2">A feature that only reports information isn't finished.</h2>
      <p>Every capability answers one question: what work can 16Ahead complete without waiting for you? It is complete only when 16Ahead can do all six.</p>
    </div>
    <div class="grid grid--170">{loop}</div>
    <div class="grid grid--380">
      <div class="card card--dark"><span class="cap">An analyst says</span><b class="quote quote--muted">"LinkedIn engagement dropped 37%."</b></div>
      <div class="card card--panel"><span class="cap cap--blue">16Ahead says</span><b class="quote">"LinkedIn engagement dropped 37%. I analyzed the last 40 posts, found technical screenshots outperform quote cards, generated five replacement posts, scheduled them for Tuesday and Thursday, and will update the strategy after results come in."</b></div>
    </div>
  </div>
</section>
<section class="wrap cta">
  <h2>What's your mission?</h2>
  <p>{HOME_DESCRIPTION}</p>
  <div class="cta__btns"><a class="btn btn--blue" href="{APP_URL}">Start</a><a class="btn btn--surface" href="{HOME}">Back to 16ahead.com</a></div>
</section>'''
    video = {"@type": "VideoObject", "name": "One Mission, start to finish", "description": DESCRIPTION,
             "thumbnailUrl": f"{SITE}/media/16ahead-io-poster.jpg", "contentUrl": f"{SITE}/media/16ahead-io.mp4",
             "uploadDate": "2026-10-28", "duration": "PT1M"}
    tech = {"@type": "TechArticle", "headline": "Orchestration and context.", "description": DESCRIPTION,
            "url": f"{SITE}/", "publisher": {"@id": f"{HOME}/#organization"}}
    return shell("/", TITLE, DESCRIPTION, body, [video, tech])


def not_found():
    body = f'''<section class="wrap nf">
  <span class="eyebrow">Error 404</span>
  <h1>This step isn't in the plan.</h1>
  <p>The page moved or never existed.</p>
  <div class="cta__btns"><a class="btn btn--blue" href="/">How 16Ahead works</a><a class="btn btn--surface" href="{HOME}">16ahead.com</a></div>
</section>'''
    return shell("/404", "Page not found · 16Ahead", "This page moved or never existed.", body, robots="noindex")


def main():
    sync_menu()
    (OUT / "index.html").write_text(home(), encoding="utf-8")
    (OUT / "404.html").write_text(not_found(), encoding="utf-8")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE}/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>\n</urlset>\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("built index.html, 404.html, sitemap.xml into", OUT.name)


if __name__ == "__main__":
    main()
