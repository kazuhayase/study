# Talent Management DB — AI Assistant Context

## Project
生命保険グループ3社のタレントデータをSnowflakeに集約する読み取り専用分析基盤。

## Current Phase
Excelファイル監査 → Silverスキーマ確定 → IT entityスキルヒートマップ（5月末目標）

## Stack
- Local: DuckDB（プロトタイプ・スキーマ検証）
- Production: Snowflake（Bronze/Silver/Gold構造）
- Pipeline: Python scripts
- AI normalization: Claude API（Bronze→Silver変換のみ）

## Architecture

```
Bronze（生データ・不変）
  raw_it.*        ← Excel ITSS/DSS
  raw_dia.*       ← DIA（ExaWizards）
  raw_insurance.* ← Kaonavi
  raw_udemy.*     ← Udemy
      ↓ AI正規化（解析のみ・スコア変更なし）
Silver（クレンジング済・再実行可能）
  silver_it.*, silver_dia.*, silver_insurance.*, silver_udemy.*
      ↓
Gold（統合ビュー）
  gold.employees          ← 3社統合社員マスタ
  gold.skill_assessments  ← 全評価データ統合
  gold.skill_taxonomy     ← ITSS/DSS/DIA/Udemy統一タクソノミー
  gold.learning_activity  ← Udemy受講履歴
      ↓
Analytics
  view: skills_heatmap  ← スキル×エンティティ×レベル分布
  view: talent_map      ← 社員×スキル×レベル×エンティティ
```

## Critical Rules

1. **個人情報列は必ずENCRYPT/DECRYPT_AS_STRING使用（AES-256-GCM）**
   - `entity_employees.name_enc`
   - `employee_reviews.score_enc`, `comment_enc`
   - クエリ前に必ず実行: `SET passphrase = '（パスフレーズ）';`
   - 復号パターン: `DECRYPT_AS_STRING(name_enc, $passphrase)::VARCHAR AS name`

2. **AIは解析・正規化のみ。1-5スコアは人間入力を絶対に変更しない**

3. **BronzeはImmutable。Silver/Goldは再実行可能**
   - エラー訂正はSilverを修正→Gold再計算。Bronzeは触らない。

## How to Work With Me

**調査・デバッグ（investigate モード）**
「なぜこのクエリが遅いか」「このエラーの原因は」「なぜ件数が合わないか」
→ 推測で直さない。根本原因を特定してから修正する。

**アーキテクチャレビュー（plan-eng-review モード）**
「このスキーマ設計を見てほしい」「実装計画のレビュー」「このアーキテクチャで問題ないか」
→ Snowflakeベストプラクティス・エッジケース・パフォーマンス・テストカバレッジを順番に確認する。

**コードレビュー（review モード）**
「このSQLを確認して」「このPythonスクリプトをレビューして」
→ SQL安全性・LLM信頼境界（AIがスコアを変えていないか）・副作用を中心にチェックする。

**進捗保存（checkpoint モード）**
「ここまでの状況を整理して」「次回どこから再開するか」
→ 現状・決定事項・残タスク・次のアクションをまとめる。

## Open Questions（未解決・クリティカルパス）

1. **Excelファイルの列構造**（最優先・スキーマ確定のブロッカー）
2. グループ共通社員番号の存在確認（クロスエンティティ結合の鍵）
3. DXサブシジアリのデータソース（DIA以外に何があるか）
4. KaonaviエクスポートはAPIかファイルか（連携方式未確定）
5. DIA（ExaWizards）の納品フォーマット（CSV/API/Webのみか）
6. UdemyのAPIアクセス権限（ライセンス条件次第）

## Success Criteria

- CIOが「スキルXをレベルY以上持つ人」を3社横断で検索できる
- IT entityスキルヒートマップ：2026年5月末にSnowflakeで稼働
- 全社プラットフォーム：2026年9月末
- AI正規化エラー率：手動レビュー必要レコードが5%未満
