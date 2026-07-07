"""Live cricket data fetcher — Australia Tests, ODIs & T20s."""

import json
import os
import random
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from .series import (
    ALL_FORMATS,
    AUSTRALIA_TEST_SERIES,
    DEMO_FIXTURES,
    FORMAT_LABELS,
    FORMAT_ODI,
    FORMAT_T20,
    detect_format,
    detect_series,
    fixture_lookup,
    get_roster,
    get_series,
)


from .broadcast import BROADCAST_PARTNERS, get_broadcast_links as _get_broadcast_links

CRICAPI_BASE = "https://api.cricapi.com/v1"

# Backwards compatibility
BROADCAST_LINKS = BROADCAST_PARTNERS

# Ball outcome weights per format
_OUTCOME_WEIGHTS = {
    "test": [
        {"runs": 0, "wicket": False, "weight": 35},
        {"runs": 1, "wicket": False, "weight": 22},
        {"runs": 2, "wicket": False, "weight": 12},
        {"runs": 4, "wicket": False, "weight": 14},
        {"runs": 6, "wicket": False, "weight": 5},
        {"runs": 0, "wicket": True, "weight": 6},
        {"runs": 1, "wicket": False, "weight": 3, "extra": "wide"},
        {"runs": 0, "wicket": False, "weight": 3, "extra": "noball"},
    ],
    "odi": [
        {"runs": 0, "wicket": False, "weight": 22},
        {"runs": 1, "wicket": False, "weight": 20},
        {"runs": 2, "wicket": False, "weight": 14},
        {"runs": 4, "wicket": False, "weight": 22},
        {"runs": 6, "wicket": False, "weight": 10},
        {"runs": 0, "wicket": True, "weight": 7},
        {"runs": 1, "wicket": False, "weight": 3, "extra": "wide"},
        {"runs": 0, "wicket": False, "weight": 2, "extra": "noball"},
    ],
    "t20": [
        {"runs": 0, "wicket": False, "weight": 15},
        {"runs": 1, "wicket": False, "weight": 15},
        {"runs": 2, "wicket": False, "weight": 12},
        {"runs": 4, "wicket": False, "weight": 25},
        {"runs": 6, "wicket": False, "weight": 18},
        {"runs": 0, "wicket": True, "weight": 10},
        {"runs": 1, "wicket": False, "weight": 3, "extra": "wide"},
        {"runs": 0, "wicket": False, "weight": 2, "extra": "noball"},
    ],
}


@dataclass
class MatchInfo:
    id: str
    title: str
    status: str
    format: str = "test"
    format_label: str = "Test"
    series: str = ""
    series_name: str = ""
    trophy: str = ""
    venue: str = ""
    score: str = ""
    update: str = ""
    teams: list[str] = field(default_factory=list)
    source: str = "demo"


def _match_phase(fmt: str, over_num: int, max_overs: int) -> str:
    if fmt == "test":
        return ""
    if over_num < 6:
        return "powerplay"
    remaining = max_overs - over_num
    if remaining <= 5:
        return "death"
    return "middle"


class CricketDataFetcher:
    """Fetches live Australia cricket data; multi-format demo fallback."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("CRICAPI_KEY", "")
        self._demo_states: dict[str, dict] = {}

    def _fetch_json(self, url: str) -> dict | None:
        req = urllib.request.Request(url, headers={
            "User-Agent": "TwelfthManCommentary/3.0",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                return json.loads(resp.read())
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
            return None

    def get_broadcast_links(self, series_id: str | None = None) -> dict:
        return _get_broadcast_links(series_id)

    def get_all_series(self) -> list[dict]:
        return [
            {
                "id": s.id,
                "name": s.name,
                "trophy": s.trophy,
                "opponent": s.opponent,
                "emoji": s.emoji,
            }
            for s in AUSTRALIA_TEST_SERIES.values()
        ]

    def get_formats(self) -> list[dict]:
        return [{"id": f, "label": FORMAT_LABELS[f]} for f in ALL_FORMATS]

    def find_australia_matches(
        self,
        series_filter: str | None = None,
        format_filter: str | None = None,
    ) -> list[MatchInfo]:
        """Find all major Australia matches (Tests, ODIs, T20s)."""
        all_matches: list[MatchInfo] = []
        seen_ids: set[str] = set()

        if self.api_key:
            for endpoint in ("currentMatches", "matches"):
                data = self._fetch_json(
                    f"{CRICAPI_BASE}/{endpoint}?apikey={self.api_key}&offset=0")
                if data and data.get("status") == "success":
                    for m in data.get("data", []):
                        title = m.get("name", m.get("title", ""))
                        teams = m.get("teams", [])
                        series_id = detect_series(title, teams)
                        if not series_id:
                            continue
                        fmt = detect_format(title, m.get("matchType", ""))
                        if format_filter and fmt != format_filter:
                            continue
                        mid = str(m.get("id", m.get("unique_id", "")))
                        if mid in seen_ids:
                            continue
                        seen_ids.add(mid)
                        series = get_series(series_id)
                        all_matches.append(MatchInfo(
                            id=mid,
                            title=title,
                            status=m.get("status", m.get("matchStarted", "live")),
                            format=fmt,
                            format_label=FORMAT_LABELS.get(fmt, fmt),
                            series=series_id,
                            series_name=series.name if series else "",
                            trophy=series.trophy if series else "",
                            venue=m.get("venue", ""),
                            teams=teams if isinstance(teams, list) else [],
                            source="cricapi",
                        ))

        for f in self._build_demo_fixtures():
            if f.id not in seen_ids:
                if series_filter and f.series != series_filter:
                    continue
                if format_filter and f.format != format_filter:
                    continue
                all_matches.append(f)
                seen_ids.add(f.id)

        if series_filter:
            all_matches = [m for m in all_matches if m.series == series_filter]
        if format_filter:
            all_matches = [m for m in all_matches if m.format == format_filter]

        order = {"live": 0, "true": 0, "upcoming": 1, "fixture": 2}
        fmt_order = {"t20": 0, "odi": 1, "test": 2}
        all_matches.sort(key=lambda m: (
            order.get(str(m.status).lower(), 3),
            fmt_order.get(m.format, 3),
            m.series,
            m.title,
        ))
        return all_matches

    def find_australia_tests(self, series_filter: str | None = None) -> list[MatchInfo]:
        return self.find_australia_matches(series_filter=series_filter)

    def _build_demo_fixtures(self) -> list[MatchInfo]:
        results = []
        for fix in DEMO_FIXTURES:
            series = get_series(fix["series"])
            fmt = fix.get("format", "test")
            roster = get_roster(fix["series"], fmt)
            venue = fix.get("venue", roster["venue"])
            abbr = roster["opponent_abbr"]
            r, w, o, b = roster["runs"], roster["wickets"], roster["overs"], roster["balls"]
            results.append(MatchInfo(
                id=fix["id"],
                title=fix["title"],
                status=fix["status"],
                format=fmt,
                format_label=FORMAT_LABELS.get(fmt, fmt),
                series=fix["series"],
                series_name=series.name if series else "",
                trophy=series.trophy if series else "",
                venue=venue,
                score=f"{abbr} {r}/{w} ({o}.{b})" if fix["status"] == "live" else "",
                update=roster["lead_text"] if fix["status"] == "live" else "",
                teams=["Australia", series.opponent if series else ""],
                source="demo" if fix["id"].startswith("demo") else "fixtures",
            ))
        return results

    def _match_meta(self, match_id: str) -> dict:
        fix = fixture_lookup(match_id)
        if fix:
            return {
                "series": fix["series"],
                "format": fix.get("format", "test"),
            }
        for m in self.find_australia_matches():
            if m.id == match_id:
                return {"series": m.series or "ashes", "format": m.format or "test"}
        return {"series": "ashes", "format": "test"}

    def _series_for_match(self, match_id: str) -> str:
        return self._match_meta(match_id)["series"]

    def _format_for_match(self, match_id: str) -> str:
        return self._match_meta(match_id)["format"]

    def _is_demo_match(self, match_id: str) -> bool:
        return match_id.startswith("demo-") or match_id.startswith("fixture-")

    def get_match_score(self, match_id: str) -> dict | None:
        if self.api_key and not self._is_demo_match(match_id):
            data = self._fetch_json(
                f"{CRICAPI_BASE}/cricketScore?apikey={self.api_key}&id={match_id}")
            if data and data.get("status") == "success":
                return data.get("data", data)
        return self._demo_score(match_id)

    def get_next_ball(self, match_id: str) -> dict | None:
        if self.api_key and not self._is_demo_match(match_id):
            score = self.get_match_score(match_id)
            if score:
                meta = self._match_meta(match_id)
                return self._ball_from_score(score, meta["series"], meta["format"])
        return self._demo_next_ball(match_id)

    def _ball_from_score(self, score_data: dict, series_id: str, fmt: str) -> dict | None:
        update = score_data.get("status", score_data.get("matchStarted", ""))
        if not update:
            return None
        roster = get_roster(series_id, fmt)
        weights = _OUTCOME_WEIGHTS.get(fmt, _OUTCOME_WEIGHTS["test"])
        runs_opts = [o["runs"] for o in weights]
        run_weights = [o["weight"] for o in weights]
        runs = random.choices(runs_opts, weights=run_weights)[0]
        over_str = score_data.get("overs", "0.0")
        over_num = int(over_str.split(".")[0]) if "." in str(over_str) else 0
        return {
            "over": over_str,
            "over_number": over_num,
            "score": f"{score_data.get('score', '')}",
            "runs": runs,
            "wicket": random.random() < (0.10 if fmt == "t20" else 0.06),
            "batsman": score_data.get("batsman", random.choice(roster["batsmen"])),
            "bowler": score_data.get("bowler", random.choice(roster["bowlers"])),
            "batting_team": roster["batting_team"],
            "phase": _match_phase(fmt, over_num, roster.get("max_overs", 50)),
            "update": str(update),
        }

    def _init_demo_state(self, match_id: str) -> dict:
        meta = self._match_meta(match_id)
        roster = get_roster(meta["series"], meta["format"])
        return {
            "series_id": meta["series"],
            "format": meta["format"],
            "runs": roster["runs"],
            "wickets": roster["wickets"],
            "overs": roster["overs"],
            "balls": roster["balls"],
            "max_overs": roster.get("max_overs", 999),
            "batsman": roster["batsmen"][0],
            "bowler": roster["bowlers"][0],
            "batting_team": roster["batting_team"],
            "batting_abbr": roster["batting_abbr"],
            "batsmen": list(roster["batsmen"]),
            "bowlers": list(roster["bowlers"]),
            "fielders": list(roster["fielders"]),
            "lead_text": roster["lead_text"],
            "last_phase": "",
        }

    def _demo_score(self, match_id: str) -> dict:
        if match_id not in self._demo_states:
            self._demo_states[match_id] = self._init_demo_state(match_id)
        s = self._demo_states[match_id]
        over_str = f"{s['overs']}.{s['balls']}"
        return {
            "score": f"{s['batting_abbr']} {s['runs']}/{s['wickets']} ({over_str})",
            "status": s["lead_text"],
            "batsman": s["batsman"],
            "bowler": s["bowler"],
            "format": s["format"],
        }

    def _demo_next_ball(self, match_id: str) -> dict:
        if match_id not in self._demo_states:
            self._demo_score(match_id)
        s = self._demo_states[match_id]
        fmt = s["format"]

        outcomes = _OUTCOME_WEIGHTS.get(fmt, _OUTCOME_WEIGHTS["test"])
        weights = [o["weight"] for o in outcomes]
        outcome = random.choices(outcomes, weights=weights)[0]

        runs = outcome["runs"]
        if outcome.get("extra") == "wide":
            s["runs"] += 1
        elif outcome.get("extra") == "noball":
            s["runs"] += 1
        elif not outcome["wicket"]:
            s["runs"] += runs
        else:
            s["wickets"] += 1
            runs = 0

        s["balls"] += 1
        if s["balls"] >= 6:
            s["balls"] = 0
            s["overs"] += 1

        over_str = f"{s['overs']}.{s['balls']}"
        score_str = f"{s['batting_abbr']} {s['runs']}/{s['wickets']} ({over_str})"

        fielder = random.choice(s["fielders"])
        bowler_short = s["bowler"].split()[-1]
        dismissals = [
            f"c {fielder.split()[-1]} b {bowler_short}",
            f"lbw b {bowler_short}",
            f"b {bowler_short}",
            f"st {fielder.split()[-1]} b {bowler_short}",
            f"c {fielder.split()[-1]} b Lyon",
        ]

        phase = _match_phase(fmt, s["overs"], s["max_overs"])

        ball = {
            "over": over_str,
            "over_number": s["overs"],
            "score": score_str,
            "runs": runs,
            "wicket": outcome["wicket"],
            "batsman": s["batsman"],
            "bowler": s["bowler"],
            "batting_team": s["batting_team"],
            "dismissal": random.choice(dismissals) if outcome["wicket"] else "",
            "maiden": s["balls"] == 0 and runs == 0 and not outcome["wicket"],
            "phase": phase,
            "format": fmt,
        }
        if outcome.get("extra"):
            ball["extra"] = outcome["extra"]

        if outcome["wicket"]:
            s["batsman"] = random.choice(s["batsmen"])
        if random.random() < 0.05:
            s["bowler"] = random.choice(s["bowlers"])

        return ball

    def reset_demo(self, match_id: str | None = None):
        if match_id:
            self._demo_states.pop(match_id, None)
        else:
            self._demo_states.clear()