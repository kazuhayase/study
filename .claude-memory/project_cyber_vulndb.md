---
name: project-cyber-vulndb
description: Cyber/vulndb (BOD 26-04 脆弱性優先度DB) の構築完了・設計判断・実測性能・ハマりどころ
metadata: 
  node_type: memory
  type: project
  originSessionId: 41df3b55-7289-4580-945a-d0fab356337e
  modified: 2026-08-20T22:33:39.243Z
---

`Cyber/vulndb` — CISA BOD 26-04 対応の脆弱性優先度 DuckDB。2026-08-21 に初版を構築し
master へ push 済み（commit 2975e00）。空ディレクトリからの新規作成。

## BOD 26-04 の要点（2026-06-10 発行、知識カットオフ後）

BOD 22-01(KEV) と 19-02 を置換。CVSS 基準の期限を廃止し、4変数16通りで
3日 / 14日 / 60日 / 次回システム更新時 に分類。KEV 掲載 × Total control の3行は
「3日＋フォレンジック triage」。

- 4変数: Publicly Exposed（**組織側が判定**）/ In the KEV / Automatable / Technical Impact
- 期限の起算日は「KEV 掲載日」と「資産上での検出日」の**早い方**（Appendix A に明記）
- **Table 1 は本文中の PNG 画像**として公開されており HTML の `<table>` ではない。
  `https://www.cisa.gov/sites/default/files/2026-06/BOD_26-04_Table_1_Remediation_Timelines_0.png`
- **cisa.gov は WebFetch を 403 で拒否する。curl にブラウザ UA を付ければ 200**。
  KEV JSON フィードも同様。

## 設計判断（なぜそうしたか）

- **NVD API 2.0 が Vulnrichment SSVC を `metrics.ssvcV203` に同梱**しており、KEV も
  `cisaExploitAdd` で持つ。つまり NVD 1本で BOD の3変数がほぼ揃う。KEV カタログと
  Vulnrichment は冗長ではなく「鮮度・欠損の上書きソース」として併用。
  優先順位は `rebuild.py` のパス実行順で表現している（先に権威ソースを REPLACE、
  後から NVD を IGNORE で穴埋め）
- **SSVC のキー表記が2種類**: NVD は `technicalImpact`、Vulnrichment は `Technical Impact`。
  片方だけ対応するとカバレッジが静かに半減する
- 資産インベントリが無いので Gold は**公開時／内部時の両方**を算出（`days_if_exposed` /
  `days_if_internal`）。`matrix_row_*` を持たせて「なぜその期限か」を説明可能にしている
- **期限は KEV 掲載 CVE しか埋めない**。CVE 公開日で代用しない（指令にその規定が無い）
- EPSS は BOD の4変数ではない。**SSVC 未付与 CVE を手動判定する順序付け**に使う
  （`gold.ssvc_gap_triage`）。これが本DBの実用上の主目的
- マトリクスは `migrations/005_seed_bod2604_matrix.sql` にデータとして保持し、
  `tests/test_bod2604.py` が独立転記した16行と突合。CISA は年度ごとに見直すと明記

## 実測値（2026-08-21）

- 全CVE: 380,688件。NVD 生JSON 全件で 2.08GB、CPE 設定を除くと 1.55GB（CPEは26%）
- Vulnrichment: SSVC 付与は全件ロード後で 176,635件 = **48.6%**（CISA 公表の約45.8%と整合）。
  ただし**新しい CVE ほど高い**（下の年次別を参照）。年次別統計が実用上重要
- Vulnrichment tarball 85MB（git clone は331MB）
- EPSS 日次CSV 約36万件

## 性能のハマりどころ（最重要）

**DuckDB の `executemany` は約1,800行/秒しか出ない。** これで2回踏んだ:

| 対象 | executemany | ファイル経由 |
|---|---|---|
| EPSS 36万行 | 約11分 | `read_csv` に .csv.gz を渡して **0.06秒** |
| `rebuild` 全体 | **77分** | `db.bulk_insert`（JSONL + `read_json`）で **6.7秒** |

読み出しとパースは速い（17万件で計1.5秒）。遅い時は**書き込み側を疑う**。
`db.bulk_insert()` が共通経路。新しい一括投入は必ずこれを通すこと。

## 構造的な不変条件

`TARBALL_BREAKEVEN_FILES` (150) < `COMPARE_FILE_PAGE_LIMIT` (300) を必ず保つ。
GitHub compare API は files を300件で打ち切るため、300件返った応答は切り捨てと区別できない。
閾値が下にあることで、差分パスが切り捨て応答を掴んでカーソルだけ進める
（＝変更を恒久的に取りこぼす）事故が構造的に起きない。

## 全件初期ロード完了（2026-08-20, run 32421602350）

`NVD_API_KEY` は取得済み・GitHub Secrets 登録済み。CI で全件 init が **38分**で成功。

- CVE 総数 **381,322**（Rejected 除く判定対象 363,306）
- SSVC 付与 176,635 = **48.6%**
- KEV 掲載 1,673、うち **SSVC 欠落は 0件**
  → 期限が最も厳しい KEV 群は全て機械判定できる。手動判定が要るのは KEV 外だけ
- DB **373MB**（事前想定の1GBより小さい）、Parquet 79MB
- 日次スケジュール（15:00 UTC = 翌0:00 JST）稼働中。差分更新は実測10秒前後

**年次別 SSVC カバレッジの差が想定以上に大きい**（全体48.6%という単一の数字は実態を隠す）:

```
2024 99.2% / 2025 94.9% / 2026 88.8% / 2023 83.4%
2022 54.2% / 2021 22.9% / 2020 15.2% / 2019 13.6%
```

SSVC の穴はほぼ全て2022年以前。手動判定のバックログは「新しい脆弱性が半分未判定」ではなく
**古い脆弱性の棚卸し**であり、緊急性の質が違う。`gold.coverage_stats` を年次で出す設計にした
判断はここで効いた。

ローカルへ全件を入れるなら init を流し直すより artifact 取得が速い:
`gh run download <run-id> --repo kazuhayase/study -n cyber-vulndb-<run-id> -D Cyber/data/`

## 未了

- Phase 2（資産テーブル）は未着手
- Phase 2（資産テーブル）は未着手。指令 Phase III のタグ項目がそのままスキーマになる:
  組織／サブ組織、環境(prod/dev)、エクスポージャ(public/internal)、資産種別

## ベンダーアドバイザリ収集（AWS/Microsoft/Broadcom/IBM、2026-08-21 Windows機で実装）

BOD 判定(gold)とは無関係の別系統として `bronze.vendor_advisories` / `silver.vendor_advisory`
を追加（migrations 006/007）。**bronze/silver に着地させるところまでがこの実装のスコープ**で、
gold への統合や社内DBとの結合は別途行う想定（意図的に未実装）。

- 4社とも無認証・公開エンドポイントで取得可能と実機確認済み（詳細は `Cyber/CLAUDE.md`）:
  AWS は RSS 丸ごと置換、Microsoft は MSRC CVRF API（`Accept: application/json` 必須 —
  無いと XML が返り `json.loads` が壊れる、一度踏んだ）、Broadcom は `segment:""` で全事業部
  横断のページング API、IBM は非公式の製品名検索API（全件／日付範囲取得は不可、
  `config.IBM_PRODUCT_SEARCH_TERMS` に無い製品は取りこぼす — カバレッジの構造的limit）
- **IBM の日次更新コストが大きい**: 検索語15件 × 最大2,000件/24MBを毎回フルダウンロード。
  実測で init 完了まで約27分（他3社は数分以内）。CI の日次実行時間が気になる場合は
  `IBM_PRODUCT_SEARCH_TERMS` を絞るのが手軽な対処
- 実データでの検証結果（2026-08-21時点、smoketest.duckdb）: aws 85件、broadcom 4,178件、
  ibm 5,510件、microsoft（直近24ヶ月）25,430件、CVE紐付けビュー `silver.vendor_advisory_cve`
  で53,979組
- テストは実データ由来のフィクスチャ（`tests/fixtures/{aws,msrc,broadcom,ibm}_*_sample.json`）
  で `tests/test_parsers.py` に追加済み。`.venv` 無しでも動く（transform.py は標準ライブラリ
  のみで duckdb 非依存）

### 2026-08-25: フル init 完走 + http.py の耐障害性を大幅強化

このWindows機のネットワークが著しく不安定な晩で、NVD全件initが**当初の見積り(数十分)に対し
数時間~でも完走しない**という事態になり、根本原因を3つ特定・修正した:

1. **`http.client.IncompleteRead` が retry 対象の例外集合から漏れていた**
   (`urllib.error.URLError, TimeoutError, ConnectionError` のみを捕捉、`IncompleteRead` は
   `http.client.HTTPException` の別系統)。接続が転送途中で切られる事故がこのネットワークでは
   頻発し、これが最大の原因だった。`http.py` の `_fetch` に `http.client.HTTPException` を追加
2. **JSON パースがリトライループの外側にあった**(`get_json` = `json.loads(get_bytes(...))`)。
   転送自体は「成功」扱いなのに中身が truncated な JSON になるケースがあり(200 OK・期待サイズ
   っぽい bytes 数でも中身が壊れている実例を確認)、`json.JSONDecodeError` が無防備に伝播して
   `sync()` 全体がクラッシュしていた。`http._fetch_json` を新設し、JSON パースもリトライ対象に
   含めた(`get_json`/`post_json` 共通化)
3. **`HTTP_TIMEOUT` が120秒と長すぎた**。ソケットの無応答タイムアウト(転送全体の制限ではない)
   なので、20秒に短縮しても大きい転送は壊れない。この夜のネットワークは「繋がらない」より
   「繋がるが途中で無応答になる」ことが多く、120秒だと1回の詰まりの検知だけで2分溶ける計算に
   なっていた。20秒に短縮して体感速度が大幅改善

さらに **NVD に startIndex のページ単位レジューム機能を追加**(`meta.sync_state` に
`nvd_init_progress` として逐次保存、完走時に削除)。**IBM にも語単位のレジューム機能を追加**
(`meta.sync_state` に `ibm_term_done:<term>` として語ごとに記録、`init` は既に成功済みの語を
スキップ、`update` は毎回全語を舐める)。どちらも「中断しても振り出しに戻らない」ことが目的。

**IBM 検索語の追加分割**(2026-08-25、`config.IBM_PRODUCT_SEARCH_TERMS`):
`WebSphere` も 2,000件キャップ+約24MBで頻繁に失敗したため Db2 と同様に分割
(`IBM WebSphere`, `WebSphere Application Server Liberty/Network Deployment/Portal/Commerce/
for z/OS` 等)。ユーザーの社内脆弱性管理台帳の検索キーワード一覧(職場情報のためリポジトリには
未収録)から `IBM Data Server Client`・`IBM InfoSphere Data Replication`・
`WebSphere Application Server` も追加。**IBM API の同一クエリが再現性なく毎回サイズが変わる**
(例: "Db2 Warehouse" が3.6MB→21MBと変動)ことを確認済み — 分割は緩和策であり根治ではない
- **CVE ID の `~`(OR)構文は数値レンジではない**ことを実機検証で確定(`CVE-2026-00000~
  CVE-2026-00200` は0件、実在CVE2つの範囲指定も期待した範囲展開はされず3件のみ)。NVD由来の
  IBM起点CVE(`source_identifier='psirt@us.ibm.com'`、8,407件)をバッチ`~`検索する代替案は
  技術的に成立する(150~200件/バッチが安全、300件でHTTP 414)が、8,407件を捌くには
  約40~55リクエスト必要で今回は不採用。ユーザーは「キーワード方式を継続」と判断
- 全件 init 完走実績(2026-08-25、このWindows機、`cyber.duckdb`、後続のマージ後の最終値):
  silver.cve 382,270件、silver.kev 1,675件、silver.ssvc 177,756件、
  silver.vendor_advisory 36,813件(aws 88 / microsoft 25,628 / broadcom 4,180 / ibm 6,917)

### `Cyber/` は git 完全対象外に(2026-08-25)

**大きな方針転換: `Cyber/`(本ファイルの対象)はコード・データ・CSV出力すべて git 管理外に
なった。private リポへの分離も一度実施したが、ユーザー判断で撤回・削除。** 詳細な手順・
残課題(**`.github/workflows/cyber-vulndb-update.yml` が Cyber/ 消失により次回実行で失敗する
見込み、対応要**)は [[project-repo-setup]] の「Cyber/ は git 完全対象外化」節を参照。
今後 vulndb の作業はこの Windows 機のローカルディスク上でのみ完結する前提になる。

**バックアップ方針、2026-08-27に確定**: プログラム本体(`src/`・`migrations/`・`tests/`・
`README.md`・`CLAUDE.md`・`pyproject.toml`・`requirements.txt`、`.venv`とDBは除外)を
`E:\hayase\src\Cyber\`へ手動コピー。GitHubには一切残っていないコードの唯一のバックアップ
がこれになる(現状は手動・都度コピー、自動化は未対応)。Snowflakeアップロード用CSVの置き場は
`E:\hayase\export-snowflake\`。両フォルダの説明メモを`E:\hayase\README.md`として作成済み。
なお`data\cyber.duckdb`は2026-08-27時点で**5.76GB**まで肥大化(2026-08-20時点373MBから急増)
しており、DuckDBの未回収領域(繰り返しのUPDATE/DELETEによる断片化)が疑われる —
`VACUUM`実行での検証は未実施(ユーザーはプログラム本体の保存を優先し、DB側は今回は保留)。

### 2026-08-25 続き: IBM CVEバッチフォールバック実装・カバレッジ検証・CSVエクスポート実装

**IBM に自動フォールバック機構を実装**(`sources/ibm.py`)。製品名検索語が5回リトライ後も
失敗した場合、`silver.cve WHERE source_identifier='psirt@us.ibm.com' AND description_en
ILIKE '%<語>%'` で候補CVEを抽出し、`config.IBM_CVE_BATCH_SIZE`(150件)ずつ `~` 区切りの
CVE ID バッチクエリでリトライする(`_fetch_cve_batch_fallback`)。`silver.cve` 未構築時
(初回initの最中など)は候補0件で従来通りスキップにフォールバックする設計。

**カバレッジ検証(重要な発見)**: NVD由来のIBM起点CVE 8,407件 vs 実際に収集できたCVE 8,943件
(重複はvendor='ibm'のupsert込み)を突き合わせたところ、**6,695件が未収集**と判明。内訳:
- 1,012件: Rejected CVE(無効採番、実害なし)
- 大半: `IBM_PRODUCT_SEARCH_TERMS` に**存在しない製品**(TRIRIGA, Rational, IBM i, Curam,
  Domino, Content Navigator, Concert, Business Process Manager, Sametime, Security Identity
  Manager/Verify Access, DataPower Gateway, API Connect, Aspera Faspex, Connections,
  Robotic Process Automation, Langflow OSS 等多数) — 未追加のまま
- **【重要】「ちょうど2,000件で成功」した語も truncation していた**: Maximo(160件欠落)・
  QRadar・WebSphere Portal(103件)・Sterling・Security Guardium(102件)・Tivoli系が該当。
  「失敗した語だけ分割すればいい」という前提が誤りで、**2,000件ちょうどはキャップ到達のサイン**
  という教訓。欠落は全年代にほぼ均等分布(2026年ですら324件欠落)しており、
  「古いブレティンが未索引」という説は否定された(純粋にキーワードカバレッジの問題)
- 対応: `QRadar Suite/Log Manager/Network Insights/Vulnerability Manager/Risk Manager`、
  `Maximo Application Suite/Manage/Monitor/Health/Predict`、
  `Tivoli Storage Manager/Key Lifecycle Manager`、`Guardium Data Encryption`、
  `Sterling File Gateway/Connect`、`WebSphere Portal Server` を追加(元の広い語も保持)。
  検索語は最終的に**52語**(重複なし)

**IBM `update` を CVE指定ベースに再設計・実装済み(2026-08-26)**: `sources/ibm.py` を
`_sync_init`(既存の52語フルスイープ、失敗時フォールバック・語単位レジューム維持)と
`_sync_update`(新規)に分離。`update` はもう52語を舐めない — `silver.cve WHERE
source_identifier='psirt@us.ibm.com' AND greatest(published, last_modified) > <前回カーソル>`
で新規/更新CVEを特定し、`ibm_update_since` カーソル(`meta.sync_state`)からの差分だけを
CVEバッチ(`~`区切り、150件/バッチ、`_fetch_cve_id_batches` に共通化)で取得する。
カーソル未設定時(この再設計以前に構築したDB)は現在時刻をベースラインとして設定するだけで
何も取得しない(過去分は直近の `init` が既にカバー済みという前提)。
実測(2026-08-26、カーソルを2026-08-20にセットしてテスト): 203件の新規/更新CVE→2バッチ→
377件のアドバイザリ取得、所要時間は数十秒(旧方式の52語フルスイープは約27分)。
**この再設計により「`update` は`init`用の語単位レジュームが効かない」問題も解消**
(そもそも語をスイープしないため無関係になった)。
なお `update` はNVD側にまだ存在しないブランドの新規参入は拾えない(そのブランドの最初のCVEが
NVDに載るまでは見えない)ため、**`init` の全語スイープは今後も定期的に(手動で)回す価値がある**。

**Snowflake向けCSVエクスポートを実装**(`src/vulndb/export_snowflake.py`、
`python -m vulndb export-snowflake --what all|nvd|kev|vulnrichment|vendor`)。
ユーザー提供の社内仕様書(VulnMgmtデータ取得スクリプト仕様書)に準拠、UTF-8 BOMなし・LF改行・
NULL=空文字・複数値はパイプ区切り(vendor広告のCVE_IDのみ仕様通りLF区切り)を実装・実データで
検証済み(NVD 382,270行/487MB、KEV 1,674行、Vulnrichment 174,420行、vendor 36,813行)。
**意図的に空欄にした項目**: SSVC_DECISION(CISAの正式決定木は3変数だけでは導出不可のため
推測しない)、ENRICHED_CWE/ENRICHED_CPE(該当するCISA-ADPコンテナのパスを確認できず)、
vendor広告側の PRODUCT_NAME/SEARCH_STRING/VERSION/TARGET_PRODUCT/BASE_SCORE等
(silver.vendor_advisory に対応カラムが無い)。**このスクリプト自体もCyber/配下でgit対象外**。

**2つのDBファイルをマージ済み**: `cyber_others.duckdb`(ベンダー広告を並行取得した際の別ファイル)
の bronze 4テーブルを `cyber.duckdb` に `ATTACH` 経由でコピーし、`cyber_others.duckdb` は削除。
以後は `cyber.duckdb` 1本に統一。

### 2026-08-26: 全ソース update 実行・DB統合時の見落としを修正

前回セッションで `cyber_others.duckdb`(ベンダー広告を並行取得した際の別ファイル)の
bronze 4テーブルを `cyber.duckdb` にATTACH経由でマージしたが、**`meta.sync_state`
(カーソル)と `meta.fetch_log` のマージを忘れていた**(該当ファイルは既に削除済みで
復元不可)。影響: Microsoft(`CurrentReleaseDate`)・Broadcom(`notificationId`)の
カーソルが消え、次回 `update` はこの2ソースだけ「軽い再init相当」(全期間/全ページ再走査)
になった。実害は「無駄な帯域」のみで壊れてはおらず、その回の実行後は正しく再設定された。
**教訓**: 複数DBファイルをATTACH+マージする際は bronze だけでなく `meta.sync_state`・
`meta.fetch_log` も忘れずマージすること。

NVD・KEV・EPSS・Vulnrichment・AWS・Microsoft・Broadcom の7ソースで `update` を実行
(自動リトライループ、4回の試行でネットワーク瞬断=`getaddrinfo failed`を乗り越えて完走)。
最終値: silver.cve 382,999(+729)・kev 1,676・ssvc 178,314・epss_current 364,277・
vendor_advisory 36,852。NVDの差分取得(`lastModStartDate`/`EndDate`カーソル)が正しく
機能していることも実地で確認(2026-08-25〜26の窓で28件取得)。

### 2026-08-26 続き: IBM WebUI分析でCVEインデックスAPIを発見・カバレッジ問題を構造的に解決

ユーザー指示でIBMのブレティン一覧ページ(`ibm.com/support/pages/bulletin`)をブラウザで開き、
ネットワーク通信を解析(実機ブラウザでの読み込み後、`javascript_tool`でfetch実行して
レスポンス構造を確認)。**無認証・無登録の新エンドポイントを発見**:
`securityapp/api/site/datalist?offset=0&limit=1000`(既存の`securityapp/api/search`と
同じ製品ドロップダウン用API)。`offset`/`limit`は検索APIと同様に無視されるが、レスポンスの
`results.cve_ids`が**IBMのセキュリティ・ブレティンDBが把握する全CVE ID(23,265件、正規化後)**
になっている — ページ本文の「A full list of all CVEs affecting IBM products can be found in
our CVE Database」の実体。**プレーンなcurl(cookie無し)でも200が返る**ことを確認済み
(ブレティン一覧ページ本体はbot対策で描画されないが、このAPI自体はcurlで直接叩ける)。

**重要**: `psirt@us.ibm.com`起点でNVDに載るCVEだけでなく、IBM製品に**バンドルされた
サードパーティCVE**(例: watsonxに同梱されたGoogle Chromeの脆弱性)も含む。旧方式(NVD由来の
IBM起点CVEをカーソル追跡)では原理的に見えない集合であり、既存の52検索語スイープの
「未収録製品は取りこぼす」問題とは別種の構造的カバレッジ穴だった。

**実装**(`sources/ibm.py`・`config.py`): `_fetch_known_cve_ids()`でdatalist APIから全CVE ID
取得・正規化(`^CVE-\d{4}-\d+$`でフィルタ、"MSC-"内部ID等5件のゴミを除去)、
`_sync_cve_gap_fill()`で`silver.vendor_advisory_cve WHERE vendor='ibm'`との差分を
既存の`_fetch_cve_id_batches`(150件/バッチ)で取得。**init・updateの両方の最後に必ず実行**
(52語スイープ・NVDカーソル方式は当面併用 — 前者は新規ブランドの一次発見、後者は既知CVEの
改訂検知に引き続き必要なため)。テスト(`test_parsers.py`・`test_bod2604.py`)は無影響で通過。

**実行結果**(2026-08-26、このWindows機、`cyber.duckdb`): 未収集14,314件を検出、96バッチ中
93バッチ成功・39,669件のアドバイザリを新規取り込み(4バッチはこの機体の既知のネットワーク
不安定=`IncompleteRead`で失敗し次回updateへ持ち越し、状態保持不要で自動再検出される設計)。
IBM広告アドバイザリは6,917→**15,985件**、紐付きCVE(distinct)は8,988→**22,639件**に増加。
残った4バッチ分は翌日(2026-08-27)の全ソース`update`で**実地に自動再検出・全6バッチ成功**を確認済み
(設計どおりの自己修復が実証された)。

その後 `export-snowflake --what all` を再実行し、増分を含む最新4ファイルを
`data/export-snowflake/` に出力済み: cve_updated(NVD) 382,999行/488MB・
known_exploited_vulnerabilities(KEV) 1,676行・vulnrichment 175,398行・
**vendor_hp(ベンダー広告) 45,920行**(IBMギャップフィル分を反映して増加)。

### 2026-08-27: Snowflakeエクスポートに差分(incremental)モードを実装、KEVの差分検出不能問題を修正

ユーザーが「本日は全件アップロード、それ以降は差分更新にしたい」と要望。`export_snowflake.py`は
従来フル出力しか無かった(`export_all`)ため、差分モードを新規実装。

**設計**: `meta.sync_state`に`export_snowflake_<name>`(nvd/kev/vulnrichment/vendor)という
既存sync源のカーソル(`nvd`/`kev`等の裸キー)と衝突しない専用キーでカーソルを保持。
NVD/ベンダー広告は各行のbronzeテーブル(`bronze.nvd_cve`/`bronze.vendor_advisories`)の
`fetched_at`(REPLACE時にDEFAULT now()が効く=「前回syncで実際に触られた行」を意味する)で
直接フィルタ。Vulnrichmentはsilverが毎回全rebuildされ`fetched_at`を持たないため、
`bronze.vulnrichment.fetched_at`で該当CVE IDを絞り込んでからsilver.ssvcを引く間接フィルタ。
`cli.py export-snowflake --mode full|incremental`(デフォルトfull)。**full実行時も対象カーソルを
今回の実行時刻へ起点セット**するため、初回フル→以降incrementalの運用がそのまま繋がる
(`export_full`/`export_incremental`、内部は同じループ構造)。

**踏んだ事故**: KEV/Vulnrichment/ベンダー広告の3ファイルは**日付のみのファイル名**
(`vendor_hp_20260827.csv`)だったため、動作確認で同日中に2回実行した際に**本物のフルデータが
0件の差分結果で上書きされるデータ損失事故**が実際に発生(NVDのみ時刻まで含む命名だったため無事)。
即座に3ファイルとも時刻まで含む命名(`_HHMMSS`)に修正し、正しいデータで復元。
**教訓**: 同日複数回実行があり得るエクスポート/バックアップ処理は、日付のみのファイル名を
絶対に使わないこと。

**KEVの差分検出が実質無効化されていた問題**: `kev.py`が毎回カタログ全体を
`DELETE`→丸ごと再`INSERT`する設計だったため、内容不変の行even含め`fetched_at`が
全件更新されてしまい、「`since`でフィルタ」が事実上ずっと全件ヒットしていた
(ユーザー自身が「KEVは全件取得としてもSnowflakeには差分更新とできないか」と指摘して発覚)。
`kev.py`を修正: 既存`bronze.kev`と新規カタログをcve_id単位で`raw_json`比較
(`sort_keys=True`でキー順序ゆらぎを無視)し、**内容が実際に変わった行だけ**INSERT、
削除も差集合分だけDELETE(以前は全削除)。2回連続実行で実地検証: 1回目は書式統一のため
全1,682件が"変更"扱い、2回目は**「0 changed/new, 0 removed」**と正しく差分ゼロを確認。

**バックグラウンドタスクの出力バッファリング問題**(この日の副次的な教訓): Windows上で
Pythonの標準出力をファイルにリダイレクトすると、非TTYのため**プロセス終了までフルバッファされ
途中経過が一切見えない**。加えてDuckDBは書き込み中ファイルへの同時読み取り接続も拒否するため、
DB越しの進捗確認も不可。対策: 長時間バックグラウンド実行時は`python -u`(アンバッファ)を
付けること。ただしexport系は行ごとにprintしない設計のため`-u`でも完了まで無出力なのは正常。

**プログラム本体のバックアップ**: `E:\hayase\src\Cyber\`(`.venv`とDB除外、GitHubに一切
残っていないコードの唯一のバックアップ)。Snowflake向けCSVは`E:\hayase\export-snowflake\`。
両フォルダの説明は`E:\hayase\README.md`。`cyber.duckdb`が5.76GBまで肥大化(2026-08-20時点
373MBから急増、DuckDBの未回収領域の疑いあり、`VACUUM`検証は未実施)。

### 2026-08-27 続き: ユーザー提供の参照実装(社内スクリプト)とNVD exportを突合・3件のバグを修正

ユーザーが現行運用中のPowerShellスクリプト(`V3_nagasawa.ps1`、社内デスクトップ上、APIキーは
本文に含めず参照)を提示し、`export_snowflake.py`のNVD出力と突合。**カラム構成(CVE_ID〜
Description、20列)は完全一致** — この社内仕様書に基づく実装で相互に参照関係にあると確認。

**PS1側の重大な欠陥(こちらのバグではないが記録)**: `Invoke-RestMethod`を1回呼ぶだけで
NVD APIのページング(`resultsPerPage`/`startIndex`)を一切行っていない。NVD APIは1リクエスト
最大2,000件までしか返さないため、**対象期間の更新件数が2,000件を超えると超過分が黙って
欠落する**。直近の弊方nvd.pyのログで実際に「2,859件」(2日分)という、この閾値を超える
実例が観測されている。ユーザーへの報告のみ、PS1側の修正はスコープ外。

**この突合で発覚した`export_snowflake.py`側のバグ3件を修正**(`_affected_products`に統合、
旧`_nvd_cpes`は削除):
1. `cpeMatch`の`vulnerable:false`エントリ(脆弱性の前提条件であり対象製品ではない)を
   除外していなかった → Vendor/Affected_Productsに無関係な製品が混入していた。生成時
   (export関数内)で除外するよう修正(検索時除外との比較検討の結果、生JSONは`raw_json`に
   無加工で残るためどちらでもデータは失われないが、Snowflake側の全クエリに除外ロジックを
   要求する設計は壊れやすいと判断しユーザーも同意)
2. `versionStartIncluding`/`versionEndExcluding`等のバージョン範囲を解決していなかった
   → 範囲指定CVEのAffected_Productsが常に無意味な`*`表示になっていた。PS1と同じ
   `(>= X AND < Y)`形式の範囲文字列を組み立てるよう修正
3. CPE列を`f"cpe:2.3:a:{vendor}:{product}:{version}"`で決め打ち再構築していた
   → 実際のpart種別(`o`=OS・`h`=ハードウェア等)を無視して`a`固定になり、かつバージョン
   範囲も欠落していた。生の`criteria`文字列をそのまま使うよう修正(PS1と同じアプローチ)

実データ(CVE-2001-0191、cpeMatch 2件中vulnerable:falseが1件・バージョン範囲あり)で
3点とも意図通り動作することを確認済み。`tests/test_parsers.py`は無影響で通過。

### 2026-08-28: IBMバッチクエリの「静かな打ち切り」を発見・修正、IBM収集量が2.3倍に

**ユーザーが実物のブレティンURL(node 7284532, IBM Spectrum Control / CVE-2024-40094)を挙げて
「これは取れているか」と質問したのが発端**。DBには無く、調査で構造的な欠陥が3つ判明した。

**根本原因: IBM検索APIの2,000件キャップによる静かな打ち切り**。`items_count`は返却件数と同値
(実測確認)で「本当は何件あるか」を返さないため、**ちょうど2,000件=打ち切りのサイン**が唯一の
検出手段。1CVEあたりのブレティン数が想像以上に多く(CVE-2023-44487は**236件**、CVE-2022-22965
は58件、CVE-2024-40094は37件)、150CVEをまとめると平均13件で上限に達する。過去ログに
`batch 1/6 (150 CVEs) -> 2000 advisorie(s)`という記録が実際に残っていた。
さらに検証中、この応答が**78MB受信してもIncompleteRead**になることも判明(IBMレコードはHTML
本文を丸ごと含むため上限まで詰まると80MB近く)。

**実装した対策(すべてテスト付き)**:
1. **打ち切り検出＋再帰分割**(`_fetch_ids_halving`): 上限ちょうどなら半分ずつに分けて再取得
2. **失敗時も分割**(深さ2まで=1バッチ最大4クエリ): 巨大応答のタイムアウト救済。回線ダウン時の
   増殖を防ぐため深さ制限。「失敗は回線ダウンかサイズ超過か区別できない」が両者は逆の対処を
   要求する、という判断
3. **世代管理**(`_CURRENT_GENERATION`, `ibm_gapfill_generation`): 差分ロジックは「1件でもあれば
   取得済み」としか判断できず**「一部だけ取得済み」を検知できない**ため、世代番号で一度限りの
   全件再取得を強制。完了後は自動で軽い差分モードに戻る
4. **失敗CVEの個別キュー**(`ibm_resweep_pending`): 当初「最初の失敗以降は進捗を記録しない」
   設計にしたが、**23,330件規模では1件の失敗が数時間分の進捗を無効化する**と実行中に判明
   (バッチ1/156で1件失敗→カーソルが最後まで保存されない)。失敗CVEだけを正確に記録して次回
   リトライする方式に変更。カーソルは常に前進する
5. **DNS断サーキットブレーカー**(`http._is_network_down`/`_wait_for_network`): 夜間実行で
   **リトライの89%(1,205/1,352)がgetaddrinfo失敗=回線断**と判明。43バッチを死んだ回線に投げ
   続けて6,380件を失敗記録した。DNS断を検知したら30秒ごとに復旧を確認しながら最大30分待ち、
   復旧したらリトライ回数を消費せず再開する
6. **サイズ比例タイムアウト**(`IBM_TIMEOUT_PER_CVE=0.5`): タイムアウト率がバッチサイズと明確に
   相関(100+CVEで0.63〜1.13回/クエリ、20-49CVEで0.05回)。サーバーが80MBのJSONを組み立てる
   時間が20秒を超えるため。`HTTP_TIMEOUT`も20→30秒(DNS断を別処理にしたので無応答=輻輳の
   可能性が高くなったため)
7. **バックオフを2/4/8/16→2/16/16/16に**(`http.RETRY_BACKOFF`、ユーザー提案): 数式から明示的
   な数列に変更。**これは検証中の仮説**であり確定した結論ではない — 旧数式を否定した根拠
   (成功率10.4%→7.3%→3.1%→1.6%の低下)は、この階段がもう扱わないDNS断のデータだったため
8. **ETA表示**(`_progress`、ユーザー提案): 「アドバイザリ件数から時間予測できないか」という
   提案から実装。1バッチあたりの件数は299〜3,872件(中央値1,024)と13倍の開きがあるため、
   バッチ数より件数ベースのスループットの方が実態を反映する。なお**取得件数(生)と保存件数
   (重複排除後)は5〜6倍違う**(1ブレティンが該当CVEごとに重複して返るため)ので表示を区別

**結果**: IBMブレティン 15,985→**36,325件(2.3倍)**、IBM紐付きCVE 22,639→23,347件、
ベンダー広告計 46,605→66,396件。**node 7284532は取得済みに、CVE-2024-40094は13→33件**。
世代フラグ確定・リトライ待ち0件で、以降は軽い差分モードに戻る。

**新規テスト**: `tests/test_ibm_batching.py`(打ち切り検出・分割・重複排除・失敗の個別記録)、
`tests/test_http_outage.py`(回線断の待機・復旧・ばたつき・タイムアウトの誤検出防止)。
実装過程で実際に2件のバグをテストが捕捉した(分割時の重複でメモリ2.5倍膨張、進捗の無効化)。

### 2026-08-31: DNS断ハンドリングの実装漏れを修正、Snowflake向け4ファイルを再生成・完了

**`download()`にサーキットブレーカーが入っていなかった**: 2026-08-27にDNS断対応を実装した際、
`http._fetch`にだけ適用し、tarball取得用の別経路`http.download()`に入れ忘れていた。
2026-08-31の全ソース`update`で瞬断が起き、**`_fetch`を通る7ソースは乗り越えたのに、
`download()`を使う唯一のソースであるvulnrichmentだけが落ちた**(しかも`cmd_update`が
exit 1を返すため`&&`連鎖が止まり、後続のエクスポートも実行されなかった)。
`download()`にも同じ`_is_network_down`/`_wait_for_network`を適用し、
`tests/test_http_outage.py`に回帰テストを追加。**教訓: 横断的な耐障害性を足すときは、
同種の処理経路がほかにないか必ず確認すること**(この場合HTTP取得経路が2つあった)。

**Snowflake向けフルエクスポート完了**(`*_20260831_010918.csv`、DB件数と4ファイルすべて一致を
確認済み): NVD 384,678行/498.60MB・KEV 1,685行・vulnrichment 177,002行・
**vendor_hp 66,716行/15.51MB**。8/27比でベンダー広告が+20,111行(IBM打ち切り修正の反映)。
`--mode full`実行により差分用カーソルも再設定済みで、次回以降は`--mode incremental`が使える。
なお2026-08-28に中断した`*_20260828_030848.csv`は削除済み。

### 2026-08-31 続き: DB肥大化の原因究明・エクスポート列の大幅な拡充

**Snowflakeへのアップロードは未実施のまま終了**(時間切れ)。ファイルは完成済み。

#### DuckDB肥大化 — 原因は DuckDB ではなく `rebuild` の作り方だった

`cyber.duckdb` が 373MB→5.88GB(約16倍)になった件を調査。**`rebuild_all()` が Silver 全テーブルを
`DELETE` してから全件再投入するが、DuckDB の `DELETE` はファイル内の領域を解放しない**ため、
rebuild 1回ごとに死んだ世代が積み上がっていた。silver.* が実行数の **13〜20倍**を占有し、
主キーで upsert するだけの bronze.* は 1.0x で健全 — この差が原因の切り分けになった。
`CHECKPOINT` では縮まない(実測確認)。

対策として **`python -m vulndb compact` を実装**(`db.compact()`)。メモリDB経由で
元を READ_ONLY のまま ATTACH し `COPY FROM DATABASE` で新ファイルへ複写、
**全テーブルの行数とビュー集合を突合してから差し替え**、差し替え後に再オープン確認。
実測 5.88GB→2.95GB(2.93GB回収)を49秒。冪等。既定で `.bak` を残す(`--no-backup` あり)。
**月1回程度の実行が必要**(圧縮しても rebuild のたびにまた積み上がる)。
`Cyber/CLAUDE.md` に節を追加済み。

**「DuckDBをやめるか」も検討したが継続**と判断。Bronze に生JSONを持つ価値は
「パーサーを直したら再取得なしで作り直せる」ことで、この日だけで NVD CSV を3回・
vendor_hp CSV を5回作り直しており、生JSONが無ければ都度数時間の再取得が必要だった。
Parquet化は肥大化が原理的に起きなくなるので筋が良く、BACKLOG に設計メモとして記録。

#### vendor_hp の空欄を実測ベースで埋めた(ユーザーの指摘が起点)

**ユーザーの指摘で自分の誤りが2件見つかった**:
1. 「IBMはCVSSを提供していない」→ **誤り**。`field_vulnerability_details` の HTMLコメント内に
   `cvedetailsstart{...}cvedetailsend` という埋め込みJSONがあり `score`/`vector` を持つ
2. 「ENRICHED_CWE/CPE のパスが見つからない」→ **調査不足**。CISA-ADPコンテナの
   `problemTypes[].descriptions[].cweId` と `affected[].cpes[]` に存在した

実装した項目と充足率(すべて 0% からの改善):
- **Microsoft PRODUCT_NAME 100%**: CVRF文書の `ProductTree.FullProductName` から
  ProductID→製品名を解決(**migration 008** で `bronze.msrc_product` 追加、7,486件)。
  `init --sources microsoft` で160リリース分を再取得して投入
- **CPE列を新設(22→23列、末尾追加)**: Microsoft 99%。**NVDのCPEとは冗長でない** —
  NVD は上流プロジェクトを、MSRC は同梱する Microsoft 製品を指す
  (CVE-2022-2289: NVD `a:vim:vim` vs MSRC `a:microsoft:cm1_vim_9.0.0050-1`)
- **IBM VERSION 67%**: `field_affected_products` のHTML表から。**列位置ではなくヘッダ名で
  版数列を特定**(`Affected Product(s) | APAR(s) | Version(s)` のように3列目に来る形があり、
  位置決め打ちだと APAR 番号を版数として出力してしまう)。セル内に入れ子タグがあるため
  `html.parser.HTMLParser` を使用。製品名と版数が同一セルの表は末尾の版数を抽出
- **NVDによるスコア補完**: IBM 46→**98%**、Microsoft 80→**99%**、Broadcom 0→**48%**、
  AWS 0→**98%**。ベンダーがスコアを出していない行に限り NVD の CVSS を入れ、
  **`REMARKS` に出典を記録**(`BASE_SCORE and CVSS from NVD; vendor published none`)。
  `silver.cve` ではなく生JSONから取得 — silver は v3.1/v4.0 しか持たず**11.5万件を取りこぼす**、
  かつ `export_nvd` と同じ `_nvd_cvss` を使うことで同一CVEが2ファイルで違うスコアを示す事故を防ぐ
- Broadcom PRODUCT_NAME 77→88%(USN形式タイトルから)、Microsoft UPDATED_DATE 0→100%
  (`ReleaseDate` はほぼ全件ゼロ日付 `0001-01-01`、実際の日付は `RevisionHistory` にある)
- vulnrichment の ENRICHED_CWE 20.3% / ENRICHED_CPE 11.4%
- ついでに vulnrichment エクスポートの KEV 判定を **17.7万回のSQL→セット照合**に(性能)

**埋まらないと確定した項目**(全ギャップを実測調査、`Cyber/BACKLOG.md` に根拠付きで記録):
Broadcom の52%は**CVE IDが1件も無い**広告で照合キー自体が無い / IBM BASE_SCORE の33%は
「Refer to the security bulletin(s)」という参照専用広告 / Microsoft の20%は Chromium 系で
Google の評価に委ねている / Broadcom は CVSS 項目自体が API に無い。

**AWS対応は見送り**(BACKLOG に記録)。公開サービス名リスト(認証不要、195件)を見つけたが
カバー率31%が上限で、残りは AWS が公開する OSS/SDK。NVD の CPE の方が網羅的だった。
ユーザー提供の資産リストと照合したところ AWS 該当は僅少と判明(**資産リストの内容は職場情報のため
公開リポジトリには記載しない**。`Cyber/BACKLOG.md` 側にのみ数値あり)。

**`Cyber/BACKLOG.md` を新規作成**。「やらないと決めたこと」を根拠と再検討条件つきで残す方針。

**資産テーブル(Phase 2)は当面作らない方針**とユーザーが明言。この PC には社内データを
安全にインポートできず**書き出しのみ可能**なため。状況が変われば再検討。
SSVC_DECISION はこれが前提なので、併せて保留。

### 次回(2026-09-01)の予定

1. **外部からの情報取得**(全ソース `update`)
2. **差分ファイル作成**: `python -m vulndb export-snowflake --what all --mode incremental`
   (今日の `--mode full` でカーソルは各ファイルの出力時刻に設定済み)
3. **Snowflake へ投入**: 今日作った4ファイル(下記)＋明日の差分ファイル

今日作成済みでアップロード待ちのファイル(`Cyber/data/export-snowflake/`、全て検証済み):
- `cve_updated_20260831_010918.csv` 384,678行 / 498.60MB / 20列
- `known_exploited_vulnerabilities_20260831_010918.csv` 1,685行 / 0.92MB / 11列
- `vulnrichment_20260831_020756.csv` 177,002行 / 10.65MB / 8列
- `vendor_hp_20260831_071808.csv` 66,721行 / 53.31MB / **23列**

**投入前に必ず確認すること**:
- **`vendor_hp` が 22→23列**(末尾に `CPE`)。**Snowflake 側の取り込み定義に列追加が必要**
- 引用符内に改行を含むため**物理行数とレコード数が一致しない**
  (`FIELD_OPTIONALLY_ENCLOSED_BY = '"'` が必要)。取り込み後に上記の行数と突合すること
- CVE_ID 単位の**置き換え(REPLACE/UPSERT)**になっているか。追加(INSERT)方式だと重複する

**未了**: `E:\hayase\src\Cyber\` へのバックアップ(USB取り外し中のため次回接続時に実施)。
`compact` / BACKLOG.md / 今回の export 改修が未反映。

### 2026-09-01: 全ソースupdate＋差分エクスポート、Broadcom の CVE_ID を 48%→81% に回収

#### 差分エクスポートの運用が初めて回った

朝に全ソース `update`(8ソース全て成功。前日DNS断で落ちた vulnrichment も `download()` 修正が効いて完走)
→ `export-snowflake --what all --mode incremental`。**498MB→305KB** と差分が正しく効いた
(NVD 364行 / KEV 2行 / vulnrichment 386行 / vendor_hp 6行)。**ユーザーはこの差分を取り込み済み**。

#### Broadcom: アドバイザリページを取得して CVE_ID を回収

`affectedCve` が空の広告が 2,199 件(4,217中)。値は空文字・`N/A`・`None`・`Multiple`・
**`See CVE list in advisory`**(568件、Broadcom自身がページを見よと書いている)。

実装(**migration 009** で `bronze.broadcom_advisory_page` 追加、HTMLを原文保存):
- タイトルからのCVE抽出も追加(+162件、ネットワーク不要)
- ページ取得 1,475件成功 / 724件はログイン必須。`status` 列で区別し、**login は次回リトライしない**
  (アカウントが要るので何度試しても同じ)
- rebuild で silver へマージ。**`affectedCve` があればそちらを優先**
  (ページスキャンは関連記事欄のCVEも拾うため、Broadcomが明示した対象CVEを上位に置く)

**結果: CVE_IDあり 2,018(48%) → 3,410(81%)、広告×CVE 64,883組、ユニークCVE 14,834。**

**踏んだバグ(重要な教訓)**: ログインページ判定を本文中の `/c/portal/login` で行ったが、
**この文字列は全ページのナビゲーションに存在**し、724件のログインページが「CVE 0件の正常な広告」
として保存された。**HTTP 200 で返る**ためステータスでも気づけない。
サイズ分布の不自然な二極化(63KB台 724件 / 108KB超 1,475件)から発覚。
`<title>` が完全な判別材料(`Home - Broadcom support portal` = ログイン、
`Support Content Notification...` = 本物)。リダイレクト後の最終URLを主判定にし
(`http._fetch` に `meta` 引数を追加して `final_url` を返す)、保存済みHTMLにも使えるよう
タイトル判定を併用。**再取得なしで724件を再分類**。

#### ユーザー提供情報からの発見: 現行運用より取得範囲が広い

ユーザーの現行運用は `security-advisory?segment=VC`(他に VT/VA)から取得。
本実装は `segment=""` で **15種類の接頭辞・4,217件**を取得しており、VC/VT/VA 相当は
1,768件(VTDSA 1,424 / VCDSA 340 / VADSA 4)にすぎない。
残る Symantec(SYMSA 479)・Brocade(BSNSA 881)・メインフレーム(MFDSA 888)・旧CA系は
VC/VT/VA のページには出てこない。**しかも CVE が欠けているのはこの外側**
(VCDSA 100% / VTDSA 97% に対し MFDSA 32%、GENSA 32%)。

#### HAR解析(ユーザーがEdge DevToolsから提供)で打ち止めを確認

- **詳細取得APIは存在しない**。一覧でクリックしたときに飛ぶのは
  `support-content-notification/.../SecurityAdvisories/0/38017` への**ページ遷移1本だけ**で、
  これは既に取得している経路そのもの。`fetchSecurityAdvisory`/`getAssociatedSecurityAdvisories`/
  `loadPatchData` はJS内部の関数名でURLではない(minifierが同一変数へまとめて代入している形)
- **取得方法はブラウザと同等**。ブラウザが200で取れた 38017 を素のGETで取得して 185,213 bytes
  (ブラウザ 185,216 と3バイト差)
- **ログイン必須ページは本当に必須**。一覧訪問でセッションCookie取得＋`Referer` 付与＋
  ブラウザ同等のヘッダでも 302 のまま。認証情報は使わない方針
- サイトのAPIパラメータも我々と同一構造(違いは pageSize 20 vs 100、segment "VC" vs "")

残り807件の内訳: **616件がログイン必須**(うち592件がMFDSA)、191件はページ取得済みだが
本文にCVEの記載が無い。**技術的な打ち手は尽きた**と判断。

### 次回(2026-09-02)の予定

**最優先: `vendor_hp` のフル出力と再投入**

```bash
cd C:\Users\haya001\github\study\Cyber
.venv\Scripts\python -m vulndb export-snowflake --what vendor --mode full
```

**なぜ差分ではだめか(実測確認済み)**: 差分は `bronze.vendor_advisories.fetched_at > カーソル`
で絞るが、今回の Broadcom 改修は**APIを再取得せず rebuild で silver の cve_ids を埋めた**もの。
そのため差分エクスポートは **0行**になり、1,475件の変更が丸ごと漏れる。
**パーサーや補完ロジックを変えたときは差分では拾えない** — IBM で踏んだ
「差分は"一部だけ取得済み"を検知できない」と同じ構図。

`vendor_hp` のみでよい(NVD・KEV・vulnrichment はコードも取得も変えていないため、
今日取り込んだ差分のままで正しい)。66,727行 / 約53MB。

**⚠ 明日いちばんに確認すること**: **昨日(8/31)のフル4ファイルが Snowflake に投入済みか。**
本日朝の時点では「まだアップロードしていない」とのことで、その後「今日の差分は取り込んだ」と
のみ聞いている。**差分だけを入れて土台のフルが入っていないと、Snowflake 側は数百行しかない**
状態になる。投入済みなら vendor_hp のフルだけ入れ直せばよい。

その他:
- `vendor_hp` は **23列**(末尾 CPE)。Snowflake 側の定義に列追加が必要
- 引用符内に改行があるため物理行数≠レコード数(`FIELD_OPTIONALLY_ENCLOSED_BY = '"'` が必要)
- CVE_ID 単位の置き換え(REPLACE/UPSERT)であること

**未了**: `E:\hayase\src\Cyber\` へのバックアップ(USB取り外し中)。
`compact` / BACKLOG.md / export改修 / migration 008・009 / Broadcom改修が未反映。

### 2026-09-02: 差分エクスポートが「新規レコードしか拾えない」バグを発見・修正

#### 症状と発見の経緯

全ソース `update` は8ソース成功。だが KEV の差分エクスポートが **0行**なのに、取り込みログは
「1687 changed/new」と言っていた。この食い違いを追って発覚。
きっかけは CISA が KEV に **`forensicTriage`** フィールドを新設(catalogVersion 2026.09.01、
値は Yes 38 / No 1,649)し、全1,687件の raw_json が一斉に変わったこと。
**catalog 全体が動く日でなければ、もっと長く気づけなかった。**

#### 根本原因: DuckDB の INSERT OR REPLACE は列リスト外に DEFAULT を再適用しない

```sql
INSERT OR REPLACE INTO bronze.kev (cve_id, raw_json, catalog_version, fetch_id) SELECT ...
```

`fetched_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)` は**列リストに無い**。DuckDB はこの場合
**既存値を据え置く**(DEFAULT を再評価しない)。つまり既存行は何度内容を上書きされても
**最初の挿入時刻のまま**で、新規キーだけが現在時刻を得る。

`export_snowflake` の差分は全て `WHERE fetched_at > カーソル` なので、
**差分＝新規レコードのみ、既存レコードへの変更は全部欠落**していた。実測(9/2朝):

| テーブル | 取り込み報告 | 実際に fetched_at 更新 | 漏れ |
|---|---:|---:|---:|
| bronze.nvd_cve | 1,515 | 480 | 1,035 |
| bronze.kev | 1,687 | 0 | 1,687 |
| bronze.vulnrichment | 177,848 | 479 | 多数 |
| bronze.vendor_advisories | 1,469 | 19 | 約1,450 |

**8/27 の「KEV を内容比較ベースに修正」は変更検出は正しかったが、書き込み側がこの仕様のため
下流に伝わっていなかった。** 直したつもりが直っていない状態が1週間続いた。
**ユーザーが 9/1 に投入した差分4ファイルも同じ理由で不完全**(新規分のみ)。

#### 修正(`db.py` に集約)

- `bulk_insert` に `key` / `compare` / `stamp` を追加。
  - `stamp="fetched_at"` で**明示的に now() を書く**(DEFAULT に頼らない)
  - `key`+`compare` で**内容が本当に変わった行だけ書く**。これが無いと、フルtarball再読込の
    vulnrichment や modified-window の NVD が毎回全行を stamp して差分が全件になる
  - **比較は SQL 側**(temp table + LEFT JOIN + `IS DISTINCT FROM`)。
    `bronze.nvd_cve.raw_json` だけで1GB超あり Python の dict に載せられない
  - `compare` には**ペイロード列だけ**を入れる。`commit_sha`/`catalog_version`/`fetch_id` は
    毎回変わるので、入れると全行が「変更あり」になる
- **`bronze_insert()` を新設し、テーブル名→(key, compare) を `_BRONZE_KEYS` に集約。**
  `bronze.vendor_advisories` は4モジュール(IBMは1モジュール内4か所)から書かれるため、
  呼び出し側に引数を書かせると必ずどこかで忘れる。**忘れられない形にするのが修正の本体。**
- 各ソースの `rows_ingested` を**実書き込み数**に変更(「17万件読んだ」と「17万件変わった」は
  別の主張。差分エクスポートは後者を見ている)
- `tests/test_bulk_insert.py` 新規(11項目)。既存2テストも通過

#### 教訓

- **「DEFAULT があるから埋まる」は upsert では成り立たない。** 列リストに入れるか明示的に書く
- **取り込みログの件数と、実際にテーブルが変わった件数を突き合わせる**。
  今回は「1687 changed/new なのに差分0行」という**内部矛盾**だけが手がかりだった
- **バグの再発防止は「正しい引数を渡す」ではなく「引数を渡さなくても正しい」形にする**

#### 今日の出力(全て `--mode full`、検証済み)

`Cyber/data/export-snowflake/` の `*_20260902_013654.csv`:

| ファイル | レコード | 列 | サイズ | 物理行 |
|---|---:|---:|---:|---:|
| `cve_updated` | 385,522 | 20 | 499.51MB | 841,142 |
| `known_exploited_vulnerabilities` | 1,687 | **12** | 0.92MB | 1,687 |
| `vulnrichment` | 177,867 | 8 | 10.69MB | 177,867 |
| `vendor_hp` | 66,746 | **23** | 54.25MB | 242,448 |

- **KEV は 11→12列**(末尾 `forensicTriage`)、`vendor_hp` は 23列(末尾 `CPE`)。
  **どちらも Snowflake 側の取り込み定義に列追加が必要**
- Broadcom は 3,410/4,219 (81%) が CVE_ID 付きで載っている
- **`fetched_at` の取り残しは再取得では復元できない**(内容は既に正しく、比較すると
  「0 changed」になるため)。だから今日はフル投入が唯一の正解だった

#### エクスポート用フォルダの運用(2026-09-02 にユーザーが導入)

`Cyber/data/export-snowflake/` の**直下は「これから投入するファイルだけ」**を置く。
投入済み・破棄したものは `Imported_or_dismissed/` へ移す(ユーザーが手動で実施)。
直下を見れば投入対象が一目で分かる状態を保つこと。

**ハッシュ違い＝内容違いとは限らない。** 同日の `vendor_hp` 2本がサイズ同一・ハッシュ相違
だったが、実体は**行の並び順だけ**の差だった(`rebuild` が silver を作り直すと順序が変わる)。
CSV を比較するときは行の集合として突合すること。

### 次回(2026-09-03)の予定

**まず: 9/2 のフル4ファイルの Snowflake 投入結果を確認する。**
投入は**別の担当者に依頼**しており、ユーザーが翌日に結果を知らせる予定。
期待レコード数は上表のとおり。**物理行数の方でロードされていたら
`FIELD_OPTIONALLY_ENCLOSED_BY = '"'` の指定漏れ**。

その後:

1. 全ソース `update` → **今度は差分が正しく出るはず**。
   `export-snowflake --what all --mode incremental` の件数が
   「新規だけ」に見えないか(nvd の update 件数と差分件数が乖離していないか)を必ず確認する。
   差分カーソルは 9/2 の full 出力時点(`2026-09-02T01:36:54Z`)で4種ともセット済み
2. `vulndb compact`(9/2時点で 5.06GB、rebuild 後さらに増加。月1回運用)
3. **`E:\hayase\src\Cyber\` へのバックアップ**(USB未接続で 9/1・9/2 とも未了)。
   `compact` / BACKLOG.md / export改修 / migration 008・009 / Broadcom改修 /
   今回の `bronze_insert` 改修と `tests/test_bulk_insert.py` が未反映

関連: [[project-repo-setup]] [[project-security-scan]]

---

## 2026-09-03: 日次運用の引き渡し＋検証の誤検知を修正

### Snowflake 投入は 9/3 分まで完了

**9/2 のフル4ファイル、および 8/31〜9/2 の分は投入済み。9/3 の差分4ファイルも投入し、
レコード件数が一致することをユーザーが確認した。**
件数一致＝`FIELD_OPTIONALLY_ENCLOSED_BY = '"'` が正しく効いている証拠
(物理行数でロードされていれば桁が合わない)。

9/3 の差分(基準 `2026-09-02T01:36:54Z`、ファイル名 `*_20260903_061559.csv`):

| ファイル | レコード | サイズ |
|---|---:|---:|
| `cve_updated` | 1,014 | 1.04MB |
| `known_exploited_vulnerabilities` | 7 | 0.01MB |
| `vulnrichment` | 553 | 0.02MB |
| `vendor_hp` | 1,308 | 1.03MB |

**9/2 に直した差分バグは治っている**: NVD の update 件数 1,015 に対し差分 1,014 行。
「新規だけ」に縮んでいない。

### verify() の CRLF 誤検知(本日の主要な修正)

`cve_updated` が **CRLF行末**として BAD 判定された。**誤検知だった。**

- ファイル内の CR は 37個、CR+LF の出現も 37個 → **全ての CR が CR+LF の一部**
- しかしレコード数は 1,015。本当に CRLF 行末なら CR+LF は 1,015個以上あるはず
- 37個すべてが **NVD の説明文の内部**(引用符で囲まれたフィールド内)にあった

原因は `verify()` の `b"(CR)(LF)" in head` という**単純な部分文字列検索**で、
引用符の内外を区別できていなかったこと。

**これは実害のあるバグ。** `OPERATIONS.md` はこの警告に対し
「**取り込まず開発者へ連絡**」と指示しているため、**正常なファイルで日次運用が止まる**。

修正: `_crlf_record_separator()` を新設し、引用符の内外を1バイトずつ追跡する方式に変更
(二重引用符 `""` は2回トグルして相殺されるので特別扱い不要)。回帰テスト5件を
`tests/test_export_fields.py` に追加。全6テスト通過。

#### 教訓

- **検査コードのバグは、本体のバグより気づきにくく、運用を止める力は同じ。**
  誤検知は「安全側の失敗」ではない — マニュアルが「投入するな」と言う以上、実害がある
- **CSV を扱うコードで生バイト検索をしてはいけない。** 行区切りとフィールド内容は
  引用符の状態を追わないと区別できない。csv パーサを通すか、状態機械を書くこと
- 疑わしい判定が出たら**まず数を突き合わせる**。今回は「CR+LF が37個、レコードは1,015件」
  という不一致だけで誤検知と断定できた

### 長時間実行の落とし穴: バッテリ駆動でサスペンド

`update` が2時間経っても終わらず、`vulnrichment.tar.gz.part` が 22MB → 0 に**2回**戻っていた。

原因は回線ではなく**電源**。AC接続時は「スリープしない」設定だが、
**DCでは3分で寝る**(`powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` で DC=0xb4=180秒)。
復帰のたびに TCP が切れ、83.6MB の tarball が振り出しに戻っていた。

**長時間の取得を走らせる前に電源アダプタを接続すること。** `OPERATIONS.md` の
「実行がとても遅い」節に明記した。

#### HTTP Range による中断再開は不可能(検証済み)

「途中から再開できれば解決する」と考えて実装しようとしたが、**配信元が非対応**だった:

```
GET codeload.github.com/.../tar.gz  with Range: bytes=1000000-1000999
  -> status 200 (206ではない) / Accept-Ranges なし / Content-Length 87,674,186
```

codeload は tarball を都度動的生成するため範囲指定を無視する。
**書いても毎回200が返り、現状と同じ「最初から」になる**ところだった。
`BACKLOG.md` に否定的結果として記録済み。

**教訓: 外部サービスに依存する改善は、着手前に1回のリクエストで前提を確認する。**
今回はヘッダだけ見れば済んだ(ボディを読みに行くと83MBのダウンロードが始まって詰まる)。

### その他

- **`E:\hayase\src\Cyber\` へのバックアップを実施**(9/1・9/2 の未了分を解消)。
  `.venv` / `data` / `__pycache__` を除外した robocopy
- IBM ギャップフィルは分割の末端で `CVE-0000-00000`(不正なCVE ID)が単独で
  2,000件キャップに当たる。実害はないが、いずれ除外してよい
- Broadcom の新規2件はいずれもログイン必須ページだった(既知の打ち止め領域)

### 次回(2026-09-04)から: 日次運用は `daily.bat`

**このチャットで実行するのはやめ、コマンドで回す体制に移行する。**
`daily.bat` / `monthly-compact.bat` / `OPERATIONS.md`(日本語の運用マニュアル)は作成済み。

継続改善はこのチャットで行うが、**日次の実行は他の人ができる状態**にしてある。

未了・保留:

1. **`vulndb compact` が未実行**(9/2時点で5.06GB、その後の rebuild でさらに増加)。
   月1回運用。日次実行と同時に走らせないこと
2. **運用ユーザーのフォルダへの移設は未実施**。手順は `OPERATIONS.md`
   「別のユーザー・別の場所へ移す場合」に記載済み。
   **`.venv` をコピーしてはいけない**(editable install の `.pth` が元の場所を指し続け、
   エラーも出ずに元のDBを読み書きする)。移設後は `daily.bat` 冒頭の
   `code:` / `database:` 2行が両方コピー先を指しているか必ず確認する

関連: [[project-repo-setup]] [[project-security-scan]]

---

## 2026-09-07: user01 での実行環境を構築、daily.bat の文字コード事故を実行前に発見

### user01 に自己完結した環境を作成(検証済み)

**この機体には管理者権限が無く、システム全体の Python も無い。** `.venv` が参照する
Python は `C:\Users\haya001\AppData\Local\Python\pythoncore-3.14-64` で、
**他の利用者(user01)からは読めない場所**にある。`uv` も入っていない。

対応: **Python 実行環境そのもの(137MB)を運用フォルダにコピーして自己完結させた。**

```
C:\Users\user01\Cyber\
  python\       ← pythoncore-3.14-64 の複製(コピー元と無関係に動く)
  .venv\        ← python\python.exe から作り直し(uvではなくpython -m venv + pip)
  src\ tests\ migrations\ *.bat *.md
  data\cyber.duckdb  ← compact後3.14GBを複製、user01にFullControl確認済み
```

`vulndb status` で `code: C:\Users\user01\Cyber\src` `database: ...\user01\Cyber\data\cyber.duckdb`
を確認し、haya001 への参照が無いことも全ファイル走査で確認済み。silver.cve 385,847等、
開発側と行数一致。

**`OPERATIONS.md` の移行手順を、この検証結果に基づいて書き換えた**(元の手順は
`uv venv` 前提で、システム全体 Python が無いこの機体では成立しなかった)。

### daily.bat / monthly-compact.bat の重大な文字コード事故(実行前に発見)

**本番投入前の動作検証で、`.bat` 本体が壊れていることが分かった。**

作成時、`.bat` は **UTF-8 / LF改行**で保存されていた(Write ツールの既定)。
cmd.exe はこれを正しく読めない。実機で `daily.bat` のロジック部分をスタブ化して実行したところ:

```
'くよぁE、Ecd' は、内部コマンドまたは外部コマンド、...認識されていません。
'を読む。環墁E数はユーザーごとの設定で、管琁E限が' は、...認識されていません。
```

`cd /d "%~dp0"` を含む複数の `rem` コメント行が文字化けした末に**コマンドとして実行を
試みていた**。たまたま末尾の `exit /b 0` に到達して見かけ上は「正常終了」になっていたが、
`cd /d` すら実行されていない状態だった。**もし気づかず配布していたら、user01 の実行で
原因不明の失敗が起きていた。**

修正を2段階で試した:

1. `chcp 65001` を `@echo off` の直後に追加 → **不十分**。日本語表示は直ったが、
   一部の `rem` コメント行がまだ誤ってコマンド解釈された(全角記号の一部がメタ文字に
   化けていた模様。`chcp 65001` はコンソールの表示コードページを変えるだけで、
   バッチファイル読み取り時の解釈タイミングとは別問題らしい)
2. **CP932(Shift-JIS) + CRLF に変換 → 完全に解消。** 日本語Windowsのcmd.exeが
   素で読める形式に合わせたのが正解だった。`chcp` は不要なので外した

修正後、`daily.bat`(引数`full`込み)・`monthly-compact.bat` とも実機で
スタブ経由の実行検証を行い、日本語表示・`if/else`分岐・引数解釈・
APIキーのファイル読み取り/環境変数優先のいずれも正しく動作することを確認した。

#### 教訓

- **`.bat` は必ず CP932 + CRLF で保存すること。** UTF-8 は cmd.exe との相性が悪く、
  `chcp` を足しても完全には直らない。日本語を含むバッチファイルは有無を言わさずCP932
- **「exit code 0 で終わった」は「正しく動いた」の証拠にならない。** 今回は文字化けで
  本来の処理(`cd /d`含む)が丸ごと飛んでいたのに、たまたま最後の行に到達して0で終わっていた。
  **標準出力・標準エラーの中身まで見て初めて動作確認したことになる**
- **配布前に実機で動かして確認する。** 今回はコード変更後、いきなり本番投入せず
  「動作検証」の段階を踏んだために事故を未然に防げた

### NVD API キーの受け渡し

環境変数は利用者ごとの設定で、管理者権限が無いと他の利用者には設定できない。
`daily.bat` に「環境変数 → 無ければ `nvd_api_key.txt` の1行目」という2段の探索を追加し、
`OPERATIONS.md` に節を追加した。**`nvd_api_key.txt` の作成はAPIキーを直接扱うため
自動モードのclassifierにブロックされた** — ファイル経由は見送り、**ユーザーが user01 に
ログインして環境変数 `NVD_API_KEY` を直接設定する方式を選択**(下記)。

### user01 での初回本番実行、成功

ユーザーが user01 にログインし、GUI(アカウントの環境変数を編集)で `NVD_API_KEY` を設定。
**`setx` はその場のウィンドウには反映されない**ので、設定後に新しいウィンドウを開いてから
実行する必要がある点を案内した。

`daily.bat` 実行開始直後に `code:`/`database:` の2行が user01 側を指すことをユーザーが確認。
実行中、haya001 側から `cyber.duckdb.wal` と `vulnrichment.tar.gz.part` の存在で
進捗を横から観測できた(プロセス所有者はクロスユーザーのため `GetOwner` では見えないが、
ファイルの更新は見える)。

完走後、ユーザーが Snowflake へアップロード。出力ファイルを検証:

| ファイル | レコード数 |
|---|---:|
| `cve_updated` | 2,527 |
| `known_exploited_vulnerabilities` | 3 |
| `vulnrichment` | 743 |
| `vendor_hp` | 6,924 |

4ファイルとも検証通過。**これで user01 への日次運用移行が実質完了した。**

#### 誤検知: 件数が1件ずれて見えた騒動

ユーザー報告の件数(KEV 4件・Vulnrichment 744件)が実際のレコード数と**ちょうど+1**
(ヘッダー行を含めた行数と一致)だったため、「Snowflakeがヘッダー行をデータとして
取り込んでいる」という重大な事故を疑い、`OPERATIONS.md` に `SKIP_HEADER = 1` の
節を書いて user01 側にも配布した。

**ユーザーの一言で誤りと判明**: 「カウントはしていますが、ヘッダ行をデータとして
取り込んでいるわけではありません」。実際は**ロード結果画面がヘッダーを含めて
数えて表示しているだけ**で、テーブルの中身は正しかった。書いた節を撤回し、
「画面表示は+1に見えることがあるが実害なし」という正確な注記に差し替えて再配布。

##### 教訓

- **「件数が符合しない」だけでは原因を決め打ちしない。** ヘッダー行込みの数と
  ぴったり一致したのは強い状況証拠だったが、**実際にテーブルの中身を見る前に
  マニュアルへ「事故」として書いてしまった**のは早すぎた。今回はユーザーが
  実際の画面仕様を知っていたから即座に訂正できたが、本来は先に
  `SELECT * FROM ... WHERE CVE_ID = 'CVE_ID'` のような直接確認を求めるべきだった
- **ロード結果画面の集計仕様はツールによって「ヘッダー込みで数える」ことがある。**
  DBの実データが正しいかどうかは別問題として切り分けて確認すること

### 残っている作業

移行後は**開発フォルダのデータベースが別物になる**運用に切り替わる。
開発側で最新データが必要になったら user01 側の `cyber.duckdb` を都度コピーする。
それ以外、当面のタスクは完了。継続改善はこのチャットで行う。

関連: [[project-repo-setup]] [[project-security-scan]]

---

## 2026-09-10: README 全面改訂 + IBM の不正 CVE ID フィルタ

### README.md を9月時点の実態に書き直し（フロー図追加）

8/25 で止まっていた `README.md` を現状に合わせて全面改訂:

- 役割を2つ明記（BOD 判定 / ベンダーアドバイザリ集約）、最終成果物は Snowflake 向け4CSV
- **データフロー図を新設**（縦フロー主体。CJK 幅ずれを避けて罫線囲みは不使用）:
  8ソース → bronze → silver → (gold: BOD系) / (vendor_advisory: gold に入れない) → 4CSV → Snowflake
- データソースを4→**8**（ベンダー4種の取得方法と制約を表に）
- `bronze.vendor_advisories` / `msrc_product` / `broadcom_advisory_page`、migration 001-009 対応表
- **Snowflake 向け CSV セクション新設**（4ファイルの元テーブル・列数・full/incremental・カーソル・取り込み定義）
- コマンドを `python -m vulndb ...` に統一（コンソールスクリプト未登録）、`daily`/`compact`/`export-snowflake` 追加
- 運用を「GitHub Actions」→「運用担当PCで `daily.bat`」に修正

ついでに `OPERATIONS.md` の KEV 列数を 11→**12**（`forensicTriage` 追加分。ファイル内で不整合だった）。

### IBM: 不正な CVE ID（`CVE-0000-00000` 等）をフィルタ

9/3 の実行ログに出ていた
`ibm: gap-fill batch ... (CVE-0000-00000) hit the 2000-result cap on a single CVE` の原因と対策。

**原因**: `CVE-0000-00000` は **IBM の datalist インデックス（`results.cve_ids`）に実在する**
プレースホルダ。取り込みフィルタ `_CVE_ID_RE = ^CVE-\d{4}-\d+$` が緩く、これを通していた。
`q=CVE-0000-00000` は IBM 側で数千件マッチ → 2,000 cap 到達 → 1 CVE なので分割不能 →
毎回 `rows_skipped` に計上される、という無害だが無駄なループになっていた。

**対策**（`sources/ibm.py`）: `_CVE_ID_RE` を capture 付きに変え、`_is_valid_cve_id()` を新設。
**年 >= 1999 かつ serial > 0** を要求（CVE 採番は 1999 開始。serial 0 は存在しない）。
`_fetch_known_cve_ids()` のフィルタをこれに差し替え。

**ライブ検証**: 実際の datalist 23,874 件に対し、新フィルタが追加で落とすのは
**`CVE-0000-00000` と `CVE-0201-0769`（年 0201）の2件だけ**。正規の CVE は1件も落ちない。

`tests/test_ibm_batching.py` に `_is_valid_cve_id` の8ケースを追加。全6テスト通過。

#### 見送った案（ユーザーと相談のうえ）

「正当な1CVEで 2,000 超」への追加分割（日付キーセット・製品名 AND・datalist 個別取得）は
**保留**。実測の密な CVE は 37〜236件で、1脆弱性に IBM が 2,000本の別々の報を出すことは
現実にはほぼ起きない。現状の末端処理（最新 2,000 件を保持して skip 計上）で実害は小さい。
実在 CVE が末端に落ちた実績が出たら、まず `q=` が日付境界構文を持つかプローブして採否判断。
（`BACKLOG.md` には未記載。必要なら追記）

### 未了

- **E: へのバックアップ**（今回の ibm.py / test / README / OPERATIONS 改訂分）。
  E: 未接続のため保留。再接続時に `robocopy ... /XD .venv data __pycache__ .pytest_cache python`

関連: [[project-repo-setup]] [[project-security-scan]]
