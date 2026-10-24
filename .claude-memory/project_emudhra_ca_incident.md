---
name: emudhra-emsign-ca-incident-remediation
description: 2026-10 eMudhra/emSign中間CA秘密鍵漏洩インシデントへの対応(pip/certifi/uv/venv) - Debian機で実施済み
metadata:
  node_type: memory
  type: project
  originSessionId: f72ce0e9-0aa1-4705-8324-df7805e32834
  modified: 2026-10-24T04:25:04.452Z
---

## インシデント概要（2026-10-17発覚）

eMudhraブランド名emSignの中間CA証明書8件（TLS用6件、コード署名用2件）の秘密鍵が、
P-384鍵生成時の鍵ラップ処理の欠陥により極端に弱い値（1〜255の範囲）で生成されていたことが
判明。公開証明書だけから秘密鍵を計算可能 = 誰でも任意サイトのTLS証明書を偽造できる状態。
実際に確認された侵害ルートは **emSign ECC Root CA – G3** のみ。Chrome/Firefoxは
2026-10-17〜19に該当中間証明書をブロック、Chromeはルート自体を2026-10-27にトラストストアから
削除予定。

**Why:** pip/uv/certifi はOS証明書ストアに依存せず自前でCA束を同梱しているツールが多く、
OS側(apt/ca-certificates)を更新しただけでは直らない。PyPIからの通常の`pip install --upgrade`
自体がこの漏洩の影響を受けるTLS経路を使う可能性があるため、公式はハッシュ値固定インストールを
推奨している。

## 修正版バージョン（公式アナウンス = discuss.python.org #109576 より）

| ツール | 修正版 |
|---|---|
| pip | 26.2.2 |
| certifi | 2026.10.19 (advisory最低ライン) / **2026.10.23推奨**（非侵害ルートとの互換性） |
| uv | 0.13.4 |
| sigstore | 4.5.1 |
| conda | 26.9.4 |
| pixi | 0.82.1 |

## このDebian機での対応（2026-10-24実施）

### 発見した環境
- `mls-seminar/.venv` (python3.11.2) — pip 23.0.1 / certifi 2025.11.12 **要修正**
- `LLM/act-MLS2024/python/sample-server/.venv`, `LLM/DA-Elyza2024/python/sample-server/.venv`
  (poetry in-project venv) — 同日の`uvx poetry update`実行時に新規作成され、
  pip 26.2.2 / certifi 2026.10.23が最初から入っていた（対応不要、確認のみ）
- `~/.cache/pypoetry/virtualenvs/llm-server-*-py3.13` (2件、llm-server用) — 同上、対応不要
- uv本体 `/home/kazu/.local/bin/uv` — **0.10.4（要修正）**
- sigstore / pixi / conda — **このマシンには未インストール（対象外）**
- system apt pip (`python3-pip` 23.0.1) — Debianはpipを自前certifi非同梱・システムCA store依存に
  パッチ済み(他マシン非公式情報)。本機のシステムCA storeを確認した結果、実際に侵害された
  `emSign ECC Root CA – G3` は**そもそも含まれていなかった**(後述)。緊急対応不要と判断。

### 実施した修正
1. **pip** (`mls-seminar/.venv`): 公式ハッシュ固定コマンドで更新
   ```
   python -m pip install "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
   ```
   このハッシュは`https://pypi.org/pypi/pip/26.2.2/json`の公式digestと一致することを確認済み。
2. **certifi**: pip更新後に`pip install --upgrade certifi` → 2026.10.23。
3. **venv全体sync**: `pip install --no-deps -r requirements.txt`で、当日先に実施した通常の
   脆弱性スキャン修正（anyio/pillow/tornado等）もまとめて実インストール。
   - **副産物の互換性問題3件を発見・修正**（テキスト編集だけでは見逃す）:
     - soupsieve 3.0.4 は Python>=3.11.5 必須だがこのvenvは3.11.2 → 2.9.2に変更
       (Dependabotの最低修正ライン2.9.0は満たしクリーン)
     - jupyterlab 4.6.4 で新規ランタイム依存 `jupyter-builder>=1.0.2` が追加されていた
       (4.5.9には無かった) → 明示的に追加
     - anyio 4.15.1 が `typing_extensions>=4.16.0` を要求 → 4.15.0から更新
   - `pip check`でクリーン確認、jupyterlab/notebook/pillow importとjupyter --versionで
     動作確認済み。
4. **uv本体**: `uv self update`はOS証明書ストア依存(`UV_SYSTEM_CERTS=true`)か旧uv自体のTLS検証に
   依存するため使わず、GitHub Releasesから`uv-x86_64-unknown-linux-gnu.tar.gz`と同梱の
   `.sha256`ファイルを個別取得してハッシュ照合→展開→`~/.local/bin/uv`を手動置換(旧バイナリは
   `.../scratchpad/uv_backup/`に保存)。0.10.4 → 0.13.4。

### OSトラストストア調査結果（重要・対応不要と判断した根拠）
`/etc/ssl/certs/ca-certificates.crt`を調査した結果、本機には以下のeMudhra/emSignルートが
含まれていた: `emSign Root CA - C1`、`emSign ECC Root CA - C3`、`emSign Root CA - G1`。
しかし**実際に侵害が確認されたのは`emSign ECC Root CA - G3`のみ**で、このルートは
本機のバンドルに**存在しなかった**。C1/C3はcurlが予防的に削除した一方でcertifi自身は
「侵害未確認」として保持を選択、G1はChromeが調査中で結論未出。したがって
`update-ca-certificates`でのルート無効化などのOS設定変更は実施しなかった
（システムセキュリティ設定の変更はユーザー自身の判断に委ねる方針、かつ今回は
certifi自身の判断と整合して不要と結論）。
Debian `ca-certificates`パッケージは20250419~deb12u2のまま(2026-10-24時点で候補バージョンなし
= まだDebian側のセキュリティ更新が来ていない)ことも確認済み。

**How to apply:** 今後別マシン(特にWindows機・Mac機)でも同様の手順を踏むこと: (1)
`pip --version`/`uv --version`で現状確認、(2) venvを`find -iname pyvenv.cfg`で**depth制限なし**
で網羅的に洗い出す(今回当初`-maxdepth 4`で2件の`.venv`を見逃した)、(3) 必ずPyPI JSON API等で
ハッシュを独立に再検証してから使う、(4) `pip install -r requirements.txt`のようなテキスト編集後は
**実際にvenvへインストールして`pip check`で確認する**(編集だけでは互換性問題を検出できない)、
(5) OSトラストストアに実際に侵害されたルートが含まれているかを確認してから対応の緊急度を
判断する(存在しないルートを心配して不要なシステム設定変更をしない)。[[project_security_scan]]
