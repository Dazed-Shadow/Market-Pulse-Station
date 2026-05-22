# CLAUDE.md — Market Pulse Station

> Project brief for Claude Code. Read this before doing any work in this repo.

## What this project is

A 12-week learning project building toward a physical market-monitoring device:
an **ESP32 + 4" SPI touchscreen** that pulls live price data over WiFi, computes
TA signals (SMA crossover, RSI), shows them on a touch dashboard, and fires a
physical LED/buzzer alert on a signal. Ambient temp/humidity from a DHT22 sits in
a sidebar. The user is extending an existing data-science / stock-TA background
into a physical (MicroPython) medium — the patterns transfer, the medium is new.

## Roadmap (authoritative copy in `docs/roadmap.md`)

| Phase | Theme | Weeks | Ships |
|---|---|---|---|
| 1 | Hello Hardware | 1–2 | Breathing LED (PWM) |
| 2 | Sensing the World | 3–4 | Signal Logger (rolling avg = SMA) |
| 3 | Going Wireless | 5–6 | Live Price Fetcher (WiFi + API) |
| 4 | Touch & Display | 7–9 | Touchscreen Dashboard Shell |
| Final | Market Pulse Station | 10–12 | Full async dashboard + alerts |

Firmware for each phase goes in `firmware/phaseN/`. Keep each phase runnable on
its own; don't refactor earlier phases into the final architecture until Phase 5.

## Conventions

- **Language:** MicroPython (not CPython). Use `machine`, `network`, `urequests`,
  `uasyncio`, `framebuf` — not their desktop equivalents.
- **Display driver:** unknown until the user confirms the chip. Branch on
  ILI9341 vs ST7796 — do not hard-code one until confirmed.
- **Secrets:** WiFi creds and any API keys live in `firmware/secrets.py`, which is
  **gitignored**. Provide `firmware/secrets.example.py` as the template. Never
  commit a real SSID/password/key. (See Pattern A in the integration playbook.)
- **Style:** small, readable files; comments that explain the *why* and the
  data-science parallel where one exists (e.g. "rolling avg ≈ SMA-10").

## Notion command center (Pattern C — see docs/notion-setup.md)

This project mirrors its decisions/state to Notion so context survives between
chat sessions. Connection is via an **internal integration** token in `.env` and
project-owned Python scripts in `scripts/` — not the Claude OAuth connector and
not a local MCP server. This mirrors the HZ project's setup exactly.

**Notion landing page:** `https://www.notion.so/LANDING-PAGE-3683d60a7be9804995a4d4f08814adc5`

Structure created by `python scripts/notion_seed.py`:
- **Decisions DB** — Name (title), Date, Status, Area, Notes
- **Session Log** — Name, Date, Phase, Agent, Outcome
- **Sprint Tracker** — Task, Status, Sprint, Owner, Due

The integration must be added as a **Connection** on the landing page (page
`···` menu → Connections) before the scripts will work. See `docs/notion-setup.md`
for the full walkthrough.

## What to do first

1. If `git` isn't initialized here, run `scripts/bootstrap.sh` (it inits, makes the
   first commit, and prints the steps to add a GitHub remote — it will **not** push
   or create anything on GitHub without the user doing it themselves).
2. Confirm `.gitignore` covers `firmware/secrets.py`.
3. Create the Notion internal integration at https://www.notion.so/profile/integrations,
   drop the token in `.env` as `NOTION_TOKEN`, add the integration as a Connection
   on the landing page (page `···` → Connections), then run `python scripts/notion_seed.py`.
4. Confirm the display driver chip (ILI9341 or ST7796) from the product listing.
5. Then wait for hardware to begin Phase 1.

## Guardrails

- Don't push to any remote, create GitHub repos, or change repo visibility on the
  user's behalf — print the commands and let them run them.
- Don't write real secrets into any tracked file.
- Treat the display-driver choice as unconfirmed until the user states it.
