# MicroPython Learning Roadmap
### ESP32 + 4" LCD Touchscreen

A phased path from blinking an LED to a standalone physical TA dashboard. Each phase is a brick in the wall toward the final build: the **Market Pulse Station**.

---

## Phase 1 — Hello Hardware
**Week 1–2**

Get MicroPython running on ESP32. Learn the core loop: input → logic → output.

**Learning Goals**
- Flash MicroPython firmware onto ESP32
- Run your first script via Thonny IDE
- Blink an LED with a loop — your "Hello World"
- Read a button press and respond to it
- Understand GPIO pins, pull-up/pull-down resistors

**Hardware Needed:** ESP32 board · Breadboard · LEDs (any color) · 220Ω resistors · Jumper wires · Push button
**Tools & Libraries:** Thonny IDE · esptool.py (flash firmware) · MicroPython REPL

**Phase Project — Breathing LED**
PWM-driven LED that pulses in and out like a heartbeat. First taste of analog-style control from digital output.

```python
import machine, time
led = machine.PWM(machine.Pin(2))
led.freq(1000)

while True:
    for duty in range(0, 1024, 8):
        led.duty(duty)
        time.sleep_ms(10)
    for duty in range(1023, 0, -8):
        led.duty(duty)
        time.sleep_ms(10)
```

---

## Phase 2 — Sensing the World
**Week 3–4**

Add sensors. Think of each sensor as a live data feed — same mindset as market data ingestion.

**Learning Goals**
- Wire and read a DHT22 (temp + humidity)
- Understand I2C vs SPI vs UART protocols
- Log timestamped readings to a list (in-memory)
- Detect anomalies: is temp rising fast? (delta logic)
- Write data to a file on the ESP32 flash

**Hardware Needed:** DHT22 temperature sensor · 10kΩ resistor · Optional: BMP280 (I2C pressure)
**Tools & Libraries:** Thonny file manager · MicroPython ujson · utime module

**Phase Project — Signal Logger**
Log sensor readings every 5 seconds. Calculate a rolling 10-sample average — exactly like an SMA on price data.

```python
import dht, machine, time, ujson

sensor = dht.DHT22(machine.Pin(4))
readings = []

def rolling_avg(data, n=10):
    window = data[-n:]
    return sum(window) / len(window)

while True:
    sensor.measure()
    temp = sensor.temperature()
    readings.append(temp)
    avg = rolling_avg(readings)
    print(f"Temp: {temp:.1f}C | SMA-10: {avg:.2f}")
    time.sleep(5)
```

> **→ Bridge to final:** Sensor data becomes the feed. Same smoothing logic as your TA work.

---

## Phase 3 — Going Wireless
**Week 5–6**

ESP32's superpower is WiFi. Connect to the internet and pull live data — stocks, weather, crypto.

**Learning Goals**
- Connect ESP32 to your WiFi network
- Make HTTP GET requests with urequests
- Parse JSON API responses
- Handle connection drops gracefully
- Pull live stock or crypto price from a free API

**Hardware Needed:** ESP32 (built-in WiFi) · No extra hardware needed
**Tools & Libraries:** urequests library · network module · Free APIs: CoinGecko, Open-Meteo, Yahoo Finance

**Phase Project — Live Price Fetcher**
Poll a crypto or stock price every 60 seconds. Compare to last reading — flag if move > 1% (your first physical alert trigger).

```python
import network, urequests, time

SSID = "your_wifi"
PASSWORD = "your_pass"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)

last_price = None
while True:
    r = urequests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    price = r.json()["bitcoin"]["usd"]
    r.close()
    if last_price:
        delta = (price - last_price) / last_price * 100
        print(f"BTC: ${price:,} | delta {delta:+.2f}%")
        if abs(delta) > 1.0:
            print("ALERT: >1% move!")
    last_price = price
    time.sleep(60)
```

> **→ Bridge to final:** This is the data pipeline for your final project. WiFi → API → logic → output.

---

## Phase 4 — Touch & Display
**Week 7–9**

Bring your 4" LCD touchscreen online. This is the UI layer — think of it as your dashboard renderer.

**Learning Goals**
- Wire LCD to ESP32 via SPI
- Install ili9341 or st7796 MicroPython driver
- Draw text, shapes, and color fills
- Read touch input (XPT2046 chip usually)
- Build a simple menu with tap navigation

**Hardware Needed:** 4" LCD Touchscreen (SPI) · SPI wiring: MOSI, MISO, CLK, CS, DC, RST
**Tools & Libraries:** ili9341 / st7796 driver · XPT2046 touch driver · framebuf module

**Phase Project — Touchscreen Dashboard Shell**
A tappable home screen with 3 panel buttons: Price, Sensors, Settings. No data yet — just navigation and layout.

```python
# Pseudocode structure (driver-dependent)
from ili9341 import Display
from xpt2046 import Touch

display = Display(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4))
touch = Touch(spi2, cs=Pin(14))

panels = ["Market", "Sensors", "Settings"]

def draw_menu():
    for i, label in enumerate(panels):
        display.fill_rect(20, 60 + i*70, 280, 55, color565(30,30,60))
        display.draw_text(30, 78 + i*70, label, font, color565(0,229,204))

while True:
    draw_menu()
    x, y = touch.get_touch()
    if x and 20 < x < 300:
        panel = (y - 60) // 70
        print(f"Tapped: {panels[panel]}")
```

> **→ Bridge to final:** This shell becomes the housing for your final project's entire UI.

---

## Final Project — Market Pulse Station
**Week 10–12**

Everything converges. A physical TA dashboard with live data, touch UI, alerts, and sensor awareness.

**Learning Goals**
- Live price feed for 2–3 tickers on screen
- SMA crossover detection with visual signal flag
- RSI gauge rendered as a color arc
- Temperature/humidity sidebar (ambient awareness)
- Tap a ticker to drill into its mini chart
- LED or buzzer alert on signal trigger

**Hardware Needed:** ESP32 · 4" Touchscreen · DHT22 · RGB LED or buzzer · Enclosure (optional)
**Tools & Libraries:** All prior libraries · Custom TA logic from your data science work · ujson config file for tickers

**The Build — Market Pulse Station**
A standalone physical device that monitors markets with TA signals, rendered on a touch display. Your data science brain in a box.

```python
import uasyncio as asyncio

async def fetch_prices():
    # Poll API every 60s, update shared state
    pass

async def compute_signals():
    # SMA crossover, RSI on latest N candles
    # Trigger LED/buzzer if signal fires
    pass

async def render_display():
    # Redraw dashboard every 5s
    # Handle touch input -> panel switch
    pass

asyncio.run(asyncio.gather(
    fetch_prices(), compute_signals(), render_display()
))
```

---

## Hardware Shopping List

Full hardware list across all phases. You already have the ESP32 and 4" screen on the way — the starter kit covers Phase 1 & 2. Total additional spend is minimal.

### Phase 1
- **ESP32 DevKit (2-pack, USB-C, WROOM-32E)** — Core board, covers all phases — [Amazon](https://www.amazon.com/dp/B09MQJWQN2)
- **Electronics Starter Kit** (Breadboard, LEDs, Resistors, Buttons, Jumper Wires) — Covers Phase 1 & 2 basics in one box — [Amazon](https://www.amazon.com/dp/B08Y81TS5C)

### Phase 2
- **HiLetgo DHT22/AM2302 Temp & Humidity Sensor Module (2-pack)** — No extra resistor needed, module has pull-up built in — [Amazon](https://www.amazon.com/dp/B07D7W3TNX)

### Phase 3
- *No new hardware* — ESP32 WiFi is built in. Just a free CoinGecko or Open-Meteo API key.

### Phase 4
- **4" LCD Touchscreen** — *already on order!* Confirm driver chip (ILI9341 or ST7796) from the product listing.

### Final Project
- **CHANZON RGB LED Common Cathode 5mm (100-pack)** — Signal light for buy/sell/neutral state — [Amazon](https://www.amazon.com/dp/B01C19ENDM)
- **Passive Buzzer Module for ESP32 (2-pack)** — Tone alert on TA signal trigger — [Amazon](https://www.amazon.com/dp/B0DYDN31PV)

---

*The through-line: you're not learning hardware from scratch — you're extending a data mindset into a physical medium. The patterns are the same.*
