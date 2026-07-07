"""Broadcast & radio integration — TV, TuneIn, iHeartRadio, Rova, and more."""

from __future__ import annotations

# Each partner: category tv|radio, platform for styling, optional app_url for deep links
BROADCAST_PARTNERS: dict[str, dict] = {
    # ── Radio: TuneIn ──────────────────────────────────────────────
    "tunein_abc_grandstand": {
        "name": "TuneIn — ABC Grandstand",
        "url": "https://tunein.com/radio/ABC-Grandstand-p329200/",
        "app_url": "tunein://station/s329200",
        "logo": "📻",
        "platform": "tunein",
        "category": "radio",
        "region": "AU",
        "description": "Live ABC cricket radio — pair with spoof commentary",
        "series_boost": ["ashes", "border_gavaskar", "south_africa", "pakistan",
                         "sri_lanka", "west_indies", "bangladesh"],
    },
    "tunein_tms": {
        "name": "TuneIn — BBC Test Match Special",
        "url": "https://tunein.com/radio/Test-Match-Special-p123619/",
        "app_url": "tunein://station/s123619",
        "logo": "📻",
        "platform": "tunein",
        "category": "radio",
        "region": "UK",
        "description": "Iconic BBC TMS Ashes & Test commentary",
        "series_boost": ["ashes"],
    },
    "tunein_cricket_search": {
        "name": "TuneIn — Cricket Search",
        "url": "https://tunein.com/search/?query=cricket%20australia",
        "app_url": "tunein://search/cricket%20australia",
        "logo": "🔍",
        "platform": "tunein",
        "category": "radio",
        "region": "ALL",
        "description": "Find live cricket stations worldwide on TuneIn",
        "series_boost": [],
    },
    "tunein_sport": {
        "name": "TuneIn — Sports Radio",
        "url": "https://tunein.com/sports/",
        "logo": "🏅",
        "platform": "tunein",
        "category": "radio",
        "region": "ALL",
        "description": "Browse sports talk & live event radio on TuneIn",
        "series_boost": [],
    },
    # ── Radio: iHeartRadio ─────────────────────────────────────────
    "iheart_sports": {
        "name": "iHeartRadio — Live Sports",
        "url": "https://www.iheart.com/genre/sports-15/",
        "app_url": "iheartradio://genre/sports",
        "logo": "❤️",
        "platform": "iheart",
        "category": "radio",
        "region": "US",
        "description": "Live sports radio & talk across iHeart stations",
        "series_boost": ["ashes", "west_indies"],
    },
    "iheart_cricket_search": {
        "name": "iHeartRadio — Cricket",
        "url": "https://www.iheart.com/search/?q=cricket",
        "app_url": "iheartradio://search/cricket",
        "logo": "🔍",
        "platform": "iheart",
        "category": "radio",
        "region": "ALL",
        "description": "Search cricket podcasts & sports stations on iHeart",
        "series_boost": [],
    },
    "iheart_sports_talk": {
        "name": "iHeartRadio — Sports Talk",
        "url": "https://www.iheart.com/podcast/genre/sports-26/",
        "logo": "🎙️",
        "platform": "iheart",
        "category": "radio",
        "region": "US",
        "description": "Sports podcasts & live talk — great alongside Tests",
        "series_boost": [],
    },
    # ── Radio: Rova (NZ) ─────────────────────────────────────────
    "rova_sport_nation": {
        "name": "Rova — Sport Nation",
        "url": "https://www.rova.nz/radio/sport-nation",
        "app_url": "https://www.rova.nz/radio/sport-nation",
        "logo": "🇳🇿",
        "platform": "rova",
        "category": "radio",
        "region": "NZ",
        "description": "NZ sport radio — Trans-Tasman & international cricket",
        "series_boost": ["trans_tasman"],
    },
    "rova_the_edge": {
        "name": "Rova — The Edge",
        "url": "https://www.rova.nz/radio/the-edge",
        "logo": "📡",
        "platform": "rova",
        "category": "radio",
        "region": "NZ",
        "description": "MediaWorks sport updates on Rova during big matches",
        "series_boost": ["trans_tasman"],
    },
    "rova_home": {
        "name": "Rova — Live Radio",
        "url": "https://www.rova.nz/",
        "app_url": "https://www.rova.nz/",
        "logo": "🔊",
        "platform": "rova",
        "category": "radio",
        "region": "NZ",
        "description": "New Zealand's free radio app — sport & music stations",
        "series_boost": [],
    },
    # ── Radio: other ─────────────────────────────────────────────
    "ca_cricket_radio": {
        "name": "Cricket Australia Radio",
        "url": "https://www.cricket.com.au/cricket-radio",
        "logo": "🏏",
        "platform": "cricket_au",
        "category": "radio",
        "region": "AU",
        "description": "Official CA live audio commentary stream",
        "series_boost": ["ashes", "border_gavaskar", "south_africa", "pakistan",
                         "sri_lanka", "west_indies", "bangladesh", "trans_tasman"],
    },
    "abc_listen": {
        "name": "ABC Listen",
        "url": "https://www.abc.net.au/listen/live/24",
        "logo": "📻",
        "platform": "abc",
        "category": "radio",
        "region": "AU",
        "description": "ABC Grandstand live via ABC Listen app",
        "series_boost": ["ashes", "border_gavaskar"],
    },
    # ── TV / streaming ─────────────────────────────────────────────
    "fox_sports_au": {
        "name": "FOX Sports Australia",
        "url": "https://www.foxsports.com.au/cricket",
        "logo": "🦊",
        "platform": "fox",
        "category": "tv",
        "region": "AU",
        "description": "Live Tests, ODIs, T20s & international coverage",
        "series_boost": [],
    },
    "kayo": {
        "name": "Kayo Sports",
        "url": "https://kayosports.com.au/sports/cricket",
        "logo": "📺",
        "platform": "fox",
        "category": "tv",
        "region": "AU",
        "description": "Stream every Australia match live (subscription)",
        "series_boost": [],
    },
    "sky_sports_uk": {
        "name": "Sky Sports Cricket",
        "url": "https://www.skysports.com/cricket",
        "logo": "📡",
        "platform": "sky",
        "category": "tv",
        "region": "UK",
        "description": "Live Tests, ODIs, T20s & world cricket",
        "series_boost": ["ashes"],
    },
    "sky_sports_ashes": {
        "name": "Sky Sports — The Ashes",
        "url": "https://www.skysports.com/watch/sport/cricket/ashes",
        "logo": "🏆",
        "platform": "sky",
        "category": "tv",
        "region": "UK",
        "description": "Dedicated Ashes hub with live streams",
        "series_boost": ["ashes"],
    },
    "bbc_sport": {
        "name": "BBC Sport Cricket",
        "url": "https://www.bbc.co.uk/sport/cricket",
        "logo": "📻",
        "platform": "sky",
        "category": "tv",
        "region": "UK",
        "description": "Ball-by-ball text & Test Match Special links",
        "series_boost": ["ashes"],
    },
    "star_sports_in": {
        "name": "Star Sports (India)",
        "url": "https://www.hotstar.com/in/sports/cricket",
        "logo": "⭐",
        "platform": "star",
        "category": "tv",
        "region": "IN",
        "description": "Border-Gavaskar, ODIs & T20 coverage",
        "series_boost": ["border_gavaskar"],
    },
}

# Series-specific radio presets shown at the top
SERIES_RADIO_PRESETS: dict[str, list[str]] = {
    "ashes": [
        "tunein_tms", "tunein_abc_grandstand", "ca_cricket_radio",
        "tunein_cricket_search", "iheart_sports",
    ],
    "border_gavaskar": [
        "tunein_abc_grandstand", "ca_cricket_radio", "abc_listen",
        "tunein_cricket_search", "iheart_cricket_search",
    ],
    "trans_tasman": [
        "rova_sport_nation", "rova_the_edge", "tunein_abc_grandstand",
        "ca_cricket_radio", "rova_home",
    ],
    "south_africa": [
        "tunein_abc_grandstand", "ca_cricket_radio", "tunein_sport", "iheart_sports",
    ],
    "pakistan": [
        "tunein_abc_grandstand", "ca_cricket_radio", "tunein_cricket_search",
    ],
    "sri_lanka": [
        "tunein_abc_grandstand", "ca_cricket_radio", "tunein_cricket_search",
    ],
    "west_indies": [
        "tunein_abc_grandstand", "ca_cricket_radio", "iheart_sports", "tunein_sport",
    ],
    "bangladesh": [
        "tunein_abc_grandstand", "ca_cricket_radio", "tunein_cricket_search",
    ],
}

DEFAULT_RADIO_PRESETS = [
    "tunein_abc_grandstand", "ca_cricket_radio", "tunein_cricket_search",
    "iheart_sports", "rova_sport_nation", "tunein_tms",
]


def _partner_to_dict(key: str, partner: dict, boosted: bool = False) -> dict:
    return {
        "id": key,
        "name": partner["name"],
        "url": partner["url"],
        "app_url": partner.get("app_url", ""),
        "logo": partner["logo"],
        "platform": partner["platform"],
        "category": partner["category"],
        "region": partner["region"],
        "description": partner["description"],
        "boosted": boosted,
    }


def get_broadcast_links(series_id: str | None = None) -> dict:
    """Return TV and radio links, ordered for the active series."""
    presets = SERIES_RADIO_PRESETS.get(series_id or "", DEFAULT_RADIO_PRESETS)
    seen: set[str] = set()
    radio: list[dict] = []
    tv: list[dict] = []

    # Boosted radio presets first
    for key in presets:
        if key in BROADCAST_PARTNERS and key not in seen:
            p = BROADCAST_PARTNERS[key]
            if p["category"] == "radio":
                radio.append(_partner_to_dict(key, p, boosted=True))
            else:
                tv.append(_partner_to_dict(key, p, boosted=True))
            seen.add(key)

    # Series-boosted partners
    if series_id:
        for key, p in BROADCAST_PARTNERS.items():
            if key in seen:
                continue
            if series_id in p.get("series_boost", []):
                entry = _partner_to_dict(key, p, boosted=True)
                if p["category"] == "radio":
                    radio.append(entry)
                else:
                    tv.append(entry)
                seen.add(key)

    # Remaining partners by category
    for key, p in BROADCAST_PARTNERS.items():
        if key in seen:
            continue
        entry = _partner_to_dict(key, p)
        if p["category"] == "radio":
            radio.append(entry)
        else:
            tv.append(entry)
        seen.add(key)

    # Star Sports first for BGT on TV
    if series_id == "border_gavaskar":
        star = [l for l in tv if l["platform"] == "star"]
        rest = [l for l in tv if l["platform"] != "star"]
        tv = star + rest

    return {
        "tv": tv,
        "radio": radio,
        "links": radio + tv,  # backwards compat
        "series_id": series_id or "",
        "radio_platforms": ["tunein", "iheart", "rova"],
    }


def get_platform_info() -> list[dict]:
    return [
        {
            "id": "tunein",
            "name": "TuneIn Radio",
            "url": "https://tunein.com/",
            "description": "Global radio — ABC Grandstand, BBC TMS & more",
        },
        {
            "id": "iheart",
            "name": "iHeartRadio",
            "url": "https://www.iheart.com/",
            "description": "US sports radio, podcasts & live events",
        },
        {
            "id": "rova",
            "name": "Rova",
            "url": "https://www.rova.nz/",
            "description": "New Zealand live radio including Sport Nation",
        },
    ]