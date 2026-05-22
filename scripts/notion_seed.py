"""
One-shot database creator for Market Pulse Station's Notion command center.

Creates three databases as children of the landing page defined by
NOTION_LANDING_PAGE_ID in .env:
  - Decisions DB
  - Session Log
  - Sprint Tracker

Idempotent: if a database with the target title already exists as a direct
child of the landing page, the script skips it and prints "already exists".

Before running:
  1. Create an internal integration at https://www.notion.so/profile/integrations
  2. Add NOTION_TOKEN and NOTION_LANDING_PAGE_ID to .env
  3. Open the landing page in Notion → ··· → Connections → add the integration
     (Without this step, every API call returns 404 even with a valid token.)
  4. Run: python scripts/notion_seed.py
"""

import sys
from pathlib import Path

# Ensure the project root is on the path so `from scripts.notion_client` works
# whether you run this as `python scripts/notion_seed.py` or `python -m scripts.notion_seed`.
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.notion_client import get_client, get_landing_page_id


# ── Database schemas ───────────────────────────────────────────────────────────
# Property colours are assigned to match HZ conventions where the option names
# overlap; new options use sensible colour choices (Opus review invited).

DECISIONS_PROPS = {
    "Name": {"title": {}},
    "Date": {"date": {}},
    "Status": {"select": {"options": [
        {"name": "Proposed",   "color": "gray"},
        {"name": "Accepted",   "color": "green"},
        {"name": "Superseded", "color": "yellow"},
    ]}},
    "Area": {"select": {"options": [
        {"name": "Hardware", "color": "orange"},
        {"name": "Firmware", "color": "blue"},
        {"name": "Infra",    "color": "purple"},
        {"name": "Docs",     "color": "gray"},
    ]}},
    "Notes": {"rich_text": {}},
}

SESSION_LOG_PROPS = {
    "Name": {"title": {}},
    "Date": {"date": {}},
    "Phase": {"select": {"options": [
        {"name": "Phase 1", "color": "blue"},
        {"name": "Phase 2", "color": "green"},
        {"name": "Phase 3", "color": "yellow"},
        {"name": "Phase 4", "color": "orange"},
        {"name": "Final",   "color": "red"},
    ]}},
    "Agent": {"select": {"options": [
        {"name": "Opus",   "color": "purple"},
        {"name": "Sonnet", "color": "blue"},
        {"name": "JR",     "color": "orange"},
    ]}},
    "Outcome": {"rich_text": {}},
}

SPRINT_TRACKER_PROPS = {
    "Task": {"title": {}},
    "Status": {"select": {"options": [
        {"name": "Todo",        "color": "gray"},
        {"name": "In Progress", "color": "yellow"},
        {"name": "Blocked",     "color": "red"},
        {"name": "Done",        "color": "green"},
    ]}},
    "Sprint": {"select": {"options": [
        {"name": "Phase 1", "color": "blue"},
        {"name": "Phase 2", "color": "green"},
        {"name": "Phase 3", "color": "yellow"},
        {"name": "Phase 4", "color": "orange"},
        {"name": "Final",   "color": "red"},
    ]}},
    "Owner": {"select": {"options": [
        {"name": "JR",     "color": "orange"},
        {"name": "Opus",   "color": "purple"},
        {"name": "Sonnet", "color": "blue"},
    ]}},
    "Due": {"date": {}},
}

# Ordered list of (title, schema) pairs to create.
DATABASES = [
    ("Decisions DB",   DECISIONS_PROPS),
    ("Session Log",    SESSION_LOG_PROPS),
    ("Sprint Tracker", SPRINT_TRACKER_PROPS),
]


# ── Idempotency check ──────────────────────────────────────────────────────────

def _existing_child_db_titles(client, landing_page_id: str) -> dict[str, str]:
    """
    Return a mapping of {title: database_id} for every database that is already
    a direct child of the landing page.

    Uses the blocks endpoint to list children, then fetches database metadata
    only for child_page / child_database blocks to avoid unnecessary calls.
    """
    existing = {}
    cursor = None
    while True:
        kwargs = {"block_id": landing_page_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = client.blocks.children.list(**kwargs)
        for block in resp.get("results", []):
            block_type = block.get("type")
            if block_type == "child_database":
                title = block.get("child_database", {}).get("title", "")
                existing[title] = block["id"]
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return existing


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    client = get_client()
    landing_id = get_landing_page_id()

    print(f"\nMarket Pulse Station — Notion seed")
    print(f"Landing page ID: {landing_id}\n")

    # Check what already exists so we can skip rather than duplicate.
    print("Checking for existing databases...")
    try:
        existing = _existing_child_db_titles(client, landing_id)
    except Exception as exc:
        print(f"\nERROR: Could not list children of the landing page.")
        print(f"  → {exc}")
        print(
            "\nMost common cause: the integration hasn't been added as a Connection.\n"
            "  1. Open the landing page in Notion.\n"
            "  2. Click ··· → Connections → find your integration → Add.\n"
            "  3. Re-run this script."
        )
        sys.exit(1)

    created = []
    skipped = []

    for title, props in DATABASES:
        if title in existing:
            db_id = existing[title]
            print(f"  SKIP  '{title}' — already exists  ({db_id})")
            skipped.append(title)
        else:
            print(f"  CREATE '{title}'...")
            db = client.databases.create(
                parent={"type": "page_id", "page_id": landing_id},
                title=[{"type": "text", "text": {"content": title}}],
                properties=props,
            )
            db_id = db["id"]
            print(f"         → created  ({db_id})")
            created.append((title, db_id))

    print()
    print("─" * 60)
    print(f"Done. Created: {len(created)}  |  Skipped: {len(skipped)}")
    if created:
        print("\nNew database IDs:")
        for t, i in created:
            print(f"  {t}: {i}")
    print()


if __name__ == "__main__":
    main()
