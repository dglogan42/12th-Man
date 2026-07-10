# Twelfth Man — Australia Cricket Commentary

Live **Twelfth Man**-style spoof commentary for **all major Australia matches** — Tests, ODIs, and T20s. A parody tribute to Billy Birmingham's *The Twelfth Man*, with Richie Benaud, Bill Lawry, Tony Greig, and the rest of the Channel Nine commentary box.

Pair the spoof feed with real coverage on **FOX Sports**, **Sky Sports**, **TuneIn**, **iHeartRadio**, **Rova**, or **Star Sports**.

## Features

- **8 Test series** — Ashes, Border-Gavaskar, Trans-Tasman, South Africa, Pakistan, Sri Lanka, West Indies, Bangladesh
- **3 formats** — Tests, ODIs, and T20s with format-specific banter (powerplay, death overs, "get on with it!")
- **27 demo matches** — live simulations for every major opponent and format
- **Classic spoof lines** — *"Got him, yes! Piss off! You're out!"*, Richie's *"chew runs"*, Tony's car keys in the pitch, Indian name parodies, and more
- **Free TTS** — Google Translate voices per commentator (AU / UK / US accents), with browser speech fallback
- **Radio integration** — TuneIn (ABC Grandstand, BBC TMS), iHeartRadio, Rova (Sport Nation), Cricket Australia Radio, ABC Listen
- **TV integration** — FOX Sports AU, Kayo, Sky Sports UK, Star Sports India
- **Live scores (optional)** — connect a free [CricketData.org](https://cricketdata.org) API key for real ball-by-ball data

## Requirements

- Python 3.10+
- A modern web browser (for the UI and TTS playback)
- No pip dependencies — stdlib only

## Quick Start

```bash
git clone <your-repo-url>
cd twelfth-man-ashes-commentary
python3 server.py
```

Open **http://localhost:8765** in your browser.

1. Filter by **format** (Test / ODI / T20) and **series**
2. Open a **Listen Live** link (TuneIn, Rova) or **Watch Live** link (FOX, Sky)
3. Select a demo match and hit **Start Commentary**
4. Toggle **Speak commentary aloud** for TTS voices

### Live data (optional)

Register for a free key at [cricketdata.org](https://cricketdata.org), then:

```bash
export CRICAPI_KEY=your_api_key_here
python3 server.py
```

The app will auto-detect live Australia Tests, ODIs, and T20s.

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8765` | HTTP server port |
| `CRICAPI_KEY` | — | CricketData.org API key for live scores |
| `QUIET` | — | Set to suppress server request logs |

## Formats

| Format | Demo matches | Commentary highlights |
|--------|--------------|----------------------|
| **Test** | 8 live demos | Ashes lines, Richie's "chew", pitch reports |
| **ODI** | 7 live demos | Powerplay & death-over banter |
| **T20** | 7 live demos | Fast feed, *"Get on with it!"*, maximum carnage |

## Supported series

| Series | Opponent | Trophy |
|--------|----------|--------|
| The Ashes | England | The Ashes urn |
| Border-Gavaskar Trophy | India | Border-Gavaskar Trophy |
| Trans-Tasman Trophy | New Zealand | Trans-Tasman Trophy |
| Australia v South Africa | South Africa | Freedom Trophy |
| Australia v Pakistan | Pakistan | — |
| Australia v Sri Lanka | Sri Lanka | — |
| Australia v West Indies | West Indies | Frank Worrell Trophy |
| Australia v Bangladesh | Bangladesh | — |

## Radio & TV partners

### Listen live

| Platform | Stations | Best for |
|----------|----------|----------|
| [TuneIn](https://tunein.com/) | ABC Grandstand, BBC Test Match Special | Ashes & AU home series |
| [iHeartRadio](https://www.iheart.com/) | Live Sports, cricket search | US sports radio |
| [Rova](https://www.rova.nz/) | Sport Nation, The Edge | Trans-Tasman & NZ cricket |
| Cricket Australia Radio | Official live audio | All AU internationals |
| ABC Listen | ABC Grandstand | Australian coverage |

Links reorder by series — e.g. **BBC TMS** first for the Ashes, **Rova Sport Nation** first for NZ Tests.

### Watch live

| Region | Service |
|--------|---------|
| Australia | [FOX Sports](https://www.foxsports.com.au/cricket), [Kayo Sports](https://kayosports.com.au/sports/cricket) |
| UK | [Sky Sports Cricket](https://www.skysports.com/cricket), [Sky Sports Ashes](https://www.skysports.com/watch/sport/cricket/ashes) |
| India | [Star Sports / JioHotstar](https://www.hotstar.com/in/sports/cricket) |

## Text-to-speech

Commentary lines can be spoken aloud via the free **Google Translate TTS** API (no key required):

| Commentator | Accent |
|-------------|--------|
| Richie, Bill, Ian, Slats | Australian (`en-au`) |
| Tony, Greg | British (`en-gb`) |
| Darrell, Max | American (`en-us`) |

Use **Test Bill Lawry** in the sidebar to preview. Uncheck *Use free Google TTS API* to fall back to your browser's Web Speech API.

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matches` | GET | List matches (`?series=`, `?format=`) |
| `/api/commentary` | GET | Commentary feed (`?match_id=`, `?since=`) |
| `/api/score` | GET | Live score for a match |
| `/api/broadcast` | GET | Radio & TV links (`?series=`) |
| `/api/tts` | GET | MP3 audio (`?text=`, `?commentator=`) |
| `/api/tts/voices` | GET | Commentator voice config |
| `/api/start` | POST | Start commentary (`{"match_id": "..."}`) |
| `/api/stop` | POST | Pause commentary |
| `/api/reset` | POST | Reset match state |

## Project structure

```
twelfth-man-ashes-commentary/
├── LICENSE
├── README.md
├── server.py              # HTTP server & REST API
├── commentary/
│   ├── broadcast.py       # TuneIn, iHeart, Rova, TV links
│   ├── cricket.py         # Live data & demo simulators
│   ├── engine.py          # Commentary generator
│   ├── lines.py           # Twelfth Man quotes & parodies
│   ├── series.py          # Series, formats & fixtures
│   └── tts.py             # Free Google TTS
└── static/
    ├── index.html
    ├── style.css
    ├── app.js
    └── tts.js
```

## Disclaimer

This project is a **parody tribute** to Billy Birmingham's *The Twelfth Man*. It is not affiliated with, endorsed by, or connected to:

- Billy Birmingham or *The Twelfth Man* rights holders
- FOX Sports, Kayo, Sky Sports, Star Sports, or Cricket Australia
- TuneIn, iHeartRadio, Rova, the ABC, or the BBC
- Google or CricketData.org

Player name parodies and commentator impersonations are affectionate satire for entertainment only. Use official broadcasts for real match coverage.

## License

[MIT License](LICENSE) — Copyright (c) 2026 Twelfth Man Ashes Commentary contributors.
## Media policy

Ship original / free UI art only. Do not commit scraped site dumps, broadcaster logos, or third-party product images.
