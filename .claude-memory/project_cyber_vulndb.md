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

関連: [[project-repo-setup]] [[project-security-scan]]
