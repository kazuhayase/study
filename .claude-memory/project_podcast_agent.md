---
name: Podcast要約エージェント
description: scripts/podcast/ の構成・動作・設計判断のメモ
type: project
---

**場所:** `~/github/study/scripts/podcast/`

**構成:**
- `extract.py` — SQLite（ZMTEPISODE）+ TTMLファイルからテキスト抽出
- `summarize.py` — mlx-lm（Qwen2.5-7B-Instruct-4bit）で要約
- `main.py` — CLIエントリポイント。対話・バッチ・エージェントモード対応
- `.venv/` — uv管理のvenv（gitignore済み）
- `summaries/` — 出力先（gitignore済み）。ファイル名は `YYYY-MM-DD_タイトル.md`
- `logs/` — LaunchAgentのログ（gitignore済み）

**主なフラグ:**
```bash
.venv/bin/python main.py --unplayed --all --mail kazuyoshi.hayase@gmail.com
```
- `--unplayed`: 未再生エピソードのみ（ZPLAYSTATE=0）
- `--all`: 全件バッチ処理。summaries/に既存ファイルがあればスキップ
- `--mail ADDRESS`: Mail.appでメール送信（tempfile経由でAppleScript呼び出し）
- `--model`: mlx-lmモデル名を変更可能（env: PODCAST_MODEL）

**自動実行:** LaunchAgent `com.kazu.podcast-summary` で毎日6:45に実行
- plist: `~/Library/LaunchAgents/com.kazu.podcast-summary.plist`
- 管理: `launchctl load/unload ~/Library/LaunchAgents/com.kazu.podcast-summary.plist`

**設計上のポイント・ハマりどころ:**
- TTMLファイル名: DBには `transcript_xxx.ttml` だが実ファイルは `transcript_xxx.ttml-xxx.ttml`（globで対応）
- AppleScriptへの本文渡し: f-string埋め込みは改行・引用符でクラッシュ → tempfile経由
- OllamaはM5 Pro（Metal4 / macOS Tahoe 26）未対応 → mlx-lmに切り替え
- ZPUBDATE: Core Dataタイムスタンプ（2001-01-01起算の秒数）→ `_APPLE_EPOCH + timedelta(seconds=ts)`
