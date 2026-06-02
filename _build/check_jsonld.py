#!/usr/bin/env python3
"""Validate site JSON-LD coverage and syntax."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_RE = re.compile(
    r"<script\s+type=[\"']application/ld\+json[\"']\s*>(.*?)</script>",
    re.DOTALL | re.IGNORECASE,
)
WEBPAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}


def slug_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[:-len("/index.html")]
    return Path(rel).stem


def graph_nodes(payload: object) -> list[dict]:
    if isinstance(payload, dict) and isinstance(payload.get("@graph"), list):
        return [node for node in payload["@graph"] if isinstance(node, dict)]
    if isinstance(payload, dict):
        return [payload]
    return []


def node_types(nodes: list[dict]) -> set[str]:
    types = set()
    for node in nodes:
        node_type = node.get("@type")
        if isinstance(node_type, list):
            types.update(str(item) for item in node_type)
        elif node_type:
            types.add(str(node_type))
    return types


def main() -> None:
    failures = []
    html_paths = sorted(
        path for path in ROOT.rglob("*.html")
        if ".git" not in path.parts
    )

    for path in html_paths:
        slug = slug_for(path)
        markup = path.read_text(encoding="utf-8")
        blocks = SCRIPT_RE.findall(markup)
        if not blocks:
            failures.append(f"{path.relative_to(ROOT)}: missing JSON-LD")
            continue

        all_nodes = []
        for index, block in enumerate(blocks, 1):
            try:
                payload = json.loads(block)
            except json.JSONDecodeError as exc:
                failures.append(f"{path.relative_to(ROOT)} block {index}: invalid JSON ({exc})")
                continue
            all_nodes.extend(graph_nodes(payload))

        types = node_types(all_nodes)
        if not (types & WEBPAGE_TYPES):
            failures.append(f"{path.relative_to(ROOT)}: missing WebPage-family entity")
        if slug and slug != "404" and "BreadcrumbList" not in types:
            failures.append(f"{path.relative_to(ROOT)}: missing BreadcrumbList")
        if slug.startswith("insights/") and slug != "insights" and "Article" not in types:
            failures.append(f"{path.relative_to(ROOT)}: missing Article")
        if slug.startswith("case-studies/") and slug != "case-studies" and "Article" not in types:
            failures.append(f"{path.relative_to(ROOT)}: missing Article")
        if slug in {"applications", "case-studies", "insights", "solution"} and "ItemList" not in types:
            failures.append(f"{path.relative_to(ROOT)}: missing ItemList")
        if "SearchAction" in markup:
            failures.append(f"{path.relative_to(ROOT)}: SearchAction present without site search")

    if failures:
        print("JSON-LD validation failed:")
        for failure in failures:
            print(f" - {failure}")
        raise SystemExit(1)

    print(f"JSON-LD validation passed for {len(html_paths)} HTML file(s).")


if __name__ == "__main__":
    main()
