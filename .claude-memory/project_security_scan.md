---
name: セキュリティスキャン手法・既知リスク・自動化設定
description: OSV APIによるスキャン手法・Mac制約の回避策・既知CVE・週次自動化ルーティンの詳細
type: project
originSessionId: 979e4fb4-591a-49da-99fc-843d02f27d66
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
| chromadb | 1.5.9 | CVE-2026-45829 (CRITICAL) | 2026-05-30時点で修正版なし。trust_remote_code=True を使わなければ攻撃不可。PyPI新バージョンが出たらアップグレード。 |
| axios | ^1.16.1 (3ファイル) | — | 1.6.7から修正済み。次回スキャンで 1.16.1 が引き続き安全か確認する。 |

### 修正済みファイル（2026-05-30）
- `LLM/DA-Elyza2024/python/requirements.txt` — chromadb CVE コメント追記
- `LLM/DA-Elyza2024/javascript/da-elyza-rag/package.json` — axios 1.6.7→1.16.1
- `LLM/DA-Elyza2024/javascript/act-mls2024/package.json` — 同上
- `LLM/act-MLS2024/javascript/act-mls2024/package.json` — 同上
- `LLM/FDUA2025/majority_trial.py` — os.system() → subprocess.run()
- `LLM/FDUA2025/trial_vote_old.py` — 同上
- `R/DS/test_rev.R` — ハードコード絶対パスをコメントアウト

---

## 週次自動スキャン（設定済み）

- **スケジュール**: 毎週月曜 9:00 JST（UTC 0:00）、cron: `0 0 * * 1`
- **ルーティンID**: `trig_01NTDkYt1CRMm9R47ULyoRfQ`
- **管理**: https://claude.ai/code/routines/trig_01NTDkYt1CRMm9R47ULyoRfQ
- **スコープ**: リポジトリ全体（find で再帰的に全ディレクトリ）
- **モデル**: claude-sonnet-4-6
- **動作**: OSV スキャン → 修正 → コミット（`fix(security): weekly scan YYYY-MM-DD`） → push（全自動・確認不要）

**Why:** セキュリティ対応を完全に自動化し、ユーザーが依頼しなくても最新の脆弱性に対応し続けるため。

**How to apply:** 手動でスキャンを依頼された場合も同じ OSV API 手法を使う。既知リスクテーブルは毎回スキャン後に更新する。
