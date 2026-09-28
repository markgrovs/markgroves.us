#!/usr/bin/env python3
"""Check IndieWeb markup on every generated writing permalink."""

import argparse
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


class EntryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.active = None
        self.article_depth = 0
        self.discovery = set()

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        classes = set(attrs.get("class", "").split())
        if tag == "link" and attrs.get("rel") in ("webmention", "authorization_endpoint", "token_endpoint"):
            self.discovery.add(attrs["rel"])
        if tag == "article" and self.active is not None:
            self.article_depth += 1
        elif tag == "article" and "h-entry" in classes:
            self.active = {"classes": set(), "urls": [], "bookmarks": [], "dates": [],
                           "author": False, "named_heading": False}
            self.article_depth = 1
            self.entries.append(self.active)
        if self.active is None:
            return
        self.active["classes"].update(classes)
        if {"p-author", "h-card"} <= classes:
            self.active["author"] = True
        if tag == "h1" and "p-name" in classes:
            self.active["named_heading"] = True
        if "u-url" in classes and attrs.get("href"):
            self.active["urls"].append(attrs["href"])
        if "u-bookmark-of" in classes:
            self.active["bookmarks"].append(attrs.get("href", ""))
        if "dt-published" in classes:
            self.active["dates"].append(attrs.get("datetime", ""))

    def handle_endtag(self, tag):
        if tag == "article" and self.active is not None:
            self.article_depth -= 1
            if self.article_depth == 0:
                self.active = None


def feed_urls(root, section):
    feed = ElementTree.parse(root / section / "index.xml").getroot()
    return {item.findtext("guid") for item in feed.findall("./channel/item")}


def read_page(root, url):
    route = urlsplit(url).path.lstrip("/")
    path = root / route / "index.html"
    page = EntryParser()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="Hugo output directory")
    args = parser.parse_args()
    root = args.site.resolve()
    posts = feed_urls(root, "posts")
    links = feed_urls(root, "links")
    logs = feed_urls(root, "log")
    essays = feed_urls(root, "essays") - posts
    types = {"post": posts, "link": links, "log": logs, "essay": essays}
    failures = []
    for kind, urls in types.items():
        for url in urls:
            page = read_page(root, url)
            if len(page.entries) != 1:
                failures.append(f"{url}: expected one h-entry, found {len(page.entries)}")
                continue
            entry = page.entries[0]
            if not {"e-content", "u-url", "u-uid", "dt-published"} <= entry["classes"]:
                failures.append(f"{url}: missing core entry properties")
            if url not in entry["urls"]:
                failures.append(f"{url}: canonical u-url does not match the permalink")
            if not entry["author"]:
                failures.append(f"{url}: missing nested p-author h-card")
            if not entry["dates"] or any(not date for date in entry["dates"]):
                failures.append(f"{url}: missing machine-readable publication date")
            else:
                for date in entry["dates"]:
                    try:
                        datetime.fromisoformat(date.replace("Z", "+00:00"))
                    except ValueError:
                        failures.append(f"{url}: invalid publication date {date}")
            if kind in ("post", "essay", "link") and not entry["named_heading"]:
                failures.append(f"{url}: missing named entry heading")
            if kind == "link" and (len(entry["bookmarks"]) != 1 or not entry["bookmarks"][0]):
                failures.append(f"{url}: missing bookmark target")
            if kind != "link" and entry["bookmarks"]:
                failures.append(f"{url}: unexpected bookmark target")
            if not {"webmention", "authorization_endpoint", "token_endpoint"} <= page.discovery:
                failures.append(f"{url}: missing discovery endpoint")

    for route in ("now", "cv", "colophon"):
        page = read_page(root, f"https://markgroves.us/{route}/")
        if page.entries:
            failures.append(f"/{route}/: ordinary page incorrectly marked h-entry")

    home = (root / "index.html").read_text(encoding="utf-8")
    if home.count('class="site-header h-card"') != 1 or home.count('class="home h-card"'):
        failures.append("/: expected one representative site h-card")

    print("Checked", ", ".join(f"{len(urls)} {kind}s" for kind, urls in types.items()))
    if failures:
        print("\n".join(sorted(failures)))
        raise SystemExit(1)
    print("IndieWeb entry and discovery markup passes")


if __name__ == "__main__":
    main()
