# CLAUDE.md — Cyber/vulndb

BOD 26-04 対応の脆弱性優先度DB。設計の背景と使い方は `README.md` を参照。
ここには作業時に踏み外しやすい点だけ書く。

## 環境

- uv 管理の `.venv`（Python 3.13）。`uv pip install -r requirements.txt && uv pip install -e .`
- src レイアウトなので **editable install しないと `python -m vulndb` が動かない**
- 依存は duckdb のみ。HTTP・gzip・tar・CSV はすべて標準ライブラリで済ませる。
  新しい依存を足す前に、標準ライブラリで足りないか確認すること

## 絶対に守ること

### 決定マトリクスは指令の写し

`migrations/005_seed_bod2604_matrix.sql` は CISA BOD 26-04 Appendix A, Table 1 の転記。
**推測で書き換えない。** 変更するときは必ず一次情報を取り直して突合する:

```bash
curl -sL -A "Mozilla/5.0 ..." https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk
# Table 1 は本文中の PNG 画像として公開されている（HTML の <table> ではない）
```

`tests/test_bod2604.py` が独立に転記した16行を保持しているので、片方だけ直すと必ず落ちる。
**両方直すのが正しい手順**であって、テストを実装に合わせるのは誤り。

### cisa.gov は User-Agent を見る

デフォルトの urllib / curl の UA では 403 が返る。`config.USER_AGENT` を必ず使う。

### SSVC のキー形式が2種類ある

同じ決定点をソースごとに違う表記で持っている。片方だけ対応するとカバレッジが静かに半減する。

- NVD: `metrics.ssvcV203[].ssvcData.options[]` → `exploitation` / `automatable` / `technicalImpact`
- Vulnrichment: `containers.adp[].metrics[].other.content.options[]` → `Exploitation` / `Automatable` / `Technical Impact`

`transform._normalise_ssvc_options` が吸収している。

### ソースの優先順位を崩さない

`rebuild.py` は**実行順序で優先順位を表現している**。権威のあるソースを先に
`INSERT OR REPLACE` で入れ、後続の NVD ミラーは `INSERT OR IGNORE` で穴埋めするだけ。
パスの順序を入れ替えると precedence が壊れる。

- `silver.kev`: KEV カタログ > Vulnrichment > NVD
- `silver.ssvc`: Vulnrichment > NVD

### 期限を勝手に埋めない

BOD 26-04 の起算日は「KEV 掲載日」と「資産上で検出した日」の**早い方**。
資産インベントリが無い現状では KEV 掲載 CVE しか `due_date_*` を出せない。
CVE 公開日で代用しないこと — 指令にその規定は無い。

## 性能上の落とし穴

**DuckDB の `executemany` は約1,800行/秒しか出ない。** これが本プロジェクト最大の罠で、
実測で2回踏んだ:

| 対象 | executemany | ファイル経由 |
|---|---|---|
| EPSS 36万行の取り込み | 約11分 | `read_csv` に .csv.gz を渡して **0.06秒** |
| `rebuild` 全体 | **77分** | `db.bulk_insert`（JSONL + `read_json`）で **6.7秒** |

**行を1件ずつバインドさせず、DuckDB にファイルを読ませること。**
`db.bulk_insert()` がその共通経路で、dict を一時 JSONL に書いて `read_json` で投入する。
JSONL なのはクォート・改行・NULL の扱いを自前でエスケープせずに済むから。
新しく一括投入を書くときは必ずこれを通す。

なお Bronze の読み出しとパース自体は速い（17万件で読み込み0.09秒＋`json.loads`1.3秒＋
パース0.16秒）。遅いと感じたら書き込み側を疑うこと。

- `rebuild` は毎回 Bronze 全件を作り直す（NVD は1パスに統合済み）。数秒で終わるので
  差分更新にする理由がない
- Vulnrichment の初回 tarball 取り込みは約2.5分。日次更新は compare API の差分
- Vulnrichment 差分の閾値には**不変条件がある**: `TARBALL_BREAKEVEN_FILES` (150) は
  必ず `COMPARE_FILE_PAGE_LIMIT` (300) より小さく保つこと。
  GitHub の compare API は files を300件で打ち切るため、300件返った応答は
  「ちょうど300件」なのか「切り捨て」なのか区別できない。閾値が下にあることで、
  差分パスが切り捨て済みの応答を掴んでカーソルだけ進める（＝変更を恒久的に取りこぼす）
  事故が構造的に起きない

## やってはいけない

- **DuckDB ファイルを git にコミットしない。** ルートの pre-commit が 500KB 超を弾く。
  受け渡しは Actions cache と artifact 経由
- `data/` と `logs/` は gitignore 済み。生フィードをリポジトリに置かない
- ルートの `.gitignore` が `*.sql` を無視するため、`Cyber/.gitignore` の
  `!*.sql` 打ち消しを消さないこと（マイグレーションが追跡されなくなる）
- ルートの `.gitignore` は `.gitignore` 自体も無視する。`Cyber/.gitignore` は
  `git add -f` で強制追跡している（`talent-mgmt-db` や `scripts/podcast` と同じ扱い）。
  一度追跡されていれば以降の更新は普通にコミットできる

## テスト

pytest は使わない（リポジトリ全体の慣習）。標準ライブラリのみ:

```bash
.venv/bin/python tests/test_bod2604.py   # マトリクス16行 + Gold ビューの判定
.venv/bin/python tests/test_parsers.py   # 実データ由来のフィクスチャでパーサ検証
```

フィクスチャは実フィードから取得した本物（CPE と references だけ削って軽量化）。
差し替えるときも合成データではなく実データを使うこと。
