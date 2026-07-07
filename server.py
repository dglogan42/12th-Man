#!/usr/bin/env python3
"""Twelfth Man Commentary Server — Tests, ODIs & T20s involving Australia."""

import json
import os
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))

from commentary import CommentaryEngine, CricketDataFetcher
from commentary.tts import list_voices, synthesize

PORT = int(os.environ.get("PORT", "8765"))
STATIC_DIR = Path(__file__).parent / "static"

fetcher = CricketDataFetcher()
engine = CommentaryEngine()

_match_sessions: dict[str, dict] = {}
_lock = threading.Lock()


def get_session(match_id: str) -> dict:
    with _lock:
        if match_id not in _match_sessions:
            _match_sessions[match_id] = {
                "lines": [],
                "running": False,
                "thread": None,
                "match_id": match_id,
            }
        return _match_sessions[match_id]


def commentary_loop(match_id: str):
    session = get_session(match_id)
    matches = fetcher.find_australia_matches()
    match = next((m for m in matches if m.id == match_id), None)
    venue = match.venue if match else "the MCG"
    title = match.title if match else "Australia Match"
    series_id = match.series if match else fetcher._series_for_match(match_id)
    fmt = match.format if match else fetcher._format_for_match(match_id)

    intro_lines = engine.generate_session_start(venue, title, series_id, fmt)
    with _lock:
        session["lines"].extend([l.to_dict() for l in intro_lines])

    while session["running"]:
        ball = fetcher.get_next_ball(match_id)
        if ball:
            lines = engine.generate_from_ball(ball)
            with _lock:
                session["lines"].extend([l.to_dict() for l in lines])
                if len(session["lines"]) > 200:
                    session["lines"] = session["lines"][-200:]
        time.sleep(random_delay(fmt))

    session["thread"] = None


def random_delay(fmt: str = "test") -> float:
    import random
    if fmt == "t20":
        return random.uniform(2.0, 5.0)
    if fmt == "odi":
        return random.uniform(3.0, 7.0)
    return random.uniform(4.0, 9.0)


class CommentaryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format, *args):
        if os.environ.get("QUIET"):
            return
        super().log_message(format, *args)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        series_filter = qs.get("series", [None])[0]
        format_filter = qs.get("format", [None])[0]

        if path == "/api/series":
            self._json_response({
                "series": fetcher.get_all_series(),
                "formats": fetcher.get_formats(),
            })
        elif path == "/api/matches":
            self._json_response(self._get_matches(series_filter, format_filter))
        elif path == "/api/broadcast":
            series_id = qs.get("series", [None])[0]
            self._json_response(fetcher.get_broadcast_links(series_id))
        elif path == "/api/commentary":
            match_id = qs.get("match_id", ["demo-ashes-test"])[0]
            since = float(qs.get("since", ["0"])[0])
            session = get_session(match_id)
            lines = [l for l in session["lines"] if l["timestamp"] > since]
            self._json_response({
                "lines": lines,
                "running": session["running"],
                "match_id": match_id,
            })
        elif path == "/api/score":
            match_id = qs.get("match_id", ["demo-ashes-test"])[0]
            score = fetcher.get_match_score(match_id)
            self._json_response({"score": score or {}})
        elif path == "/api/tts/voices":
            self._json_response({"voices": list_voices(), "provider": "google_translate"})
        elif path == "/api/tts":
            text = qs.get("text", [""])[0]
            commentator = qs.get("commentator", ["richie"])[0]
            audio, voice = synthesize(text, commentator)
            if audio:
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-TTS-Voice", voice.get("locale", "en-au"))
                self.end_headers()
                self.wfile.write(audio)
            else:
                self._json_response({"error": "TTS synthesis failed"}, status=502)
        elif path == "/":
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

        if parsed.path == "/api/start":
            match_id = data.get("match_id", "demo-ashes-test")
            session = get_session(match_id)
            if not session["running"]:
                session["running"] = True
                if match_id.startswith("demo-"):
                    fetcher.reset_demo(match_id)
                t = threading.Thread(target=commentary_loop, args=(match_id,), daemon=True)
                session["thread"] = t
                t.start()
            self._json_response({"status": "started", "match_id": match_id})

        elif parsed.path == "/api/stop":
            match_id = data.get("match_id", "demo-ashes-test")
            session = get_session(match_id)
            session["running"] = False
            self._json_response({"status": "stopped", "match_id": match_id})

        elif parsed.path == "/api/reset":
            match_id = data.get("match_id", "demo-ashes-test")
            session = get_session(match_id)
            session["running"] = False
            session["lines"] = []
            fetcher.reset_demo(match_id)
            self._json_response({"status": "reset", "match_id": match_id})

        else:
            self.send_error(404)

    def _get_matches(
        self,
        series_filter: str | None = None,
        format_filter: str | None = None,
    ) -> dict:
        matches = fetcher.find_australia_matches(series_filter, format_filter)
        has_api = bool(fetcher.api_key)
        return {
            "matches": [
                {
                    "id": m.id,
                    "title": m.title,
                    "status": m.status,
                    "format": m.format,
                    "format_label": m.format_label,
                    "series": m.series,
                    "series_name": m.series_name,
                    "trophy": m.trophy,
                    "venue": m.venue,
                    "score": m.score,
                    "update": m.update,
                    "teams": m.teams,
                    "source": m.source,
                }
                for m in matches
            ],
            "series": fetcher.get_all_series(),
            "formats": fetcher.get_formats(),
            "api_connected": has_api,
            "api_hint": (
                "Set CRICAPI_KEY for live Tests, ODIs & T20s (free at cricketdata.org)"
                if not has_api
                else "Connected — live Australia matches from CricketData.org"
            ),
        }

    def _json_response(self, data: dict, status: int = 200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    os.chdir(STATIC_DIR)
    server = HTTPServer(("0.0.0.0", PORT), CommentaryHandler)
    series_list = ", ".join(s.opponent for s in __import__("commentary.series", fromlist=["AUSTRALIA_TEST_SERIES"]).AUSTRALIA_TEST_SERIES.values())
    print(f"""
 ╔══════════════════════════════════════════════════════════╗
 ║   🏏  TWELFTH MAN CRICKET COMMENTARY  🏏                   ║
 ║   Tests · ODIs · T20s — Australia Spoof Commentary      ║
 ╠══════════════════════════════════════════════════════════╣
 ║   Local:   http://localhost:{PORT:<5}                        ║
 ║   Series:  {series_list:<47}║
 ╠══════════════════════════════════════════════════════════╣
 ║   FOX Sports AU · Kayo · Sky Sports UK · Star Sports IN  ║
 ║   🔊 Free TTS — Google Translate voices per commentator   ║
 ╠══════════════════════════════════════════════════════════╣
 ║   Demo mode active. For live scores set:                 ║
 ║   export CRICAPI_KEY=your_key   (free at cricketdata.org)║
 ╚══════════════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping commentary box...")
        server.shutdown()


if __name__ == "__main__":
    main()