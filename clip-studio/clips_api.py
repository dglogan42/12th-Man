"""Shared clip registry & podcast RSS — configurable per sports app."""

from __future__ import annotations

import html
import threading
import time
import uuid
from urllib.parse import quote

_lock = threading.Lock()
_registries: dict[str, list[dict]] = {}
_MAX_CLIPS = 50


def configure_podcast(
    app_id: str,
    title: str,
    description: str,
    author: str,
    guid_prefix: str | None = None,
) -> None:
    _registries.setdefault(app_id, [])
    _registries[f"{app_id}__meta"] = [{
        "title": title,
        "description": description,
        "author": author,
        "guid_prefix": guid_prefix or f"{app_id}-clip",
    }]


def _meta(app_id: str) -> dict:
    meta_list = _registries.get(f"{app_id}__meta", [])
    if meta_list:
        return meta_list[0]
    return {
        "title": f"{app_id} Sports Clips",
        "description": "Sports commentary clips",
        "author": "Sports Clip Studio",
        "guid_prefix": f"{app_id}-clip",
    }


def register_clip(
    app_id: str,
    text: str,
    announcer: str = "default",
    commentator_name: str = "Announcer",
    event_title: str = "Live Sports",
    caption: str = "",
) -> dict:
    with _lock:
        clips = _registries.setdefault(app_id, [])
        clip = {
            "id": str(uuid.uuid4())[:8],
            "text": text[:500],
            "announcer": announcer,
            "commentator_name": commentator_name,
            "event_title": event_title,
            "caption": caption[:1000],
            "created": time.time(),
        }
        clips.insert(0, clip)
        if len(clips) > _MAX_CLIPS:
            clips.pop()
        return clip


def list_clips(app_id: str) -> list[dict]:
    with _lock:
        return list(_registries.get(app_id, []))


def generate_rss(app_id: str, base_url: str, tts_path: str = "/api/tts") -> str:
    meta = _meta(app_id)
    base = base_url.rstrip("/")
    items = []
    for clip in list_clips(app_id):
        tts_url = (
            f"{base}{tts_path}?text={quote(clip['text'])}"
            f"&announcer={quote(clip['announcer'])}"
        )
        title = html.escape(
            f"{clip['commentator_name']}: {clip['text'][:80]}"
            + ("…" if len(clip['text']) > 80 else ""),
        )
        desc = html.escape(clip.get("caption") or clip["text"])
        pub = time.strftime(
            "%a, %d %b %Y %H:%M:%S +0000",
            time.gmtime(clip["created"]),
        )
        guid = f"{meta['guid_prefix']}-{clip['id']}"
        items.append(f"""    <item>
      <title>{title}</title>
      <description>{desc}</description>
      <pubDate>{pub}</pubDate>
      <guid isPermaLink="false">{guid}</guid>
      <enclosure url="{html.escape(tts_url)}" length="0" type="audio/mpeg"/>
    </item>""")

    if not items:
        items.append(f"""    <item>
      <title>{html.escape(meta['title'])} — Get started</title>
      <description>Clip commentary lines in the app to populate this feed.</description>
      <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
      <guid isPermaLink="false">{meta['guid_prefix']}-placeholder</guid>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{html.escape(meta['title'])}</title>
    <link>{html.escape(base)}</link>
    <description>{html.escape(meta['description'])}</description>
    <language>en</language>
    <itunes:author>{html.escape(meta['author'])}</itunes:author>
    <itunes:summary>{html.escape(meta['description'])}</itunes:summary>
    <itunes:category text="Sports"/>
    <itunes:explicit>no</itunes:explicit>
{chr(10).join(items)}
  </channel>
</rss>"""