# Hive IP — New Website Plan

*Prepared April 2026*

---

## 1. Brief in one paragraph

A new hiveip.co.uk that positions Hive IP as the modern, end-to-end leader in unique coding for FMCG — covering generation, two flexible print routes (in-factory via the ACG, or supplied directly to the brand's packaging supplier for inside-pack printing), cloud validation, fraud monitoring, and consumer support. The site needs to win two audiences simultaneously: **FMCG marketing/brand teams** (who care about agility, engagement and ROI) and **FMCG procurement and operations** (who care about cost, security, install effort, and SLAs). Tone is light, clean and corporate — confident B2B, orange as accent on white. It must do three jobs equally well: generate inbound enquiries, act as a credibility tool for live sales conversations, and educate the market on why modern unique coding (with either print route) outperforms the legacy way of doing things. Built as static HTML/CSS/JS so it's fast, cheap to host, and easy to maintain. **The site is engineered for SEO from the ground up — every page, URL, content structure and asset is optimised to rank for the high-intent keyword clusters around *unique codes*, *unique-code printing* and *promotions*** (full strategy in section 7). English-only at launch, but architected so additional languages can be slotted in later.

---

## 2. Positioning & message hierarchy

The site needs to make one big idea unmistakable on the home page, then unfold it for different readers.

**The big idea.** Hive IP turns every pack into a digital touchpoint — at a fraction of the cost, with the security of a closed-loop system, and the agility to launch promotions in days rather than months. It's the only end-to-end solution that does generation, print (in your factory or at your packaging supplier), cloud validation, fraud monitoring and consumer support together.

**The proof.** 200+ ACGs operating across PepsiCo factories in the UK, Netherlands and Portugal. Hive's codes power the Sun Saver loyalty programme for News UK. Billions of codes generated and validated per year — across both print routes.

**The savings.** Up to 80% lower print costs vs the legacy packaging-supplier route. 99.85% uptime. 10–15 minute ACG install per line. Hot-swappable hardware.

**The business model.** ACGs are typically supplied into your factory at no charge. There is no fee for the codes that are printed — you only pay when a unique code is actually used on a live campaign. The hardware, the unused codes, and the validation infrastructure are all included. This is the single most important commercial fact about working with Hive IP and it should appear prominently on the home page, the model page, and the why-in-factory page.

**The always-on advantage.** Because there is no cost penalty for printing codes that aren't used, every pack can carry a unique code 24/7. Your packaging is *always* promotionally ready. New campaigns — including digital direct-to-consumer pushes — can launch in days or even hours rather than the months a traditional supply-chain print cycle requires. You're no longer limited to on-pack promotions planned a quarter in advance.

**The differentiator.** Algorithmic generation and algorithmic validation — no database lookup, no codes stored on the ACG, no codes shared with third parties unless required. Pay only for codes used in market.

**The flexibility.** Two print routes, one validation backbone. The ACG installed in your factory is the most cost-effective option and our recommended approach for medium-to-high volumes. For brands that need codes printed inside the pack, want a smaller pilot, or where a factory install isn't practical, we supply codes directly to your packaging supplier in their required format — and still handle validation, fraud monitoring and consumer support end-to-end.

**The foundational argument.** A unique code is simply the right primitive for proof-of-purchase. Till receipts can be faked. Batch codes (the same code on every pack) provide no security at all and can be reused indefinitely. A unique code can only be used once, is audited end-to-end, never exists in a database that could leak, and can be supported by AI Vision audit checks when the campaign risk profile warrants it.

Every page should ladder back to one of these seven pillars: proof, savings, business model, always-on, differentiator, flexibility, foundational argument.

---

## 3. Sitemap

A flat, focused sitemap. No deep navigation; every key story is one click from the home page.

```
/                              Home
/solution                      The Hive IP Solution (overview of the end-to-end system)
  /solution/in-factory         In-factory print via the ACG (primary route) — also the canonical "What is an ACG?" explainer
  /solution/at-supplier        Inside-pack print via your packaging supplier (alternative route)
  /solution/validation         Cloud validation, security, fraud monitoring & API
  /solution/consumer-support   Consumer Support Panel
/acg                           301-redirects to /solution/in-factory#what-is-an-acg (memorable URL for emails/proposals)
/why-unique-codes              Why unique codes are the right proof-of-purchase mechanism
/why-in-factory                The case for in-factory printing — and an honest answer on outside-the-pack security
/applications                  What unique codes unlock
  /applications/promotions     On-pack & digital promotions
  /applications/loyalty        Loyalty & multi-purchase rewards
  /applications/anti-counterfeit  Brand protection & traceability
  /applications/supply-chain   Supply chain, provenance, sustainability
/case-studies                  Index of customer stories
  /case-studies/pepsico        PepsiCo: 200+ ACGs across Europe
  /case-studies/news-uk        News UK: Sun Saver loyalty programme
  /case-studies/<anonymised>   Anonymised stories (Kellogg's, Andrex etc. as 'a leading…')
/our-model                     Our business model: free ACGs, pay-on-use, always-on packaging
/insights                      Articles & thought leadership
  /insights/<slug>             Individual articles
/about                         Company & contact
/contact                       Enquiry form
```

The footer currently carries core company links only; privacy, terms and security pages are intentionally excluded until final content is ready.

---

## 4. Page-by-page content plan

**A site-wide convention worth flagging up front: the way "ACG" is introduced.** Because *Automated Code Generator* is a coined term, we never assume the reader has met it. On every page, the first mention of the abbreviation is wrapped in an `<abbr title="Automated Code Generator">ACG</abbr>` element (which gives a hover tooltip, accessible to screen readers) **and** is hyperlinked to the canonical explainer at `/solution/in-factory#what-is-an-acg`. Subsequent mentions on the same page are plain text. The first mention is also typically followed by a brief in-sentence definition the first time it appears in the page's main copy ("…using Hive IP's ACG, the small hardware unit that…"), so even readers who don't hover or click still understand what it is. The same convention applies to other branded or technical terms — *BBD*, *closed-loop*, *allocation*, *batch prefix* — and keeps the writing accessible to procurement readers and FMCG marketers who haven't been steeped in the category.



### Home

A single-screen hero that anchors the whole proposition: a confident headline (working line: *"Every pack, a digital touchpoint."* or *"Unique coding, generated in your factory. Validated in the cloud. Used by the world's biggest brands."*), a sub-line explaining what you do in one sentence, and two CTAs side by side — one for marketing audiences (*See how it works*) and one for procurement (*Calculate your savings*). A muted, motion-restrained hero image — either a clean ACG hardware shot or an over-the-shoulder factory line photograph.

Beneath the hero, six short bands tell the story in roughly this order:

1. **The proof band.** PepsiCo and News UK logos (the only two we can name publicly), plus a strapline: *"Trusted to generate and validate billions of unique codes a year."* Number tiles: 200+ ACGs / Billions of codes p.a. / 99.85% SLA / 10-min install.
2. **Why unique codes (the foundational argument).** A short band that frames the proof-of-purchase problem and contrasts unique codes against the alternatives — till receipts (easily faked) and batch codes (no security at all). Single hero idea: *"A unique code is the only proof-of-purchase that can be used once, audited end-to-end, and never exists in a database."* Click-through to /why-unique-codes.
3. **What we do.** Three columns — Generate, Print, Validate — each with a short paragraph and a link into the deeper Solution page. The *Print* column makes the dual-route point explicit: *"In your factory using our ACG, or supplied to your packaging supplier — your choice. The rest of the system is identical."*
4. **Always promotionally ready.** The single most distinctive commercial message. Headline: *"Free hardware. Pay only when a code is used. Every pack ready to promote, every day of the year."* Three short supporting points: ACGs supplied at no charge; codes printed all year at no cost; you only pay when codes are used in a live campaign — so digital direct-to-consumer pushes can launch in days, not months. Click-through to /our-model.
5. **Why in-factory.** A teaser of the savings and security argument, with a single hero stat (*"Save 78% or more on print cost vs the legacy supplier route"*) and a link to the full /why-in-factory page.
6. **Applications.** Tile grid of the four use cases (Promotions, Loyalty, Anti-counterfeiting, Supply chain) — each tile clicks into its own page.

Closes with a final CTA band — name, email, phone, calendar link — and the form footer. Nothing else competes with that final ask.

### /solution and its four children

`/solution` is a single overview page anchored by an updated closed-loop diagram that shows **both print routes** feeding into the same cloud validation backbone (Generation → Print, either via ACG-in-factory *or* via your packaging supplier → Cloud Validation & Security → Brand app/agency → Consumer Support Panel → Marketing data). It introduces each of the four pillars in 100–150 words with a "read more" into the dedicated child page. The framing is deliberately inclusive: brands choose the print route that suits them; everything downstream is identical.

`/solution/in-factory` is the deep page on the ACG hardware and the recommended route for medium-to-high volumes. It is also the canonical "what is an ACG?" explainer for the entire site — every other page that mentions an ACG links here on first mention.

The page opens with an unmissable **"What is an ACG?"** section (anchor: `#what-is-an-acg`), built from your canonical wording so the term is defined the first time any reader meets it:

> **ACG** stands for *Automated Code Generator*. It is a small hardware unit that contains Hive IP's proprietary code-generation algorithm and is designed to operate with all major makes of in-factory Best Before Date printers.
>
> - Our ACGs connect directly to the factory's in-line printers.
> - When the printer requests a unique code, the ACG generates a non-sequential unique code on the fly, transmits it to the printer, and logs the event.
> - The same unique code is never passed twice.
> - For security, no unique codes are ever stored on the ACG.
> - The printer prints the code as a string, and/or in a scannable format (QR or Data Matrix).
> - The unique codes generated by the ACG are automatically and immediately synchronised with our cloud-based validation and security service, and are ready to be used the moment they leave the line.

This block sits beneath a hero photograph of the ACG 2000 and a small labelled diagram showing it slotted between the printer controller and the coder. Below the explainer the page widens into the rest of the story: where it sits in the line, how fast it installs (15 min), the multiple-cipher proprietary algorithm, the 26-batch / 5m-per-batch architecture, the LED status diagnostics, hot-swappable spares, compatibility with Markem-Imaje SmartDate / X60 / X65 and other major brands. Sidebar: *Want the operation manual? Email us.* Closes with a callout: *"If a factory install isn't right for you — see our packaging-supplier route."*

**A short `/acg` redirect URL** (301-ing to `/solution/in-factory#what-is-an-acg`) is set up so the explainer has a clean, memorable address you can drop into emails, proposals and pitch decks.

`/solution/at-supplier` is the deep page on the alternative route — and it's positioned as a first-class option, not a fallback. The story is: when this route makes sense (the brand prefers inside-pack printing for aesthetic or security reasons; volumes are too low to justify ACGs; the production line can't accommodate an install; the brand wants to pilot before committing to hardware); how it works (Hive generates the codes algorithmically and supplies them in the format the packaging supplier requires, encrypted, with delivery confirmation); what stays the same (validation, security, fraud monitoring, consumer support, API integration with agencies are all identical to the in-factory route). The page tackles the "inside vs outside the pack" question head-on rather than dodging it. Closes with a comparison table that lays out the trade-offs honestly so readers can self-select.

`/solution/validation` is the cloud story — and applies equally to both print routes. Algorithmic validation rather than database lookup. Hosted on AWS. 99.85% SLA. Cross-referenceable audit trail. Optional AI Vision audit workflows when the campaign risk profile warrants them. Real-time fraud monitoring and risk scoring. The API. Easy integration for digital agencies (mention that several major agencies are already familiar with the API without naming them).

`/solution/consumer-support` is the CSP page. Account hierarchy (team leader sets up team members), ability to check codes, view consumer history, generate replacement codes (with full audit). Screenshots if you have them; otherwise UI mockups built from the deck description.

### /why-unique-codes

This is the foundational page — the answer to *"why is this even the right way to verify a purchase?"* — and it sits before /why-in-factory in the navigation because the print-route argument only matters once a reader has accepted that unique codes are the right primitive in the first place. Many marketing teams reach for till receipts or batch codes by default; this page makes the case for unique codes calmly and with evidence.

Structure as a comparison-led long-form article:

**The problem.** Promotions need a way to verify a real purchase happened. The mechanic you choose decides how secure the campaign is, how easily it can be audited, and how much fraud you'll absorb.

**The four common mechanics, side by side.**

- *No verification.* Free entry / shelf scanning / "anyone can play" promotions. Vulnerable to bots and incentive farming. Rarely viable for anything with monetary value attached.
- *Till receipts.* Trivially faked, photographed, edited or generated with image tools. Hard to audit at scale. High consumer friction (consumer has to keep, photograph and upload the receipt). Receipt fraud is a known, growing problem in promotional marketing.
- *Batch codes.* The same code printed on every pack of a SKU. The code can be entered once and then reused indefinitely by anyone — there is no way to enforce single use, because every consumer has the same code. Limiting entries per account doesn't fix it: bots and fraudsters simply create more accounts. As a security mechanism, batch codes provide essentially nothing — and despite this, around 90% of European on-pack promotions still use them, because unique codes have historically been complex and expensive to print.
- *Unique codes.* Every pack carries its own unguessable, non-sequential code. Each code can only be used once, by one consumer, ever. Every entry is logged with a full audit trail. Cross-referenceable against the consumer record, the SKU, the production date and the production line.

**Why unique codes win.** Single-use enforcement at the system level (not a policy you have to police). A complete audit trail per code and per consumer. Cross-reference against meta-data — SKU, market, production date, line — which itself is a layer of fraud detection. Risk-scoring of consumer behaviour patterns. Campaign-level statistics that are actually meaningful because the entries that produced them are real.

**Hive IP's closed-loop architecture takes the security further.** Codes are generated algorithmically using a multiple-cipher proprietary algorithm. They are *never stored* on the ACG; they are *never held* in a list or database that could be leaked or breached. On validation, the code is reverse-engineered against an algorithmic allocation, not looked up in a table of individual entries. Codes are not passed between third parties unless required (for example, when supplied to a packaging supplier — and even then, the file is encrypted in transit). The systemic risk that has compromised entire campaigns at competing providers — large databases of issued codes leaking — does not exist in our architecture.

**AI Vision can add an audit layer when needed.** When a unique code is printed on the outside of the pack (which we strongly recommend for cost, speed and consumer experience), the residual fraud concern is in-store code copying. In practice this is rare, but recent AI Vision advances make it feasible to add an audit step that checks the user is not in-store when submitting the code. The check can be applied to every entry or triggered selectively when a consumer's behaviour looks suspicious, with BBD and production-line data cross-referenced against the submitted code.

**The takeaway.** A unique code is the only proof-of-purchase that can be used once, audited end-to-end, never exists in an exposable database, and can be supported by AI Vision audit checks when the risk profile warrants it. Till receipts and batch codes can't do any of those things. If your campaign has any monetary value attached, the right primitive is a unique code.

End the page with two CTAs: *See the cost case for in-factory printing* (link to /why-in-factory) and *Talk to us about your next campaign* (contact form).

### /why-in-factory

This is your single most persuasive marketing asset. It needs to live as its own page because it's the conversion engine for procurement audiences and because it's where the *"yes, but what about code copying?"* objection gets answered openly and completely.

Structure as a long-form article with a clear narrative arc: *the old way (packaging-supplier coding only, codes hidden inside the pack)* → *what's wrong with it for most use cases (cost, lead times, supply-chain risk, no SKU data, frustrating consumer experience)* → *the Hive in-factory way (the ACG, codes printed alongside the BBD on the outside)* → *the numbers* → *the agility upside* → *the consumer experience upside* → *the honest answer on code copying* → *when the supplier route is still the right call*.

Pull the *Reasons to print Unique-Codes In-Factory* PDF into web copy, but reframe any specific-£ comparisons as **savings percentages and savings ranges** rather than published rates. Replace the original cost-per-million tables with a "savings vs the legacy approach" comparison: typical industry rate at the packaging supplier (publicly known to be in the £3,000–£5,000 per million range), the saving Hive customers typically achieve (78% or more), and the additional saving from each subsequent campaign in the engagement period. The page does not quote Hive's own per-code rate. End with two CTAs: *Get a tailored savings estimate* and *See how PepsiCo deployed at scale*.

**The code-copying section deserves dedicated treatment** because it's the question you get asked the most. The page should answer it confidently and with data — not defensively. The argument, in the same order you'd make it in a sales conversation:

1. *Most consumers don't copy codes.* The overall incidence of code-copying on prize draws and point-collection schemes is statistically tiny relative to legitimate entries. We measure it on every campaign.
2. *Two types of copying, and only one is solved by hiding the code.* "Type 1" is in-store copying (someone scans without buying). "Type 2" is sharing — a legitimate buyer giving the code to a friend or family member. Type 2 happens whether the code is on the inside or outside of the pack, so hiding the code doesn't actually solve it. Type 2 is also the more common type by a clear margin.
3. *AI Vision can audit the rare in-store copying concern.* When suspicious entry patterns appear, the campaign can ask the user to scan the code and surrounding environment so it can check the user is not standing in-store when submitting the code. The same scan can capture the BBD and production-line data for cross-reference against the code itself.
4. *A measure-retain-audit framework backstops the rest.* For higher-stakes promotions — prize draws with monetary value — winners can be required to retain their pack and produce it on request. Audits are typically only triggered on participants who have won something of real value or who have breached a risk-score threshold, so the operational overhead is small.
5. *The advantages of outside-the-pack printing more than cover the cost of any residual fraud.* Lower print cost, faster speed-to-market, no need to rip open packs, easier mobile scanning, far better consumer experience and consequently higher engagement rates — these compound into a much larger commercial benefit than the marginal fraud they enable.

The conclusion is the one you make in person: for the vast majority of promotions, printing on the outside is the right answer. For the small set of campaigns where the brand judges the risk profile differently, we offer the supplier route — and the rest of the system (validation, fraud monitoring, support) is identical.

### /applications and children

These exist to hook each persona with the use case they care about. They're shorter pages, each ~400 words, anchored by a real customer outcome.

- **Promotions.** Lead with the Lucozade/Mo Farah agility narrative (anonymised — *"a leading sports drink brand"*) — just-in-time digital promotions, days not months. Pull in the "always-on coding" idea: standard packs that are quietly ready for any digital push at any time.
- **Loyalty.** Lead with Sun Saver (named — News UK). Cover multi-purchase reward mechanics, points collection, repeat-purchase data — Lurpak and McVitie's outcomes anonymised.
- **Anti-counterfeiting.** A unique code as a "passport" for product authenticity, brand protection, and sale-channel verification.
- **Supply chain.** Provenance, sustainability data, recall handling, SKU/production-line traceability — the angle from the May 2021 deck about codes carrying meta-data.

### /case-studies

A clean index page with cards. Each card has a tile image (or a brand mark for the named studies), a one-line outcome and a click-through.

- **PepsiCo** — named, detailed. The story is scale: 200+ ACGs across the UK, Netherlands and Portugal, integrated with Markem-Imaje coders, supporting global Doritos and Walkers promotions. Reference the WESA programme and the Doritos case study numbers (50m codes, 78% or more saving).
- **News UK / Sun Saver** — named, detailed. Hive IP supplies and validates the unique codes underpinning the Sun Saver loyalty programme.
- **Five anonymised studies.** Kellogg's *(a global cereal brand)*, Andrex *(a leading household brand)*, Tetley *(a major beverage brand)*, McVitie's *(a top biscuit brand)*, Lucozade *(a sports drink brand)*, Lurpak *(a leading dairy brand)*, Co-op partnership story. Same structure each: brief, mechanic, Hive's role, results — all the strong numbers retained, just no brand name.

### /our-model

This is the page that explains *how working with Hive IP commercially works*, and it's deliberately not called "Pricing" — there are no specific rates published here. The point of the page is to communicate the business model and the savings, not a price list.

**Headline:** *"Free hardware. Pay only when you use a code. Always promotionally ready."*

**The model in three short paragraphs:**

1. *We supply the ACGs at no charge.* Hive IP typically provides and installs the Automated Code Generators into your factory free of charge. There is no capital expenditure, no hardware purchase, no ongoing licence on the units themselves. We support and service them throughout the engagement.

2. *We don't charge for the codes you print — only for the codes you use.* Every pack coming off the line can carry a unique code, every day of the year. There is no per-code or per-pack print fee. You pay only when codes are used on a live campaign — when a real consumer enters the code, a real promotion validates it, a real interaction happens. If a campaign uses fewer codes than expected, you pay less.

3. *Validation, fraud monitoring, security and consumer support are included.* The cloud infrastructure, the API, the fraud-detection systems, the audit trail, and the Consumer Support Panel come as part of the engagement, not as separately-priced add-ons.

**The implication — being "promotionally ready" 24/7.** Because every pack already carries a unique code, you are never waiting for a print run to catch up with a marketing idea. A campaign that would traditionally take three to six months — design, brief the packaging supplier, print run, supply chain, into store — can launch in days or even hours. That changes what marketing teams can actually do: real-time digital direct-to-consumer pushes triggered by an event (a sporting moment, a weather pattern, a competitor move), targeted regional pilots, fast experiments, sponsorship reactivation, and personalised rewards — none of which are practical when codes have to be planned and printed months ahead.

**The savings story.** The legacy approach — codes printed at the packaging supplier — typically charges three to five thousand pounds per million coded packs, regardless of how many codes are eventually used in market. With Hive IP's in-factory model, the same campaign typically saves 78% or more, depending on volume and frequency. The savings deepen with every additional campaign run inside the engagement period because the hardware and the unused codes are already in place.

**Embed an interactive savings calculator** at the bottom of the page — three inputs (annual pack volume, number of campaigns per year, average campaign size) and an output card that shows the *legacy approach cost*, the *typical Hive IP saving range as a percentage*, and the *estimated saving in pounds*. The calculator does not publish Hive's specific per-million rate; it shows the comparative saving and ends with a CTA: *"Get a tailored estimate for your programme."* Pure JavaScript, no backend. This is the strongest lead-generation hook on the site for procurement audiences without exposing pricing publicly.

**Closes with two CTAs:** *"Talk to us about your factory"* (primary, links to /contact) and *"See how PepsiCo deployed at scale"* (secondary, links to the PepsiCo case study).

### /insights

Index page with 6 articles at launch, with structure to add more. Each article ~600–900 words, drawn from existing materials but rewritten for web readability with proper headings, pull quotes and a clear takeaway. Proposed launch articles:

1. *Receipts, batch codes, unique codes: which proof-of-purchase mechanic actually works?* — the foundational comparison piece. Walks through the four mechanics, the fraud profile of each, and why a unique code paired with closed-loop validation is the only one that can be enforced as single-use, audited end-to-end and never exposed in a database.
2. *Why in-factory unique-code printing can save 78% or more* — adapted from your *Reasons to print Unique-Codes In-Factory* PDF.
3. *Two routes to printing unique codes — and how to choose between them* — a balanced piece on in-factory ACG vs codes supplied to your packaging supplier, the trade-offs, and which fits which kind of brand and campaign. Positions Hive as the only provider that does both well.
4. *Closed-loop coding: why algorithmic validation beats database lookup* — adapted from the Overview of Capabilities and validation explainers.
5. *Outside vs inside the pack: an honest answer on code copying* — directly addresses the most common objection. Type 1 vs Type 2 copying, optional AI Vision audit checks for the rare in-store concern, the measure-retain-audit framework, and why the engagement gains from outside-pack codes more than cover the residual fraud.
6. *From on-pack to digital: how to run agile, just-in-time promotions* — built on the Lucozade/Mo Farah story (anonymised) and the standard-pack-with-codes argument from the September deck.

### /about

Short and confident. What Hive IP is, who it serves, where it operates (UK, Netherlands, Portugal — with implicit room for more). A one-paragraph founder/leadership note (you'll need to give me text or sign off on what's already known about the team). Press/contact details.

### /contact

A single-column page: short heading, a 4-field form (name, company, role, message) that posts via a service like Formspree or Web3Forms (works with static hosting, sends to your inbox), plus your direct email and phone alongside the form. Optional Calendly booking link below the form for prospects who want to skip ahead.

---

## 5. Design direction (light, clean, corporate)

Drawing from the brand cues in your decks but lightening the palette so it works as a marketing site rather than a presentation:

**Colour.** White and off-white as the primary backgrounds (not black like the decks). Hive orange (`#F26B1F` approximately — I'll match exactly to your logo) reserved as the accent for headlines, links, CTA buttons and key stats. Charcoal `#1A1A1A` for body text. A muted grey `#6B6B6B` for secondary text. One single dark band somewhere on each page (often the final CTA) so the brand still gets a moment of dramatic contrast — that ties back to the deck aesthetic without overwhelming the site.

**Typography.** A modern geometric sans for headlines (Inter, Geist or your existing deck font if it's licensed for web — I'll match). A neutral readable sans for body. Generous line-height; left-aligned; no centred body text.

**Layout.** Generous whitespace. Maximum content width around 1200px on desktop. Single-column hero, two/three-column feature bands, single-column long-form. Edges of sections get full-bleed colour bands so navigation between sections is visually rhythmic.

**Responsive: desktop, tablet and mobile.** The site is designed and built to work properly on every device a buyer might use — a procurement manager on a 27" monitor, a marketer on a 13" laptop in a meeting, a senior buyer reading on a tablet on the train, a brand manager checking the site on their phone between calls. Mobile is treated as a first-class experience, not a scaled-down afterthought. Concretely:

- *Breakpoints.* Built mobile-first using fluid CSS (rem/em units, CSS Grid and Flexbox, container queries where helpful). Three primary breakpoints — small (under 640px, phones), medium (640–1024px, tablets and smaller laptops), large (1024px and above, desktops). The layout reflows naturally between them rather than locking to fixed pixel widths, so the site looks intentional on every screen size including unusual ones (foldables, ultra-wide monitors, in-car displays).
- *Mobile navigation.* On phones the main nav collapses into a hamburger that opens a full-height drawer with the same hierarchy as the desktop nav. The Hive logo stays top-left, a single primary CTA (*Contact*) stays top-right so the most important action is always one tap away. The header is sticky but slim so it doesn't eat into mobile screen height.
- *Content reflow.* Multi-column feature bands collapse to single columns on mobile in the right reading order. Tables (the comparison tables on /why-unique-codes and /why-in-factory) reflow to stacked card layouts on small screens rather than horizontally scrolling, because horizontally scrolling tables are punishing on a phone. The closed-loop diagram on /solution becomes a vertical flow diagram on mobile rather than shrinking text into illegibility.
- *Touch-friendly targets.* All interactive elements are at least 44×44px (the WCAG and Apple HIG minimum), with at least 8px of clear space between adjacent tappable items. Form inputs are large enough for thumbs, with native mobile keyboards triggered correctly (`type="email"` for email fields, `inputmode="numeric"` for the savings-calculator inputs, etc.). No hover-only interactions — every state achievable on a desktop has a touch-equivalent.
- *The savings calculator on mobile.* The three inputs stack vertically with full-width controls; the output card sits beneath the inputs rather than alongside; the comparison graphic switches from side-by-side bars on desktop to stacked bars on mobile. Numeric input uses a numeric keypad. Result updates live as values change.
- *Imagery.* Every image served as a responsive `<picture>` element with appropriate `srcset` so phones don't download desktop-resolution assets. AVIF and WebP variants where supported, with sensible fallbacks. Hero photographs cropped for mobile so the focal point isn't lost when the aspect ratio shifts to portrait.
- *Typography on mobile.* Body text never drops below 16px (browsers will trigger zoom on inputs below 16px on iOS, breaking the experience). Line lengths kept within 45–75 characters at every breakpoint. Heading sizes scale down on small screens but stay confidently large enough to feel intentional.
- *Performance on mobile networks.* Core Web Vitals targets apply on simulated 4G as well as desktop. The site is engineered to be usable on slower connections and older phones — that's where a procurement manager often first encounters the site, after a colleague has forwarded a link.
- *Testing approach.* Manual testing on real devices (iPhone, Android phone, iPad) plus browser dev-tools simulation across the standard viewport sizes during build. A final cross-device QA pass on real hardware before launch, covering iOS Safari, Android Chrome, desktop Chrome, Edge, Firefox, and Safari. Lighthouse mobile audits scoring 95+ on every page.

**Imagery.** Three ingredient types: clean studio shots of the ACG hardware (you have one in the deck — we'd want a higher-resolution version), factory line photography (atmospheric, slight motion blur, no faces or identifiable brand packaging unless we have permission), and clean diagrams (the closed-loop architecture, the ACG slotting between controller and coder). No stock photography of generic businesspeople — the product is concrete enough to carry the imagery on its own.

**Motion.** Restrained. Subtle fade-in on scroll for content blocks. No carousels. No auto-playing video. One animated diagram on the home page (the closed-loop flow) is enough — everything else is static.

**Accessibility.** WCAG 2.2 AA throughout — colour contrast, keyboard navigation, alt text, semantic HTML, focus rings. Procurement audiences increasingly require this for vendor evaluations.

---

## 6. Build approach

A static site, hand-built in HTML/CSS/JS, organised so each page is a self-contained file with shared header/footer/styles.

**Structure on disk:**

```
/Hive IP WebSite/
  index.html
  solution/
    index.html
    acg.html
    validation.html
    consumer-support.html
  applications/
    index.html
    promotions.html
    loyalty.html
    anti-counterfeit.html
    supply-chain.html
  why-in-factory.html
  case-studies/
    index.html
    pepsico.html
    news-uk.html
    cereal-brand.html  (anonymised)
    …
  our-model/
    index.html        (with the savings calculator embedded)
  insights/
    index.html
    why-in-factory-printing-is-cheaper.html
    closed-loop-validation.html
    …
  about/
    index.html
  contact/
    index.html
  assets/
    css/
      site.css        (one stylesheet, organised with CSS custom properties for theming)
    js/
      main.js
      savings-calculator.js
    img/
      logo/
      acg/
      diagrams/
      factory/
      case-studies/
    fonts/
```

**Performance.** Plain HTML with no framework keeps the site fast by default. CSS bundled into a single file with custom properties for the theme. JavaScript minimal — only the savings calculator and progressive enhancements (mobile nav, scroll animations) need it. Images served as responsive `<picture>` elements with WebP/AVIF and proper `srcset`. Targeted Lighthouse score: 95+ on all four pillars.

**Hosting.** Cloudflare Pages, Netlify, or GitHub Pages. All free or near-free, all support custom domains, all give automatic HTTPS, all support form submissions via free tiers (Cloudflare Pages Functions / Netlify Forms / Formspree). My recommendation is Cloudflare Pages for the combination of speed, generosity of free tier, and built-in DNS.

**Form handling.** Web3Forms or Formspree for the contact form — both work with static hosting and email straight to you. No server, no database.

**Analytics.** Plausible or Cloudflare Web Analytics — both privacy-respecting, both lightweight, both ICO-friendly. Avoid Google Analytics unless you have a strong reason for it.

**Future multilingual support.** We'll structure URLs as `/en/...` from the start (or use root for English and `/nl/...`, `/pt/...` for added languages later). The CSS, JS and image assets stay shared; only the HTML duplicates per language. This means adding Dutch or Portuguese later is purely a translation exercise, not a rebuild.

---

## 7. SEO & content optimisation

The site is built to rank, not just to read well. The unique-coding category is fragmented online — there are large equipment vendors who don't talk about marketing applications, and marketing agencies who don't understand the print stack. Hive IP can plausibly own the centre of that conversation if the site is architected for it. SEO is treated as a foundational concern, on a par with design and build, not a finishing pass.

**Target keyword clusters.** Three primary clusters drive the strategy:

- *Unique codes / unique coding.* Head terms: "unique codes", "unique coding", "unique code generation", "unique codes for promotions". Mid-tail: "unique codes vs batch codes", "unique codes for FMCG", "single-use promotional codes", "proof of purchase codes". Long-tail: "what's the difference between batch codes and unique codes", "how do unique codes prevent promotional fraud".
- *Unique-code printing.* Head terms: "unique code printing", "on-pack unique codes", "in-factory code printing". Mid-tail: "automated code generator", "ACG printer", "Markem-Imaje unique code integration", "in-factory code generator". Long-tail: "how to print unique codes on packaging", "cost of printing unique codes per million", "alternatives to packaging supplier unique-code printing", "what is an automated code generator". The /solution/in-factory page is explicitly optimised to win the *what is an ACG / what is an automated code generator* search — that's a high-intent, low-competition query where Hive IP can credibly own the definitional answer.
- *Promotions / proof of purchase.* Head terms: "promotional code platform", "FMCG promotion software", "consumer promotion validation". Mid-tail: "proof of purchase for promotions", "till-receipt fraud", "promotional code fraud protection", "AI promotional code validation". Long-tail: "how to verify proof of purchase without till receipts", "best promotional mechanic for FMCG launches".

Each top-level page anchors one cluster: /why-unique-codes anchors the first cluster, /solution and /why-in-factory anchor the second, /applications and the case studies anchor the third. The Insights articles are written to capture mid-tail and long-tail traffic that the static pages can't naturally absorb.

**On-page SEO baked into every page.**

- Each page has a thoughtful, hand-written title tag (50–60 characters) and meta description (150–160 characters), both of which include the page's primary keyword phrase and a clear value proposition.
- A single H1 per page that uses the primary keyword phrase as part of a real sentence — not keyword-stuffed.
- Sub-headings (H2/H3) carry secondary keyword variants and follow a logical hierarchy that helps both readers and search engines understand structure.
- URL slugs are short, lowercase, hyphen-separated, and keyword-led (e.g., `/why-unique-codes`, `/solution/in-factory`, `/insights/receipts-batch-codes-unique-codes`).
- Internal linking is deliberate. Every page links forward to the next logical step in the funnel and back to the foundational arguments. Cornerstone pages (/why-unique-codes, /why-in-factory, /our-model) are linked from every relevant content page using descriptive anchor text rather than "click here".
- Image alt text describes the image and its content meaningfully — useful both for accessibility and for image search.
- Headings, body copy and link anchors avoid the temptation of jargon-only language. We write for a procurement reader skim-reading on a Tuesday afternoon, not for a search algorithm.

**Technical SEO.**

- Clean semantic HTML throughout (header, nav, main, article, section, footer). No div-soup.
- An `XML sitemap` generated for the full site and submitted to Google Search Console and Bing Webmaster Tools.
- A `robots.txt` that explicitly allows indexing and points to the sitemap.
- Canonical URLs on every page, pre-emptively configured so that adding Dutch and Portuguese later (with `/nl/...` and `/pt/...` paths) won't dilute ranking authority via duplicate content.
- `hreflang` tags scaffolded into the head from day one, ready for multilingual versions.
- Schema.org structured data (JSON-LD) on every relevant page: `Organization` schema on the home page (with logo, social profiles, contact details), `Product` schema on /solution/in-factory and /solution/at-supplier, `Article` schema on every Insights article, `FAQPage` schema on /why-unique-codes and /why-in-factory (where there's natural Q&A structure), `BreadcrumbList` schema across all internal pages.
- OpenGraph and Twitter Card meta tags on every page so internal links shared on LinkedIn, Slack, Teams and X render with proper preview cards. This is significant for B2B because buying conversations happen in those channels.
- Page speed and Core Web Vitals are first-class: target Largest Contentful Paint under 2.0 seconds on 3G simulation, Cumulative Layout Shift under 0.05, Interaction to Next Paint under 100ms. Achieved by keeping the site static, lazy-loading images below the fold, using AVIF/WebP with proper `srcset`, deferring non-critical JS, and avoiding render-blocking fonts (fonts loaded via `font-display: swap`).
- Mobile-first responsive layout, tested across the standard breakpoints. Mobile usability is now the dominant ranking signal for B2B searches happening from phones during meetings.
- HTTPS-only with HSTS, no mixed content, no insecure third-party scripts.

**Content cadence.** Insights articles aren't a launch-and-forget. The plan is to publish one new article per month for the first six months after launch, on topics chosen specifically to fill keyword gaps that the static pages don't cover. I'll suggest the first six months' editorial calendar once we're past launch — built on a combination of search-volume research, your sales team's most common inbound questions, and gaps in the competitor landscape.

**Backlink and authority strategy (light touch, no spam).** The strongest organic signals come from unbiased third-party references. Three legitimate routes worth pursuing alongside the build: (a) PR-friendly pieces in industry trade publications (Packaging News, FMCG, The Drum, Promotional Marketing magazine) referencing the PepsiCo / News UK deployments, (b) speaking slots or guest articles for senior team members, and (c) ensuring your existing customer relationships, agency partners, and Markem-Imaje references include a hyperlink to hiveip.co.uk where appropriate. None of this is paid, none of it is link farming — but each materially improves the domain authority that underpins every keyword you'll ever rank for.

**Measurement.** Google Search Console, Bing Webmaster Tools and a privacy-respecting analytics tool (Plausible or Cloudflare Web Analytics) configured at launch. Monthly review of: keyword positions for the priority terms, organic click-through rates, bounce rates on cornerstone pages, conversions on the contact form. Targets: top-3 ranking on at least eight priority unique-coding/printing keywords within six months of launch; sustained organic enquiry volume of at least one qualified lead per week from search by month nine.

---

## 8. Phased rollout

A four-phase build so you see meaningful progress quickly and can give feedback before more work depends on each decision.

**Phase 1 — Foundations & home page (1–2 sessions).** Set up the directory structure, build the design system (colours, typography, components, header/footer), build the home page in full. You sign off on the look, feel and tone before we go wider.

**Phase 2 — Solution, Why-Unique-Codes & Why-In-Factory (2 sessions).** The pages that do the heaviest sales lifting. /solution + its four children, the foundational /why-unique-codes long-form (proof-of-purchase argument), and the /why-in-factory long-form (print route + code-copying answer). By the end of this phase you have a site that could already drive enquiries — even before case studies and insights are live.

**Phase 3 — Case studies, applications, our-model (1–2 sessions).** Build the case-study index and the named PepsiCo / News UK studies in detail; build the four applications pages and the /our-model page (with the savings calculator). This rounds out the sales story.

**Phase 4 — Insights, about, contact, polish (1 session).** Draft the six launch articles, build /about and /contact, run accessibility and performance passes, set up hosting and the form handler, and connect the domain. Includes a final cross-device QA pass on real iPhone, Android phone, iPad, and desktop browsers (Chrome, Edge, Firefox, Safari) to verify every page works as intended on every screen — no page ships without sign-off on both desktop and mobile.

**Indicative total effort:** 5–7 working sessions to launch. Faster if you're decisive on copy and imagery, slower if we iterate heavily on visual direction.

---

## 9. What I need from you to start

1. **Logo files** — the original SVG / high-resolution PNG of the orange-and-grey Hive IP logo (you've supplied one PNG; an SVG will look sharper at all sizes).
2. **An ACG hardware photograph** at print resolution — the deck shot is the right composition but probably not high enough resolution for hero use.
3. **Confirmation on the Sun Saver detail** — anything you'd like emphasised or avoided, given News UK is the named customer.
4. **Sign-off on calling the others anonymously** — confirm you're comfortable with phrases like *"a leading global cereal brand"* etc. for Kellogg's, Andrex, Tetley, McVitie's, Lucozade, Lurpak, Co-op.
5. **About-page copy guidance** — a short paragraph or two on the Hive IP story, when it was founded, and how you'd like leadership to be presented (named or kept low-key).
6. **Domain access** — DNS access for hiveip.co.uk so we can repoint when we're ready to launch (or set up a staging subdomain like `new.hiveip.co.uk` first).

---

## 10. Open questions / decisions to revisit later

- Whether to gate the ACG operation manual download (lead capture) or leave it open as a credibility piece.
- Whether to add Dutch and Portuguese language versions in v1.1 once English is validated, or wait for clear demand signal.
- Whether the savings calculator should email-gate the result ("enter your email to see your full savings breakdown") for stronger lead capture, or remain open for trust.
- Whether to add a press / news ticker if and when there's a rhythm of announcements worth surfacing.

---

*Once you're happy with this plan, I'll start with Phase 1 — foundations and the home page — and we'll iterate from there.*
