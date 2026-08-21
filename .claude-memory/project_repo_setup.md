---
name: studyリポジトリセットアップ状況
description: CLAUDE.md・セキュリティ自動化・Mac固有注意点など、リポジトリ全体の設定状況
type: project
originSessionId: 979e4fb4-591a-49da-99fc-843d02f27d66
---
## リポジトリ設定（2026-05-30時点）

### CLAUDE.md
- リポジトリルートに配置済み
- 日本語応答・英語コード規約・自動メモリ更新ルール・セキュリティワークフロー・コミット規約を定義
- セキュリティワークフローは OSV API ベース（pip-audit / gh は Mac では使えないため）
- 「確認不要でコミット・push」を明記済み

### .claude/settings.json（コミット済み）
セキュリティスキャン用のコマンドをプロジェクト全体で許可：
```json
["python3 *", "grep *", "find *",
 "git add/commit/push/pull/merge/log/diff/status/worktree/branch *",
 "npm audit *", "pip-audit *", "ls *"]
```

### セキュリティ自動化（2026-05-30設定）
- **週次ルーティン**: 毎週月曜 9:00 JST（= UTC 0:00）に自動実行
- ルーティンID: `trig_01NTDkYt1CRMm9R47ULyoRfQ`
- 管理URL: https://claude.ai/code/routines/trig_01NTDkYt1CRMm9R47ULyoRfQ
- スコープ: **リポジトリ全体**（find で再帰的に全ディレクトリを対象）
- 実行内容: OSV APIスキャン → 修正 → コミット → push（全自動）

### その他セットアップ済み
- `.github/workflows/gitleaks.yml` — シークレットスキャン自動化
- `.gitleaks.toml` / `.pre-commit-config.yaml` / `Makefile`
- `prompts/_meta/` — プロンプトライブラリテンプレート

---

## Mac固有の注意点

- **メモリパス**: `/Users/kazu/.claude/projects/-Users-kazu-github-study/memory/`（Debianは `/home/kazu/.claude/...`）
- **Ollama**: このMac（M5 Pro / macOS Tahoe）では動作しない → mlx-lm を使う
- **pip-audit**: Python 3.14 環境で失敗する（fugashi/scikit-learn のビルドエラー）→ OSV API 直接呼び出しで代替
- **gh CLI**: インストールされていない → OSV API / curl で代替

**Why:** リポジトリ横断でClaude Codeの動作を統一し、セキュリティ対応を完全自動化するため。

**How to apply:** セキュリティチェックは pip-audit / gh を使わず OSV API スクリプトで実行。設定変更後は必ず CLAUDE.md・memory・settings.json の3点セットを更新する。


## リポジトリ分離（2026-07-11）
- **actuary/ 配下は別リポジトリ `kazuhayase/actuary`（private）に分離**。ディスク上のパスは
  `~/github/study/actuary/` のまま（studyの中にネストした独立gitリポ。studyの.gitignoreで `actuary/` を無視）。
  経緯: studyがpublicで教科書・過去問PDF等が公開状態だったため、git filter-repoで
  actuary履歴を抽出（170コミット保持）→private新リポへ、study側は全履歴からactuaryを除去して
  force-push（コミット494→363、.git 213MB→97MB）。旧 claude/zen-hamilton ブランチは削除（マージ済みだった）。
- **他マシン対応（要実施）**: Debian・Windows(Cowork)は study を再クローンし、
  `git clone git@github.com:kazuhayase/actuary.git study/actuary` を追加実行。
  Coworkからprivateリポを触るにはそのマシンでのGitHub認証が必要。
- gh CLI をこのMacにインストール・認証済み（keyring、repoスコープ）。以前の「gh未インストール」記述は失効。
- ローカルの worktree-security-fixes ブランチ（未マージ）は旧履歴のまま温存
  → 再開時は新masterへ cherry-pick すること。
- GitHub上の旧SHA直アクセスはGC まで残存し得る（fork 0のためリスク小。完全消去はGitHubサポート依頼）。
