"""Extract plain text from Apple Podcasts TTML transcript files."""

import sqlite3
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

PODCASTS_BASE = Path.home() / "Library/Group Containers/243LU875E5.groups.com.apple.podcasts"
DB_PATH = PODCASTS_BASE / "Documents/MTLibrary.sqlite"
TTML_BASE = PODCASTS_BASE / "Library/Cache/Assets/TTML"

TTML_NS = "http://www.w3.org/ns/ttml"
PODCASTS_NS = "http://podcasts.apple.com/transcript-ttml-internal"


@dataclass
class Episode:
    title: str
    podcast: str
    transcript_id: str

    @property
    def ttml_path(self) -> Path | None:
        # DB stores e.g. "PodcastContent221/.../transcript_123.ttml"
        # but the cached file is "transcript_123.ttml-123.ttml" (extra suffix)
        base = TTML_BASE / self.transcript_id
        if base.exists():
            return base
        matches = list(base.parent.glob(f"{base.name}-*.ttml"))
        return matches[0] if matches else None

    @property
    def has_transcript(self) -> bool:
        return self.ttml_path is not None


def list_episodes(limit: int = 50, unplayed_only: bool = False) -> list[Episode]:
    # ZPLAYSTATE: 0=未再生, 1=途中, 2=再生済み
    played_filter = "AND e.ZPLAYSTATE = 0" if unplayed_only else ""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT e.ZTITLE, p.ZTITLE, e.ZTRANSCRIPTIDENTIFIER
        FROM ZMTEPISODE e
        JOIN ZMTPODCAST p ON e.ZPODCAST = p.Z_PK
        WHERE e.ZTRANSCRIPTIDENTIFIER IS NOT NULL
        {played_filter}
        ORDER BY e.ZPUBDATE DESC
        LIMIT ?
        """,
        (limit * 3,),  # fetch extra to account for missing cache files
    )
    rows = cur.fetchall()
    conn.close()

    episodes = [Episode(title=r[0], podcast=r[1], transcript_id=r[2]) for r in rows]
    return [ep for ep in episodes if ep.has_transcript][:limit]


def extract_text(episode: Episode) -> str:
    """Parse TTML and return plain text grouped by sentence."""
    path = episode.ttml_path
    if path is None:
        raise FileNotFoundError(f"TTMLファイルが見つかりません: {episode.transcript_id}")
    tree = ET.parse(path)
    root = tree.getroot()

    sentences = []
    for span in root.findall(f".//{{{TTML_NS}}}span[@{{{PODCASTS_NS}}}unit='sentence']"):
        words = [
            w.text
            for w in span.findall(f"{{{TTML_NS}}}span")
            if w.get(f"{{{PODCASTS_NS}}}unit") == "word" and w.text
        ]
        if words:
            sentences.append(" ".join(words))

    return "\n".join(sentences)
