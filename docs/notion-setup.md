# Notion Command Center — Setup (Pattern C)

This project connects to Notion via an **internal integration** and project-owned
Python scripts — no OAuth, no Claude connector. Token lives in `.env`; scripts live
in `scripts/`. This mirrors HZ's `scripts/notion_client.py` pattern (we use the
filename `notion_api.py` here to avoid shadowing the PyPI `notion-client` package).

## Structure

```
[Market Pulse Station]            ← landing page (URL in CLAUDE.md)
├── Decisions DB     → Name (title), Date, Status, Area, Notes
├── Session Log      → Name, Date, Phase, Agent, Outcome
└── Sprint Tracker   → Task, Status, Sprint, Owner, Due
```

## One-time setup

### 1 — Create an internal integration

Go to: https://www.notion.so/profile/integrations

Click **"New integration"**, give it a name (e.g. `MPS-BOT`), choose your
workspace, and click **Save**. Copy the **Internal Integration Token** — it
starts with `secret_`.

### 2 — Add the token to `.env`

At the project root, copy `.env.example` to `.env` (already gitignored), then
fill in the two values:

```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_LANDING_PAGE_ID=3683d60a-7be9-8049-95a4-d4f08814adc5
```

The landing page ID is the 32-hex string at the end of the page URL:
`https://www.notion.so/Your-Page-Title-3683d60a7be9804995a4d4f08814adc5`

Strip the title slug and insert dashes in the standard UUID format, or just
paste the plain 32-hex string — the script normalizes both forms.

### 3 — Connect the integration to the landing page (CRITICAL)

This is the step everyone forgets. A valid token is not enough — Notion also
requires you to explicitly grant the integration access to the page:

1. Open the **Market Pulse Station** landing page in Notion.
2. Click the `···` (More options) menu in the top-right.
3. Choose **Connections**.
4. Search for your integration name (e.g. `MPS-BOT`) and click **Add**.

**If you skip this step, every API call returns HTTP 404** even though the token
is valid and the page exists. Sub-pages and databases created under the landing
page inherit access automatically — you only need to do this once on the root.

### 4 — Create the databases

With the `.env` file in place and the connection added, run:

```bash
python scripts/notion_seed.py
```

This creates the three databases (Decisions, Session Log, Sprint Tracker) as
children of the landing page. The script is idempotent: if a database with the
target title already exists under the landing page, it prints "already exists"
and skips it.

## Tracked vs. ignored files

| File | Tracked? |
|---|---|
| `.env` | No — gitignored. Contains the real token. |
| `.env.example` | Yes — placeholder template. |
| `scripts/notion_api.py` | Yes — shared API wrapper. |
| `scripts/notion_seed.py` | Yes — one-time DB creator. |

## Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` | Bad or missing token | Re-copy the token from the integration settings page; check for extra whitespace in `.env` |
| `404 Not Found` | Integration not connected to the page | Re-do step 3: open the page → `···` → Connections → add the integration |
| `400 Bad Request` | Schema mismatch (property name or type wrong) | Check the property definitions in `notion_seed.py` against what Notion expects; delete the partial DB in Notion and re-run |
| `RuntimeError: NOTION_TOKEN not set` | `.env` not found or variable name wrong | Confirm `.env` exists at the project root and key is `NOTION_TOKEN` |
