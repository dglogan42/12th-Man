"""Minimal Google Translate TTS proxy — shared by static sports apps."""

import hashlib
import re
import urllib.error
import urllib.parse
import urllib.request

_CACHE: dict[str, bytes] = {}
_CACHE_MAX = 128
_MAX_CHARS = 220
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

LOCALE_MAP = {
    "default": "en-gb",
    "morag": "en-gb",
    "richie": "en-au",
    "bill": "en-au",
    "tony": "en-gb",
    "kitt": "en-us",
    "hoff": "en-us",
    "kiwi": "en-nz",
    "mcenroe": "en-us",
    "warney": "en-au",
    "golf": "en-us",
    "wwe": "en-us",
    "f1": "en-gb",
    "de": "de-de",
    "fr": "fr-fr",
}


def prepare_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[^\w\s.,!'?\-–—]", "", text)
    if len(text) > _MAX_CHARS:
        text = text[: _MAX_CHARS - 3] + "..."
    return text


def _cache_key(text: str, locale: str) -> str:
    return hashlib.md5(f"{locale}:{text}".encode()).hexdigest()


def synthesize(text: str, announcer: str = "default", locale: str | None = None) -> bytes | None:
    loc = locale or LOCALE_MAP.get(announcer, "en-gb")
    prepared = prepare_text(text)
    if not prepared:
        return None

    key = _cache_key(prepared, loc)
    if key in _CACHE:
        return _CACHE[key]

    params = urllib.parse.urlencode({
        "ie": "UTF-8",
        "client": "tw-ob",
        "tl": loc,
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