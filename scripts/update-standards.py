#!/usr/bin/env python3
"""Fetch the currently published parts of ETSI ES 201 873."""

import argparse
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
DELIVER_URL = "https://www.etsi.org/deliver/"
DELIVERABLE = re.compile(
    r"^ETSI ES 201 873-(?P<part>\d+) V(?P<version>\d+(?:\.\d+)*) "
    r"\((?P<published>\d{4}-\d{2})\)$"
)
ETSI_NUMBER = re.compile(
    r"^ETSI\s+(?P<kind>[A-Z]+)\s+(?P<series>\d+)\s+(?P<document>\d+)"
    r"(?:-(?P<part>\d+))?$"
)


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


def fetch_standards():
    """Return all published, non-historical ES 201 873 search results."""
    query = {
        "format": "json",
        "page": 1,
        "search": "ES 201 873",
        "title": 0,
        "etsiNumber": 1,
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
        return json.load(response)


def select_current_standards(results):
    """Keep the newest published version of every active ES 201 873 part."""
    current = {}
    for result in results:
        if result["ACTION_TYPE"] != "PU" or result["STATUS_CODE"] != "12":
            continue

        match = DELIVERABLE.match(result["ETSI_DELIVERABLE"])
        if not match:
            continue

        part = int(match["part"])
        standard = {
            "number": f"ETSI ES 201 873-{part}",
            "version": match["version"],
            "published": match["published"],
            "title": result["TITLE"],
            "url": f"{DELIVER_URL}{result['EDSpathname']}{result['EDSPDFfilename']}",
        }
        if part not in current or version_key(standard["version"]) > version_key(
            current[part]["version"]
        ):
            current[part] = standard

    return sorted(
        current.values(),
        key=lambda standard: etsi_number_key(standard["number"]),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Write current TTCN-3 standard metadata from ETSI."
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="JSON file to write",
    )
    args = parser.parse_args()

    try:
        standards = select_current_standards(fetch_standards())
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        sys.exit(f"Unable to retrieve ETSI standards: {error}")

    if not standards:
        sys.exit("ETSI returned no current ES 201 873 standards.")

    document = {
        "source": SOURCE_URL,
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "standards": standards,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(standards)} TTCN-3 standards to {args.output}")


if __name__ == "__main__":
    main()
