#!/usr/bin/env python3
"""Check a Commonplace production build against a legacy Hugo build."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.identifiers = set()
        self.references = []
        self.images_without_alt = []

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get("id"):
            self.identifiers.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.identifiers.add(attrs["name"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src", ""))


def pages(root):
    result = {}
    for path in root.rglob("*.html"):
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        result[path] = parser
    return result


def route_files(root):
    return {str(path.relative_to(root)) for path in root.rglob("*")
            if path.is_file() and path.suffix in (".html", ".xml")}


def feed_guids(root, feed):
    path = root / feed
    channel = ElementTree.parse(path).getroot().find("channel")
    return [item.findtext("guid") for item in channel.findall("item")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="new production output directory")
    parser.add_argument("--baseline", type=Path, help="legacy production output directory")
    args = parser.parse_args()
    site = args.site.resolve()
    errors = []
    rendered = pages(site)

    if args.baseline:
        baseline = args.baseline.resolve()
        for route in sorted(route_files(baseline) - route_files(site)):
            errors.append(f"lost route: /{route}")
        original_guids = set(feed_guids(baseline, "index.xml"))
        current_guids = set(feed_guids(site, "index.xml"))
        for guid in sorted(original_guids - current_guids):
            errors.append(f"lost feed GUID: {guid}")

    for path, document in rendered.items():
        for source in document.images_without_alt:
            errors.append(f"image missing alt attribute: {path.relative_to(site)} {source}")
        for reference in document.references:
            uri = urlsplit(reference)
            if uri.scheme and (uri.scheme not in ("http", "https") or uri.netloc != "markgroves.us"):
                continue
            if uri.netloc and uri.netloc != "markgroves.us":
                continue
            if not uri.path and uri.fragment:
                target = path
            elif uri.path.startswith("/"):
                target = site / unquote(uri.path).lstrip("/")
            elif uri.path:
                target = path.parent / unquote(uri.path)
            else:
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"missing target: {path.relative_to(site)} {reference}")
            elif uri.fragment and target.suffix == ".html":
                target_doc = rendered.get(target.resolve())
                if target_doc and unquote(uri.fragment) not in target_doc.identifiers:
                    errors.append(f"missing fragment: {path.relative_to(site)} {reference}")

    feeds = {name: feed_guids(site, f"{name}/index.xml")
             for name in ("posts", "links", "essays", "log")}
    root_feed = feed_guids(site, "index.xml")
    if len(root_feed) != len(set(root_feed)):
        errors.append("duplicate root feed GUID")
    for name, guids in feeds.items():
        for guid in guids:
            if guid not in root_feed:
                errors.append(f"{name} feed item absent from root: {guid}")
    for guid in feeds["links"]:
        if guid in feeds["posts"] or guid in feeds["essays"]:
            errors.append(f"link in writing feed: {guid}")
    for guid in feeds["posts"]:
        if guid not in feeds["essays"]:
            errors.append(f"legacy post absent from Essays: {guid}")
    if set(feeds["posts"]) & set(feeds["log"]):
        errors.append("Log contains a legacy post")

    print(f"Checked {len(rendered)} HTML pages and {len(root_feed)} root feed items")
    if errors:
        print("\n".join(sorted(set(errors))))
        raise SystemExit(1)
    print("Routes, local references, image attributes, and feed membership pass")


if __name__ == "__main__":
    main()
