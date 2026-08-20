# vulndb — BOD 26-04 脆弱性優先度データベース

CISA **BOD 26-04「Prioritizing Security Updates Based on Risk」**（2026-06-10 発行）の判定を
機械的に行うための DuckDB データベース。NVD・CISA KEV・CISA Vulnrichment・FIRST EPSS を
取り込み、CVE ごとに是正期限を算出する。

---

## BOD 26-04 とは

BOD 22-01（KEV）と BOD 19-02 を置き換えた指令。**CVSS スコアによる期限設定を廃止**し、
次の4変数で 16 通りに分類して期限を決める。

| 変数 | 内容 | 出所 |
|---|---|---|
| **Publicly Exposed** | 資産が公衆網から到達可能か | **各組織が判定**（CISA は提供しない） |
| **In the KEV** | CVE が KEV カタログに掲載されているか | CISA |
| **Automatable** | 攻撃者が全手順を自動化できるか | CISA（Vulnrichment / SSVC） |
| **Technical Impact** | 全体制御か部分制御か | CISA（Vulnrichment / SSVC） |

期限は **3日・14日・60日・次回システム更新時** の4層。KEV 掲載かつ Total control の3行には
**フォレンジック triage**（侵害済みか否かの調査）が追加で課される。日数は暦日。

### 期限の起算日

指令 Appendix A の定義:

> The timelines defined in Table 1 begin when either (1) CISA adds the vulnerability to the KEV
> Catalog, or (2) ... the agency enumerates or identifies the vulnerability on an asset ...
> **Whichever event occurs first** starts the remediation timeline.

本DBは資産インベントリを持たないため、算出できるのは (1) のみ。したがって
`due_date_*` が埋まるのは **KEV 掲載 CVE だけ**で、それ以外は検出データが入るまで NULL。
これは実装の手抜きではなく、指令どおりに「まだ決まらない」ことを表している。

### 決定マトリクスの出典

`migrations/005_seed_bod2604_matrix.sql` が唯一の正。
[指令本文](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)の
Appendix A, Table 1（[PNG 画像](https://www.cisa.gov/sites/default/files/2026-06/BOD_26-04_Table_1_Remediation_Timelines_0.png)
として公開）から 2026-08-20 に転記した。

CISA は Table 1 を**年度ごとに見直す**と明記しているため、この表は将来変わる。
`tests/test_bod2604.py` が独立に転記した16行を保持しており、シードが変われば必ず落ちる。

> **注意**: cisa.gov は一部の自動取得クライアントに 403 を返す。ブラウザの User-Agent を付ければ通る。

---

## データソース

| ソース | 取得方法 | 供給するもの |
|---|---|---|
| **NVD CVE API 2.0** | 差分は `lastModStartDate`（最大120日窓）、全件は `startIndex` ページング | CVE 本体・CVSS・CWE・CPE、および `metrics.ssvcV203`（Vulnrichment の SSVC ミラー）と `cisaExploitAdd`（KEV フラグ） |
| **KEV カタログ** | JSON 全件（約1,700件）を毎回置換 | KEV 掲載・`dateAdded`・`knownRansomwareCampaignUse` |
| **Vulnrichment** | 初回は tarball（約85MB）、以降は GitHub compare API で差分ファイルのみ | SSVC 決定点（`containers.adp[].metrics[].other`） |
| **EPSS** | 日次全件 CSV.gz（約36万件、13:30 UTC 更新） | 30日以内の悪用確率と percentile |

**NVD だけで BOD の3変数がほぼ揃う**（2026-08-20 に実データで確認）。
KEV カタログと Vulnrichment は冗長ではなく、NVD の反映遅れを補正する上書きソースとして働く:

- KEV: カタログが正（NVD は `knownRansomwareCampaignUse` を持たない）
- SSVC: Vulnrichment が正（NVD はそのミラーで、遅れることがある）

### EPSS の役割

EPSS は BOD の4変数**ではない**。存在意義は別のところにある。

CISA の SSVC 付与は全CVEに及ばない。付与されていない CVE は Automatable と Technical Impact を
**自組織で判定する必要があり**、指令はその順序を示していない。EPSS は「今後30日の悪用確率」を
与えるので、未判定 CVE のうちどれを先に人手で見るかを決められる。
これを実装したのが `gold.ssvc_gap_triage` で、本DBの実用上の主目的である。

なお SSVC カバレッジは年によって大きく違う（新しい CVE ほど高い）。
`gold.coverage_stats` が年次別に出すのはそのため。

---

## 使い方

```bash
uv venv --python 3.13
uv pip install -r requirements.txt
uv pip install -e .

# NVD API キー（無料）があると全件ロードが桁で速くなる: 5req/30秒 -> 50req/30秒
export NVD_API_KEY=...

python -m vulndb init       # 全件初期ロード（約38万CVE）
python -m vulndb update     # 差分更新（前回の同期点から再開）
python -m vulndb status     # 件数・カバレッジ・最終取得状況
python -m vulndb query CVE-2024-3400
python -m vulndb triage --limit 25   # SSVC 未付与CVEを対応すべき順に
python -m vulndb export     # Parquet 書き出し
python -m vulndb rebuild    # 再取得せず Bronze から Silver を作り直す
```

疎通確認だけなら NVD を狭い窓に限定できる:

```bash
python -m vulndb init --sources nvd kev epss --pub-start 2026-08-01
```

### テスト

pytest は使わない（リポジトリの慣習に合わせ標準ライブラリのみ）:

```bash
python3 tests/test_bod2604.py
python3 tests/test_parsers.py
```

---

## 構成

メダリオン構成（`talent-mgmt-db` の規約を踏襲）。

```
bronze.*   上流のペイロードをそのまま保持。Silver はここから何度でも作り直せるので、
           パーサのバグで NVD から38万件を取り直す事態にならない。
silver.*   型付け・1CVE1行。ソース間の優先順位はここで解決する。
gold.*     ビュー。BOD 26-04 の判定を行う。毎回再計算されるため入力とズレ得ない。
meta.*     マイグレーション台帳、取得ログ（失敗も記録）、差分同期の再開位置。
```

`gold.cve_bod2604` は資産エクスポージャが未知のため **公開時と内部時の両方**を算出する
（`days_if_exposed` / `days_if_internal`）。資産テーブルが入れば片方を選ぶだけで確定する。

各行には `matrix_row_*`（Table 1 の何行目を適用したか）を持たせている。指令は
「なぜその CVE を先に直したか」を説明できることを求めており、その根拠になる。

### 将来の拡張（Phase 2）

資産インベントリと検出結果を足すと期限が確定する。指令 Phase III が求めるタグ項目は
そのままスキーマになる: 組織／サブ組織、環境（prod/dev）、**エクスポージャ（public/internal）**、
資産種別（server / application / network device）。

---

## 更新の運用

GitHub Actions（`.github/workflows/cyber-vulndb-update.yml`）が日次で `update` を実行する。
DuckDB ファイルは Actions cache で持ち回り、成果物は artifact として保存する。
リポジトリの pre-commit が 500KB 超のファイルを弾くため、**DB は git にコミットしない**。
