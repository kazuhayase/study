# TEAM MEMORY — Talent Management DB

最終更新: 2026-05-12

## 現フェーズ
**Excelファイル監査 → Silverスキーマ確定 → ITスキルヒートマップ（5月末目標）**

## プロジェクト状況

### 完了済み
- Bronze/Silver/Gold アーキテクチャ設計（design-20260412.md）
- Bronzeスキーマ（IT entity）: `migrations/001_bronze_it_schema.sql`
- PII暗号化ポリシー確定（AES-256-GCM、ENCRYPT/DECRYPT_AS_STRING）
- Cortex Code向けコンテキスト文書（docs/snowsight-talent-mgmt-prompt.md）
- Excelファイル（3年分・200ファイル以上）の読み込み成功
- 約75名分の社員データベース構築

### 進行中
- Excelファイル列構造の監査（**クリティカルパス**）
- Silverスキーマ設計

### 未着手
- DX subsidiary データソース確認
- Kaonavi連携方式確定
- DIA（ExaWizards）納品フォーマット確認
- Udemy APIアクセス権限確認

## 既知問題・注意事項

### PII暗号化（最重要）
現在はPoC環境のため専用ロール未発行。以下3列は暗号化済み：
- `entity_employees.name_enc`
- `employee_reviews.score_enc`
- `employee_reviews.comment_enc`

**全SQLで必ずDECRYPT_AS_STRINGを使うこと。セッション前に `SET passphrase` を実行。**

本番移行時: 専用ロール・Dynamic Data Maskingに切り替え予定。

### Snowflake RBACの誤解（解決済み）
2026-04-18に発覚: タレマネ担当以外もアクセス可能な状態だったため暗号化で対応。

### gstackスキル
- Snowsight Cortex Code: このワークスペースのスキルを使用
- Claude Code CLI: `~/.claude/skills/` に全スキルインストール済み

## クリティカルパス（未解決ブロッカー）

1. **Excelファイルの列構造**（Silverスキーマのブロッカー）
2. グループ共通社員番号の存在確認
3. DXサブシジアリのデータソース

## 成功基準
- ITスキルヒートマップ: 2026年5月末にSnowflakeで稼働
- 全社プラットフォーム: 2026年9月末
- AI正規化エラー率: 手動レビュー必要レコードが5%未満
