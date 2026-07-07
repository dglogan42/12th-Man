"""Free TTS via Google Translate (no API key) with Web Speech fallback hints."""

import hashlib
import re
import urllib.error
import urllib.parse
import urllib.request
from functools import lru_cache


# Commentator → Google TTS locale (free, no key required)
COMMENTATOR_VOICES = {
    "richie": {"locale": "en-au", "label": "Richie Benaud", "rate_hint": 0.88, "pitch_hint": 0.9},
    "bill": {"locale": "en-au", "label": "Bill Lawry", "rate_hint": 1.15, "pitch_hint": 1.2},
    "tony": {"locale": "en-gb", "label": "Tony Greig", "rate_hint": 1.0, "pitch_hint": 0.95},
    "ian": {"locale": "en-au", "label": "Ian Chappell", "rate_hint": 0.95, "pitch_hint": 0.85},
    "greg": {"locale": "en-gb", "label": "Greg Chappell", "rate_hint": 0.92, "pitch_hint": 0.9},
    "max": {"locale": "en-us", "label": "Max Walker", "rate_hint": 1.25, "pitch_hint": 1.1},
    "darrell": {"locale": "en-us", "label": "Darrell Eastlake", "rate_hint": 1.35, "pitch_hint": 1.15},
    "slats": {"locale": "en-au", "label": "Michael Slater", "rate_hint": 1.2, "pitch_hint": 1.05},
}

DEFAULT_VOICE = COMMENTATOR_VOICES["richie"]
MAX_TTS_CHARS = 200
_CACHE: dict[str, bytes] = {}
_CACHE_MAX = 128

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def prepare_text(text: str) -> str:
    """Normalize text for speech synthesis."""
    text = text.strip()
    # Richie's famous "chew" = two
    text = re.sub(r"\bchew\b", "two", text, flags=re.IGNORECASE)
    # Remove emoji / special chars that break TTS
    text = re.sub(r"[^\w\s.,!'?\-–—]", "", text)
    if len(text) > MAX_TTS_CHARS:
        text = text[: MAX_TTS_CHARS - 3] + "..."
    return text


def get_voice(commentator_id: str) -> dict:
    return COMMENTATOR_VOICES.get(commentator_id, DEFAULT_VOICE)


def list_voices() -> list[dict]:
    return [
        {"id": k, **{key: v for key, v in cfg.items()}}
        for k, cfg in COMMENTATOR_VOICES.items()
    ]


def _cache_key(text: str, locale: str) -> str:
    return hashlib.md5(f"{locale}:{text}".encode()).hexdigest()


def synthesize_google(text: str, locale: str = "en-au") -> bytes | None:
    """Fetch MP3 audio from Google Translate TTS (free, unofficial endpoint)."""
    prepared = prepare_text(text)
    if not prepared:
        return None

    key = _cache_key(prepared, locale)
    if key in _CACHE:
        return _CACHE[key]

    params = urllib.parse.urlencode({
        "ie": "UTF-8",
        "client": "tw-ob",
        "tl": locale,
        "q": prepared,
    })
    url = f"https://translate.google.com/translate_tts?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            audio = resp.read()
            if len(audio) < 100:
                return None
            if len(_CACHE) >= _CACHE_MAX:
                _CACHE.pop(next(iter(_CACHE)))
            _CACHE[key] = audio
            return audio
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None


def synthesize(text: str, commentator_id: str = "richie") -> tuple[bytes | None, dict]:
    """Return (mp3_bytes, voice_config) for a commentator line."""
    voice = get_voice(commentator_id)
    audio = synthesize_google(text, voice["locale"])
    return audio, voice