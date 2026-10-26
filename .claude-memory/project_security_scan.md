---
name: セキュリティスキャン手法・既知リスク・自動化設定
description: OSV APIによるスキャン手法・Mac制約の回避策・既知CVE・週次自動化ルーティンの詳細
type: project
originSessionId: 979e4fb4-591a-49da-99fc-843d02f27d66
modified: 2026-10-24T04:13:49.325Z
---
## スキャン手法（Mac環境）

### Python依存関係 → OSV API（pip-audit は使わない）
pip-audit は Python 3.14 で fugashi/scikit-learn のビルドに失敗するため、OSV API を直接使う：

```python
import urllib.request, json

def check_osv(pkg, ver, ecosystem="PyPI"):
    data = json.dumps({"version": ver, "package": {"name": pkg, "ecosystem": ecosystem}}).encode()
    req = urllib.request.Request("https://api.osv.dev/v1/query", data=data,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    return result.get("vulns", [])
```

npm パッケージは `ecosystem="npm"` で同じAPIを使う。

### gh CLI → 使えない（未インストール）
Dependabot API は OSV API で代替。`gh api repos/kazuhayase/study/dependabot/alerts` は実行不可。

---

## 既知リスク（毎回のスキャンで確認すること）

| パッケージ | バージョン | CVE | 状況 |
|---|---|---|---|
| chromadb | 1.5.9 | CVE-2026-45829 (CRITICAL) + CVE-2026-45833 (HIGH) | 2026-10-26時点で両方とも修正版なし。trust_remote_code=True を使わなければ攻撃不可。PyPI新バージョンが出たらアップグレード。 |
| axios | ^1.20.0 (3ファイル, 2026-10-24に1.16.1から更新) | 1.20.0はFIX版 | 1.20.0はCVE-2026-101901等複数の2026 advisoryの修正版。安全確認済み(2026-10-26)。 |
| socket.io / socket.io-client | ^4.7.4 → ^4.8.0 (2ファイル, 2026-10-26に更新) | CVE-2026-59725 (High, CVSS 7.5) | 4.7.4はEngine.IOポーリング接続消耗によるDoS。4.8.0で修正版(Mendの情報)。streaming-chat-app×2で更新済み。 |
| torch / setuptools | torch==2.11.0 / setuptools<82 (LLM/openmythos-test) | GHSA-rrmf-rvhw-rf47 / GHSA-h35f-9h28-mq5c, GHSA-xmj3-9gf7-h52w | サードパーティ open-mythos==0.5.0 がtorch==2.11.0を厳密ピン→setuptools<82強制。open-mythosの新版待ち。いずれもローカルアクセス前提の低リスク。 |

### 修正済みファイル（2026-05-30）
- `LLM/DA-Elyza2024/python/requirements.txt` — chromadb CVE コメント追記
- `LLM/DA-Elyza2024/javascript/da-elyza-rag/package.json` — axios 1.6.7→1.16.1
- `LLM/DA-Elyza2024/javascript/act-mls2024/package.json` — 同上
- `LLM/act-MLS2024/javascript/act-mls2024/package.json` — 同上
- `LLM/FDUA2025/majority_trial.py` — os.system() → subprocess.run()
- `LLM/FDUA2025/trial_vote_old.py` — 同上
- `R/DS/test_rev.R` — ハードコード絶対パスをコメントアウト

---

## Debianマシンでのスキャン（2026-10-24実施）

このDebian機（/mnt/ubuntu/home/kazuyoshi/github/study, apt update&upgrade済み・再起動前）で手動依頼によりスキャン実施。
`gh` CLI は導入済み・認証済み（kazuhayaseアカウント）だったため、Dependabot API も併用できた。

**重要な発見: requirements.txt/package.json だけのスキャンでは `poetry.lock`/`uv.lock` 内の
transitive依存の脆弱性を見逃す。** Dependabot cross-check (`gh api .../dependabot/alerts`) で
以下のlockファイルに脆弱なtransitive依存（anyio, certifi, urllib3, black, langgraph-sdk,
aiohttp, filelock, fsspec, datasets, multidict, transformers等）が見つかった:
- `LLM/DA-Elyza2024/python/sample-server/poetry.lock` + `llm-server/poetry.lock`
- `LLM/act-MLS2024/python/sample-server/poetry.lock` + `llm-server/poetry.lock`
- `LLM/model-compare/uv.lock`, `LLM/openmythos-test/uv.lock`

**修正方法**: `uv lock --upgrade-package <name>`（複数指定可）、poetryは未インストールだが
`uvx poetry update <name>` でサンドボックス実行可能（インストール不要、プロジェクトディレクトリに
副作用なし、poetry.lockのみ更新される）。

**修正不能な既知の制約（2026-10-24時点）**:
- `LLM/openmythos-test`: サードパーティ `open-mythos==0.5.0`（PyPI最新）が `torch==2.11.0` を
  厳密ピン → torchが `setuptools<82` を要求。torch GHSA-rrmf-rvhw-rf47、setuptools
  GHSA-h35f-9h28-mq5c / GHSA-xmj3-9gf7-h52w は open-mythos の新バージョンが出るまで修正不可
  （いずれもローカルアクセス前提の低リスク）。`pyproject.toml` にコメントで記録済み。
- chromadb==1.5.9: CVE-2026-45829 (CRITICAL) に加え CVE-2026-45833 (HIGH) も既知（2026-10-19に
  他マシンで追記）。両方とも引き続き修正版なし。

**今回の修正ファイル（14件、mergeコミット55b0fad）**: mls-seminar/requirements.txt（11パッケージ）、
LLM/DA-Elyza2024/python/requirements.txt（pypdf）、axios 1.16.1→1.20.0（3 package.json）、
@babel/core 7.20.0→7.29.6（2 package.json）、poetry.lock×4、uv.lock×2、openmythos-test/pyproject.toml。
push時に他マシンの2026-10-19スキャン(chromadb CVE-2026-45833追記)とコンフリクトしたため
`git merge origin/master` で解消（両方のCVE記載を保持）。

## 週次自動スキャン（2026-10-26 Cowork環境）

**制約: Cowork環境でOSV APIがプロキシ(403)でブロックされる。** `api.osv.dev:443` はproxy policyでCONNECT拒否。
代替手段：WebSearch でCVE検索 + GitHub Dependabot APIは `gh api` (403: Resource not accessible by integration) で取得不可。
→ **WebSearch によるCVE手動確認**に依存。次回以降もCoworkではWebSearch検索を先に行うこと。

**今回の修正ファイル（3件、コミット83bbbf3）**:
- `LLM/DA-Elyza2024/javascript/streaming-chat-app/package.json` — socket.io/socket.io-client 4.7.4→4.8.0
- `LLM/act-MLS2024/javascript/streaming-chat-app/package.json` — 同上
- `LLM/DA-Elyza2024/python/requirements.txt` — chromadb CVEコメント日付更新(2026-10-24→2026-10-26)

**Why:** Dependabot cross-checkは「OSVはrequirements.txt/package.jsonしか見ない」という既存の
Mac向けメモの想定を裏付けた。次回以降もlockファイル(poetry.lock/uv.lock)を必ず含めてスキャンする。

**How to apply:** 今後どのマシンでスキャンしても、Step 1-2のOSV直接スキャンに加えて
`find . -iname "poetry.lock" -o -iname "uv.lock"` でlockファイルを洗い出し、同じOSV API
(バッチエンドポイント `/v1/querybatch` が速い)でチェックすること。`gh` CLIがあればDependabot
cross-checkも必ず行う。

## 週次自動スキャン（設定済み）

- **スケジュール**: 毎週月曜 9:00 JST（UTC 0:00）、cron: `0 0 * * 1`
- **ルーティンID**: `trig_01NTDkYt1CRMm9R47ULyoRfQ`
- **管理**: https://claude.ai/code/routines/trig_01NTDkYt1CRMm9R47ULyoRfQ
- **スコープ**: リポジトリ全体（find で再帰的に全ディレクトリ）
- **モデル**: claude-sonnet-4-6
- **動作**: OSV スキャン → 修正 → コミット（`fix(security): weekly scan YYYY-MM-DD`） → push（全自動・確認不要）

**Why:** セキュリティ対応を完全に自動化し、ユーザーが依頼しなくても最新の脆弱性に対応し続けるため。

**How to apply:** 手動でスキャンを依頼された場合も同じ OSV API 手法を使う。既知リスクテーブルは毎回スキャン後に更新する。
