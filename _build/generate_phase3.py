#!/usr/bin/env python3
"""
Phase 3 page generator.

Generates static HTML for case studies and applications using a shared
header/footer template. Outputs go directly into the site's public tree;
this script is itself not deployed.

Run: python3 _build/generate_phase3.py
"""

import html as html_lib
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------- Helpers ------------------------------------------------------

def rel(depth):
    """Return the relative path prefix for the given depth from site root.
    depth=1 means the page is at /case-studies/ (one level deep);
    depth=2 means /case-studies/pepsico/ (two levels deep).
    """
    return "../" * depth


# Post-processing: rewrite directory-style and root-relative links so the site
# works both via file:// (local preview) and on a real web server.
_LINK_EXCLUDE = ('http://', 'https://', '//', 'mailto:', 'tel:', 'data:', 'javascript:', '#')
_ATTR_RE = re.compile(r'(\b(?:href|src|action))="([^"]*)"')

def _fix_link(url: str, depth: int) -> str:
    if not url or url.startswith(_LINK_EXCLUDE):
        return url
    suffix = ''
    path = url
    for sep in ('?', '#'):
        if sep in path:
            i = path.index(sep)
            suffix = path[i:]
            path = path[:i]
            break
    if path.startswith('/'):
        path = path.lstrip('/')
        if depth > 0:
            path = ('../' * depth) + path
    if path == '' or path.endswith('/'):
        path = path + 'index.html'
    return path + suffix

def _normalise_links(html: str, depth: int) -> str:
    return _ATTR_RE.sub(
        lambda m: f'{m.group(1)}="{_fix_link(m.group(2), depth)}"',
        html,
    )


def page(*, depth, title, description, slug_path, og_title=None, og_desc=None,
         og_image=None, og_image_width=None, og_image_height=None,
         body_html, breadcrumbs, schema_extra="", current_nav_key, page_class="",
         show_final_phone=True):
    """Render a full HTML page using site conventions."""
    r = rel(depth)
    canonical = f"https://hiveip.co.uk/{slug_path}/"

    nav_items = [
        ("why-unique-codes", "Why unique codes"),
        ("solution",         "Solution"),
        ("why-in-factory",   "Why in-factory"),
        ("applications",     "Applications"),
        ("case-studies",     "Case studies"),
        ("insights",         "Insights"),
        ("our-model",        "Our model"),
    ]

    def nav_links():
        out = []
        for key, label in nav_items:
            curr = ' aria-current="page"' if key == current_nav_key else ""
            out.append(f'      <a href="{r}{key}/"{curr}>{label}</a>')
        return "\n".join(out)

    breadcrumb_items = "\n".join(
        f'          <li><a href="{r}{href}">{label}</a></li>' if href is not None
        else f'          <li aria-current="page">{label}</li>'
        for href, label in breadcrumbs
    )

    breadcrumb_schema_items = []
    for i, (href, label) in enumerate(breadcrumbs, 1):
        if href is None:
            href_full = canonical
        elif href == "":
            href_full = "https://hiveip.co.uk/"
        else:
            href_full = f"https://hiveip.co.uk/{href}"
        breadcrumb_schema_items.append(
            '      { "@type": "ListItem", "position": ' + str(i) +
            ', "name": "' + label + '", "item": "' + href_full + '" }'
        )

    breadcrumb_schema = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
""" + ",\n".join(breadcrumb_schema_items) + """
    ]
  }
  </script>"""

    final_phone_html = """
        &middot;
        <a href="tel:+447787826362">+44&nbsp;7787&nbsp;826&nbsp;362</a>""" if show_final_phone else ""

    og_t = og_title or title
    og_d = og_desc  or description
    if og_image is None:
        generated_og = {
            "case-studies/pepsico": "assets/img/og/generated/pepsico.png",
            "case-studies/news-uk": "assets/img/og/generated/news-uk-sun-saver.png",
            "case-studies/cereal-brand": "assets/img/og/generated/cereal-brand.png",
            "case-studies/household-brand": "assets/img/og/generated/household-brand.png",
            "case-studies/sports-drink-brand": "assets/img/og/generated/sports-drink-brand.png",
            "applications/promotions": "assets/img/og/generated/agile-digital-promotions.png",
            "applications/loyalty": "assets/img/og/generated/news-uk-sun-saver.png",
            "applications/supply-chain": "assets/img/og/generated/beyond-promotions-five-uses.png",
            "solution/consumer-support": "assets/img/og/generated/consumer-support-panel.png",
            "solution/validation": "assets/img/og/generated/closed-loop-validation.png",
            "insights/proof-of-purchase-mechanics": "assets/img/og/generated/proof-of-purchase-mechanics.png",
            "insights/in-factory-printing-cheaper": "assets/img/og/generated/in-factory-printing-cheaper.png",
            "insights/closed-loop-validation": "assets/img/og/generated/closed-loop-validation.png",
            "insights/outside-vs-inside-pack-code-copying": "assets/img/og/generated/outside-vs-inside-pack-code-copying.png",
            "insights/agile-digital-promotions": "assets/img/og/generated/agile-digital-promotions.png",
            "insights/beyond-promotions-five-uses": "assets/img/og/generated/beyond-promotions-five-uses.png",
            "solution/in-factory": "assets/img/og/acg.png",
            "solution": "assets/img/og/solution.png",
            "solution/at-supplier": "assets/img/og/solution.png",
            "why-in-factory": "assets/img/og/why-in-factory.png",
            "why-unique-codes": "assets/img/og/why-unique-codes.png",
            "our-model": "assets/img/og/why-in-factory.png",
            "applications": "assets/img/og/why-unique-codes.png",
            "insights": "assets/img/og/why-unique-codes.png",
        }
        og_image = generated_og.get(slug_path.strip("/"), "assets/img/og/home.png")
    if og_image_width is None:
        og_image_width = 1200
    if og_image_height is None:
        og_image_height = 675 if "/generated/" in og_image else 630
    meta_title = html_lib.escape(html_lib.unescape(title), quote=True)
    meta_desc = html_lib.escape(html_lib.unescape(description), quote=True)
    meta_og_title = html_lib.escape(html_lib.unescape(og_t), quote=True)
    meta_og_desc = html_lib.escape(html_lib.unescape(og_d), quote=True)
    meta_og_image = f"https://hiveip.co.uk/{og_image.lstrip('/')}"
    favicon_links = f"""
  <link rel="icon" href="{r}favicon.ico" sizes="any">
  <link rel="icon" href="{r}assets/img/favicons/favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="{r}assets/img/favicons/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{r}assets/img/favicons/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{r}assets/img/favicons/apple-touch-icon.png">
  <link rel="manifest" href="{r}site.webmanifest">"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Hive IP">
  <meta property="og:title" content="{meta_og_title}">
  <meta property="og:description" content="{meta_og_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{meta_og_image}">
  <meta property="og:image:width" content="{og_image_width}">
  <meta property="og:image:height" content="{og_image_height}">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:title" content="{meta_og_title}">
  <meta name="twitter:description" content="{meta_og_desc}">
  <meta name="twitter:image" content="{meta_og_image}">
  <meta name="twitter:card" content="summary_large_image">
{favicon_links}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{r}assets/css/site.css">
{breadcrumb_schema}
{schema_extra}
</head>
<body class="{page_class}">

<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header" role="banner">
  <div class="container site-header__inner">
    <a class="brand" href="{r}" aria-label="Hive IP — home">
      <img src="{r}assets/img/logo/hive-logo.png" alt="Hive IP" width="140" height="62">
    </a>
    <nav class="primary-nav" data-nav aria-label="Primary">
{nav_links()}
    </nav>
    <a class="btn btn--primary header-cta" href="{r}contact/">Talk to us</a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-drawer" data-nav-toggle>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke-linecap="round"/></svg>
    </button>
  </div>
  <div id="mobile-drawer" class="mobile-drawer" data-nav-drawer aria-label="Mobile menu">
    <div class="mobile-drawer__inner" data-nav>
{nav_links()}
      <a href="{r}about/">About</a>
      <a class="btn btn--primary" href="{r}contact/">Talk to us</a>
    </div>
  </div>
</header>

<main id="main">

  <nav class="container breadcrumbs" aria-label="Breadcrumb" style="margin-top: 1.5rem;">
    <ol>
{breadcrumb_items}
    </ol>
  </nav>

{body_html}

  <section class="section section--dark cta-final">
    <div class="container">
      <span class="eyebrow">Talk to us</span>
      <h2>Let&rsquo;s see what unique codes could do for your next campaign.</h2>
      <p>Whether you&rsquo;re running global promotions on hundreds of millions of packs, launching a single digital push, or scoping a brand-protection programme &mdash; we&rsquo;ll build the right route in.</p>
      <div class="cta-final__actions">
        <a class="btn btn--primary btn--lg" href="{r}contact/">Send an enquiry</a>
        <a class="btn btn--ghost btn--lg" href="{r}our-model/">See our model</a>
      </div>
      <p class="cta-final__contact">
        Or get straight in touch:
        <a href="mailto:info@hiveip.co.uk">info@hiveip.co.uk</a>
{final_phone_html}
      </p>
    </div>
  </section>

</main>

<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-brand">
        <img src="{r}assets/img/logo/hive-logo.png" alt="Hive IP" width="120" height="54" style="height: 40px; width: auto;">
        <p>End-to-end unique-coding for FMCG. Generation, print, validation, fraud monitoring and consumer support &mdash; all from one team.</p>
      </div>
      <div class="footer-col">
        <h5>Solution</h5>
        <ul>
          <li><a href="{r}solution/in-factory/">In-factory print (ACG)</a></li>
          <li><a href="{r}solution/at-supplier/">Packaging-supplier print</a></li>
          <li><a href="{r}solution/validation/">Cloud validation</a></li>
          <li><a href="{r}solution/consumer-support/">Consumer Support Panel</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Why Hive IP</h5>
        <ul>
          <li><a href="{r}why-unique-codes/">Why unique codes</a></li>
          <li><a href="{r}why-in-factory/">Why in-factory</a></li>
          <li><a href="{r}our-model/">Our model</a></li>
          <li><a href="{r}case-studies/">Case studies</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="{r}about/">About Hive IP</a></li>
          <li><a href="{r}insights/">Insights</a></li>
          <li><a href="{r}contact/">Contact</a></li>
          <li><a href="mailto:info@hiveip.co.uk">info@hiveip.co.uk</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="footer-year">2026</span> Hive IP Ltd. All rights reserved.</span>
    </div>
  </div>
</footer>

<script>document.getElementById('footer-year').textContent = new Date().getFullYear();</script>
<script src="{r}assets/js/main.js" defer></script>
</body>
</html>
"""
    return html


def write(path: str, html: str):
    # Compute depth from the output path (e.g., 'case-studies/pepsico/index.html' → depth 2)
    parts = [p for p in path.replace('\\', '/').split('/') if p and p != '.']
    parts = parts[:-1]  # drop filename
    depth = len(parts)
    html = _normalise_links(html, depth)
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(html, encoding="utf-8")
    print(f"  wrote {path}  ({len(html):,} bytes)")


# ---------- Case study helper -------------------------------------------

def case_study_body(*, eyebrow, h1, lead, chips, stats, brief, mechanic, hive_role, results, logo_html="", quote=None, related_links=None):
    """Render the body for a case study page."""
    chip_html = "".join(f'<li class="chip">{c}</li>' for c in chips)
    stat_cards = "".join(
        f'<div class="case-stat"><span class="case-stat__num">{n}</span><span class="case-stat__label">{l}</span></div>'
        for n, l in stats
    )
    qt = ""
    if quote:
        qt = f'''
          <blockquote class="quote-block">
            <p class="quote-block__text">&ldquo;{quote['text']}&rdquo;</p>
            <p class="quote-block__attr"><strong>{quote['name']}</strong>{quote.get('role','')}</p>
          </blockquote>'''

    related = ""
    if related_links:
        items = "".join(f'<li><a href="{href}">{label}</a></li>' for href, label in related_links)
        related = f"<h3>Related</h3><ul>{items}</ul>"

    n_stats = len(stats)
    stat_grid_class = "case-stats--3" if n_stats == 3 else "case-stats--4" if n_stats == 4 else ""

    return f"""
  <section class="section">
    <div class="container">
      <div class="page-hero__inner">
        {logo_html}
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <ul class="chip-row" style="margin-top: 1rem;">{chip_html}</ul>
      </div>

      <div class="case-stats {stat_grid_class}">
        {stat_cards}
      </div>

      <div class="prose" style="margin-top: 3rem;">
        <h2>The brief</h2>
        {brief}

        <h2>The mechanic</h2>
        {mechanic}

        <h2>Hive IP&rsquo;s role</h2>
        {hive_role}

        <h2>The results</h2>
        {results}

        {qt}

        {related}
      </div>
    </div>
  </section>
"""


# ---------- Application page helper -------------------------------------

def application_body(*, eyebrow, h1, lead, why_unique, mechanic_block, example_html, related_apps):
    why_items = "".join(
        f'''<div class="feature-row">
          <div class="feature-row__icon">{icon}</div>
          <div><h3>{h}</h3><p>{p}</p></div>
        </div>''' for h, p, icon in why_unique
    )

    related_html = "".join(
        f'<a class="card" href="{href}"><h3>{title}</h3><p>{desc}</p></a>'
        for href, title, desc in related_apps
    )

    return f"""
  <section class="section">
    <div class="container">
      <div class="page-hero__inner application-hero__inner">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <header class="section-header">
        <span class="eyebrow">Why unique codes fit</span>
        <h2>What unique codes uniquely enable here.</h2>
      </header>
      <div class="feature-stack">
        {why_items}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="prose" style="max-width: 70ch;">
        <h2>How a typical campaign works</h2>
        {mechanic_block}
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="prose" style="max-width: 70ch;">
        <h2>An example in practice</h2>
        {example_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <header class="section-header">
        <span class="eyebrow">Other applications</span>
        <h2>Same per-pack identifier, more uses across the business.</h2>
      </header>
      <div class="cards cards--3">
        {related_html}
      </div>
    </div>
  </section>
"""


# ---------- ICONS for application pages ----------------------------------

ICONS = {
    "trophy":    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5h14v6a7 7 0 01-14 0z"/><path d="M9 19v-3M15 19v-3M8 21h8"/></svg>',
    "heart":     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21l-7-7a4 4 0 015.66-5.66L12 9.66l1.34-1.32A4 4 0 0119 14z"/></svg>',
    "shield":    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/></svg>',
    "box":       '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/></svg>',
    "clock":     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>',
    "spark":     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v6M12 15v6M3 12h6M15 12h6M5.6 5.6l4.2 4.2M14.2 14.2l4.2 4.2M5.6 18.4l4.2-4.2M14.2 9.8l4.2-4.2"/></svg>',
    "check":     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-9"/></svg>',
    "stack":     '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/></svg>',
    "leaf":      '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21c0-9 7-16 16-16-1 9-7 16-16 16z"/><path d="M5 21c4-4 8-7 12-9"/></svg>',
}


# ---------- Page definitions and render ---------------------------------

# ===== Case studies =====

CASE_STUDIES = [
    {
        "slug": "case-studies/pepsico",
        "depth": 2,
        "page_title": "PepsiCo: 200+ ACGS deployed across PepsiCo factories — Hive IP case study",
        "page_desc": "One of Hive IP's largest deployments: 200+ Automated Code Generators installed across PepsiCo factories, supporting Doritos, Walkers and other PepsiCo brands.",
        "current_nav_key": "case-studies",
        "breadcrumbs": [("", "Home"), ("case-studies/", "Case studies"), (None, "PepsiCo")],
        "body": case_study_body(
            logo_html='<img class="case-hero-logo case-hero-logo--pepsico" src="../../assets/img/logos/pepsico.png" alt="PepsiCo" width="900" height="311" loading="eager" decoding="async">',
            eyebrow="Case study · PepsiCo",
            h1="200+ ACGS deployed across PepsiCo factories.",
            lead="One of the largest in-factory unique-coding programmes in European FMCG. More than 200 of Hive IP&rsquo;s ACGs sit on PepsiCo production lines, generating unique codes for Doritos, Walkers and other PepsiCo brands across multiple campaigns and markets.",
            chips=["In-factory", "Multi-market", "Snacks", "Doritos", "Walkers"],
            stats=[
                ("200+", "ACGs installed across PepsiCo factories"),
                ("Multiple", "markets served across PepsiCo campaigns"),
                ("100s of millions", "of unique codes generated for PepsiCo per year"),
                ("0", "production-line slowdowns from ACG deployment"),
            ],
            brief="""
              <p>PepsiCo runs unique-coded promotions for global FMCG brands &mdash; including Doritos and Walkers &mdash; that need hundreds of millions of unique-codes a year, requiring the scale, security and audit posture that a multinational FMCG demands.</p>
              <p>The legacy approach &mdash; codes printed at the packaging supplier &mdash; carried high per-pack costs, long lead times before campaigns could launch, and logistical complexities. So PepsiCo wanted to bring code generation in-factory, integrated with the existing BBD (Best Before Date) printers already on every line.</p>
            """,
            mechanic="""
              <p>Hive IP carried out a factory audit on each site &mdash; line by line, printer by printer, SKU by SKU &mdash; and configured ACGs to match. The ACGs plug into the existing Best Before Date coders without disrupting the production setup. Each line installed in 10&ndash;15 minutes, hot-swappable spares were stocked at every site.</p>
              <p>For each campaign, Hive IP allocates codes per market, per SKU, per line. Operators select the appropriate batch via the Markem controller in the usual way; the ACG generates codes that match the allocation; the codes appear on the outside of the pack alongside the BBD; the full code inventory is synchronised in real time with the cloud validation system.</p>
            """,
            hive_role="""
              <ul>
                <li>Factory audit and line-by-line ACG configuration across PepsiCo sites.</li>
                <li>Supply, install and ongoing service of 200+ ACG units, with hot-swappable spares.</li>
                <li>Cloud validation, fraud monitoring, optional fraud audit workflows where applicable, and the API integration with PepsiCo&rsquo;s appointed agencies.</li>
                <li>Consumer Support Panel for each market, with team-leader account setup and one-hour training per market.</li>
                <li>Direct support during print incidents (mis-allocated codes, batch misselection, etc.) using the team&rsquo;s years of experience resolving such cases.</li>
              </ul>
            """,
            results="""
              <ul>
                <li><strong>Operational scale.</strong> The PepsiCo deployment is one of the largest of its kind in European FMCG.</li>
                <li><strong>Cost.</strong> The in-factory model dramatically reduces the per-million-coded-pack cost compared to the legacy supplier route, and aligns Hive IP&rsquo;s billing with codes actually used in market rather than codes printed.</li>
                <li><strong>Agility.</strong> With every pack already coded, PepsiCo&rsquo;s marketing teams can launch new digital campaigns in days rather than the months a print-cycle previously required.</li>
                <li><strong>Security.</strong> The closed-loop architecture means no list of codes ever exists outside Hive IP&rsquo;s systems &mdash; removing the leak risk that comes with passing code files between organisations.</li>
              </ul>
            """,
            related_links=[
                ("../../solution/in-factory/", "What is an ACG?"),
                ("../../why-in-factory/", "The case for in-factory"),
            ],
        ),
    },
    {
        "slug": "case-studies/news-uk",
        "depth": 2,
        "page_title": "News UK / Sun Saver: unique codes powering loyalty — Hive IP case study",
        "page_desc": "Hive IP supplies and validates the unique codes that underpin News UK's Sun Saver loyalty programme — millions of codes a year, with full audit and consumer support.",
        "current_nav_key": "case-studies",
        "breadcrumbs": [("", "Home"), ("case-studies/", "Case studies"), (None, "News UK / Sun Saver")],
        "body": case_study_body(
            logo_html='<img class="case-hero-logo case-hero-logo--sun" src="../../assets/img/logos/sun-savers.png" alt="The Sun Savers" width="256" height="58" loading="eager" decoding="async">',
            eyebrow="Case study · News UK",
            h1="Unique codes powering the Sun Saver loyalty programme.",
            lead="Hive IP supplies and validates the unique codes that underpin News UK&rsquo;s Sun Saver loyalty programme &mdash; millions of codes a year, with full audit, fraud monitoring and consumer support, integrated into News UK&rsquo;s consumer-facing experience.",
            chips=["Loyalty", "Publishing", "News UK", "Sun Saver"],
            stats=[
                ("Sun Saver", "loyalty programme powered end-to-end"),
                ("Billions", "of unique codes generated each year"),
                ("Multi year", "campaign"),
            ],
            brief="""
              <p>Sun Saver is one of the UK&rsquo;s largest publisher-run loyalty programmes, rewarding readers for their engagement with The Sun. The programme requires a high-volume, high-frequency, fraud-resistant code system that integrates cleanly with News UK&rsquo;s consumer-facing apps and websites.</p>
              <p>The codes need to be unique, single-use, audited end-to-end, and resilient against the kinds of bot-driven and account-farming behaviour any large-scale loyalty programme attracts.</p>
            """,
            mechanic="""
              <p>Hive IP generates the unique codes algorithmically using its proprietary multi-cipher algorithm. The codes are supplied in the format News UK requires for distribution to readers via the publication. When a reader enters a code in the Sun Saver app or website, the code is sent to Hive IP&rsquo;s validation API, which returns the validity, any fraud flags, and the meta-data needed for the consumer-facing experience.</p>
              <p>The system handles the full lifecycle: code generation, distribution, validation, fraud monitoring, audit trail, and customer support.</p>
            """,
            hive_role="""
              <ul>
                <li>Algorithmic code generation, with the security architecture that makes a database breach of issued codes structurally impossible.</li>
                <li>Cloud validation via Hive IP&rsquo;s API, integrated by News UK&rsquo;s digital team.</li>
                <li>Fraud monitoring with configurable thresholds tuned to the loyalty mechanic.</li>
              </ul>
            """,
            results="""
              <ul>
                <li><strong>End-to-end loyalty mechanic.</strong> Sun Saver runs on Hive IP&rsquo;s codes, with no exposure to the systemic database-leak risk that would otherwise put a high-profile loyalty programme at risk.</li>
                <li><strong>Operational scale.</strong> Billions of codes generated and validated, with the audit trail to support the consumer-support team in resolving any issue a reader raises.</li>
                <li><strong>Fraud resilience.</strong> Risk-scoring and behavioural pattern detection keep the programme statistics meaningful and reduce the noise of bot-driven entries.</li>
              </ul>
            """,
            related_links=[
                ("../pepsico/", "PepsiCo"),
                ("../../applications/loyalty/", "Loyalty applications"),
                ("../../solution/validation/", "Cloud validation &amp; fraud monitoring"),
            ],
        ),
    },
    {
        "slug": "case-studies/cereal-brand",
        "depth": 2,
        "page_title": "A leading global cereal brand: 'Buy 3, get 1 free' — Hive IP case study",
        "page_desc": "Anonymised case study: a top-3 global cereal brand used Hive IP unique codes for a 'Buy 3, get 1 free' on-pack promotion. +3.2% market share, ~£750k saving on fixed-fee insurance, 78%+ reduction in code-print cost.",
        "current_nav_key": "case-studies",
        "breadcrumbs": [("", "Home"), ("case-studies/", "Case studies"), (None, "A leading global cereal brand")],
        "body": case_study_body(
            eyebrow="Case study · Anonymised",
            h1="Securing end-of-aisle space without in-store discounting.",
            lead="A top-3 global cereal brand used Hive IP unique codes to run a &lsquo;Buy 3, get 1 free&rsquo; on-pack mechanic. Three unique codes across three packs unlocked a free-cereal voucher &mdash; redeemable in store. The promotion delivered shelf space, share, and a powerful consumer database for follow-up activity.",
            chips=["Promotions", "On-pack", "Cereal", "Anonymised"],
            stats=[
                ("+3.2%", "Market-share uplift"),
                ("~£750k", "Saving on fixed-fee promotional insurance"),
                ("78%+", "Reduction in code-print cost vs the legacy supplier route"),
                ("Hundreds of K", "Consumer records captured for follow-up"),
            ],
            brief="""
              <p>The brand wanted to win additional off-shelf retail presence without resorting to price discounting at the till. They also wanted to capture consumer data they could re-engage later with a follow-up &ldquo;free cereal &amp; milk&rdquo; campaign.</p>
              <p>Their existing supply chain for generating, printing and validating unique codes was complex, expensive and fragmented across multiple parties &mdash; raising both cost and security concerns.</p>
            """,
            mechanic="""
              <p>Each pack carried a unique code. Three codes (one per pack) submitted by the same consumer unlocked a printable voucher redeemable in store for a free pack. The codes were single-use and validated centrally; the audit trail tied every entry back to a specific consumer record for the follow-up campaign.</p>
            """,
            hive_role="""
              <p>Hive IP delivered the end-to-end programme: code generation, in-factory print integration, cloud validation, and fraud monitoring &mdash; replacing what had previously been a fragmented chain of suppliers with a single integrated platform.</p>
            """,
            results="""
              <ul>
                <li><strong>+3.2% market-share uplift</strong> over the promotional period.</li>
                <li><strong>End-of-aisle space</strong> won from major grocery retailers, without paying for the listing or running in-store discounts.</li>
                <li><strong>~£750,000 saved</strong> on fixed-fee promotional insurance, alongside <strong>~£1m saving</strong> across overall campaign costs.</li>
                <li><strong>78%+ reduction in code-print cost</strong> versus the legacy packaging-supplier approach.</li>
                <li><strong>Hundreds of thousands of consumer records</strong> captured, used to run a more efficient follow-up campaign.</li>
              </ul>
            """,
            related_links=[
                ("../household-brand/", "A leading household brand"),
                ("../../applications/promotions/", "Promotions applications"),
            ],
        ),
    },
    {
        "slug": "case-studies/household-brand",
        "depth": 2,
        "page_title": "A leading household brand: digital reactivation through social — Hive IP case study",
        "page_desc": "Anonymised case study: a household brand used Hive IP unique codes to measure how social-media followers convert into purchases. +34% purchase from Facebook, 24% incremental footfall to a major retailer.",
        "current_nav_key": "case-studies",
        "breadcrumbs": [("", "Home"), ("case-studies/", "Case studies"), (None, "A leading household brand")],
        "body": case_study_body(
            eyebrow="Case study · Anonymised",
            h1="Turning social-media followers into measurable purchases.",
            lead="A leading household brand used Hive IP unique codes as the connective tissue between social-media activity and real, repeat purchase &mdash; with results that reshaped how the brand allocated its marketing spend.",
            chips=["Loyalty", "Social", "Household", "Anonymised"],
            stats=[
                ("+34%", "Purchase uplift from social-media followers"),
                ("24%", "Incremental footfall driven to a major retailer"),
                ("12&times;", "Sales impact vs non-recipients"),
            ],
            brief="""
              <p>The brand wanted to understand how its social-media followers were &mdash; or weren&rsquo;t &mdash; converting into real purchase activity. It also wanted to drive incremental footfall to a major retailer and prove the impact attributable to a digital push.</p>
            """,
            mechanic="""
              <p>The brand was already running a points-based loyalty mechanic where consumers earned points by entering Hive IP unique codes from packs. A digital activation invited social followers to donate their points to a charity partner. Each subsequent purchase &mdash; tracked through unique-code entries &mdash; could then be attributed back to the social activation.</p>
              <p>Separately, a geo-targeted email targeted ~30,000 loyalty members who lived near 10 stores of a major UK retailer, offering them extra points for purchasing the brand at that retailer specifically. The unique codes entered after that activation were tied to those redemptions.</p>
            """,
            hive_role="""
              <p>Hive IP&rsquo;s unique-coding platform underpinned both activations &mdash; generation, validation, fraud monitoring, and the audit trail that allowed the brand to attribute purchase activity to specific marketing pushes.</p>
            """,
            results="""
              <ul>
                <li><strong>+34% purchase uplift</strong> from social-media followers in the months following the activation.</li>
                <li><strong>24% incremental footfall</strong> to the targeted major UK retailer.</li>
                <li><strong>12&times; sales impact</strong> compared to similar consumers who didn&rsquo;t receive the activation.</li>
                <li>Insights that reshaped the brand&rsquo;s view of how its social spend converts to sales &mdash; and how on-pack and digital channels reinforce each other.</li>
              </ul>
            """,
            related_links=[
                ("../cereal-brand/", "A leading global cereal brand"),
                ("../../applications/loyalty/", "Loyalty applications"),
            ],
        ),
    },
    {
        "slug": "case-studies/sports-drink-brand",
        "depth": 2,
        "page_title": "A leading sports-drink brand: just-in-time digital activation — Hive IP case study",
        "page_desc": "Anonymised case study: a sports-drink brand used Hive IP's always-on coding to launch a digital direct-to-consumer push within minutes of a major sporting moment, without any new printing.",
        "current_nav_key": "case-studies",
        "breadcrumbs": [("", "Home"), ("case-studies/", "Case studies"), (None, "A leading sports-drink brand")],
        "body": case_study_body(
            eyebrow="Case study · Anonymised",
            h1="A digital direct-to-consumer push live within minutes of a major sporting moment.",
            lead="A leading sports-drink brand wanted to capitalise on the moment a sponsored athlete won a major championship &mdash; without losing days or weeks waiting for a print run. With every pack already coded by Hive IP, the campaign launched within minutes of the result.",
            chips=["Promotions", "Sports", "Just-in-time", "Anonymised"],
            stats=[
                ("Minutes", "From sporting result to email going live"),
                ("Days", "From idea to live campaign &mdash; instead of months"),
                ("High", "Engagement rates from time-relevance"),
            ],
            brief="""
              <p>The brand sponsored an athlete who was rapidly becoming the centre of public attention ahead of a major sporting event. The marketing team wanted to be ready to react the instant the athlete won &mdash; not wait for the planning, briefing, printing and supply-chain cycle of a traditional on-pack promotion.</p>
            """,
            mechanic="""
              <p>Because Hive IP had been printing unique codes on every pack of the brand all year, the packs were already &ldquo;promotionally ready&rdquo; sitting on shelves nationwide. The marketing team designed and built a digital experience that would let consumers enter their on-pack code to win a chance to train with the athlete &mdash; and held it ready to fire.</p>
              <p>When the athlete won the championship, the campaign went live within minutes. An email went to a targeted segment of consumers; a digital experience let them enter their unique code from a pack they already had at home. Validation, fraud monitoring and reward fulfilment all ran through Hive IP&rsquo;s standard infrastructure.</p>
            """,
            hive_role="""
              <p>The whole campaign rested on Hive IP&rsquo;s always-on coding model: every pack carrying a code, validation infrastructure live, no incremental print-cost penalty for coding everything. The activation could only happen because of decisions made months earlier about how the brand wanted to be set up.</p>
            """,
            results="""
              <ul>
                <li><strong>Live within minutes</strong> of the athlete&rsquo;s win &mdash; capturing public mood at its peak.</li>
                <li><strong>Days, not months</strong> from idea to live campaign &mdash; without any new printing or supply-chain cycle.</li>
                <li><strong>High engagement rates</strong> driven by the time-relevance of the activation.</li>
                <li>Demonstrated the strategic value of always-on coding as a marketing-agility lever, not just a cost reduction.</li>
              </ul>
            """,
            related_links=[
                ("../cereal-brand/", "A leading global cereal brand"),
                ("../../applications/promotions/", "Promotions applications"),
                ("../../why-in-factory/", "The case for in-factory"),
            ],
        ),
    },
]


# ===== Case studies index =====

CASE_INDEX = {
    "slug": "case-studies",
    "depth": 1,
    "page_title": "Case studies — Hive IP",
    "page_desc": "Selected Hive IP customer case studies. Named programmes (PepsiCo, News UK / Sun Saver) and anonymised stories from leading FMCG brands across cereal, household, and sports drinks.",
    "current_nav_key": "case-studies",
    "breadcrumbs": [("", "Home"), (None, "Case studies")],
}


def case_index_body():
    cards = []
    cases = [
        ("pepsico/", "PepsiCo", "200+ ACGs installed",
         "One of the largest in-factory unique-coding programmes in European FMCG. Doritos, Walkers and other PepsiCo brands across multiple campaigns and markets.",
         "Named"),
        ("news-uk/", "News UK / Sun Saver", "Loyalty for one of the UK's largest publisher loyalty programmes",
         "Hive IP supplies and validates the unique codes underpinning News UK's Sun Saver loyalty programme.",
         "Named"),
        ("cereal-brand/", "A leading global cereal brand", "+3.2% market share, 78%+ print savings",
         "&lsquo;Buy 3, get 1 free&rsquo; on-pack mechanic that won shelf space without in-store discounting.",
         "Anonymised"),
        ("household-brand/", "A leading household brand", "+34% purchase from social, 12&times; sales impact",
         "Loyalty mechanic that connected social-media followers to real purchase data &mdash; and reshaped the brand&rsquo;s spend allocation.",
         "Anonymised"),
        ("sports-drink-brand/", "A leading sports-drink brand", "Live within minutes of a sporting moment",
         "Always-on coding meant a major digital activation could launch the moment a sponsored athlete won &mdash; not months later.",
         "Anonymised"),
    ]
    for href, title, headline, desc, chip in cases:
        if href == "pepsico/":
            media = '<img class="case-logo-card case-logo-card--pepsico" src="../assets/img/logos/pepsico.png" alt="PepsiCo" width="900" height="311" loading="lazy" decoding="async">'
            media_class = "case-card__media case-card__media--logo"
        elif href == "news-uk/":
            media = '<img class="case-logo-card case-logo-card--sun" src="../assets/img/logos/sun-savers.png" alt="The Sun Savers" width="256" height="58" loading="lazy" decoding="async">'
            media_class = "case-card__media case-card__media--logo"
        elif href == "cereal-brand/":
            media = '<img src="../assets/img/case-studies/cereal-brand.svg" alt="Illustration of a global cereal promotion using unique on-pack codes" width="1200" height="675" loading="lazy" decoding="async">'
            media_class = "case-card__media"
        elif href == "household-brand/":
            media = '<img src="../assets/img/case-studies/household-brand.svg" alt="Illustration of a household brand loyalty mechanic linked to verified purchase data" width="1200" height="675" loading="lazy" decoding="async">'
            media_class = "case-card__media"
        elif href == "sports-drink-brand/":
            media = '<img src="../assets/img/case-studies/sports-drink-brand.svg" alt="Illustration of always-on sports-drink coding ready for live campaign activation" width="1200" height="675" loading="lazy" decoding="async">'
            media_class = "case-card__media"
        else:
            raise ValueError(f"No case-study card media configured for {href}")
        cards.append(f"""
        <a class="case-card" href="{href}">
          <div class="{media_class}">
            {media}
          </div>
          <div class="case-card__body">
            <span class="case-card__chip">{chip} &middot; {headline}</span>
            <h3>{title}</h3>
            <p>{desc}</p>
            <span class="case-card__cta">Read the case <svg class="arrow" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8h10M9 4l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          </div>
        </a>""")

    return f"""
  <section class="section">
    <div class="container">
      <div class="page-hero__inner">
        <span class="eyebrow">Case studies</span>
        <h1>Selected Hive IP customer programmes.</h1>
        <p class="lead">Two named customer programmes &mdash; PepsiCo and News UK&rsquo;s Sun Saver &mdash; alongside anonymised stories from leading FMCG brands across cereal, household and sports drinks. All run on the same end-to-end Hive IP platform.</p>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="cards cards--3">
        {''.join(cards)}
      </div>
    </div>
  </section>
"""


# ===== Applications =====

APPLICATIONS = [
    {
        "slug": "applications/promotions",
        "depth": 2,
        "page_title": "Unique codes for FMCG promotions — Hive IP",
        "page_desc": "On-pack and digital direct-to-consumer promotions powered by unique codes. Just-in-time launches, verified entries, and real engagement data — without the print-cycle delay.",
        "current_nav_key": "applications",
        "breadcrumbs": [("", "Home"), ("applications/", "Applications"), (None, "Promotions")],
        "body": application_body(
            eyebrow="Applications · Promotions",
            h1="On-pack and digital promotions, powered by unique codes.",
            lead="The original use case for unique codes &mdash; and still the most common one. With every pack carrying a code, you can run on-pack promotions without the supply-chain wait, and run digital direct-to-consumer pushes whenever an opportunity appears.",
            why_unique=[
                ("Single-use enforcement",
                 "Each code can only be used once, by one consumer. Promotion mechanics that depend on real proof-of-purchase actually work, rather than being gamed by repeated entries.",
                 ICONS["check"]),
                ("Just-in-time launches",
                 "When every pack already carries a code, a campaign that would traditionally take three to six months can launch in days or hours. React to live events, sponsorship moments, and competitor pushes.",
                 ICONS["clock"]),
                ("Verified engagement data",
                 "Every entry is a real consumer interaction with a real pack. Campaign statistics are meaningful because the entries that produced them are verifiable.",
                 ICONS["spark"]),
                ("Both on-pack and digital channels",
                 "The same coded packs sitting on shelves can be activated through on-pack messaging or pulled into digital pushes &mdash; the brand&rsquo;s choice, depending on the campaign.",
                 ICONS["trophy"]),
            ],
            mechanic_block="""
              <p>A typical promotion runs in five steps:</p>
              <ol>
                <li>Marketing decides on a mechanic (instant win, prize draw, free product, multi-purchase reward, etc.) and the eligible SKUs and markets.</li>
                <li>The agency builds the consumer-facing experience &mdash; web or app &mdash; with Hive IP&rsquo;s API integrated for code validation.</li>
                <li>The campaign goes live; consumers enter unique codes from packs in the experience.</li>
                <li>Hive IP validates each entry, returns the result and any associated metadata, and applies fraud monitoring and risk-scoring in real time.</li>
                <li>Marketing reads the campaign data; the consumer-support team handles any queries via the Consumer Support Panel.</li>
              </ol>
              <p>The novel part isn&rsquo;t the mechanic &mdash; mechanics have been around for decades. The novel part is the speed at which they can launch and the fidelity of the data they produce.</p>
            """,
            example_html="""
              <p>One example, anonymised: a leading sports-drink brand wanted to capitalise on a major sporting moment involving a sponsored athlete. Because every pack already carried a unique code, the brand could launch a digital activation within minutes of the result &mdash; an email to targeted consumers offering the chance to win a training session with the athlete, redeemable by entering the code on a pack they already had at home. The campaign would have been impossible under a print-supply-chain timeline; it was straightforward under Hive IP&rsquo;s always-on coding model.</p>
              <p><a href="../../case-studies/sports-drink-brand/">Read the full case study &rarr;</a></p>
            """,
            related_apps=[
                ("../loyalty/", "Loyalty &amp; rewards", "Multi-purchase rewards, points collection, repeat-purchase tracking."),
                ("../anti-counterfeit/", "Anti-counterfeiting", "Use the same per-pack identifier as a brand-protection signature."),
                ("../supply-chain/", "Supply chain", "Traceability, provenance, sustainability data and recall."),
            ],
        ),
    },
    {
        "slug": "applications/loyalty",
        "depth": 2,
        "page_title": "Unique codes for loyalty &amp; rewards — Hive IP",
        "page_desc": "Multi-purchase rewards, points-collection mechanics and repeat-purchase tracking powered by unique codes. The same mechanic behind News UK's Sun Saver programme.",
        "current_nav_key": "applications",
        "breadcrumbs": [("", "Home"), ("applications/", "Applications"), (None, "Loyalty &amp; rewards")],
        "body": application_body(
            eyebrow="Applications · Loyalty",
            h1="Loyalty programmes that reward real purchases.",
            lead="Multi-purchase rewards, points-collection mechanics and repeat-purchase tracking. Unique codes turn every pack into an authenticated proof-of-purchase event &mdash; the foundation of any meaningful loyalty programme.",
            why_unique=[
                ("Real proof-of-purchase",
                 "A loyalty programme is only as good as its proof. Unique codes are single-use and enforce real purchases, eliminating the bot- and account-farm noise that plagues batch-code or no-verification mechanics.",
                 ICONS["heart"]),
                ("Clean, actionable consumer data",
                 "Because a fake account can&rsquo;t enter a code it doesn&rsquo;t physically have, the member database a unique-code programme produces is essentially self-cleaning. Every record corresponds to a real person who made a real purchase &mdash; the foundation of meaningful personalisation, lifetime-value modelling, and ROI measurement.",
                 ICONS["check"]),
                ("Per-consumer history",
                 "Every code entry is tied to a consumer record. You see what each member has bought, when, where, and over what time period &mdash; making personalisation and lifetime-value modelling possible.",
                 ICONS["stack"]),
                ("Fraud-resilient at scale",
                 "Behavioural risk-scoring catches the abuse patterns that long-running loyalty programmes attract. Configurable thresholds tune the mechanic to your tolerance.",
                 ICONS["shield"]),
            ],
            mechanic_block="""
              <p>A typical multi-purchase loyalty programme runs like this:</p>
              <ol>
                <li>Consumers register with the programme.</li>
                <li>Every pack purchased carries a unique code; consumers enter it to earn points or progress through a tiered mechanic.</li>
                <li>Each entry is validated by Hive IP&rsquo;s API, with fraud monitoring running in the background.</li>
                <li>Consumers redeem points for rewards &mdash; products, vouchers, charitable donations, prizes, experiences.</li>
                <li>The audit trail per consumer powers the personalised follow-up activity that turns short-term participation into long-term value.</li>
              </ol>
            """,
            example_html="""
              <p><strong>Sun Saver</strong> is one of the UK&rsquo;s largest publisher-run loyalty programmes, run by News UK for readers of The Sun. Hive IP supplies and validates the unique codes that underpin the programme &mdash; millions of codes a year, with full audit, fraud monitoring and consumer support. <a href="../../case-studies/news-uk/">Read the full case study &rarr;</a></p>
              <p>Anonymised: a leading household brand ran a multi-purchase loyalty mechanic where consumers earned points by entering on-pack codes. A targeted social activation reactivated dormant members &mdash; resulting in a 34% purchase uplift among social followers and 24% incremental footfall to a major retailer. <a href="../../case-studies/household-brand/">Read more &rarr;</a></p>
            """,
            related_apps=[
                ("../promotions/", "Promotions", "On-pack and digital direct-to-consumer campaigns."),
                ("../anti-counterfeit/", "Anti-counterfeiting", "Use the same identifier for brand protection."),
                ("../supply-chain/", "Supply chain", "Traceability, provenance, recall."),
            ],
        ),
    },
    {
        "slug": "applications/anti-counterfeit",
        "depth": 2,
        "page_title": "Unique codes for anti-counterfeiting and brand protection — Hive IP",
        "page_desc": "Each pack carries a digital signature — a passport for authenticity. Used by support teams, retailers and consumers to verify the real product and detect counterfeit activity.",
        "current_nav_key": "applications",
        "breadcrumbs": [("", "Home"), ("applications/", "Applications"), (None, "Anti-counterfeiting")],
        "body": application_body(
            eyebrow="Applications · Anti-counterfeiting",
            h1="A digital signature on every pack.",
            lead="A unique code is more than a promotional tool. It&rsquo;s a passport for authenticity that consumers, support teams and channel partners can use to verify the real product &mdash; and that brands can use to detect counterfeit activity by what doesn&rsquo;t validate.",
            why_unique=[
                ("Unguessable",
                 "Codes are non-sequential and produced by a multi-cipher proprietary algorithm. Counterfeiters can&rsquo;t generate plausible codes by pattern-spotting from genuine ones.",
                 ICONS["shield"]),
                ("Closed-loop architecture",
                 "Codes are never stored on the ACG and never held in a database that could be leaked. There is no master list to steal &mdash; the algorithm itself is the only source of truth.",
                 ICONS["check"]),
                ("Validation in seconds",
                 "Anyone with the right access &mdash; consumer, retailer, support team, customs &mdash; can verify a code via the Hive IP system and get an immediate authenticity signal.",
                 ICONS["spark"]),
                ("Detection by absence",
                 "Codes that don&rsquo;t validate are themselves a signal. Patterns of failed validations &mdash; geographic, temporal, product-line &mdash; can pinpoint counterfeit activity in specific markets.",
                 ICONS["stack"]),
            ],
            mechanic_block="""
              <p>Anti-counterfeit programmes built on unique codes typically combine three layers:</p>
              <ol>
                <li><strong>The code on the pack.</strong> Generated by Hive IP, printed in the factory, scannable by anyone with a phone camera.</li>
                <li><strong>Validation infrastructure.</strong> Either Hive IP&rsquo;s standard API integrated into a brand-owned check experience, or a dedicated authenticity microsite branded for the campaign.</li>
                <li><strong>The signal.</strong> Genuine codes return authenticated; suspicious or invalid codes are logged. Patterns of suspicious activity surface in dashboards used by the brand&rsquo;s legal, security and operational teams.</li>
              </ol>
            """,
            example_html="""
              <p>For brands operating in markets where counterfeiting is a known risk, the anti-counterfeit application can run alongside a promotional or loyalty programme on the same codes. The cost of generating and printing the codes is already absorbed by the primary mechanic; the additional brand-protection value is essentially free, because the same per-pack identifier serves both jobs.</p>
              <p>This is one of the strongest arguments for coding every pack, all the time, regardless of whether a specific promotion is running on it.</p>
            """,
            related_apps=[
                ("../promotions/", "Promotions", "On-pack and digital activations."),
                ("../loyalty/", "Loyalty &amp; rewards", "Multi-purchase mechanics."),
                ("../supply-chain/", "Supply chain", "Traceability, provenance, recall."),
            ],
        ),
    },
    {
        "slug": "applications/supply-chain",
        "depth": 2,
        "page_title": "Unique codes for supply-chain traceability, provenance and recall — Hive IP",
        "page_desc": "Each pack carries a per-unit identifier from the moment it leaves the line. Use it for traceability, provenance, sustainability data, and clean recall handling.",
        "current_nav_key": "applications",
        "breadcrumbs": [("", "Home"), ("applications/", "Applications"), (None, "Supply chain")],
        "body": application_body(
            eyebrow="Applications · Supply chain",
            h1="A per-unit identifier from the moment it leaves the line.",
            lead="The same unique code that powers your promotion or loyalty programme is also a per-pack supply-chain identifier &mdash; one you can use for traceability, provenance, sustainability data, and clean recall handling.",
            why_unique=[
                ("Per-pack, not per-batch",
                 "A unique code identifies an individual unit, not just a production run. The granularity that makes targeted recall, fraud detection and provenance proof actually possible.",
                 ICONS["box"]),
                ("Captured at the line",
                 "When the code is printed in-factory by the ACG, it can be associated at the moment of production with the SKU, line, date and any other meta-data your operations team needs.",
                 ICONS["stack"]),
                ("Same data layer as your promotions",
                 "You don&rsquo;t need a separate identifier for supply-chain use; the codes that underpin marketing also underpin operations &mdash; one source of truth, one data model.",
                 ICONS["check"]),
                ("Provenance and sustainability stories",
                 "Use the per-pack code to link consumers to provenance data, ingredient origin, carbon-footprint information, or any sustainability-credential proof point that matters to your category.",
                 ICONS["leaf"]),
            ],
            mechanic_block="""
              <p>Supply-chain applications built on Hive IP unique codes typically work in one of two patterns:</p>
              <ol>
                <li><strong>Operational lookup.</strong> An internal team (operations, recall, customer service) enters a code and gets back the production date, line, batch and any other meta-data captured at the moment of production. Useful for targeted recall, complaint investigation, and quality forensics.</li>
                <li><strong>Consumer-facing experience.</strong> A consumer scans the pack and sees provenance, sustainability or product-story content tailored to that specific unit &mdash; not the generic SKU. Strong for premium and provenance-led categories.</li>
              </ol>
              <p>Both run on the same code-generation, validation and audit infrastructure as the rest of the Hive IP platform.</p>
            """,
            example_html="""
              <p>For brands already running unique-coding for promotions or loyalty, adding supply-chain traceability is largely a configuration exercise rather than a new programme. The codes already exist on the packs; the production meta-data is already captured at the line; the validation API can return that meta-data alongside any code submission. What&rsquo;s needed is a deliberate consumer-facing or internal-facing experience to surface it.</p>
              <p>This is one of the clearest arguments for thinking about unique-coding as a strategic data layer rather than a per-campaign expense.</p>
            """,
            related_apps=[
                ("../promotions/", "Promotions", "On-pack and digital activations."),
                ("../loyalty/", "Loyalty &amp; rewards", "Multi-purchase mechanics."),
                ("../anti-counterfeit/", "Anti-counterfeiting", "Brand protection."),
            ],
        ),
    },
]


APPS_INDEX = {
    "slug": "applications",
    "depth": 1,
    "page_title": "Applications — Hive IP",
    "page_desc": "What every pack carrying a unique code unlocks: promotions, loyalty, anti-counterfeiting, supply-chain traceability — all from the same data layer.",
    "current_nav_key": "applications",
    "breadcrumbs": [("", "Home"), (None, "Applications")],
}


def apps_index_body():
    apps = [
        ("promotions/",       "Promotions",        ICONS["trophy"], "On-pack and digital direct-to-consumer campaigns. Just-in-time launches reacting to live events. Verified entries, real engagement data."),
        ("loyalty/",          "Loyalty &amp; rewards",       ICONS["heart"],  "Multi-purchase reward schemes, tiered point collection, repeat-purchase tracking. The mechanic behind News UK&rsquo;s Sun Saver programme."),
        ("anti-counterfeit/", "Anti-counterfeiting",         ICONS["shield"], "A digital signature on every pack &mdash; a passport for authenticity, used by support teams and customers to verify the real product."),
        ("supply-chain/",     "Supply chain",                ICONS["box"],    "Traceability, provenance, sustainability data and recall handling &mdash; all anchored to the same per-pack identifier from the moment it leaves the line."),
    ]
    cards = "".join(
        f'''<a class="card" href="{href}">
          <div class="card__icon" aria-hidden="true">{icon}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
          <span class="card__cta">{title.split(' ')[0]} &rarr;</span>
        </a>''' for href, title, icon, desc in apps
    )
    return f"""
  <section class="section">
    <div class="container">
      <div class="page-hero__inner">
        <span class="eyebrow">Applications</span>
        <h1>What every pack carrying a unique code unlocks.</h1>
        <p class="lead">Unique codes started as a promotional tool. With every pack coded all the time, they become a foundation for loyalty, brand protection, supply-chain traceability and more &mdash; all from the same data layer.</p>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="cards cards--3">
        {cards}
      </div>
    </div>
  </section>
"""


# ---------- Run ----------

def main():
    print("Generating Phase 3 pages...")

    # Case studies
    write("case-studies/index.html",
          page(depth=CASE_INDEX["depth"], title=CASE_INDEX["page_title"],
               description=CASE_INDEX["page_desc"], slug_path=CASE_INDEX["slug"],
               body_html=case_index_body(), breadcrumbs=CASE_INDEX["breadcrumbs"],
               current_nav_key=CASE_INDEX["current_nav_key"]))

    for c in CASE_STUDIES:
        if c["slug"] in {"case-studies/pepsico", "case-studies/news-uk"}:
            print(f"  skipped {c['slug']}/index.html  (hand-authored page)")
            continue
        write(f"{c['slug']}/index.html",
              page(depth=c["depth"], title=c["page_title"],
                   description=c["page_desc"], slug_path=c["slug"],
                   body_html=c["body"], breadcrumbs=c["breadcrumbs"],
                   current_nav_key=c["current_nav_key"]))

    # Applications
    write("applications/index.html",
          page(depth=APPS_INDEX["depth"], title=APPS_INDEX["page_title"],
               description=APPS_INDEX["page_desc"], slug_path=APPS_INDEX["slug"],
               body_html=apps_index_body(), breadcrumbs=APPS_INDEX["breadcrumbs"],
               current_nav_key=APPS_INDEX["current_nav_key"]))

    for a in APPLICATIONS:
        write(f"{a['slug']}/index.html",
              page(depth=a["depth"], title=a["page_title"],
                   description=a["page_desc"], slug_path=a["slug"],
                   body_html=a["body"], breadcrumbs=a["breadcrumbs"],
                   current_nav_key=a["current_nav_key"]))

    print("Done.")


if __name__ == "__main__":
    main()
