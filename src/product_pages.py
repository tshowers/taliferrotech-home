"""Copy for the /products/<slug> pages. Edit here, then run src/build.py.

Sourced from each product's README, landing page and the TODD codebase.
Keep it factual: no prices, and no claims the product does not make itself.

title    -> <title> and search result headline
tagline  -> H1 under the product name
lede     -> opening paragraph (also the meta description)
features -> "What it does" cards: (heading, text)
steps    -> optional "How it works" list
fits     -> "Works with" product names (must match build.PRODUCTS names)
faq      -> (question, answer) pairs, also emitted as FAQPage schema
ios      -> True when the product has a live iPhone app
"""

PAGES = {
    "Ask TODD": {
        "slug": "ask-todd",
        "title": "Ask TODD: ask a business question, get the next move",
        "tagline": "Ask a business question. Get the next move.",
        "lede": "Ask TODD is where you talk to TODD, the intelligence layer behind every Taliferro Tech product. Tell it what is stuck in your business and it comes back with a clear next move, the right place to start, or the fastest way forward.",
        "features": [
            ("Plain-language questions", "Describe the problem the way you would to a colleague. No setup, filters or report builders."),
            ("Answers with a next move", "TODD doesn't stop at an answer. It tells you what to do next and why."),
            ("Points to the right product", "When the work belongs in Outreach, Moves, Network or another product, TODD sends you there."),
            ("Reads what you already have", "TODD works from the information already in your Taliferro Tech products, so its suggestions fit your business."),
        ],
        "steps": [
            ("Ask", "Tell TODD what is stuck or what you are trying to get done."),
            ("Decide", "TODD sorts what matters and suggests the next move."),
            ("Act", "Open the product that does the work, already pointed at the right task."),
        ],
        "fits": ["Moves", "Network", "Outreach"],
        "faq": [
            ("What is TODD?", "TODD is the AI intelligence layer behind every Taliferro Tech product. It turns scattered information into clear next moves, and works across the products to draft, nudge, validate and route the work."),
            ("How is Ask TODD different from a chatbot?", "A chatbot answers the question. Ask TODD answers with the next move and points you to the product that can do the work."),
        ],
    },
    "Find": {
        "slug": "find",
        "title": "Find: search that ends with an answer",
        "tagline": "Start with what you remember. End with the answer.",
        "lede": "Find is TODD's visual search. It puts the best-weighted answer first instead of ten blue links, drawing on authoritative answers, curated Taliferro knowledge and the web. Free, with no account required, on the web and on iPhone.",
        "features": [
            ("The answer first", "Find leads with the best-weighted answer, not a page of links to sort through."),
            ("Start from what you remember", "Describe the person, film, story or place you half remember and Find helps you get to what you mean."),
            ("Sources you can trust", "Answers draw on authoritative sources, curated Taliferro knowledge and the web."),
            ("Web and iPhone", "Search in your browser or with the Taliferro Find app."),
        ],
        "fits": ["Ask TODD"],
        "ios": True,
        "app_store": "https://apps.apple.com/us/app/taliferro-find/id6806954591",
        "faq": [
            ("Do I need an account?", "No. Find is free and works without an account."),
            ("Is there an iPhone app?", "Yes. Taliferro Find is on the App Store."),
        ],
    },
    "Maya": {
        "slug": "maya",
        "title": "Maya: your on-call AI Marketing Director",
        "tagline": "Your on-call Marketing Director.",
        "lede": "Maya is your on-call AI Marketing Director. Get candid advice on message clarity, campaigns and audience focus, learn what to fix first, then let Maya carry out the plan.",
        "features": [
            ("Message clarity", "Maya tells you plainly where your message is unclear and how to tighten it."),
            ("Campaigns", "Plan campaigns around what you are actually trying to achieve, not a template."),
            ("Audience focus", "Work out who you are talking to and what they need to hear."),
            ("What to fix first", "A prioritised view of the marketing changes that matter most right now."),
            ("A plan Maya carries out", "Turn the advice into a marketing plan, then have Maya execute it."),
        ],
        "fits": ["Social", "Outreach", "Email Creator"],
        "faq": [
            ("Is Maya a person?", "No. Maya is an AI marketing director built by Taliferro Tech on the TODD intelligence layer."),
            ("What kind of advice does Maya give?", "Candid, practical marketing advice: message clarity, campaigns, audience focus and what to fix first."),
        ],
    },
    "Network": {
        "slug": "network",
        "title": "Network: see which relationships need your attention",
        "tagline": "Know which relationships need you this week.",
        "lede": "Network is TODD's relationship graph. Every contact, company, deal and interaction is read continuously by TODD to surface who needs attention, which relationships are gaining momentum and which are at risk of going cold.",
        "features": [
            ("One relationship graph", "Contacts, companies, deals and interactions in one place instead of scattered notes."),
            ("Who needs attention", "TODD surfaces the people you should reach out to before the relationship cools."),
            ("Momentum and risk", "See which relationships are gaining momentum and which are going quiet."),
            ("Context behind the work", "Keep the people and firms behind each project connected to the work itself."),
        ],
        "fits": ["Outreach", "Lead Vault", "Moves"],
        "faq": [
            ("Is Network a CRM?", "Network holds the contacts, companies and interactions a CRM would, but it is built around TODD reading them for you and telling you who needs attention."),
        ],
    },
    "Moves": {
        "slug": "moves",
        "title": "Moves: a task workspace for work that can't stall",
        "tagline": "See what needs attention next.",
        "lede": "Moves is a momentum-focused task and project workspace for work that cannot afford to stall. Most task trackers tell you what exists. Moves shows what needs attention next: every move carries a clear next action, an owner, context, timing and a momentum signal.",
        "features": [
            ("Clear next actions", "Every task is anchored to a concrete move instead of a vague status."),
            ("Connected context", "Link moves to the projects, contacts, campaigns and documents they serve."),
            ("Drift made visible", "See which work is fresh, active, stalled or at risk, before it goes cold."),
            ("Shared accountability", "Ownership, blockers, momentum and the next action in one shared view."),
        ],
        "steps": [
            ("Create a move", "Give it a clear next action."),
            ("Connect it", "Link the project, contact, campaign or document it serves."),
            ("Watch the signal", "Momentum signals flag work that is drifting."),
            ("Act", "Take the next move before the opportunity goes cold."),
        ],
        "fits": ["Network", "Outreach", "Docs"],
        "faq": [
            ("How is Moves different from a to-do list?", "A to-do list records tasks. Moves tracks the next action on each one, who owns it and whether it is drifting, so follow-up doesn't disappear between meetings."),
            ("Can teams use Moves together?", "Yes. Moves gives a team a shared execution view with ownership and blockers visible to everyone."),
        ],
    },
    "Outreach": {
        "slug": "outreach",
        "title": "Outreach: email campaigns and follow-up with TODD",
        "tagline": "Turn attention into a real next step.",
        "lede": "Outreach is TODD's email campaign and follow-up workspace. Plan thoughtful outreach, see how people engage, and choose the right next move for each conversation instead of letting threads go dead.",
        "features": [
            ("Campaigns and email", "Create campaigns and compose emails in one workspace."),
            ("Engagement signals", "TODD watches opens, clicks and replies so you know who is interested."),
            ("The next move per conversation", "Each conversation gets a suggested next step instead of a generic sequence."),
            ("Follow-up that keeps moving", "Keep follow-up going so attention turns into a meeting, not a dead thread."),
        ],
        "fits": ["Network", "Lead Vault", "Email Creator"],
        "faq": [
            ("Does Outreach send mass email blasts?", "Outreach is built for thoughtful, personal outreach and follow-up, with TODD reading engagement to pick the next move for each conversation."),
        ],
    },
    "Pulse": {
        "slug": "pulse",
        "title": "Pulse: customer surveys TODD reads for you",
        "tagline": "Every response is a signal.",
        "lede": "Pulse is a survey and feedback tool. Create a short survey with TODD, publish it to collect real responses, and watch a results dashboard tally the answers as they arrive, instead of a spreadsheet nobody opens.",
        "features": [
            ("Build with TODD", "Create short customer surveys with TODD's help, so you ask questions worth asking."),
            ("Publish and share", "Publish your pulse and share the link to start collecting responses."),
            ("Live results", "The dashboard updates itself as responses come in, so the read on the room is always ready."),
            ("Signal, not noise", "TODD reads the responses and turns them into clear direction for your business."),
        ],
        "steps": [
            ("Build", "Create your pulse with TODD."),
            ("Share", "Publish it and send the link."),
            ("Read", "TODD tallies answers from the first response on."),
        ],
        "fits": ["Network", "Outreach", "Moves"],
        "faq": [
            ("What is a pulse?", "A short survey you send to customers or your team to get a quick, honest read on how things are going."),
        ],
    },
    "Lead Vault": {
        "slug": "lead-vault",
        "title": "Lead Vault: find and validate business leads",
        "tagline": "Find the right company. Reach the right person.",
        "lede": "Lead Vault is for finding business leads and the contacts behind them. Search companies, sectors, capabilities or buyer needs, check whether an email address is valid, and unlock the full record when a lead is worth a conversation.",
        "features": [
            ("Search the way you think", "Look up companies, sectors, capabilities, locations or buyer needs in plain language. If nothing matches, Lead Vault tries again and suggests better searches."),
            ("Validate an email", "Check whether an email address is valid and how confident that result is."),
            ("Unlock the record", "Preview a lead, then open the full contact and company details when you want them."),
            ("Recommendations", "Get a lead-specific recommendation for your outreach goal."),
            ("Lead sets from TODD", "Open lead sets TODD has already prepared for you."),
        ],
        "steps": [
            ("Search", "Describe the companies or buyers you are looking for, or validate one address."),
            ("Preview", "Review matches and their company context."),
            ("Unlock", "Open the full record for the leads you want to contact."),
        ],
        "fits": ["Network", "Outreach", "Maya"],
        "faq": [
            ("Is Lead Vault a CRM?", "No. Lead Vault focuses on lead discovery and contact access. Use Network to manage relationships and Outreach to contact people."),
            ("Can I check a single email address?", "Yes. Switch to Validate Email to check an address and see how confident the result is."),
        ],
    },
    "Social": {
        "slug": "social",
        "title": "Social: social posts drafted by TODD for LinkedIn and Threads",
        "tagline": "Keep your visibility active.",
        "lede": "Social keeps your social presence moving. Capture the signal, let TODD draft the post, review and approve it, and keep the queue going, tied to the rest of your business instead of a separate content silo.",
        "features": [
            ("Capture ideas", "Save source material for future posts as you come across it."),
            ("Drafts per platform", "TODD writes platform-specific drafts for LinkedIn and Threads."),
            ("Strategy, calendar and queue", "Plan what goes out and when, and keep the queue moving."),
            ("Connected accounts", "Manage the social accounts you post to in one place."),
        ],
        "steps": [
            ("Capture", "Save the idea, link or moment worth posting about."),
            ("Draft", "TODD drafts the post for each platform."),
            ("Approve", "Review, edit and approve before anything goes out."),
        ],
        "fits": ["Maya", "SayIt", "Image Creator"],
        "faq": [
            ("Which platforms does Social support?", "Social drafts posts for LinkedIn and Threads."),
            ("Does Social post without my approval?", "Social is built around reviewing and approving drafts before they go out."),
        ],
    },
    "SayIt": {
        "slug": "sayit",
        "title": "SayIt: social media built for organizations",
        "tagline": "Social media built for organizations.",
        "lede": "SayIt is a new type of social media, built for organizations. Create a business profile, share updates and what you need, and see who is interested so the right conversations can start.",
        "features": [
            ("A business profile", "Set up a profile for your organization, not just a personal account."),
            ("Post what you need", "Share updates and needs so the people who can help see them."),
            ("See who is interested", "Find out who responded, so you know where to start the conversation."),
            ("Connect with people who get it", "Meet organizations and people working on the same things."),
        ],
        "fits": ["Social", "Network", "Outreach"],
        "faq": [
            ("How is SayIt different from other social networks?", "SayIt is built for organizations: you post what you need, see who is interested, and start the right conversations."),
        ],
    },
    "Docs": {
        "slug": "docs",
        "title": "Docs: business documents, proposals and RFPs with TODD",
        "tagline": "Your business knowledge, ready to reuse.",
        "lede": "Docs stores the knowledge, supporting material and working context of your business where the next move can use it. Upload your documents, draft new ones, and turn RFPs into proposals.",
        "features": [
            ("Docs cockpit", "An overview of document health, proposal reuse and how fresh your knowledge is."),
            ("Add any document", "Upload PDFs, Word files, images, video and audio with descriptive details."),
            ("Document editor", "Create and edit drafts, work with .docx files and export the result."),
            ("RFPs and proposals", "Upload RFPs and review the proposals generated from them."),
        ],
        "fits": ["Moves", "Outreach", "Ask TODD"],
        "faq": [
            ("What file types can I add?", "PDFs, Word documents, images, video, audio and other reference files."),
        ],
    },
    "Email Creator": {
        "slug": "email-creator",
        "title": "Email Creator: describe an email, get designed HTML",
        "tagline": "Describe an email. Get finished HTML.",
        "lede": "Email Creator is a workspace where you chat with TODD about an email, whether it is a marketing campaign, a newsletter, an invite or a plain business email, attach images like your logo or product photos, and get a designed, email-safe HTML email to preview and download.",
        "features": [
            ("Chat it through", "Describe the email you need and TODD asks the right questions."),
            ("Add your images", "Attach a logo or product photos to use in the design."),
            ("Email-safe HTML", "Get a designed email built to display properly in email clients."),
            ("Preview and download", "Preview the result, then download it or copy the HTML."),
        ],
        "steps": [
            ("Describe", "Tell TODD what the email is for."),
            ("Attach", "Add your logo or photos, if you want them."),
            ("Download", "Preview the designed email and download the HTML."),
        ],
        "fits": ["Outreach", "Email Signature", "Image Creator"],
        "faq": [
            ("What kinds of emails can it make?", "Marketing campaigns, newsletters, invites and plain business emails."),
            ("Do I need an account?", "Yes. Sign in with your TODD account."),
        ],
    },
    "Email Signature": {
        "slug": "email-signature",
        "title": "Email Signature Builder: a professional email signature in minutes",
        "tagline": "A professional signature for any mail app.",
        "lede": "Build a branded email signature in a couple of minutes. Pick a layout, add your details and logo, then copy the HTML or download it, with step-by-step guides for installing it in your mail app.",
        "features": [
            ("Five templates", "Clean, Centered, Sidebar, Minimal and Spotlight, with a live preview."),
            ("Your brand", "Set your accent colour and add an optional call-to-action button."),
            ("Logo upload", "Drag in a PNG, JPG, WEBP, GIF or SVG logo and it is hosted for you."),
            ("Install guides", "Step-by-step instructions for Gmail, Outlook, Apple Mail and Yahoo Mail."),
        ],
        "steps": [
            ("Pick a layout", "Choose one of five templates."),
            ("Add your details", "Name, title, contact details, logo and colour."),
            ("Install", "Copy or download the HTML and follow the guide for your mail app."),
        ],
        "fits": ["Email Creator", "Outreach", "Image Creator"],
        "faq": [
            ("Do I need an account?", "No. You can build and copy your signature without signing in."),
            ("Which mail apps does it work with?", "There are install guides for Gmail, Outlook, Apple Mail and Yahoo Mail."),
        ],
    },
    "Image Creator": {
        "slug": "image-creator",
        "title": "Image Creator: describe an image, download a PNG",
        "tagline": "Describe an image. Download a PNG.",
        "lede": "Image Creator is a browser-based image workspace. Chat with TODD to create logos, icons, illustrations and other images, add your logo or example images as references, and download the result as a PNG.",
        "features": [
            ("Conversational", "TODD asks what you need and clarifies the request before creating the image."),
            ("Use references", "Attach your logo or example images to guide the result."),
            ("PNG downloads", "Download finished images straight from your browser."),
            ("Stays in your browser", "Uploads, images and the conversation stay in your browser tab. Image Creator doesn't store your images."),
        ],
        "fits": ["Social", "Email Creator", "Maya"],
        "faq": [
            ("What can I create?", "Logos, icons, illustrations and other images."),
            ("Are my images stored?", "No. Uploads, generated images and the conversation stay in your browser tab."),
            ("Do I need an account?", "Yes. Sign in with your TODD account."),
        ],
    },
    "Music": {
        "slug": "music",
        "title": "Taliferro Music: jazz, R&B and downtempo radio",
        "tagline": "Music without the noise.",
        "lede": "Taliferro Music streams jazz, R&B and downtempo live. A simple listening experience with no algorithm feed, on the web and on iPhone.",
        "features": [
            ("Live streaming", "Jazz, R&B and downtempo, streaming live."),
            ("No algorithm feed", "Just music, not a feed deciding what you should hear next."),
            ("Web and iPhone", "Listen in your browser or with the Taliferro Music Radio app."),
        ],
        "fits": [],
        "ios": True,
        "app_store": "https://apps.apple.com/us/app/taliferro-music-radio/id6806499542",
        "faq": [
            ("Do I need an account?", "No. Open Taliferro Music and start listening."),
            ("Is there an iPhone app?", "Yes. Taliferro Music Radio is on the App Store."),
        ],
    },
}
