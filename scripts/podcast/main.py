#!/usr/bin/env python3
"""
Podcast summary agent.

Current mode: interactive CLI
Future:        scheduled agent (run with --episode-id to skip selection)
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from extract import Episode, extract_text, list_episodes
from summarize import summarize

OUTPUT_DIR = Path(__file__).parent / "summaries"


def summary_path(episode: Episode) -> Path:
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in episode.title)
    prefix = f"{episode.pub_date}_" if episode.pub_date else ""
    return OUTPUT_DIR / f"{prefix}{safe_title[:80]}.md"


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


def send_mail(to: str, subject: str, body: str) -> None:
    # Write body to a temp file to avoid AppleScript string escaping issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(body)
        tmp_path = f.name

    safe_subject = subject.replace("\\", "\\\\").replace('"', '\\"')
    script = f"""
    set bodyText to read POSIX file "{tmp_path}" as «class utf8»
    tell application "Mail"
        set msg to make new outgoing message with properties {{subject: "{safe_subject}", content: bodyText, visible: false}}
        tell msg
            make new to recipient with properties {{address: "{to}"}}
        end tell
        send msg
    end tell
    """
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    finally:
        os.unlink(tmp_path)


def run(episode: Episode, save: bool = False, model: str | None = None) -> str:
    if not episode.has_transcript:
        raise FileNotFoundError(f"TTMLファイルが見つかりません: {episode.transcript_id}")

    print(f"\n文字起こしを抽出中: {episode.title}")
    transcript = extract_text(episode)  # type: ignore[arg-type]
    print(f"  {len(transcript)}文字を抽出しました")

    print("要約を生成中...\n")
    summary = summarize(episode.title, episode.podcast, transcript, model=model)

    date_str = f"  {episode.pub_date}\n" if episode.pub_date else ""
    header = f"{'=' * 60}\n  {episode.podcast}\n  {episode.title}\n{date_str}{'=' * 60}"
    print(f"{header}\n{summary}")

    if save:
        OUTPUT_DIR.mkdir(exist_ok=True)
        out_path = summary_path(episode)
        date_line = f"**公開日**: {episode.pub_date}\n\n" if episode.pub_date else ""
        out_path.write_text(f"# {episode.podcast} — {episode.title}\n\n{date_line}{summary}\n")
        print(f"\n保存しました: {out_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Apple Podcasts transcript summarizer")
    parser.add_argument("--limit", type=int, default=30, help="表示するエピソード数")
    parser.add_argument("--unplayed", action="store_true", help="未再生エピソードのみ表示")
    parser.add_argument("--all", action="store_true", help="全件を自動で要約")
    parser.add_argument("--save", action="store_true", help="summaries/ に保存")
    parser.add_argument("--mail", metavar="ADDRESS", help="要約をメール送信")
    parser.add_argument("--model", help="mlx-lmモデル名 (default: Qwen2.5-7B-Instruct-4bit)")
    # non-interactive flags for agent use
    parser.add_argument("--transcript-id", help="TTMLパス（自動実行用）")
    parser.add_argument("--episode-title", help="エピソードタイトル（自動実行用）")
    parser.add_argument("--podcast-title", help="Podcastタイトル（自動実行用）")
    args = parser.parse_args()

    if args.transcript_id:
        episode = Episode(
            title=args.episode_title or "Unknown",
            podcast=args.podcast_title or "Unknown",
            transcript_id=args.transcript_id,
        )
        summary = run(episode, save=args.save, model=args.model)
        if args.mail:
            send_mail(args.mail, f"[Podcast要約] {episode.title}", summary)
            print(f"メール送信: {args.mail}")

    elif args.all:
        episodes = list_episodes(limit=args.limit, unplayed_only=args.unplayed)
        if not episodes:
            print("文字起こし付きエピソードが見つかりません")
            sys.exit(1)

        OUTPUT_DIR.mkdir(exist_ok=True)
        pending = [ep for ep in episodes if not summary_path(ep).exists()]
        skipped = len(episodes) - len(pending)
        print(f"\n{len(episodes)}件中 {skipped}件はスキップ（要約済み）、{len(pending)}件を処理します\n")

        mail_bodies: list[str] = []
        for i, episode in enumerate(pending, 1):
            print(f"[{i}/{len(pending)}]", end=" ")
            try:
                summary = run(episode, save=True, model=args.model)
                if args.mail:
                    mail_bodies.append(f"## {episode.podcast} — {episode.title}\n\n{summary}")
            except Exception as e:
                print(f"  スキップ: {e}")

        if args.mail and mail_bodies:
            body = "\n\n---\n\n".join(mail_bodies)
            send_mail(args.mail, f"[Podcast要約] {len(mail_bodies)}件", body)
            print(f"\nメール送信: {args.mail} ({len(mail_bodies)}件)")

    else:
        episodes = list_episodes(limit=args.limit, unplayed_only=args.unplayed)
        if not episodes:
            print("文字起こし付きエピソードが見つかりません")
            sys.exit(1)
        episode = select_episode_interactive(episodes)
        summary = run(episode, save=args.save, model=args.model)
        if args.mail:
            send_mail(args.mail, f"[Podcast要約] {episode.title}", summary)
            print(f"メール送信: {args.mail}")


if __name__ == "__main__":
    main()
