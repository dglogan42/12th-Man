"""Twelfth Man commentary engine — transforms ball events into spoof commentary."""

import random
import time
from dataclasses import dataclass, field

from . import lines
from .series import FORMAT_INTROS, FORMAT_LABELS, FORMAT_STAKES_SUFFIX, get_series


@dataclass
class CommentaryLine:
    text: str
    commentator: str
    commentator_name: str
    color: str
    event_type: str
    over: str = ""
    score: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "commentator": self.commentator,
            "commentator_name": self.commentator_name,
            "color": self.color,
            "event_type": self.event_type,
            "over": self.over,
            "score": self.score,
            "timestamp": self.timestamp,
        }


class CommentaryEngine:
    """Generates Billy Birmingham / Twelfth Man style commentary from match events."""

    def __init__(self):
        self._banter_counter = 0
        self._last_over = -1
        self._series_id = "ashes"
        self._format = "test"
        self._last_phase = ""

    def set_series(self, series_id: str, fmt: str = "test"):
        self._series_id = series_id
        self._format = fmt
        self._banter_counter = 0
        self._last_over = -1
        self._last_phase = ""

    def _wrap(self, text: str, commentator_id: str, event_type: str,
              over: str = "", score: str = "") -> CommentaryLine:
        info = lines.COMMENTATORS[commentator_id]
        return CommentaryLine(
            text=text,
            commentator=commentator_id,
            commentator_name=info["name"],
            color=info["color"],
            event_type=event_type,
            over=over,
            score=score,
        )

    def _stakes_phrase(self) -> str:
        series = get_series(self._series_id)
        return series.stakes_line if series else "Series honours on the line!"

    def generate_from_ball(self, ball: dict) -> list[CommentaryLine]:
        """Convert a ball-by-ball event dict into commentary lines."""
        results: list[CommentaryLine] = []
        over = ball.get("over", "")
        score = ball.get("score", "")
        runs = ball.get("runs", 0)
        is_wicket = ball.get("wicket", False)
        batsman = ball.get("batsman", "")
        bowler = ball.get("bowler", "")
        batting_team = ball.get("batting_team", "")
        dismissal = ball.get("dismissal", "")

        bat_parody = lines.parody_name(batsman, batting_team)
        bowl_parody = lines.parody_name(bowler, "australia")

        self._banter_counter += 1
        if self._banter_counter % 18 == 0:
            banter_pool = (
                lines.BANTER_LINES
                + lines.series_banter(self._series_id)
                + lines.format_banter(self._format)
            )
            text, cid = lines.pick_line(banter_pool)
            results.append(self._wrap(text, cid, "banter", over, score))

        phase = ball.get("phase", "")
        if phase and phase != self._last_phase and self._format in ("odi", "t20"):
            pline = lines.phase_line(self._format, phase)
            if pline:
                text, cid = pline
                results.append(self._wrap(text, cid, "phase", over, score))
                self._last_phase = phase

        if is_wicket:
            text, cid = lines.pick_line(lines.WICKET_LINES)
            results.append(self._wrap(text, cid, "wicket", over, score))
            stakes = self._stakes_phrase()
            if dismissal:
                detail = f"{bat_parody} is gone! {dismissal}. {stakes}"
            else:
                detail = f"{bat_parody} is walking off! {bowl_parody} has got the breakthrough!"
            results.append(self._wrap(detail, lines.IAN, "wicket_detail", over, score))
        elif runs == 6:
            six_pool = lines.T20_SIX_LINES if self._format == "t20" else lines.SIX_LINES
            text, cid = lines.pick_line(six_pool)
            results.append(self._wrap(text, cid, "six", over, score))
            results.append(self._wrap(
                f"{bat_parody} has launched that into the members' area! Magnificent!",
                lines.RICHHIE, "six_detail", over, score))
        elif runs == 4:
            text, cid = lines.pick_line(lines.FOUR_LINES)
            results.append(self._wrap(text, cid, "four", over, score))
        elif runs == 2:
            text, cid = lines.pick_line(lines.TWO_LINES)
            results.append(self._wrap(text, cid, "two", over, score))
        elif runs == 0:
            text, cid = lines.pick_line(lines.DOT_LINES)
            results.append(self._wrap(text, cid, "dot", over, score))
        elif ball.get("extra") == "wide":
            text, cid = lines.pick_line(lines.WIDE_LINES)
            results.append(self._wrap(text, cid, "wide", over, score))
        elif ball.get("extra") == "noball":
            text, cid = lines.pick_line(lines.NO_BALL_LINES)
            results.append(self._wrap(text, cid, "noball", over, score))
        else:
            results.append(self._wrap(
                f"{runs} run{'s' if runs != 1 else ''}. {bowl_parody} to {bat_parody}.",
                lines.RICHHIE, "runs", over, score))

        over_num = ball.get("over_number")
        if over_num is not None and over_num != self._last_over:
            if ball.get("maiden"):
                text, cid = lines.pick_line(lines.MAIDEN_LINES)
                results.append(self._wrap(text, cid, "maiden", over, score))
            self._last_over = over_num

        return results

    def generate_session_start(self, venue: str = "", match_title: str = "",
                                series_id: str = "ashes", fmt: str = "test") -> list[CommentaryLine]:
        self.set_series(series_id, fmt)
        results = []
        series = get_series(series_id)
        fmt_intro = FORMAT_INTROS.get(fmt, "")
        series_intro = series.intro_line if series else fmt_intro
        if fmt != "test":
            series_intro = f"{fmt_intro} {series_intro}"
        text, cid = lines.welcome_line(venue, series_intro)
        results.append(self._wrap(text, cid, "welcome"))
        text, cid = lines.pick_line(lines.SESSION_LINES)
        results.append(self._wrap(text, cid, "session"))
        if fmt == "test":
            text, cid = lines.pick_line(lines.PITCH_REPORT_LINES)
            results.append(self._wrap(text, cid, "pitch_report"))
        elif fmt == "t20":
            results.append(self._wrap(
                "Twenty overs a side. No time for tea — get on with it!",
                lines.BILL, "format_intro"))
        else:
            results.append(self._wrap(
                "Fifty overs per side. White ball, coloured clothing — marvellous!",
                lines.RICHHIE, "format_intro"))
        banter_pool = lines.series_banter(series_id) + lines.format_banter(fmt)
        if banter_pool:
            text, cid = lines.pick_line(banter_pool)
            results.append(self._wrap(text, cid, "series_banter"))
        if match_title:
            stakes = series.stakes_line if series else "Series honours on the line!"
            stakes += FORMAT_STAKES_SUFFIX.get(fmt, "")
            fmt_label = FORMAT_LABELS.get(fmt, "")
            results.append(self._wrap(
                f"Today's {fmt_label} encounter: {match_title}. {stakes}",
                lines.BILL, "match_intro"))
        return results

    def generate_score_update(self, score: str, update: str = "") -> CommentaryLine:
        if update:
            text = f"{update} {lines.pick_line(lines.SESSION_LINES)[0]}"
        else:
            text = f"The score is now {score}. {random.choice(['Fascinating.', 'Intriguing.', 'Marvellous cricket.'])}"
        return self._wrap(text, lines.RICHHIE, "score_update", score=score)

    def generate_drinks(self) -> CommentaryLine:
        text, cid = lines.pick_line(lines.DRINKS_LINES)
        return self._wrap(text, cid, "drinks")

    def generate_rain(self) -> CommentaryLine:
        text, cid = lines.pick_line(lines.RAIN_LINES)
        return self._wrap(text, cid, "rain")