"""
Notion API client for Market Pulse Station.

Thin shared helper used by notion_seed.py (and any future scripts that
read/write to the project's Notion command center).

Pattern C: internal integration token in .env — no OAuth, no MCP connector.
Mirrors the style of HZ/scripts/notion_client.py (stdlib urllib, no extra deps
beyond notion-client for the Client object and python-dotenv for .env loading).

Module-name note: this file is `notion_api.py` (not `notion_client.py`) so it
doesn't shadow the PyPI `notion-client` package. Running `python scripts/...`
puts `scripts/` on `sys.path[0]`; a local `notion_client.py` would then
intercept the SDK import below and cause a circular import.

Usage:
    from scripts.notion_api import get_client, get_landing_page_id

    client = get_client()
    page_id = get_landing_page_id()
"""

import os
from pathlib import Path

# Load .env from the project root (one level above this script's directory).
# Must happen before importing notion_client so the token is in the environment.
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        # Fallback: parse .env manually if python-dotenv isn't installed yet.
        # This lets the script give a clear error message rather than crashing
        # on the import before we can check the token.
        for _line in _env_path.read_text().splitlines():
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from notion_client import Client  # notion-client PyPI package


def _require_env(key: str) -> str:
    """Read an environment variable or raise a clear error."""
    value = os.getenv(key, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {key}\n"
            f"  1. Copy .env.example to .env at the project root.\n"
            f"  2. Fill in the real value for {key}.\n"
            f"  3. If this is NOTION_TOKEN, get it from "
            f"https://www.notion.so/profile/integrations"
        )
    return value


def get_client() -> Client:
    """Return a configured Notion Client using the token from .env."""
    token = _require_env("NOTION_TOKEN")
    return Client(auth=token)


def get_landing_page_id() -> str:
    """Return the landing page ID from .env, normalised to plain 32-hex."""
    raw = _require_env("NOTION_LANDING_PAGE_ID")
    # Accept either dashed UUID form or plain hex; Notion API accepts both,
    # but we strip dashes here so callers don't have to think about it.
    return raw.replace("-", "")
