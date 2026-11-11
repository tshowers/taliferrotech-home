"""Company pages: /careers (moved from TODD's old /help-wanted page).

The roles are part-time and remote-friendly; applications go by email. Don't put
product prices here - they change, and they have nothing to do with a job.
"""
from urllib.parse import quote

VIDEO_ID = "EJ8Rrg8-wU8"

WHY = [
    ("Real outcomes", "You ship work that creates motion. We favor clean delivery, tight feedback, and outcomes you can point to."),
    ("Flexible and part-time", "Work around your life. Show up with intent, ship in focused sprints, and keep momentum moving forward."),
    ("Experienced team", "40+ years of building at scale. You'll get clarity, mentorship, and a bar that pushes you to be remarkable."),
]

# (anchor, title, apply-subject, bullets, schema description)
ROLES = [
    ("ai-engineer", "AI Engineer", "AI Engineer", [
        "Build AI features that create motion: enrichment, NLP search, and automation.",
        "Ship models and prompts that reduce manual work and increase follow-through.",
        "Measure impact, iterate fast, and raise the bar. We'll train where needed.",
    ], "Design and deploy models for enrichment, NLP, and automation. Measure impact and ship ML features."),
    ("marketing-specialist", "Marketing & Social Media Specialist", "Marketing & Social", [
        "Turn stories into outcomes: pipeline, demos, trials, and retention.",
        "Ship content across LinkedIn, YouTube, and email with a tight feedback loop.",
        "Run experiments, read the numbers, and get coached into remarkable execution.",
    ], "Plan and run content tied to outcomes. Grow audience across channels; analyze performance."),
    ("customer-success-agent", "Customer Success Agent", "Customer Success", [
        "Guide users to wins fast: less confusion, more motion.",
        "Turn real feedback into shipped improvements and clearer workflows.",
        "Create help articles and short videos. We'll train you on the 16Ahead playbook.",
    ], "Onboard and train customers, capture feedback, and guide wins with 16Ahead."),
    ("corporate-sales-executive", "Corporate Sales Executive", "Corporate Sales", [
        "Commission-only, no cap: 10% of every sale you close, with bonuses for fast closes and multi-seat deals.",
        "Run focused discovery with decision-makers, connect outcomes to 16Ahead without feature dumping, and close cleanly.",
        "Forecast accurately and share learnings. We coach messaging and process; you bring intent and hustle.",
    ], "Develop and close B2B opportunities; forecast and report. Commission-only, 10% per sale."),
    ("executive-assistant", "Executive Assistant", "Executive Assistant", [
        "Own scheduling, correspondence, and prep that keeps momentum tight.",
        "Turn loose ends into clear follow-ups and shipped decisions.",
        "Handle confidential information with care. We'll train you on our operating rhythm.",
    ], "Own scheduling, correspondence, and prep for key meetings; keep projects moving."),
    ("trainer", "Trainer", "Trainer", [
        "Create simple learning paths that help users ship wins fast.",
        "Run live and recorded sessions; keep it clear, calm, and practical.",
        "Measure comprehension and improve the curriculum. We'll train you on the product.",
    ], "Create learning paths; run live and recorded sessions; measure comprehension."),
    ("vp-marketing", "VP of Marketing", "VP of Marketing", [
        "Own narrative and growth with a remarkable standard and clear metrics.",
        "Launch 16Ahead's Business Momentum System positioning and drive pipeline without fluff.",
        "Lead PR and thought leadership; coach the team into consistent shipping.",
    ], "Own narrative and growth across channels; launch Business Momentum System positioning; drive pipeline."),
]

BENEFITS = [
    ("Remote-friendly", "Work from anywhere with clear goals, strong writing, and a bias toward shipping."),
    ("Flexible hours", "We care about outcomes. Show intent, deliver, repeat."),
    ("Mentorship", "Direct access to senior builders. If you want to be remarkable, we'll help you get there."),
]

APPLY_STEPS = [
    ("Email us", "Put the role you want in the subject line."),
    ("Attach your work", "A short resume or portfolio. Links are great."),
    ("Tell us what you shipped", "In 4-6 sentences, describe a project you shipped and its outcome."),
]

FAQ = [
    ("Are the roles remote?", "Yes, most roles are remote-friendly. If we need you onsite, we'll say so in the offer."),
    ("Are these part-time?", "Yes. We schedule around your availability and set clear deliverables."),
    ("What's the interview process?", "A short intro call, a practical exercise, then a debrief. Fast and respectful."),
    ("Do I need industry experience?", "Helpful, not required. Show us work you've shipped and how you think."),
]


def apply_mailto(email, subject):
    return f"mailto:{email}?subject={quote('Application - ' + subject)}"


def careers(icon, email, site):
    why = "".join(f'<div class="feat"><h3>{t}</h3><p>{d}</p></div>' for t, d in WHY)
    roles = "".join(
        f'<div class="feat role" id="{a}"><h3>{t}</h3><ul>{"".join(f"<li>{b}</li>" for b in bullets)}</ul>'
        f'<a class="btn btn--primary btn--sm" href="{apply_mailto(email, s)}">{icon("mail", 16)}Apply</a></div>'
        for a, t, s, bullets, _ in ROLES)
    benefits = "".join(f'<div class="feat"><h3>{t}</h3><p>{d}</p></div>' for t, d in BENEFITS)
    steps = "".join(f'<li><span class="num">{i + 1}</span><span><b>{t}</b><span>{d}</span></span></li>'
                    for i, (t, d) in enumerate(APPLY_STEPS))
    faq = "".join(f'<details class="qa"><summary>{q}{icon("chev", 16, "i qa__chev")}</summary><p>{a}</p></details>' for q, a in FAQ)
    general = apply_mailto(email, "Taliferro Tech")

    body = f'''<section class="phero">
  <div class="phero__copy">
    <span class="tag t-violet">Careers · Built for the Remarkable</span>
    <h1 class="display display--md">Build with Taliferro Tech</h1>
    <p class="lede">If you move with intent, you belong here. Part-time roles, flexible hours, real impact. Help build 16Ahead, the Business Momentum System for teams that want progress, not paperwork.</p>
    <p class="lede">Not there yet? We train you. If you want to be remarkable, you can belong here.</p>
    <div class="actions"><a class="btn btn--primary" href="#open-roles">See open roles</a><a class="btn btn--surface" href="#apply">How to apply</a></div>
  </div>
</section>
<section class="section section--narrow">
  <div class="video"><iframe title="The Remarkable Standard" src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
</section>
<section class="section section--narrow" id="why-taliferro">
  <span class="kicker">Why work here</span>
  <h2 class="h2 h2--sm">Build with remarkable people</h2>
  <p class="lede">We hire for intent. If you already ship work people feel, you'll thrive. If you're hungry and coachable, we'll train you.</p>
  <div class="feats">{why}</div>
</section>
<section class="section section--narrow" id="open-roles">
  <span class="kicker">Open roles</span>
  <h2 class="h2 h2--sm">Part-time positions now hiring</h2>
  <p class="lede">All roles are part-time with flexible hours, and remote-friendly unless noted.</p>
  <div class="feats">{roles}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">Benefits</span>
  <h2 class="h2 h2--sm">What you get</h2>
  <div class="feats">{benefits}</div>
</section>
<section class="section section--narrow" id="apply">
  <div class="steps"><span class="kicker">How to apply</span><ol>{steps}</ol>
    <div class="actions"><a class="btn btn--primary" href="{general}">{icon("mail")}Email {email}</a></div>
  </div>
</section>
<section class="section section--narrow">
  <h2 class="h2 h2--sm">Hiring questions</h2>
  <div class="faq">{faq}</div>
</section>
<section class="panel panel--row">
  <div class="panel__copy"><h2 class="h2 h2--sm">Ready to be remarkable?</h2><p>Ship work people feel. Create motion.</p></div>
  <a class="btn btn--primary btn--lg" href="{general}">{icon("mail")}Apply now</a>
</section>'''

    org = {"@id": f"{site}/#organization"}
    jobs = {"@type": "ItemList", "name": "Taliferro Tech open roles", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {
            "@type": "JobPosting", "title": t, "description": desc, "employmentType": "PART_TIME",
            "datePosted": "2026-10-07", "validThrough": "2027-10-07", "hiringOrganization": org,
            "jobLocationType": "TELECOMMUTE",
            "applicantLocationRequirements": {"@type": "Country", "name": "United States"},
            "url": f"{site}/careers#{a}",
            "identifier": {"@type": "PropertyValue", "name": "Taliferro Tech", "value": a}}}
        for i, (a, t, _, _, desc) in enumerate(ROLES)]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return ("/careers", "careers.html", "Careers | Taliferro Tech",
            "Part-time, remote-friendly roles at Taliferro Tech: AI engineering, marketing, customer success, sales, executive support, training and marketing leadership.",
            body, [jobs, faq_ld])


# ---------------------------------------------------------------- /investors
# Public "why talk to us" page (replaces TODD's /investor-relations and
# /investment-overview). Keep it general: no valuation, traction numbers,
# pricing, round size, terms, named pending contracts or promised returns -
# those go one-to-one, by email, after a conversation.

# The story (Nov 2026, founders): sixteen apps orchestrated into one result you
# approve in the morning, plus "what's next" (16 steps ahead). Follow-up is the
# proof that the engine works, not the headline. Never describe customers by size
# ("small business" etc.): say who it's for instead (founders, Nov 2026).
PROBLEM = [
    ("Work falls between tools", "Every app does one piece. A person still has to carry the work from one to the next, and that's where it stalls."),
    ("Nobody knows what's next", "The next move lives in someone's head. When they're busy, it waits."),
    ("Opportunities go cold", "The lead from three weeks ago never hears back. The quote nobody chased goes to someone else."),
]

BUILT = [
    ("One request, sixteen apps", "Tell 16Ahead what you want done. It turns the request into a plan, and its apps hand the work to each other: what Find discovers, Outreach uses, and Docs turns into a proposal."),
    ("Ready for your yes", "The work happens overnight. In the morning the result is waiting for approval, and nothing goes out without it."),
    ("Always the next move", "16Ahead looks at everything in motion and lines up what should happen next, so you stay sixteen steps ahead instead of one."),
]

PROOF = [
    ("Built to order", "From 2023, customers paid us to build specific tools. Instead of handing each one off, we folded them into one codebase until it was a product. Every app exists because a customer asked for it."),
    ("Tested by a hard year", "Our first customers were concentrated in supplier-diversity consulting. When federal policy changed, much of that market closed, and so did most of those customers."),
    ("Proven on follow-through", "The customers who stayed use it for the same result: no lead or quote goes cold. The same engine that keeps their follow-ups moving runs every request across all sixteen apps."),
]

WHY_NOW = [
    ("AI can finally act", "Models are now reliable enough to draft, send and update real systems, not just answer questions."),
    ("Single-purpose AI is everywhere", "AI tools that each do one job are multiplying. Businesses don't need more tools. They need the work carried across them."),
    ("The spend already exists", "Businesses already pay for this work through hires, agencies and software. 16Ahead does it for a subscription."),
]

LOOKING_FOR = [
    ("Investors", "People who back focused, capital-efficient teams and can help us reach the businesses that need follow-through, not just fund us."),
    ("Strategic partners", "Organizations that serve businesses and want to offer them results, not another tool."),
    ("Introductions", "To customers, channel partners and advisors who make the next step faster."),
]

# (name, role, sketch in /img/team/). The 1024px originals sit beside the
# 192px WebP copies used here: cwebp -q 85 -resize 192 192 <name>.png -o <name>-192.webp
TEAM = [
    ("Tyrone Showers", "Co-founder and Chairman", "tyrone-showers"),
    ("Vikki Owens", "Co-founder and Strategic Advisor", "vikki-owens"),
    ("Ted Freeman", "President", "ted-freeman"),
    ("Booker Showers", "Chief Technical Advisor", "booker"),
]


def investors(icon, email, site):
    talk = f"mailto:{email}?subject={quote('Investor conversation')}&body={quote('Name:' + chr(10) + 'Firm / role:' + chr(10) + 'What you would like to talk about:' + chr(10))}"
    cards = lambda rows: "".join(f'<div class="feat"><h3>{t}</h3><p>{d}</p></div>' for t, d in rows)
    people = "".join(
        f'<div class="feat feat--person"><img class="person__photo" src="/img/team/{img}-192.webp" alt="Sketch of {name}" '
        f'width="72" height="72" loading="lazy"><span><h3>{name}</h3><p>{role}</p></span></div>'
        for name, role, img in TEAM)
    body = f'''<section class="phero">
  <div class="phero__copy">
    <span class="tag t-blue">Investors</span>
    <h1 class="display display--md">Sixteen apps working as one</h1>
    <p class="lede">Tell 16Ahead (formerly TODD) what you want done. Overnight, its sixteen apps plan the work and hand it to each other, and in the morning the result is ready for your approval. Then it shows you what's next, so you stay sixteen steps ahead.</p>
    <div class="actions"><a class="btn btn--primary" href="{talk}">{icon("mail")}Start a conversation</a></div>
  </div>
</section>
<section class="section section--narrow">
  <span class="kicker">The problem</span>
  <h2 class="h2 h2--sm">Businesses have more tools than ever. The work still waits on people.</h2>
  <div class="feats">{cards(PROBLEM)}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">What's different</span>
  <h2 class="h2 h2--sm">Every other AI tool does one job. 16Ahead runs sixteen as one.</h2>
  <div class="feats">{cards(BUILT)}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">Proof</span>
  <h2 class="h2 h2--sm">Already producing results customers pay for</h2>
  <div class="feats">{cards(PROOF)}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">Why now</span>
  <h2 class="h2 h2--sm">The moment for software that carries the work</h2>
  <div class="feats">{cards(WHY_NOW)}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">Who we want to talk to</span>
  <h2 class="h2 h2--sm">Capital and connections that move us faster</h2>
  <div class="feats">{cards(LOOKING_FOR)}</div>
</section>
<section class="section section--narrow">
  <span class="kicker">Leadership</span>
  <h2 class="h2 h2--sm">Operators who lived the problem</h2>
  <p class="lede">Twenty-five years of building toward this, from webwareLive in 2000 to 16Ahead today.</p>
  <div class="feats">{people}</div>
</section>
<section class="panel panel--row">
  <div class="panel__copy"><h2 class="h2 h2--sm">Let's talk.</h2><p>Tell us who you are and what you're looking for. We'll follow up with the full story, customer references and a time to meet.</p></div>
  <a class="btn btn--primary btn--lg" href="{talk}">{icon("mail")}Start a conversation</a>
</section>'''
    return ("/investors", "investors.html", "Investors | Taliferro Tech",
            "Sixteen apps working as one: tell 16Ahead what you want done, approve the result in the morning, and always know what's next. Taliferro Tech is talking with investors and partners.",
            body, [])


# ---------------------------------------------------------------- /investor-room
# Password-gated videos for investors we've already talked to. The page holds no
# video URLs: js/investor-room.js posts the password to /api/investor-room (the
# investorRoom function in functions/), which returns two-hour signed links to
# the private gs://taliferro-investor-room bucket. Noindex and out of the sitemap.

def investor_room(icon, email):
    ask = f"mailto:{email}?subject={quote('Investor room access')}"
    body = f'''<section class="phero">
  <div class="phero__copy">
    <span class="tag t-blue">Investors</span>
    <h1 class="display display--md">Investor room</h1>
    <p class="lede">Private videos for investors we're in conversation with. Enter the password from your invitation.</p>
    <form class="room__gate" id="room-gate" autocomplete="off">
      <label class="room__field">{icon("lock")}<input type="password" name="password" placeholder="Password" aria-label="Password" required autocomplete="current-password"></label>
      <button class="btn btn--primary" type="submit">Open</button>
    </form>
    <p class="note" id="room-status" role="status"></p>
    <p class="note">No password? <a href="{ask}">Ask us for access</a>.</p>
  </div>
</section>
<section class="section section--narrow room__videos" id="room-videos" hidden></section>
<script src="/js/investor-room.js" defer></script>'''
    return ("/investor-room", "investor-room.html", "Investor room | Taliferro Tech",
            "Private investor videos from Taliferro Tech.", body)
