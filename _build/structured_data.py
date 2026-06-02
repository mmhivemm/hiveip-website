#!/usr/bin/env python3
"""Shared JSON-LD generation for hiveip.co.uk.

The public HTML is static, but structured data should still be maintained from
one build-time source. This module keeps the site-wide entities and per-page
schema rules together so generated and hand-authored pages stay consistent.
"""

import html
import json
import re
from pathlib import Path

BASE_URL = "https://hiveip.co.uk"
ORG_ID = f"{BASE_URL}/#organization"
WEBSITE_ID = f"{BASE_URL}/#website"
LOGO_ID = f"{BASE_URL}/#logo"
LOGO_URL = f"{BASE_URL}/assets/img/logo/hive-logo.png"
DEFAULT_IMAGE = f"{BASE_URL}/assets/img/og/home.png"
LANGUAGE = "en-GB"

ORG_MINIMAL = {
    "@type": "Corporation",
    "@id": ORG_ID,
    "name": "Hive IP",
    "url": f"{BASE_URL}/",
}

ORG_FULL = {
    **ORG_MINIMAL,
    "legalName": "HIVE IP LTD",
    "alternateName": "Hive IP Ltd",
    "identifier": "04696887",
    "logo": {
        "@type": "ImageObject",
        "@id": LOGO_ID,
        "url": LOGO_URL,
        "caption": "Hive IP logo",
    },
    "email": "info@hiveip.co.uk",
    "description": (
        "Hive IP provides end-to-end unique-coding infrastructure for FMCG "
        "brands, including code generation, in-factory or packaging-supplier "
        "print, cloud validation, fraud monitoring and consumer support."
    ),
    "areaServed": ["GB", "EU"],
    "knowsAbout": [
        "FMCG promotional marketing",
        "Unique coding systems on packaging",
        "FMCG loyalty programmes",
        "Supply chain traceability",
        "Brand protection",
        "Anti-counterfeit packaging",
        "Cloud validation APIs",
        "Automated Code Generator",
    ],
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": "info@hiveip.co.uk",
            "availableLanguage": ["en"],
        }
    ],
}

WEBSITE_MINIMAL = {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    "url": f"{BASE_URL}/",
    "name": "Hive IP",
    "publisher": {"@id": ORG_ID},
}

WEBSITE_FULL = {
    **WEBSITE_MINIMAL,
    "description": (
        "Unique codes for FMCG promotions and loyalty programmes, generated, "
        "printed and validated end-to-end."
    ),
}

PAGE_TYPE_OVERRIDES = {
    "": "WebPage",
    "about": "AboutPage",
    "contact": "ContactPage",
    "applications": "CollectionPage",
    "case-studies": "CollectionPage",
    "insights": "CollectionPage",
    "privacy-policy": "WebPage",
    "cookie-policy": "WebPage",
    "privacy": "WebPage",
}

MAIN_ENTITIES = {
    "why-unique-codes": {
        "@type": "Thing",
        "@id": f"{BASE_URL}/why-unique-codes/#topic",
        "name": "Single-use unique coding",
        "description": (
            "A proof-of-purchase approach that replaces reusable batch codes "
            "and high-friction receipt uploads with individual, single-use "
            "pack codes."
        ),
    },
    "why-in-factory": {
        "@type": "Thing",
        "@id": f"{BASE_URL}/why-in-factory/#topic",
        "name": "In-factory unique-code printing",
        "description": (
            "Printing unique codes in the production facility to reduce print "
            "cost, remove packaging supply-chain delays and keep every pack "
            "campaign-ready."
        ),
    },
    "our-model": {
        "@type": "Service",
        "@id": f"{BASE_URL}/our-model/#service",
        "name": "No CapEx promotional coding model",
        "provider": {"@id": ORG_ID},
        "description": (
            "Hive IP supplies ACG line hardware without capital expenditure "
            "and bills for codes covered by active campaign windows."
        ),
        "areaServed": ["GB", "EU"],
    },
    "solution/in-factory": {
        "@type": "Product",
        "@id": f"{BASE_URL}/solution/in-factory/#product",
        "name": "Automated Code Generator (ACG)",
        "description": (
            "A proprietary industrial hardware device that integrates with "
            "existing production-line printers to generate and print "
            "non-sequential unique codes."
        ),
        "brand": {"@id": ORG_ID},
        "manufacturer": {"@id": ORG_ID},
    },
    "solution/at-supplier": {
        "@type": "Service",
        "@id": f"{BASE_URL}/solution/at-supplier/#service",
        "name": "Packaging-supplier code provisioning",
        "provider": {"@id": ORG_ID},
        "description": (
            "Secure generation and supply of unique codes for packaging "
            "suppliers when brands prefer supplier-side or inside-pack print."
        ),
        "areaServed": ["GB", "EU"],
    },
    "solution/validation": {
        "@type": "WebApplication",
        "@id": f"{BASE_URL}/solution/validation/#software",
        "name": "Hive IP Cloud Validation API",
        "applicationCategory": ["BusinessApplication", "SecurityApplication"],
        "operatingSystem": "Cloud API",
        "author": {"@id": ORG_ID},
        "description": (
            "Cloud validation infrastructure for high-throughput, real-time, "
            "algorithmic authentication of unique code entries."
        ),
    },
    "solution/consumer-support": {
        "@type": "Service",
        "@id": f"{BASE_URL}/solution/consumer-support/#service",
        "name": "Consumer Support Panel and fraud administration dashboard",
        "provider": {"@id": ORG_ID},
        "description": (
            "Consumer support tooling for checking codes, auditing queries, "
            "viewing consumer history and monitoring fraud signals."
        ),
        "areaServed": ["GB", "EU"],
    },
    "applications/promotions": {
        "@type": "Service",
        "@id": f"{BASE_URL}/applications/promotions/#service",
        "name": "Unique codes for on-pack promotions",
        "provider": {"@id": ORG_ID},
        "description": "Unique-code mechanics for FMCG promotions, prize draws, rewards and proof of purchase.",
    },
    "applications/loyalty": {
        "@type": "Service",
        "@id": f"{BASE_URL}/applications/loyalty/#service",
        "name": "Unique codes for loyalty and rewards",
        "provider": {"@id": ORG_ID},
        "description": "Per-pack unique codes for loyalty, points collection and repeat-purchase rewards.",
    },
    "applications/anti-counterfeit": {
        "@type": "Service",
        "@id": f"{BASE_URL}/applications/anti-counterfeit/#service",
        "name": "Unique codes for anti-counterfeit and brand protection",
        "provider": {"@id": ORG_ID},
        "description": "Per-pack unique codes for consumer-facing authenticity checks and fraud monitoring.",
    },
    "applications/supply-chain": {
        "@type": "Service",
        "@id": f"{BASE_URL}/applications/supply-chain/#service",
        "name": "Unique codes for supply-chain traceability",
        "provider": {"@id": ORG_ID},
        "description": "Per-pack identifiers for provenance, traceability and supply-chain data capture.",
    },
}

ITEM_LISTS = {
    "solution": [
        ("In-factory print (ACG)", "solution/in-factory/"),
        ("Packaging-supplier print", "solution/at-supplier/"),
        ("Cloud validation", "solution/validation/"),
        ("Consumer Support Panel", "solution/consumer-support/"),
    ],
    "applications": [
        ("Promotions", "applications/promotions/"),
        ("Loyalty and rewards", "applications/loyalty/"),
        ("Anti-counterfeit", "applications/anti-counterfeit/"),
        ("Supply-chain traceability", "applications/supply-chain/"),
    ],
    "case-studies": [
        ("PepsiCo", "case-studies/pepsico/"),
        ("News UK / Sun Saver", "case-studies/news-uk/"),
        ("A leading global cereal brand", "case-studies/cereal-brand/"),
        ("A leading household brand", "case-studies/household-brand/"),
        ("A leading sports-drink brand", "case-studies/sports-drink-brand/"),
    ],
    "insights": [
        ("Unique codes, two campaign engines", "insights/on-pack-digital-campaigns/"),
        ("Receipts, batch codes, unique codes", "insights/proof-of-purchase-mechanics/"),
        ("Why in-factory unique-code printing can save 78% or more", "insights/in-factory-printing-cheaper/"),
        ("Closed-loop coding", "insights/closed-loop-validation/"),
        ("Outside vs inside the pack", "insights/outside-vs-inside-pack-code-copying/"),
        ("From on-pack to digital", "insights/agile-digital-promotions/"),
        ("Beyond promotions", "insights/beyond-promotions-five-uses/"),
    ],
}

ARTICLE_DATES = {
    "insights/on-pack-digital-campaigns": "2026-05-15",
    "insights/proof-of-purchase-mechanics": "2026-04-30",
    "insights/in-factory-printing-cheaper": "2026-04-22",
    "insights/closed-loop-validation": "2026-04-15",
    "insights/outside-vs-inside-pack-code-copying": "2026-04-08",
    "insights/agile-digital-promotions": "2026-03-30",
    "insights/beyond-promotions-five-uses": "2026-03-20",
}

FAQ_ENTITIES = {
    "why-unique-codes": [
        (
            "What's wrong with batch codes for promotions?",
            "A batch code is the same code printed on every pack of a SKU. Once one consumer enters it, anyone can reuse it indefinitely. Limiting entries per account does not help because fraudsters and bots can create more accounts.",
        ),
        (
            "Why aren't till receipts good enough as proof of purchase?",
            "Till receipts are trivially faked, photographed, edited or generated with image tools. They are hard to audit at scale and create high consumer friction.",
        ),
        (
            "What makes Hive IP's unique-coding architecture different?",
            "Codes are generated algorithmically and are not stored on the ACG or held in a master list. Validation reverse-engineers each code algorithmically rather than looking it up in a table.",
        ),
    ],
    "why-in-factory": [
        (
            "Why print unique codes in the factory?",
            "In-factory printing removes packaging supplier lead times, reduces print cost and lets every pack carry a code whether or not a campaign is already live.",
        ),
        (
            "Does printing outside the pack create code-copying risk?",
            "Hive IP treats code-copying as a measurable campaign risk. For higher-risk mechanics, brands can add audit workflows, winner pack-retention checks and optional AI Vision review.",
        ),
    ],
}


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slug_to_url(slug_path: str) -> str:
    slug = (slug_path or "").strip("/")
    if not slug:
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{slug}/"


def image_url(og_image: str | None) -> str:
    if not og_image:
        return DEFAULT_IMAGE
    if og_image.startswith("http://") or og_image.startswith("https://"):
        return og_image
    return f"{BASE_URL}/{og_image.lstrip('/')}"


def breadcrumb_graph(slug_path: str, breadcrumbs: list[tuple[str | None, str]] | None) -> dict | None:
    if not breadcrumbs:
        return None
    items = []
    canonical = slug_to_url(slug_path)
    for position, (href, label) in enumerate(breadcrumbs, 1):
        if href is None:
            item = canonical
        elif href == "":
            item = f"{BASE_URL}/"
        else:
            item = slug_to_url(href)
        items.append({
            "@type": "ListItem",
            "position": position,
            "name": clean_text(label),
            "item": item,
        })
    return {
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": items,
    }


def item_list_graph(slug_path: str) -> dict | None:
    slug = (slug_path or "").strip("/")
    items = ITEM_LISTS.get(slug)
    if not items:
        return None
    return {
        "@type": "ItemList",
        "@id": f"{slug_to_url(slug)}#itemlist",
        "name": f"{clean_text(slug.replace('-', ' ').title())} list",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "url": slug_to_url(url),
            }
            for position, (name, url) in enumerate(items, 1)
        ],
    }


def faq_graph(slug_path: str) -> dict | None:
    slug = (slug_path or "").strip("/")
    questions = FAQ_ENTITIES.get(slug)
    if not questions:
        return None
    return {
        "@type": "FAQPage",
        "@id": f"{slug_to_url(slug)}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
            for question, answer in questions
        ],
    }


def page_type_for(slug_path: str, requested: str | None = None) -> str:
    if requested:
        return requested
    slug = (slug_path or "").strip("/")
    if slug.startswith("insights/") and slug != "insights":
        return "WebPage"
    if slug.startswith("case-studies/") and slug != "case-studies":
        return "WebPage"
    return PAGE_TYPE_OVERRIDES.get(slug, "WebPage")


def article_graph(
    *,
    slug_path: str,
    title: str,
    description: str,
    image: str,
    date_published: str | None = None,
    genre: str | None = None,
) -> dict:
    canonical = slug_to_url(slug_path)
    headline = re.sub(r"\s+(?:-|\u2014|\|)\s+Hive IP(?:\s+case study)?$", "", clean_text(title))
    article = {
        "@type": "Article",
        "@id": f"{canonical}#article",
        "headline": headline,
        "description": clean_text(description),
        "image": image,
        "author": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": f"{canonical}#webpage"},
        "inLanguage": LANGUAGE,
    }
    published = date_published or ARTICLE_DATES.get((slug_path or "").strip("/"))
    if published:
        article["datePublished"] = published
    if genre:
        article["genre"] = genre
    return article


def build_graph(
    *,
    slug_path: str,
    title: str,
    description: str,
    breadcrumbs: list[tuple[str | None, str]] | None = None,
    og_image: str | None = None,
    page_type: str | None = None,
    date_published: str | None = None,
) -> dict:
    slug = (slug_path or "").strip("/")
    canonical = slug_to_url(slug)
    image = image_url(og_image)
    graph = [ORG_FULL if slug == "" else ORG_MINIMAL, WEBSITE_FULL if slug == "" else WEBSITE_MINIMAL]

    main_entity = MAIN_ENTITIES.get(slug)
    item_list = item_list_graph(slug)
    faq = faq_graph(slug)

    if main_entity:
        graph.append(main_entity)
    if item_list:
        graph.append(item_list)
    if slug == "insights":
        graph.append({
            "@type": "Blog",
            "@id": f"{canonical}#blog",
            "name": "Hive IP Insights",
            "publisher": {"@id": ORG_ID},
            "description": "Expert commentary on unique coding, FMCG promotions, fraud audit, cloud validation and in-factory print.",
        })

    requested_type = page_type_for(slug, page_type)
    webpage = {
        "@type": requested_type,
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": clean_text(title),
        "description": clean_text(description),
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID},
        "maintainer": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
        "inLanguage": LANGUAGE,
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": image,
        },
    }

    if main_entity:
        webpage["mainEntity"] = {"@id": main_entity["@id"]}
    elif slug == "insights":
        webpage["mainEntity"] = {"@id": f"{canonical}#blog"}
    elif item_list:
        webpage["mainEntity"] = {"@id": item_list["@id"]}
    elif slug in {"about", "contact"}:
        webpage["mainEntity"] = {"@id": ORG_ID}

    graph.append(webpage)

    if slug.startswith("insights/"):
        graph.append(article_graph(
            slug_path=slug,
            title=title,
            description=description,
            image=image,
            date_published=date_published,
        ))
    elif slug.startswith("case-studies/") and slug != "case-studies":
        graph.append(article_graph(
            slug_path=slug,
            title=title,
            description=description,
            image=image,
            genre="Case study",
        ))

    breadcrumb = breadcrumb_graph(slug, breadcrumbs)
    if breadcrumb:
        graph.append(breadcrumb)
    if faq:
        graph.append(faq)

    return {
        "@context": "https://schema.org",
        "@graph": graph,
    }


def render_json_ld(
    *,
    slug_path: str,
    title: str,
    description: str,
    breadcrumbs: list[tuple[str | None, str]] | None = None,
    og_image: str | None = None,
    page_type: str | None = None,
    date_published: str | None = None,
) -> str:
    payload = build_graph(
        slug_path=slug_path,
        title=title,
        description=description,
        breadcrumbs=breadcrumbs,
        og_image=og_image,
        page_type=page_type,
        date_published=date_published,
    )
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    return (
        "  <!-- JSON-LD:start -->\n"
        "  <script type=\"application/ld+json\">\n"
        f"{data}\n"
        "  </script>\n"
        "  <!-- JSON-LD:end -->"
    )


def html_path_to_slug(path: Path) -> str:
    parts = path.as_posix().split("/")
    if parts[-1] != "index.html":
        return "" if parts[-1] == "index.html" else path.stem
    return "/".join(parts[:-1])
