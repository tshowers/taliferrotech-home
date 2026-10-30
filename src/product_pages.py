"""Copy for the /products/<slug> pages. Edit here, then run src/build.py.

Sourced from each product's README, landing page and the 16Ahead codebase.
The product is 16Ahead (formerly TODD); each entry here is one of its spaces.
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
    "General Assistant": {
        "slug": "ask-todd",
        "title": "General Assistant: AI business advisor that answers with the next move",
        "tagline": "Ask a business question. Get the next move.",
        "lede": "General Assistant is where you talk to 16Ahead. Tell it what is stuck in your business and it comes back with a clear next move, the right place to start, or the fastest way forward.",
        "features": [
            ("Plain-language questions", "Describe the problem the way you would to a colleague. No setup, filters or report builders."),
            ("Answers with a next move", "16Ahead doesn't stop at an answer. It tells you what to do next and why."),
            ("Points to the right space", "When the work belongs in Outreach, Moves, Network or another space, 16Ahead sends you there."),
            ("Reads what you already have", "It works from the information already in your other spaces, so its suggestions fit your business."),
        ],
        "steps": [
            ("Ask", "Tell 16Ahead what is stuck or what you are trying to get done."),
            ("Decide", "16Ahead sorts what matters and suggests the next move."),
            ("Act", "Open the space that does the work, already pointed at the right task."),
        ],
        "fits": ["Moves", "Network", "Outreach"],
        "faq": [
            ("What is 16Ahead?", "16Ahead is one login to sixteen AI spaces that work together. It turns scattered information into clear next moves, and works across the spaces to draft, nudge, validate and route the work."),
            ("How is General Assistant different from a chatbot?", "A chatbot answers the question. General Assistant answers with the next move and points you to the space that can do the work."),
        ],
    },
    "Find": {
        "slug": "find",
        "title": "Find: AI search engine that puts the answer first",
        "tagline": "Start with what you remember. End with the answer.",
        "lede": "Find is 16Ahead's visual search. It puts the best-weighted answer first instead of ten blue links, drawing on authoritative answers, curated Taliferro knowledge and the web. Free, with no account required, on the web and on iPhone.",
        "features": [
            ("The answer first", "Find leads with the best-weighted answer, not a page of links to sort through."),
            ("Start from what you remember", "Describe the person, film, story or place you half remember and Find helps you get to what you mean."),
            ("Sources you can trust", "Answers draw on authoritative sources, curated Taliferro knowledge and the web."),
            ("Web and iPhone", "Search in your browser or with the Taliferro Find app."),
        ],
        "fits": ["General Assistant"],
        "ios": True,
        "app_store": "https://apps.apple.com/us/app/taliferro-find/id6806954591",
        "faq": [
            ("Do I need an account?", "No. Find is free and works without an account."),
            ("Is there an iPhone app?", "Yes. Taliferro Find is on the App Store."),
        ],
    },
    "Marketing Assistant": {
        "slug": "maya",
        "title": "Marketing Assistant: your on-call AI Marketing Director",
        "tagline": "Your on-call Marketing Director.",
        "lede": "Marketing Assistant is your on-call AI Marketing Director. Get candid advice on message clarity, campaigns and audience focus, learn what to fix first, then let it carry out the plan.",
        "features": [
            ("Message clarity", "It tells you plainly where your message is unclear and how to tighten it."),
            ("Campaigns", "Plan campaigns around what you are actually trying to achieve, not a template."),
            ("Audience focus", "Work out who you are talking to and what they need to hear."),
            ("What to fix first", "A prioritised view of the marketing changes that matter most right now."),
            ("A plan it carries out", "Turn the advice into a marketing plan, then have Marketing Assistant execute it."),
        ],
        "fits": ["Social", "Outreach", "Email Creator"],
        "faq": [
            ("Is Marketing Assistant a person?", "No. It is an AI marketing director, one of the sixteen spaces in 16Ahead, built by Taliferro Tech."),
            ("What kind of advice does Marketing Assistant give?", "Candid, practical marketing advice: message clarity, campaigns, audience focus and what to fix first."),
        ],
    },
    "Network": {
        "slug": "network",
        "title": "Network: relationship CRM that shows who needs your attention",
        "tagline": "Know which relationships need you this week.",
        "lede": "Network is 16Ahead's relationship graph. Every contact, company, deal and interaction is read continuously by 16Ahead to surface who needs attention, which relationships are gaining momentum and which are at risk of going cold.",
        "features": [
            ("One relationship graph", "Contacts, companies, deals and interactions in one place instead of scattered notes."),
            ("Who needs attention", "16Ahead surfaces the people you should reach out to before the relationship cools."),
            ("Momentum and risk", "See which relationships are gaining momentum and which are going quiet."),
            ("Context behind the work", "Keep the people and firms behind each project connected to the work itself."),
        ],
        "fits": ["Outreach", "Lead Vault", "Moves"],
        "faq": [
            ("Is Network a CRM?", "Network holds the contacts, companies and interactions a CRM would, but it is built around 16Ahead reading them for you and telling you who needs attention."),
        ],
    },
    "Moves": {
        "slug": "moves",
        "title": "Moves: task and follow-up tracker for work that can't stall",
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
        "title": "Outreach: AI email campaigns and automated follow-up",
        "tagline": "Turn attention into a real next step.",
        "lede": "Outreach is 16Ahead's email campaign and follow-up workspace. Plan thoughtful outreach, see how people engage, and choose the right next move for each conversation instead of letting threads go dead.",
        "features": [
            ("Campaigns and email", "Create campaigns and compose emails in one workspace."),
            ("Engagement signals", "16Ahead watches opens, clicks and replies so you know who is interested."),
            ("The next move per conversation", "Each conversation gets a suggested next step instead of a generic sequence."),
            ("Follow-up that keeps moving", "Keep follow-up going so attention turns into a meeting, not a dead thread."),
        ],
        "fits": ["Network", "Lead Vault", "Email Creator"],
        "faq": [
            ("Does Outreach send mass email blasts?", "Outreach is built for thoughtful, personal outreach and follow-up, with 16Ahead reading engagement to pick the next move for each conversation."),
        ],
    },
    "Pulse": {
        "slug": "pulse",
        "title": "Pulse: AI survey maker for customer feedback",
        "tagline": "Every response is a signal.",
        "lede": "Pulse is a survey and feedback tool. Create a short survey with 16Ahead, publish it to collect real responses, and watch a results dashboard tally the answers as they arrive, instead of a spreadsheet nobody opens.",
        "features": [
            ("Build with 16Ahead", "Create short customer surveys with 16Ahead's help, so you ask questions worth asking."),
            ("Publish and share", "Publish your pulse and share the link to start collecting responses."),
            ("Live results", "The dashboard updates itself as responses come in, so the read on the room is always ready."),
            ("Signal, not noise", "16Ahead reads the responses and turns them into clear direction for your business."),
        ],
        "steps": [
            ("Build", "Create your pulse with 16Ahead."),
            ("Share", "Publish it and send the link."),
            ("Read", "16Ahead tallies answers from the first response on."),
        ],
        "fits": ["Network", "Outreach", "Moves"],
        "faq": [
            ("What is a pulse?", "A short survey you send to customers or your team to get a quick, honest read on how things are going."),
        ],
    },
    "Lead Vault": {
        "slug": "lead-vault",
        "title": "Lead Vault: B2B lead finder with validated contacts",
        "tagline": "Find the right company. Reach the right person.",
        "lede": "Lead Vault is for finding business leads and the contacts behind them. Search companies, sectors, capabilities or buyer needs, check whether an email address is valid, and unlock the full record when a lead is worth a conversation.",
        "features": [
            ("Search the way you think", "Look up companies, sectors, capabilities, locations or buyer needs in plain language. If nothing matches, Lead Vault tries again and suggests better searches."),
            ("Validate an email", "Check whether an email address is valid and how confident that result is."),
            ("Unlock the record", "Preview a lead, then open the full contact and company details when you want them."),
            ("Recommendations", "Get a lead-specific recommendation for your outreach goal."),
            ("Lead sets from 16Ahead", "Open lead sets 16Ahead has already prepared for you."),
        ],
        "steps": [
            ("Search", "Describe the companies or buyers you are looking for, or validate one address."),
            ("Preview", "Review matches and their company context."),
            ("Unlock", "Open the full record for the leads you want to contact."),
        ],
        "fits": ["Network", "Outreach", "Marketing Assistant"],
        "faq": [
            ("Is Lead Vault a CRM?", "No. Lead Vault focuses on lead discovery and contact access. Use Network to manage relationships and Outreach to contact people."),
            ("Can I check a single email address?", "Yes. Switch to Validate Email to check an address and see how confident the result is."),
        ],
    },
    "Social": {
        "slug": "social",
        "title": "Social: AI social media post generator for LinkedIn and Threads",
        "tagline": "Keep your visibility active.",
        "lede": "Social keeps your social presence moving. Capture the signal, let 16Ahead draft the post, review and approve it, and keep the queue going, tied to the rest of your business instead of a separate content silo.",
        "features": [
            ("Capture ideas", "Save source material for future posts as you come across it."),
            ("Drafts per platform", "16Ahead writes platform-specific drafts for LinkedIn and Threads."),
            ("Strategy, calendar and queue", "Plan what goes out and when, and keep the queue moving."),
            ("Connected accounts", "Manage the social accounts you post to in one place."),
        ],
        "steps": [
            ("Capture", "Save the idea, link or moment worth posting about."),
            ("Draft", "16Ahead drafts the post for each platform."),
            ("Approve", "Review, edit and approve before anything goes out."),
        ],
        "fits": ["Marketing Assistant", "SayIt", "Image Creator"],
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
    "Store": {
        "slug": "market",
        "title": "16Ahead Store: independent stores that send each other customers",
        "tagline": "Independent stores that send each other customers.",
        "lede": "Bring your catalog and 16Ahead Store builds your store. Shoppers say what they need in plain words. When you don't carry it, Store sends them to a store in the network that does, and you earn part of that sale.",
        "features": [
            ("Shoppers describe it", "Shoppers say what they need in plain words. The store narrows it down, puts outfits and bundles together, and explains the trade-offs."),
            ("Every search goes somewhere", "If you don't carry it, a trusted store in the network does. The handoff reads like a recommendation, not an ad."),
            ("Import, approve, open", "The AI builds the store from your catalog. The one step that takes real time is payment verification, which the law requires."),
            ("Ready for AI shoppers", "Every product, price, stock level and policy is clean, structured data that AI shopping agents can read and buy from."),
        ],
        "steps": [
            ("Import your catalog", "Bring it from Shopify, Salesforce Commerce, a CSV file, or photos and price sheets."),
            ("Approve your store", "Add your logo and colors, check what the AI built, and change anything you like."),
            ("Get paid and join the network", "Connect Stripe to take orders. Nearby stores can start sending you shoppers."),
        ],
        "fits": ["Find", "Social", "Image Creator"],
        "faq": [
            ("How do referrals work?", "When a shopper asks for something you don't carry, you can send them to another store in the network. If they buy, you earn that store's commission. Every referral is labeled, and you choose which stores you send shoppers to and the minimum commission you accept."),
            ("Where can I import my catalog from?", "Shopify, Salesforce Commerce, a CSV file, or your own photos and price sheets. You approve the store before it goes live."),
            ("Do I need an account?", "Shoppers can browse without one. Merchants sign in with their 16Ahead account, using Apple, Google or an email link."),
        ],
    },
    "Docs": {
        "slug": "docs",
        "title": "Docs: AI proposal and RFP response software",
        "tagline": "Your business knowledge, ready to reuse.",
        "lede": "Docs stores the knowledge, supporting material and working context of your business where the next move can use it. Upload your documents, draft new ones, and turn RFPs into proposals.",
        "features": [
            ("Docs cockpit", "An overview of document health, proposal reuse and how fresh your knowledge is."),
            ("Add any document", "Upload PDFs, Word files, images, video and audio with descriptive details."),
            ("Document editor", "Create and edit drafts, work with .docx files and export the result."),
            ("RFPs and proposals", "Upload RFPs and review the proposals generated from them."),
        ],
        "fits": ["Moves", "Outreach", "General Assistant"],
        "faq": [
            ("What file types can I add?", "PDFs, Word documents, images, video, audio and other reference files."),
        ],
    },
    "Email Creator": {
        "slug": "email-creator",
        "title": "Email Creator: AI email generator that outputs designed HTML",
        "tagline": "Describe an email. Get finished HTML.",
        "lede": "Email Creator is a workspace where you chat with 16Ahead about an email, whether it is a marketing campaign, a newsletter, an invite or a plain business email, attach images like your logo or product photos, and get a designed, email-safe HTML email to preview and download.",
        "features": [
            ("Chat it through", "Describe the email you need and 16Ahead asks the right questions."),
            ("Add your images", "Attach a logo or product photos to use in the design."),
            ("Email-safe HTML", "Get a designed email built to display properly in email clients."),
            ("Preview and download", "Preview the result, then download it or copy the HTML."),
        ],
        "steps": [
            ("Describe", "Tell 16Ahead what the email is for."),
            ("Attach", "Add your logo or photos, if you want them."),
            ("Download", "Preview the designed email and download the HTML."),
        ],
        "fits": ["Outreach", "Email Signature", "Image Creator"],
        "faq": [
            ("What kinds of emails can it make?", "Marketing campaigns, newsletters, invites and plain business emails."),
            ("Do I need an account?", "Yes. Sign in with your 16Ahead account."),
        ],
    },
    "Email Signature": {
        "slug": "email-signature",
        "title": "Email Signature Generator: a professional HTML signature in minutes",
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
        "title": "Image Creator: AI image and logo generator, download a PNG",
        "tagline": "Describe an image. Download a PNG.",
        "lede": "Image Creator is a browser-based image workspace. Chat with 16Ahead to create logos, icons, illustrations and other images, add your logo or example images as references, and download the result as a PNG.",
        "features": [
            ("Conversational", "16Ahead asks what you need and clarifies the request before creating the image."),
            ("Use references", "Attach your logo or example images to guide the result."),
            ("PNG downloads", "Download finished images straight from your browser."),
            ("Stays in your browser", "Uploads, images and the conversation stay in your browser tab. Image Creator doesn't store your images."),
        ],
        "fits": ["Social", "Email Creator", "Marketing Assistant"],
        "faq": [
            ("What can I create?", "Logos, icons, illustrations and other images."),
            ("Are my images stored?", "No. Uploads, generated images and the conversation stay in your browser tab."),
            ("Do I need an account?", "Yes. Sign in with your 16Ahead account."),
        ],
    },
}
