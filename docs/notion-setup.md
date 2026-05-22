# Notion Command Center — Setup

Derived from the team Integration Playbook (Pattern B — Claude remote connector).
The goal: mirror this project's **decisions and state** to Notion so context
survives across chat sessions.

## The structure to build

```
[Market Pulse Station]            ← landing page (paste its URL into CLAUDE.md)
├── (free-form project description)
├── Decisions DB     → Name (title), Date, Status, Area, Notes
├── Session Log      → Name, Date, Phase, Agent, Outcome
└── Sprint Tracker   → Task, Status, Sprint, Owner, Due
```

The landing page is the single URL Claude needs. As long as the Claude integration
has access to it, it inherits access to the databases beneath it.

## Connect the connector — the two-step that catches everyone

A Notion connector is only useful after **both** steps:

1. **Authenticate to the workspace.** claude.ai → Settings → Connectors → Notion →
   Connect → OAuth. In the OAuth screen, the **workspace dropdown** is the part most
   people get wrong: pick the workspace that holds your real pages, not the empty
   personal workspace Notion spins up for new accounts.
2. **Grant page access.** On the landing page in Notion: "..." menu → Connections →
   add the Claude integration. Sub-pages and the databases inherit this.

Do only step 1 and searches return demo/template pages. Do only step 2 and the
integration won't appear in the page's Connections list (workspace isn't linked yet).

## Verify it actually works

In a Claude chat:

> Search my Notion for the page titled "Market Pulse Station"

- Real page comes back → connected correctly.
- Only "Sapiens", "Crime and Punishment", "Brave New World" style results → you're
  on a **demo workspace**. Disconnect, reconnect, choose the right workspace.

## Gotchas worth remembering

- **OAuth scopes are coarse:** "read Notion" means *all* shared pages. Keep anything
  sensitive in pages you never share with an integration.
- **Per-account, not per-session:** disconnecting in one chat doesn't disconnect
  everywhere.
- **Page shares are sticky:** audit the integration's access periodically.

## Once connected

Fill the landing-page URL into `CLAUDE.md` (the `<PASTE_NOTION_LANDING_PAGE_URL_HERE>`
placeholder). From then on, Claude Code can log decisions and session outcomes to the
databases as you work through the phases.
