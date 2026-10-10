"""Legal pages: /terms, /privacy and /privacy-rights (moved from TODD's old
/terms-and-conditions, /privacy-policy and /privacy-rights; todd.taliferro.tech
301s those paths here).

The policy text lives in legal_terms.html and legal_privacy.html and is legal
text - restyle only, never edit the wording here. When the privacy policy
changes, update PRIVACY_EFFECTIVE too.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TERMS_HTML = (HERE / "legal_terms.html").read_text(encoding="utf-8")
PRIVACY_HTML = (HERE / "legal_privacy.html").read_text(encoding="utf-8")
PRIVACY_EFFECTIVE = "June 18, 2026"

# The privacy rights request goes by email, the same as it did in TODD.
RIGHTS_EMAIL = "info@taliferro.com"
REQUEST_TYPES = [
    ("access", "Right to Know / Access", "Right to Know — What data do you hold about me?"),
    ("correct", "Right to Correct", "Right to Correct — I want to fix inaccurate data"),
    ("delete", "Right to Delete", "Right to Delete — Please delete my data"),
    ("portability", "Data Portability", "Data Portability — Export my data"),
]


def contents(html):
    return [(sid, re.sub(r"<[^>]+>", "", t).strip())
            for sid, t in re.findall(r'<section class="legal-sec" id="([^"]+)">\s*<h2>(.*?)</h2>', html)]


def legal_doc(kicker, title, html, meta=""):
    rail = "".join(f'<a href="#{sid}">{t}</a>' for sid, t in contents(html))
    return f'''<div class="legal">
  <nav class="legal__rail" aria-label="Contents"><span class="kicker">{kicker}</span>{rail}</nav>
  <article class="legal__col">
    <h1 class="display display--md">{title}</h1>
    {meta}
    {html}
  </article>
</div>'''


def pages(address, phone_display, phone_tel):
    terms = legal_doc("Terms", "Terms and Conditions", TERMS_HTML)
    privacy = legal_doc("Privacy", "Privacy Policy", PRIVACY_HTML,
                        f'<p class="legal__meta">Effective date: {PRIVACY_EFFECTIVE}</p>')

    options = "".join(f'<option value="{v}" data-label="{label}">{text}</option>' for v, label, text in REQUEST_TYPES)
    rights = f'''<div class="legal legal--single">
  <article class="legal__col">
    <h1 class="display display--md">Privacy Rights Request</h1>
    <p class="lede">Under GDPR, CCPA, and applicable privacy law you have the right to know what data we hold about you, request corrections, request deletion, or receive a portable copy. Complete the form below and we will respond within 45 days.</p>
    <form class="rights" data-rights-email="{RIGHTS_EMAIL}">
      <label class="rights__field"><span>Your email address</span><input type="email" name="email" placeholder="you@example.com" required autocomplete="email"></label>
      <label class="rights__field"><span>Request type</span><select name="type">{options}</select></label>
      <p class="rights__hint" data-for="delete" hidden>You can also delete your account directly: Settings &rarr; Update Profile &rarr; Delete Account.</p>
      <p class="rights__hint" data-for="portability" hidden>You can also export your data directly: Settings &rarr; Update Profile &rarr; Export My Data.</p>
      <label class="rights__field"><span>Additional details <small>(optional)</small></span><textarea name="details" rows="4" placeholder="Describe your request or the specific data you are asking about."></textarea></label>
      <button class="btn btn--primary" type="submit">Submit Request</button>
    </form>
    <p class="rights__done" role="status" hidden><b>Request prepared.</b> An email to {RIGHTS_EMAIL} has been opened in your mail client. Please send it to complete your request. We will respond within 45 days.</p>
    <p class="legal__meta">Taliferro Tech, LLC · {address} · <a href="tel:{phone_tel}">{phone_display}</a> · <a href="mailto:{RIGHTS_EMAIL}">{RIGHTS_EMAIL}</a> · <a href="/privacy">Privacy Policy</a></p>
  </article>
</div>'''

    return [
        ("/terms", "terms.html", "Terms and Conditions | Taliferro Tech",
         "The Terms and Conditions for Taliferro Tech, LLC websites and products, including TODD.", terms),
        ("/privacy", "privacy.html", "Privacy Policy | Taliferro Tech",
         "How Taliferro Tech, LLC collects, uses and protects your information across its websites and products, including TODD.", privacy),
        ("/privacy-rights", "privacy-rights.html", "Privacy Rights Request | Taliferro Tech",
         "Ask Taliferro Tech what data it holds about you, or request a correction, deletion or a portable copy.", rights),
    ]
