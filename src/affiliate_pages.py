"""TODD affiliate program pages: /affiliates, /affiliates/how-earnings-work and
/affiliates/terms (Claude Design handoff "Affiliate and Pricing", screens
21-23). Each page ships both designed layouts, a and b; the Layout toggle in
js/site.js switches them and remembers the choice.

Program numbers are fixed in the TODD backend (affiliateTrackingService.js,
affiliateCommission.service.js). Keep this copy in step with them, never
promise a payout schedule or payment method. The headline's earnings claim
($5,000 a month = about 7 clients at 15% of the $5,000/month Enterprise price)
must keep its qualifier next to it, and must be updated if the Enterprise price
in Stripe (STRIPE_ENTERPRISE_PRICE_ID) changes. The Terms text in affiliate_terms.html is
legal text - restyle only.
"""
import re
from pathlib import Path

TERMS_HTML = (Path(__file__).resolve().parent / "affiliate_terms.html").read_text(encoding="utf-8")

RULES = [
    ("visitors", "Visitors", "1¢ each · up to 500 a day", "eye", "blue",
     "You earn 1¢ for every unique visitor your link sends to TODD, for up to 500 visitors a day. The same person "
     "visiting again within 30 days doesn't count twice, and search engines, link previews and other automated "
     "traffic don't count. Visitors over the daily cap still count toward your bonus goal."),
    ("bonus", "The $100 bonus", "Unlocks at a goal", "gift", "yellow",
     "Every affiliate starts with a one-time $100 bonus. It stays locked until you reach 10,000 unique visitors or "
     "$100 in commission, whichever comes first, and then it's added to your available balance. Visitors and "
     "commission from before the bonus started count, and once it unlocks it stays unlocked. If you already "
     "received our earlier 100-visitor $100 bonus, that was your bonus."),
    ("enterprise", "Enterprise commission", "15% of every monthly payment", "dollar", "green",
     "When someone you referred subscribes to TODD Enterprise, you earn 15% of every monthly payment, for as long "
     "as they keep paying. Setup and customization hours are billed separately and don't earn commission."),
    ("products", "Other TODD products", "15% of the first payment", "brief", "cyan",
     "For Network, Pulse, Moves, Outreach, Docs and Social, you earn 15% of each new subscriber's first payment, "
     "whether they buy on the web or in the App Store. For App Store purchases, 15% is of the full price, before "
     "Apple's fee. Renewals don't earn more."),
    ("credit", "Who gets credit", "30 days · first click wins", "clock", "violet",
     "A visitor counts as yours for 30 days after they click your link, on every TODD site. If they clicked more "
     "than one affiliate link, the first click wins. They need to create a new TODD account and buy (or start a "
     "free trial) within those 30 days. If they start a free trial in time, you're paid when their first real "
     "payment goes through."),
    ("refunds", "Refunds", "Commission is reversed", "undo", "pink",
     "If a payment that earned you commission is refunded, the commission on that payment is removed from your "
     "balance."),
]

GOOD_TO_KNOW = [
    "Only new accounts can be credited to you. Someone who already had a TODD account before clicking your link isn't counted as your referral.",
    "You can't earn from referring yourself.",
    "If someone taps your link but then signs up only inside a TODD iPhone app, we can't connect them to you yet. Ask them to create their account on the website first.",
    "App Store purchases in currencies other than US dollars are reviewed and credited by hand, so they may take longer to appear.",
    "Taliferro may occasionally add to or correct a balance; those show as adjustments on your dashboard.",
]

PROGRAM_RULES = [
    ("1¢", "per visitor, up to 500 a day"),
    ("$100", "bonus at 10,000 visitors or $100 in commission"),
    ("15%", "of every Enterprise monthly payment"),
    ("30 days", "credit window, first click wins"),
]

STEPS = [
    ("Join", "Sign up with your email address on todd.taliferro.tech."),
    ("Copy your link", "Program Materials builds your link and ready-to-send emails."),
    ("Share and track", "Your dashboard shows visitors, your bonus progress and your balance."),
]


def layout_toggle():
    return ('<div class="layout-toggle" role="group" aria-label="Page layout"><span>Layout</span>'
            '<button type="button" data-set-layout="a" aria-pressed="true">A</button>'
            '<button type="button" data-set-layout="b" aria-pressed="false">B</button></div>')


def section_titles():
    return [(f"terms-{i + 1}", re.sub(r"<[^>]+>", "", t).strip())
            for i, t in enumerate(re.findall(r'<h2><span class="tc-num"[^>]*>\d+</span>(.*?)</h2>', TERMS_HTML))]


def pages(icon, todd_url, phone_display, phone_tel):
    join = f"{todd_url}/affiliate-signup"
    sign_in = f"{todd_url}/affiliate-sign-in"
    dashboard = f"{todd_url}/affiliate-dashboard"
    materials = f"{todd_url}/program-materials"
    ext = icon("ext", 14)

    # ------------------------------------------------------------ 21 overview
    steps = "".join(f'<div class="aff-step"><span class="aff-step__n">{i + 1}</span><div><h3>{t}</h3><p>{d}</p></div></div>'
                    for i, (t, d) in enumerate(STEPS))
    chips = "".join(f'<div class="aff-rule"><b>{v}</b><span>{l}</span></div>' for v, l in PROGRAM_RULES)
    journey = "".join(
        f'<div class="aff-journey__row"><span class="aff-ichip t-{tint}">{icon(k, 22)}</span>'
        f'<span><b>{t}</b><span>{d}</span></span><b class="aff-journey__v">{v}</b></div>'
        for k, tint, t, d, v in [
            ("eye", "blue", "A visitor clicks your link", "Counted as yours for 30 days. First click wins.", "1¢"),
            ("gift", "yellow", "You reach a goal", "10,000 visitors or $100 in commission unlocks the bonus.", "$100"),
            ("dollar", "green", "They buy Enterprise", "You earn 15% of every monthly payment.", "15%")])
    overview = f'''<div class="aff" data-layout-key="affiliates" data-layout="a">
<div class="aff-a">
  <section class="aff-hero">
    <span class="tag t-cyan">TODD Affiliate Program</span>
    <h1 class="display">Earn up to $5,000 a month sharing TODD.</h1>
    <p class="aff-qualifier">It takes about 7 active Enterprise clients. Each one pays you $750 a month: 15% of their $5,000 monthly payment.</p>
    <p class="lede">Send people to TODD with your own link. You earn for every visitor, unlock a bonus when you reach a goal, and earn a commission when someone you referred buys.</p>
    <div class="actions"><a class="btn btn--primary" href="{join}">Join the program{icon("arrow", 16)}</a><a class="btn btn--surface" href="/affiliates/how-earnings-work">How earnings work</a></div>
  </section>
  <section class="aff-tiles" aria-label="What you earn">
    <div class="aff-tile t-blue"><span class="kicker kicker--tint">Per visitor</span><b>1¢</b><p>For every new visitor your link sends, up to 500 a day.</p></div>
    <div class="aff-tile t-yellow"><span class="kicker kicker--tint">Bonus</span><b>$100</b><p>Unlocks when you reach 10,000 visitors or $100 in commission.</p></div>
    <div class="aff-tile t-green"><span class="kicker kicker--tint">Enterprise</span><b>15%</b><p>Of every monthly payment, for as long as a client you referred stays on Enterprise.</p></div>
  </section>
  <section class="section"><h2 class="h2">How it works</h2><div class="aff-steps">{steps}</div></section>
  <section class="panel panel--row">
    <div class="panel__copy"><h2 class="h2 h2--sm">Questions before you join?</h2><p>Call us. Already an affiliate? <a class="aff-link" href="{sign_in}">Sign in</a>.</p></div>
    <a class="btn btn--bg" href="tel:{phone_tel}">{icon("phone")}{phone_display}</a>
  </section>
</div>
<div class="aff-b">
  <section class="aff-split">
    <div class="aff-split__copy">
      <span class="kicker">TODD Affiliate Program</span>
      <h1 class="display display--md">Share a link. Earn up to $5,000 a month.</h1>
      <p class="aff-qualifier">It takes about 7 active Enterprise clients. Each one pays you $750 a month: 15% of their $5,000 monthly payment.</p>
      <p class="lede">Every visitor earns you a cent. Reach a goal and a $100 bonus unlocks. If someone you sent buys Enterprise, you earn 15% of every monthly payment they make.</p>
      <div class="actions"><a class="btn btn--primary" href="{join}">Join the program{icon("arrow", 16)}</a><a class="btn" href="{sign_in}">Sign in</a></div>
    </div>
    <div class="aff-journey"><span class="kicker">One referral, start to finish</span>{journey}</div>
  </section>
  <section class="aff-rules" aria-label="Program rules">{chips}</section>
  <section class="aff-invert">
    <h2>Join with your email address. Your link is ready right after.</h2>
    <div class="actions"><a class="btn btn--sm aff-outline" href="tel:{phone_tel}">{icon("phone")}{phone_display}</a><a class="btn btn--sm btn--primary" href="{join}">Join</a></div>
  </section>
</div>
{layout_toggle()}
</div>'''

    # ------------------------------------------------------ 22 how it works
    rail = "".join(f'<a href="#{rid}">{t}</a>' for rid, t, *_ in RULES) + '<a href="#good-to-know">Good to know</a>'
    know = "".join(f"<li>{x}</li>" for x in GOOD_TO_KNOW)
    know_block = (f'<ul class="aff-know">{know}</ul><p class="aff-small">The full rules are in the Affiliate Program Earnings '
                  f'section of the <a class="aff-link" href="/affiliates/terms">Affiliate Terms and Conditions</a>.</p>')
    rules_a = "".join(
        f'<section class="aff-ruleblock" id="{rid}"><span class="aff-ichip aff-ichip--52 t-{tint}">{icon(k, 26)}</span>'
        f'<div><h2>{t} <small>{tag}</small></h2><p>{body}</p></div></section>'
        for rid, t, tag, k, tint, body in RULES)
    rules_b = "".join(
        f'<section class="aff-rulecard" id="b-{rid}"><div class="aff-rulecard__head"><span class="aff-ichip aff-ichip--36 t-{tint}">{icon(k, 18)}</span>'
        f'<h2>{t}</h2><span class="aff-rulecard__tag">{tag}</span></div><p>{body}</p></section>'
        for rid, t, tag, k, tint, body in RULES)
    path_steps = "".join(
        f'<li><span class="aff-ichip aff-ichip--56 t-{tint}">{icon(k, 24)}</span><span class="kicker">{w}</span><b>{t}</b><p>{d}</p></li>'
        for k, tint, w, t, d in [
            ("eye", "blue", "Day 0", "They click your link", "You earn 1¢ for the visit. The 30-day window starts."),
            ("clock", "violet", "Within 30 days", "They sign up", "If they clicked another affiliate first, that affiliate gets the credit."),
            ("brief", "yellow", "Every month", "They pay for Enterprise", "Only the Enterprise line counts. Setup hours are billed separately."),
            ("dollar", "green", "You earn", "15% of each payment", "Every month they pay, for as long as they stay.")])
    how = f'''<div class="aff" data-layout-key="affiliates-how" data-layout="a">
<div class="aff-a aff-how">
  <nav class="aff-rail" aria-label="On this page"><span class="kicker">On this page</span>{rail}
    <span class="aff-rail__apps"><a class="aff-link" href="{dashboard}">Your dashboard{ext}</a><a class="aff-link" href="{materials}">Program materials{ext}</a></span></nav>
  <article class="aff-col">
    <h1 class="display display--md">How earnings work</h1>
    <p class="lede">There are three ways to earn: visitors, a one-time bonus and commission when someone you referred buys. Here is exactly how each one is counted.</p>
    {rules_a}
    <section class="aff-ruleblock" id="good-to-know"><span class="aff-ichip aff-ichip--52 t-blue">{icon("info", 26)}</span><div><h2>Good to know</h2>{know_block}</div></section>
    <div class="actions"><a class="btn btn--primary" href="{materials}">Get your link</a><a class="btn btn--surface" href="{dashboard}">Open your dashboard</a></div>
  </article>
</div>
<div class="aff-b">
  <section class="aff-pagehead"><h1 class="display display--md">How earnings work</h1><p class="lede">Follow one person from the moment they click your link.</p></section>
  <ol class="aff-path">{path_steps}</ol>
  <div class="aff-rulegrid">{rules_b}</div>
  <section class="aff-rulecard aff-rulecard--wide" id="b-good-to-know"><div class="aff-rulecard__head"><span class="aff-ichip aff-ichip--36 t-blue">{icon("info", 18)}</span><h2>Good to know</h2></div>{know_block}</section>
  <section class="band t-green aff-band"><div class="band__copy"><h2>Track all of this on your dashboard.</h2></div>
    <a class="btn btn--bg btn--sm" href="{dashboard}">Dashboard{ext}</a><a class="btn btn--bg btn--sm" href="{materials}">Program materials{ext}</a></section>
</div>
{layout_toggle()}
</div>'''

    # ------------------------------------------------------------- 23 terms
    titles = section_titles()
    terms_rail = "".join(f'<a href="#{sid}"><span>{i + 1}</span>{t}</a>' for i, (sid, t) in enumerate(titles))
    terms_chips = "".join(f'<a href="#{sid}">{t}</a>' for sid, t in titles)
    terms = f'''<div class="aff aff-terms" data-layout-key="affiliates-terms" data-layout="a">
  <nav class="aff-terms__rail" aria-label="Contents"><span class="kicker">Affiliate program</span>{terms_rail}</nav>
  <article class="aff-terms__col">
    <span class="tag aff-terms__pill">Affiliate program · Legal</span>
    <h1 class="display display--md">Terms and Conditions</h1>
    <nav class="aff-terms__chips" aria-label="Contents">{terms_chips}</nav>
    {TERMS_HTML}
  </article>
{layout_toggle()}
</div>'''

    return [
        ("/affiliates", "affiliates/index.html", "TODD Affiliate Program | Taliferro Tech",
         "Share TODD with your own link. Earn 1¢ per visitor, unlock a $100 bonus, and earn 15% of every Enterprise monthly payment.",
         overview),
        ("/affiliates/how-earnings-work", "affiliates/how-earnings-work.html", "How affiliate earnings work | Taliferro Tech",
         "How TODD affiliates earn: visitor pay, the $100 bonus, Enterprise and product commission, who gets credit, and refunds.",
         how),
        ("/affiliates/terms", "affiliates/terms.html", "Affiliate Terms and Conditions | Taliferro Tech",
         "The Terms and Conditions for the TODD affiliate program.", terms),
    ]
