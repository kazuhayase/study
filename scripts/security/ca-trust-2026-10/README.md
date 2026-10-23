# eMudhra / emSign 中間CA秘密鍵漏洩への対応手順 (2026-10)

eMudhra (emSign) の中間CA 8つの秘密鍵が、公開証明書から復元できる状態だった件の対応手順です
(<https://emudhra.we-have-a-problem.com/>, GHSA-6q48-6c7w-9gw2)。
独自のCAバンドルを同梱しているツールは、更新するまで該当の中間CAを信頼し続けます。

## 修正版

| ツール | 修正版 | 補足 |
|---|---|---|
| certifi | 2026.10.19 | 2026.10.18 は影響のない emSign ルートまで削除したため、10.19 を使う |
| pip | 26.2.2 | pip は certifi を**同梱** (`pip._vendor.certifi`) しているので、certifi だけ更新しても直らない |
| uv | 0.13.4 以上 (このリポジトリでは 0.13.5) | |
| pixi | 0.82.1 以上 | `webpki-root-certs` 1.0.10 / `rustls-webpki` 0.103.16 を採用 (公式 CHANGELOG) |
| sigstore | 4.5.1 | 各種の注意喚起では下限版として挙がっているが、公式 CHANGELOG には本件の記載がない。このリポジトリでは未使用 |
| conda | 26.9.4 以上 | conda-forge の `ca-certificates` / `certifi` も 2026.10.19 |
| Node.js | 22.23.4 / 24.22.1 / 26.12.1 | 2026-10-21 のセキュリティリリース。21/23/25 は EOL のため修正版なし |

## なぜハッシュを固定するのか

更新前の pip は、まだ漏洩した中間CAを信頼しています。そのため、更新版のダウンロードそのものが
中間者攻撃を受けるおそれがあります。`--require-hashes` を付けると、TLS で何を信頼しているかに
関係なく、PyPI が公開している sha256 と一致しないファイルは pip がインストールを拒否します。

`bootstrap-requirements.txt` のハッシュは、PyPI の JSON API (`https://pypi.org/pypi/<pkg>/<ver>/json`)
が公開している値です。2026-10-23 に、新規 venv へインストールして動作を確認しました。

## 手順 (各マシンで実行)

### 1. 既存の venv ごとに pip / certifi を更新

```bash
# macOS / Linux
.venv/bin/python -m pip install --require-hashes --no-deps --only-binary :all: \
    -r scripts/security/ca-trust-2026-10/bootstrap-requirements.txt
```

```powershell
# Windows
.venv\Scripts\python.exe -m pip install --require-hashes --no-deps --only-binary :all: `
    -r scripts\security\ca-trust-2026-10\bootstrap-requirements.txt
```

- `bootstrap-requirements.txt` には uv も含まれます。uv を venv に入れたくない場合は、ファイルを
  コピーして `uv==` のブロックを削除してから使ってください。
- **新規に作成した venv も対象です。** Python 3.13.16 の `ensurepip` が入れる pip は 26.2.1 なので、
  `python -m venv` の直後に必ずこの手順を実行してください。
- python.org 版の macOS インストーラを使っている場合は、`Install Certificates.command` も再実行
  してください (フレームワーク側の certifi が更新されます)。

### 2. スタンドアロンの uv を更新

```bash
uv self update 0.13.5      # 公式インストーラで入れた場合
brew upgrade uv            # Homebrew の場合
```

そのあと、uv で管理しているプロジェクトでは `uv sync` を実行し、`.venv` の certifi を
2026.10.19 にします (`uv.lock` はこのコミットで更新済みです)。

### 3. pixi / conda

```bash
pixi self-update --version 0.83.0   # 0.82.1 以上であればよい
conda update -n base conda ca-certificates certifi
```

### 4. Node.js

`node --version` が 22.23.4 / 24.22.1 / 26.12.1 以上であることを確認してください。
Docker イメージ (`FROM node`) は `docker build --pull` で再ビルドします。

### 5. 確認

```bash
python -c "import pip, pip._vendor.certifi as c; print(pip.__version__, c.__version__)"
# -> 26.2.2 2026.10.19
python -c "import certifi; print(certifi.__version__)"     # -> 2026.10.19
uv --version                                               # -> 0.13.4 以上
```
