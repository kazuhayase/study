# 週次作業まとめ — 2026-04-12 〜 2026-04-23

## 作業者
- kazuhayase（タレントマネジメント担当）

---

## ■ talent-mgmt-db プロジェクト立ち上げ（4/12）

タレントマネジメントDBのSnowflake PoC開始。

- 設計ドキュメント作成（メダリオンアーキテクチャ、Bronze/Silver/Gold構成）
- DuckDB（ローカル）→ Snowflake（本番）の移行方針を確定
- Cortex Codeに設計ドキュメント・SQLをステージ経由で渡し、設計から実装を実施

---

## ■ Bronze ITスキーマ マイグレーション（4/14）

- Excelファイル（3年分・200ファイル以上）の読み込み完了
- 約75名分の社員データベースが稼働

---

## ■ セキュリティ対応（4/18）

Snowflakeのスキーマ・ロールを部内他プロジェクトと共有していたため、意図せずアクセス可能な状態だったことを発見。  
GRANT / REVOKE・CREATE ROLE権限がないため、列レベル暗号化で対応。

| テーブル | 暗号化列 | 元の型 | 内容 |
|---|---|---|---|
| `entity_employees` | `name_enc` | VARCHAR | 氏名 |
| `employee_reviews` | `score_enc` | INTEGER | 評価スコア（1–5） |
| `employee_reviews` | `comment_enc` | VARCHAR | 評価コメント（自由文） |

- 方式：Snowflake `ENCRYPT()` / `DECRYPT_AS_STRING()`（AES-256-GCM）、パスフレーズ外部管理
- 本番移行時に専用ロール・スキーマへ切り替える方針
- 設計ドキュメントに暗号化ポリシーを追記しCortex Codeにも反映

---

## ■ セキュリティ脆弱性の修正（4/23）

mls-seminarプロジェクトの `requirements.txt` に4件の脆弱性を発見・修正。

| パッケージ | 対応 |
|---|---|
| urllib3 | 最新版に更新 |
| Pygments | 最新版に更新 |
| nbconvert | 最新版に更新 |
| fonttools | 最新版に更新 |

---

## 次回セッションへの引き継ぎ事項

- [ ] 更新した `design-20260412.md` をステージに再アップロードする
- [ ] 既存データ（75名分）の暗号化UPDATEを実行する
- [ ] 平文列（`name_canonical`, `eval_score`, `eval_comment`）の削除またはNULL化
- [ ] 本番移行時にSnowflake管理者へ専用ロール発行を申請する
