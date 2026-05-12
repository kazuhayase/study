#!/usr/bin/env python3
"""
Podcast summary agent.

Current mode: interactive CLI
Future:        scheduled agent (run with --episode-id to skip selection)
"""

import argparse
import sys
from pathlib import Path

from extract import Episode, extract_text, list_episodes
from summarize import summarize

OUTPUT_DIR = Path(__file__).parent / "summaries"


def select_episode_interactive(episodes: list[Episode]) -> Episode:
    print(f"\n文字起こしが利用可能なエピソード ({len(episodes)}件):\n")
    for i, ep in enumerate(episodes, 1):
        print(f"  {i:2}. [{ep.podcast}] {ep.title}")
    print()

    try:
        choice = int(input("番号を選択: ")) - 1
    except (ValueError, KeyboardInterrupt):
        sys.exit(0)

    if not 0 <= choice < len(episodes):
        print("無効な番号です")
        sys.exit(1)

    return episodes[choice]


def run(episode: Episode, save: bool = False) -> str:
    if not episode.has_transcript:
        raise FileNotFoundError(f"TTMLファイルが見つかりません: {episode.transcript_id}")

    print(f"\n文字起こしを抽出中: {episode.title}")
    transcript = extract_text(episode)  # type: ignore[arg-type]
    print(f"  {len(transcript)}文字を抽出しました")

    print("要約を生成中...\n")
    summary = summarize(episode.title, episode.podcast, transcript)

    header = f"{'=' * 60}\n  {episode.podcast}\n  {episode.title}\n{'=' * 60}"
    output = f"{header}\n{summary}"
    print(output)

    if save:
        OUTPUT_DIR.mkdir(exist_ok=True)
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in episode.title)
        out_path = OUTPUT_DIR / f"{safe_title[:80]}.md"
        out_path.write_text(f"# {episode.podcast} — {episode.title}\n\n{summary}\n")
        print(f"\n保存しました: {out_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Apple Podcasts transcript summarizer")
    parser.add_argument("--limit", type=int, default=30, help="表示するエピソード数")
    parser.add_argument("--save", action="store_true", help="summaries/ に保存")
    # future agent flags
    parser.add_argument("--transcript-id", help="TTMLパス（自動実行用）")
    parser.add_argument("--episode-title", help="エピソードタイトル（自動実行用）")
    parser.add_argument("--podcast-title", help="Podcastタイトル（自動実行用）")
    args = parser.parse_args()

    if args.transcript_id:
        # non-interactive mode for future scheduler/agent use
        episode = Episode(
            title=args.episode_title or "Unknown",
            podcast=args.podcast_title or "Unknown",
            transcript_id=args.transcript_id,
        )
    else:
        episodes = list_episodes(limit=args.limit)
        if not episodes:
            print("文字起こし付きエピソードが見つかりません")
            sys.exit(1)
        episode = select_episode_interactive(episodes)

    run(episode, save=args.save)


if __name__ == "__main__":
    main()
