#!/usr/bin/env python3
"""Standalone clip + TTS server for static sports apps.

Usage:
  CLIP_APP_ID=f1-monaco CLIP_PODCAST_TITLE="F1 Monaco Feed" python3 clip-server.py
  # Serves static files from current directory + /api/tts, /api/clips, /api/podcast/feed.rss
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))

from clips_api import configure_podcast, generate_rss, list_clips, register_clip
from tts_proxy import synthesize

PORT = int(os.environ.get("CLIP_PORT", os.environ.get("PORT", "8790")))
APP_ID = os.environ.get("CLIP_APP_ID", "sports-app")
PODCAST_TITLE = os.environ.get("CLIP_PODCAST_TITLE", f"{APP_ID} — Sports Clips")
PODCAST_DESC = os.environ.get(
    "CLIP_PODCAST_DESC",
    "Commentary clips from a sports fan app. Clip and share to social or podcast.",
)
PODCAST_AUTHOR = os.environ.get("CLIP_PODCAST_AUTHOR", "Sports Clip Studio")

configure_podcast(APP_ID, PODCAST_TITLE, PODCAST_DESC, PODCAST_AUTHOR)


class ClipHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/api/tts":
            text = qs.get("text", [""])[0]
            announcer = qs.get("announcer", ["default"])[0]
            locale = qs.get("locale", [None])[0]
            audio = synthesize(text, announcer, locale)
            if audio:
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(audio)
            else:
                self._json({"error": "TTS failed"}, 502)
        elif parsed.path == "/api/clips":
            self._json({"clips": list_clips(APP_ID), "app_id": APP_ID})
        elif parsed.path == "/api/podcast/feed.rss":
            host = self.headers.get("Host", f"localhost:{PORT}")
            body = generate_rss(APP_ID, f"http://{host}").encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/rss+xml; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}

        if parsed.path == "/api/clips":
            clip = register_clip(
                APP_ID,
                text=data.get("text", ""),
                announcer=data.get("announcer", "default"),
                commentator_name=data.get("commentator_name", "Announcer"),
                event_title=data.get("event_title", PODCAST_TITLE),
                caption=data.get("caption", ""),
            )
            host = self.headers.get("Host", f"localhost:{PORT}")
            self._json({"clip": clip, "feed_url": f"http://{host}/api/podcast/feed.rss"})
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def main():
    print(f"""
 ╔══════════════════════════════════════════════════╗
 ║  Sports Clip Studio — TTS + Clip Server          ║
 ╠══════════════════════════════════════════════════╣
 ║  App:     {APP_ID:<40}║
 ║  Local:   http://localhost:{PORT:<27}║
 ║  TTS:     /api/tts?text=...&announcer=...        ║
 ║  RSS:     /api/podcast/feed.rss                  ║
 ╚══════════════════════════════════════════════════╝
""")
    HTTPServer(("0.0.0.0", PORT), ClipHandler).serve_forever()


if __name__ == "__main__":
    main()