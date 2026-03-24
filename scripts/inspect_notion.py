#!/usr/bin/env python3
"""
Inspect Notion workspace structure.
Outputs a JSON report of all databases, their properties, and sample records.
Run this BEFORE writing the sync script to understand your Notion schema.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client

load_dotenv(Path(__file__).parent.parent / ".env")

_token = os.environ.get("NOTION_TOKEN")
if not _token:
    raise SystemExit("ERROR: NOTION_TOKEN not set. Add it to your .env file.")

notion = Client(auth=_token)


def inspect_workspace():
    report = {"databases": []}

    # Paginate through all databases the integration has access to
    cursor = None
    while True:
        kwargs = {"filter": {"property": "object", "value": "database"}, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        response = notion.search(**kwargs)

        for db in response["results"]:
            db_id = db["id"]
            db_title = _get_title(db.get("title", []))
            properties = {}

            for prop_name, prop_data in db.get("properties", {}).items():
                properties[prop_name] = prop_data.get("type", "<unknown>")

            # Fetch 3 sample records
            sample_rows = []
            try:
                rows = notion.databases.query(database_id=db_id, page_size=3)
                for page in rows["results"]:
                    sample = {"id": page["id"], "properties": {}}
                    for prop_name, prop_data in page.get("properties", {}).items():
                        sample["properties"][prop_name] = _extract_value(prop_data)
                    sample_rows.append(sample)
            except Exception as e:
                sample_rows = [{"error": str(e)}]

            report["databases"].append({
                "id": db_id,
                "title": db_title,
                "properties": properties,
                "sample_records": sample_rows,
            })

        if not response.get("has_more"):
            break
        cursor = response["next_cursor"]

    return report


def _get_title(title_array):
    return "".join(t.get("plain_text", "") for t in title_array)


def _extract_value(prop):
    """Extract a readable value from a Notion property."""
    t = prop.get("type")
    if t == "title":
        return _get_title(prop.get("title", []))
    elif t == "rich_text":
        return _get_title(prop.get("rich_text", []))
    elif t == "select":
        s = prop.get("select")
        return s["name"] if s else None
    elif t == "multi_select":
        return [s["name"] for s in prop.get("multi_select", [])]
    elif t == "date":
        d = prop.get("date")
        return d["start"] if d else None
    elif t == "checkbox":
        return prop.get("checkbox")
    elif t == "url":
        return prop.get("url")
    elif t == "number":
        return prop.get("number")
    elif t == "status":
        s = prop.get("status")
        return s["name"] if s else None
    else:
        return f"<{t}>"


if __name__ == "__main__":
    report = inspect_workspace()
    output_path = Path(__file__).parent.parent / "notion_structure_report.json"
    output_path.write_text(json.dumps(report, indent=2))
    print(f"Report saved to {output_path}")
    print(f"\nFound {len(report['databases'])} databases:")
    for db in report['databases']:
        print(f"  - {db['title']} ({len(db['properties'])} properties)")
