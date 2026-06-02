#!/usr/bin/env python3
"""Inject shared JSON-LD into hand-authored static pages."""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_build"))

from structured_data import render_json_ld  # noqa: E402


JSONLD_MARKED_RE = re.compile(
    r"\n\s*<!-- JSON-LD:start -->.*?<!-- JSON-LD:end -->",
    re.DOTALL,
)
JSONLD_SCRIPT_RE = re.compile(
    r"\n\s*<script\s+type=[\"']application/ld\+json[\"']\s*>.*?</script>",
    re.DOTALL | re.IGNORECASE,
)


BREADCRUMBS = {
    "why-unique-codes": [("", "Home"), (None, "Why unique codes")],
    "why-in-factory": [("", "Home"), (None, "Why in-factory")],
    "our-model": [("", "Home"), (None, "Our model")],
    "solution": [("", "Home"), (None, "Solution")],
    "solution/in-factory": [("", "Home"), ("solution/", "Solution"), (None, "In-factory print")],
    "solution/at-supplier": [("", "Home"), ("solution/", "Solution"), (None, "Packaging-supplier print")],
    "solution/validation": [("", "Home"), ("solution/", "Solution"), (None, "Cloud validation")],
    "solution/consumer-support": [("", "Home"), ("solution/", "Solution"), (None, "Consumer Support Panel")],
    "case-studies/pepsico": [("", "Home"), ("case-studies/", "Case studies"), (None, "PepsiCo")],
    "case-studies/news-uk": [("", "Home"), ("case-studies/", "Case studies"), (None, "News UK / Sun Saver")],
    "insights/on-pack-digital-campaigns": [("", "Home"), ("insights/", "Insights"), (None, "Unique codes, two campaign engines")],
    "privacy-policy": [("", "Home"), (None, "Privacy policy")],
    "cookie-policy": [("", "Home"), (None, "Cookie policy")],
    "privacy": [("", "Home"), (None, "Privacy and cookies")],
}

PAGE_TYPES = {
    "solution": "CollectionPage",
}


def slug_for(path: str) -> str:
    if path == "index.html":
        return ""
    if path.endswith("/index.html"):
        return path[:-len("/index.html")]
    return Path(path).stem


def attr_value(markup: str, pattern: str, group: int = 1) -> str:
    match = re.search(pattern, markup, re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return html.unescape(match.group(group)).strip()


def local_href_to_slug(href: str) -> str:
    href = (href or "").split("#", 1)[0].split("?", 1)[0]
    while href.startswith("../"):
        href = href[3:]
    href = href.lstrip("/")
    if href in {"", "index.html", "./index.html"}:
        return ""
    if href.endswith("/index.html"):
        return href[:-len("index.html")]
    if href.endswith("/"):
        return href
    return href


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def parse_breadcrumbs(markup: str, slug: str):
    if not slug:
        return None
    nav = re.search(
        r"<nav[^>]+class=[\"'][^\"']*breadcrumbs[^\"']*[\"'][^>]*>.*?</nav>",
        markup,
        re.DOTALL | re.IGNORECASE,
    )
    if not nav:
        return BREADCRUMBS.get(slug)
    items = []
    for li in re.findall(r"<li\b[^>]*>(.*?)</li>", nav.group(0), re.DOTALL | re.IGNORECASE):
        link = re.search(r"<a\b[^>]*href=([\"'])(.*?)\1[^>]*>(.*?)</a>", li, re.DOTALL | re.IGNORECASE)
        if link:
            label = strip_tags(link.group(3))
            items.append((local_href_to_slug(link.group(2)), label))
        else:
            label = strip_tags(li)
            if label:
                items.append((None, label))
    return items or BREADCRUMBS.get(slug)


def page_metadata(markup: str, slug: str) -> dict:
    title = attr_value(markup, r"<title>(.*?)</title>")
    description = attr_value(markup, r"<meta\s+name=[\"']description[\"']\s+content=([\"'])(.*?)\1", 2)
    og_image = attr_value(markup, r"<meta\s+property=[\"']og:image[\"']\s+content=([\"'])(.*?)\1", 2)
    if not description:
        description = title
    return {
        "slug_path": slug,
        "title": title or "Hive IP",
        "description": description,
        "breadcrumbs": parse_breadcrumbs(markup, slug),
        "og_image": og_image or None,
        "page_type": PAGE_TYPES.get(slug),
    }


def inject_jsonld(markup: str, jsonld: str) -> str:
    cleaned = JSONLD_MARKED_RE.sub("", markup)
    cleaned = JSONLD_SCRIPT_RE.sub("", cleaned)
    return cleaned.replace("</head>", f"{jsonld}\n</head>", 1)


def main() -> None:
    changed = 0
    html_paths = sorted(
        path for path in ROOT.rglob("*.html")
        if ".git" not in path.parts
    )
    for path in html_paths:
        relative_path = path.relative_to(ROOT).as_posix()
        markup = path.read_text(encoding="utf-8")
        slug = slug_for(relative_path)
        jsonld = render_json_ld(**page_metadata(markup, slug))
        updated = inject_jsonld(markup, jsonld)
        if updated != markup:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"updated {relative_path}")
        else:
            print(f"unchanged {relative_path}")
    print(f"Done. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
