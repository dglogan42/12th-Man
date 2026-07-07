"""Clip registry for Twelfth Man — uses shared sports-clip-studio API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "clip-studio"))

from clips_api import configure_podcast, generate_rss, list_clips, register_clip

APP_ID = "twelfth-man-ashes"

configure_podcast(
    APP_ID,
    title="Twelfth Man — Australia Cricket Commentary",
    description="Spoof Billy Birmingham / Twelfth Man commentary clips. Richie, Bill, Tony and the gang.",
    author="Twelfth Man Commentary",
    guid_prefix="ashes-clip",
)