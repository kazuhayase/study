# SKILL: team-status
# 全会話に自動適用されるチーム共通運用ルール

## 参照順（会話開始時）

1. `AGENTS.md` — プロジェクト概要・Critical Rules
2. `TEAM_DOCS/MEMORY.md` — 現状・既知問題
3. `TEAM_DOCS/HANDOFF.md` — 進行中タスク
4. 当日の `TEAM_DOCS/DAILY_LOG/YYYY-MM-DD.md`（存在する場合）

## 出力形式

- **説明・回答**: 日本語
- **SQL・コード**: 英語（コメントも英語）
- **構造**: 結論を先に、詳細を後に
- **SQL出力時**: 必ず暗号化列の扱いを明示する

## ガードレール（生成するSQL・コードに必ず適用）

| ルール | 内容 |
|---|---|
| PII復号 | name_enc / score_enc / comment_enc は必ずDECRYPT_AS_STRING経由 |
| Bronze保護 | raw_* テーブルへのUPDATE/DELETE/INSERT文を生成しない |
| スコア不変 | 1-5スコア列をAIで書き換えるコードを生成しない |
| passphrase確認 | SET passphrase実行前提のSQLを生成する場合は冒頭に注記する |

## 作業モード別の振る舞い

| キーワード | モード | 重点 |
|---|---|---|
| 「なぜ」「原因」「デバッグ」 | investigate | 推測せず根本原因を特定してから修正案を出す |
| 「設計」「スキーマ」「レビュー」 | plan-eng-review | ベストプラクティス・エッジケース・パフォーマンスを順に確認 |
| 「確認して」「チェック」 | review | SQL安全性・PIIルール遵守・副作用を中心にチェック |
| 「まとめて」「整理して」「ここまで」 | checkpoint | 現状・決定事項・残タスク・次アクションを記録 |
