#!/usr/bin/env python3
"""Fetch the current TTCN-3 core parts and language extensions from ETSI."""

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_URL = "https://www.etsi.org/custom/standardssearch/data.php"
SOURCE_URL = (
    "https://www.etsi.org/standards/"
    "#page=1&search=ES%20201%20873&etsiNumber=1&published=1&isCurrent=1"
)
EXTENSION_SOURCE_URL = (
    "https://www.etsi.org/standards/"
    "#page=1&search=Language%20extension&title=1&published=1&isCurrent=1"
)
DELIVER_URL = "https://www.etsi.org/deliver/"
DELIVERABLE = re.compile(
    r"^ETSI ES 201 873-(?P<part>\d+) V(?P<version>\d+(?:\.\d+)*) "
    r"\((?P<published>\d{4}-\d{2})\)$"
)
EXTENSION_DELIVERABLE = re.compile(
    r"^ETSI ES (?P<series>\d+) (?P<document>\d+) V(?P<version>\d+(?:\.\d+)*) "
    r"\((?P<published>\d{4}-\d{2})\)$"
)
EXTENSION_NAME = re.compile(
    r"TTCN-3 Language [Ee]xtensions?:\s*(?P<name>.+)$"
)
ETSI_NUMBER = re.compile(
    r"^ETSI\s+(?P<kind>[A-Z]+)\s+(?P<series>\d+)\s+(?P<document>\d+)"
    r"(?:-(?P<part>\d+))?$"
)
PART_TITLE = re.compile(r"(?P<part>Part\s+\d+:\s*.+)$")
STANDARDS_START = "<!-- standards:start -->"
STANDARDS_END = "<!-- standards:end -->"
PAGE_SIZE = 50


def version_key(version):
    return tuple(int(component) for component in version.split("."))


def etsi_number_key(number):
    """Sort ES 201 873-4 before ES 201 873-11."""
    match = ETSI_NUMBER.match(number)
    if not match:
        return (number,)
    return (
        match["kind"],
        int(match["series"]),
        int(match["document"]),
        int(match["part"] or 0),
    )


def fetch_page(search, page, *, title=0, etsi_number=1):
    """Return one page of published, non-historical ETSI search results."""
    query = {
        "format": "json",
        "page": page,
        "search": search,
        "title": title,
        "etsiNumber": etsi_number,
        "content": 0,
        "version": 1,
        "onApproval": 0,
        "published": 1,
        "withdrawn": 0,
        "historical": 0,
        "isCurrent": 1,
        "superseded": 0,
        "startDate": "1988-01-15",
        "endDate": "",
        "harmonized": 0,
        "sort": 3,
    }
    request = Request(
        f"{SEARCH_URL}?{urlencode(query)}",
        headers={
            "Accept": "application/json",
            "Referer": "https://www.etsi.org/standards/",
            "User-Agent": "ttcn3.dev standards updater",
        },
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        sys.exit("ETSI standards search did not return a list.")
    return payload


def fetch_all(search, *, title=0, etsi_number=1):
    """Return every page of one published, non-historical ETSI search."""
    results = []
    for page in range(1, 21):
        batch = fetch_page(search, page, title=title, etsi_number=etsi_number)
        results.extend(batch)
        if len(batch) < PAGE_SIZE:
            return results
    sys.exit(f"ETSI standards search for {search!r} did not finish within 20 pages.")


def select_current(results, deliverable_re, number_from_match, title_re=None):
    """Keep the newest published version of each document the pattern accepts."""
    current = {}
    for result in results:
        if result["ACTION_TYPE"] != "PU" or result["STATUS_CODE"] != "12":
            continue
        if title_re is not None and not title_re.search(result["TITLE"]):
            continue

        match = deliverable_re.match(result["ETSI_DELIVERABLE"])
        if not match:
            continue

        number = number_from_match(match)
        standard = {
            "number": number,
            "version": match["version"],
            "published": match["published"],
            "title": result["TITLE"],
            "url": f"{DELIVER_URL}{result['EDSpathname']}{result['EDSPDFfilename']}",
        }
        previous = current.get(number)
        if previous is None or version_key(standard["version"]) > version_key(
            previous["version"]
        ):
            current[number] = standard

    return sorted(current.values(), key=lambda standard: etsi_number_key(standard["number"]))


def select_current_standards(results):
    """Keep the newest published version of every active ES 201 873 part."""
    return select_current(
        results,
        DELIVERABLE,
        lambda match: f"ETSI ES 201 873-{int(match['part'])}",
    )


def select_current_extensions(results):
    """Keep the newest published version of every active TTCN-3 language extension."""
    return select_current(
        results,
        EXTENSION_DELIVERABLE,
        lambda match: f"ETSI ES {match['series']} {match['document']}",
        EXTENSION_NAME,
    )


def display_title(title):
    """Lead with the part or extension name. The series title is shared."""
    match = PART_TITLE.search(title)
    if match:
        return match["part"].strip()
    match = EXTENSION_NAME.search(title)
    if match:
        return match["name"].strip()
    return title


def format_published(published):
    try:
        parsed = datetime.strptime(published, "%Y-%m")
    except ValueError:
        return published
    return f"{parsed.strftime('%B')} {parsed.year}"


def format_updated(updated):
    parsed = datetime.fromisoformat(updated)
    return f"{parsed.day} {parsed.strftime('%B %Y')}"


def render_panel(standards):
    items = []
    for standard in standards:
        items.append(
            "\t<li>\n"
            f'\t\t<a href="{html.escape(standard["url"], quote=True)}" target="_blank" rel="noopener noreferrer">\n'
            f'\t\t\t<span class="std-part">{html.escape(display_title(standard["title"]))}</span>\n'
            "\t\t\t<span class=\"std-number\">"
            f'<span class="std-id">{html.escape(standard["number"])}</span> '
            f'<span class="std-version">V{html.escape(standard["version"])}</span>'
            "</span>\n"
            f'\t\t\t<time class="std-date" datetime="{html.escape(standard["published"], quote=True)}">'
            f'{html.escape(format_published(standard["published"]))}</time>\n'
            "\t\t</a>\n"
            "\t</li>"
        )
    body = "\n".join(items)
    return (
        '<div class="standards-panel">\n'
        '<div class="std-head" aria-hidden="true">'
        "<span>Title</span><span>ETSI number</span><span>Date</span>"
        "</div>\n"
        '<ul class="standards">\n'
        f"{body}\n"
        "</ul>\n"
        "</div>"
    )


def render_standards_html(document):
    """Render the active standards as static lists. No client-side script."""
    updated = document["updated"]
    return (
        '<h3 class="std-group">Specifications</h3>\n'
        f"{render_panel(document['standards'])}\n"
        '<h3 class="std-group">Extensions</h3>\n'
        f"{render_panel(document['extensions'])}\n"
        '<p class="std-note">Updated '
        f'<time datetime="{html.escape(updated, quote=True)}">{html.escape(format_updated(updated))}</time>.'
        "</p>\n"
    )


def inject_standards(page, fragment):
    start = page.find(STANDARDS_START)
    end = page.find(STANDARDS_END)
    if start == -1 or end == -1 or end < start:
        sys.exit(
            "HTML file is missing <!-- standards:start --> and <!-- standards:end --> markers."
        )
    end += len(STANDARDS_END)
    replacement = f"{STANDARDS_START}\n{fragment}{STANDARDS_END}"
    return page[:start] + replacement + page[end:]


def load_document(path):
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(f"Unable to read standards JSON: {error}")
    if not document.get("standards"):
        sys.exit(f"{path} does not contain standards.")
    document.setdefault("extensions", [])
    return document


def write_document(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(document['standards'])} TTCN-3 standards"
        f" and {len(document['extensions'])} extensions to {path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Write current TTCN-3 standard metadata from ETSI."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="JSON file to write",
    )
    parser.add_argument(
        "--from-json",
        type=Path,
        help="Read an existing standards JSON file instead of calling ETSI",
    )
    parser.add_argument(
        "--inject",
        type=Path,
        help="Replace the standards markers in this HTML file",
    )
    args = parser.parse_args()
    if not args.output and not args.inject:
        parser.error("Pass --output, --inject, or both.")

    if args.from_json:
        document = load_document(args.from_json)
    else:
        try:
            standards = select_current_standards(
                fetch_all("ES 201 873", title=0, etsi_number=1)
            )
            extensions = select_current_extensions(
                fetch_all("Language extension", title=1, etsi_number=0)
            )
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            sys.exit(f"Unable to retrieve ETSI standards: {error}")

        if not standards:
            sys.exit("ETSI returned no current ES 201 873 standards.")
        if not extensions:
            sys.exit("ETSI returned no current TTCN-3 language extensions.")

        document = {
            "source": SOURCE_URL,
            "extensionSource": EXTENSION_SOURCE_URL,
            "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "standards": standards,
            "extensions": extensions,
        }

    if args.output and not args.from_json:
        write_document(args.output, document)

    if args.inject:
        page = args.inject.read_text(encoding="utf-8")
        args.inject.write_text(
            inject_standards(page, render_standards_html(document)),
            encoding="utf-8",
        )
        print(
            f"Wrote {len(document['standards'])} TTCN-3 standards"
            f" and {len(document.get('extensions', []))} extensions into {args.inject}"
        )


if __name__ == "__main__":
    main()
