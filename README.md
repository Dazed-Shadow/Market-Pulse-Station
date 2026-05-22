# Market Pulse Station

A learning project that bridges Python/data-science skills into physical computing. The end goal is a standalone ESP32 + 4" touchscreen device that monitors markets with technical-analysis signals, ambient sensors, and physical alerts.

The work is structured as a **12-week, 5-phase roadmap**. Each phase ships a small working project; every project is a brick toward the final build.

## Hardware

| Item | Role | Phase |
|---|---|---|
| ESP32 DevKit (WROOM-32E, USB-C) | Core board | All |
| Breadboard + jumpers + LEDs + resistors + button | Basics | 1–2 |
| DHT22 / AM2302 sensor module | Temp + humidity feed | 2 |
| 4" LCD touchscreen (SPI, ILI9341 or ST7796) | UI layer | 4 |
| RGB LED (common cathode) | Signal light | Final |
| Passive buzzer module | Audible alert | Final |

Full shopping list with links: [`docs/roadmap.md`](docs/roadmap.md#hardware-shopping-list).

## Repo layout

```
market-pulse-station/
├── README.md            ← you are here
├── CLAUDE.md            ← project brief for Claude Code (read this first)
├── docs/
│   ├── roadmap.md       ← the full 5-phase plan + shopping list
│   └── notion-setup.md  ← how to wire the Notion command center
├── firmware/            ← MicroPython code, one folder per phase (created as you go)
├── scripts/
│   └── bootstrap.sh     ← repo init + remote wiring helper
└── .github/             ← CI later, if wanted
```

## Getting started

1. Read [`CLAUDE.md`](CLAUDE.md) — it briefs Claude Code on the whole project.
2. Skim [`docs/roadmap.md`](docs/roadmap.md) for the phase plan.
3. When hardware arrives, start Phase 1: flash MicroPython, then `firmware/phase1/`.

## Status

- [ ] Phase 1 — Hello Hardware
- [ ] Phase 2 — Sensing the World
- [ ] Phase 3 — Going Wireless
- [ ] Phase 4 — Touch & Display
- [ ] Final — Market Pulse Station
