# Talent Management DB — AI Assistant Context

## Project Overview
生命保険グループ3社（生保・ITサブシジアリ・DXサブシジアリ）のタレント・スキルデータを
Snowflakeに集約する読み取り専用分析基盤。CIOからの直接指示。

- **現フェーズ**: Excelファイル監査 → Silverスキーマ確定 → ITスキルヒートマップ（5月末目標）
- **最終期限**: 2026年9月末（全社プラットフォーム）
- **チーム**: 2名（Hayase主担当）

## Architecture

```
Bronze（生データ・不変） → Silver（AI正規化・再実行可能） → Gold（統合ビュー） → Analytics
```

| レイヤー | 内容 |
|---|---|
| Bronze | raw_it.*, raw_dia.*, raw_insurance.*, raw_udemy.* |
| Silver | 正規化済み・クレンジング済み |
| Gold | employees, skill_assessments, skill_taxonomy, learning_activity |
| Analytics | skills_heatmap, talent_map |

## Critical Rules — Must Follow Without Exception

### 1. PII暗号化（最重要）
現在はPoC環境のため列レベル暗号化を使用。以下3列は**必ずDECRYPT_AS_STRING経由**でアクセスする。

```sql
-- セッション開始時に必ず実行
SET passphrase = '（パスフレーズをここに入力）';

-- 復号パターン（必須）
DECRYPT_AS_STRING(name_enc, $passphrase)::VARCHAR    AS name
DECRYPT_AS_STRING(score_enc, $passphrase)::INTEGER   AS eval_score
DECRYPT_AS_STRING(comment_enc, $passphrase)::VARCHAR AS eval_comment
```

暗号化対象: `entity_employees.name_enc` / `employee_reviews.score_enc` / `employee_reviews.comment_enc`

平文列（`name`, `eval_score`, `eval_comment`）は**存在しない**。生成SQLに含めてはならない。

### 2. AIはパース・正規化のみ
1–5スコアは人間入力値を絶対に変更・推定しない。

### 3. Bronzeはimmutable
エラー訂正はSilverを修正 → Gold再計算。Bronzeは触らない。

## Language Convention
- 回答・説明: **日本語**
- SQL・コード・コメント: **英語**

## Team Docs（作業前に参照）
- `TEAM_DOCS/MEMORY.md` — プロジェクト現状・既知問題
- `TEAM_DOCS/HANDOFF.md` — 進行中タスク・引き継ぎ事項
- `TEAM_DOCS/DECISIONS.md` — 設計判断の記録
- `TEAM_DOCS/DAILY_LOG/YYYY-MM-DD.md` — 日次作業ログ
