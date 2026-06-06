# Streamlit in Snowflake — 実装指示書

作成日: 2026-06-06  
担当者向け引き継ぎ文書

---

## 背景・目的

talent-mgmt-db は、3社（生命保険親会社・IT子会社・DX子会社）に分散した人材・スキルデータを
Snowflake に統合し、CIO/VP が「スキルXを持つ人材は誰か」を横断的に問い合わせできるようにするプロジェクト。

本指示書は、Snowflake のデータ基盤の上に **Streamlit in Snowflake** でUIを構築する作業の
引き継ぎを目的とする。

プロジェクトのコンテキストは Snowsight 共有ワークスペースの以下を参照すること：

- `AGENTS.md` — アーキテクチャ概要・重要ルール（PII暗号化・AI非介入・Bronze不変）
- `TEAM_DOCS/MEMORY.md` — プロジェクト現状・既知問題
- `TEAM_DOCS/DECISIONS.md` — 設計判断の記録
- `TEAM_DOCS/HANDOFF.md` — 進行中タスク・引き継ぎ事項

---

## 作るもの

### 画面1: スキルマップ・ダッシュボード（閲覧専用）

CIO向けの分析ビュー。

| ウィジェット | 内容 |
|---|---|
| スキルヒートマップ | スキル × エンティティ × レベル分布（Plotly heatmap） |
| タレントマップ | 従業員 × スキル × レベル（バブルチャート or レーダーチャート） |
| フィルター | エンティティ別・スキルドメイン別・レベル閾値 |

データソース: `gold.skill_assessments`、`gold.employees`、`gold.skill_taxonomy`

### 画面2: 管理画面（閲覧・編集）

データ品質管理者向けの運用ビュー。

| ウィジェット | 内容 |
|---|---|
| レビューキュー | `needs_review = TRUE` のレコード一覧（優先表示） |
| 従業員マスタ | `gold.employees` の閲覧 |
| スキル評価編集 | `gold.skill_assessments` のレコード修正（Silver層への書き戻し） |

---

## Snowflake 接続・認証

### Streamlit in Snowflake の使い方

- Snowsight の左メニュー「Streamlit」→「+ Streamlit App」でアプリを作成（CLI不要）
- アプリはSnowflakeセッションの権限で自動接続される
- 接続には `snowflake.snowpark.context.get_active_session()` を使う

```python
from snowflake.snowpark.context import get_active_session
session = get_active_session()
```

### パスフレーズ管理（重要）

個人情報列は `ENCRYPT()` / `DECRYPT_AS_STRING()` で暗号化されている（AES-256-GCM）。
Streamlit アプリ起動時にサイドバーでパスフレーズを入力させ、セッション変数にセットする。

```python
import streamlit as st

passphrase = st.sidebar.text_input("パスフレーズ", type="password")
if passphrase:
    session.sql(f"SET passphrase = '{passphrase}'").collect()
```

暗号化対象列（平文の列名は存在しない — 必ず復号してアクセスすること）:

| テーブル | 列名 | 内容 |
|---|---|---|
| `entity_employees` | `name_enc` | 氏名 |
| `employee_reviews` | `score_enc` | 評価スコア（1–5） |
| `employee_reviews` | `comment_enc` | 評価コメント |

復号クエリの例:

```sql
SELECT
  emp_id,
  DECRYPT_AS_STRING(name_enc, $passphrase)::VARCHAR    AS name,
  DECRYPT_AS_STRING(score_enc, $passphrase)::INTEGER   AS eval_score,
  DECRYPT_AS_STRING(comment_enc, $passphrase)::VARCHAR AS eval_comment
FROM entity_employees;
```

---

## データレイヤー構成

```
Bronze（生データ・不変）→ Silver（AI正規化済み）→ Gold（分析用ビュー）→ Analytics
```

StreamlitはGoldレイヤーのビューにのみアクセスする。
Goldビューがまだ存在しない場合は、先にSnowsightでSQLを実行して作成してからStreamlitを実装すること。

### 必要なGoldビュー（未作成の場合は先に定義）

```sql
-- 従業員マスタ統合ビュー
CREATE OR REPLACE VIEW gold.employees AS ...;

-- スキル評価統合ビュー
CREATE OR REPLACE VIEW gold.skill_assessments AS ...;

-- スキルタクソノミー
CREATE OR REPLACE VIEW gold.skill_taxonomy AS ...;

-- スキルヒートマップ用集計ビュー
CREATE OR REPLACE VIEW gold.skills_heatmap AS
SELECT
  canonical_skill_id,
  entity,
  level_score,
  COUNT(*) AS employee_count
FROM gold.skill_assessments sa
JOIN gold.employees e ON sa.global_employee_id = e.global_id
GROUP BY 1, 2, 3;

-- タレントマップ用ビュー
CREATE OR REPLACE VIEW gold.talent_map AS
SELECT
  global_employee_id,
  canonical_skill_id,
  level_score,
  experience_score,
  entity,
  assessment_date
FROM gold.skill_assessments sa
JOIN gold.employees e ON sa.global_employee_id = e.global_id;
```

---

## ファイル構成（Snowsight Streamlit editor内）

Snowsight の Streamlit アプリはファイル構成をエディタ内で管理する。
推奨構成:

```
streamlit_app.py          # メインアプリ（エントリーポイント）
pages/
  01_dashboard.py         # スキルマップ・ダッシュボード
  02_admin.py             # 管理画面
utils/
  db.py                   # セッション・クエリ共通処理
  charts.py               # Plotlyチャート生成関数
```

---

## 実装ステップ

### Step 1: Goldビューの確認・作成（Snowsight SQL）

1. Snowsight「Worksheets」でGoldレイヤーのビューが存在するか確認する
2. 未作成のビューは上記のSQLを参考に作成する
3. `SELECT * FROM gold.skills_heatmap LIMIT 10;` でデータが返ることを確認する

### Step 2: Streamlitアプリの骨格作成

1. Snowsight「Streamlit」→「+ Streamlit App」で新規作成
2. 以下の骨格コードで動作確認する

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Talent Management", layout="wide")
session = get_active_session()

passphrase = st.sidebar.text_input("パスフレーズ", type="password")
if passphrase:
    session.sql(f"SET passphrase = '{passphrase}'").collect()

st.title("Talent Management Dashboard")

df = session.sql("SELECT CURRENT_USER(), CURRENT_ROLE()").to_pandas()
st.dataframe(df)
```

### Step 3: ダッシュボード画面の実装

```python
import plotly.express as px

df = session.sql("""
  SELECT
    t.source_label_ja AS skill,
    e.entity,
    AVG(sa.level_score) AS avg_level
  FROM gold.skill_assessments sa
  JOIN gold.skill_taxonomy t ON sa.canonical_skill_id = t.canonical_id
  JOIN gold.employees e ON sa.global_employee_id = e.global_id
  GROUP BY 1, 2
""").to_pandas()

pivot = df.pivot(index="skill", columns="entity", values="avg_level")
fig = px.imshow(pivot, color_continuous_scale="Blues", title="スキルヒートマップ")
st.plotly_chart(fig, use_container_width=True)
```

### Step 4: 管理画面の実装

```python
st.subheader("要確認レコード")
df_review = session.sql("""
  SELECT assessment_id, global_employee_id, canonical_skill_id,
         level_score, normalization_conf, source
  FROM gold.skill_assessments
  WHERE needs_review = TRUE
  ORDER BY normalization_conf ASC
""").to_pandas()
st.dataframe(df_review, use_container_width=True)

with st.form("edit_form"):
    assessment_id = st.text_input("Assessment ID")
    new_score = st.slider("修正後スコア", 1, 5)
    submitted = st.form_submit_button("更新")
    if submitted:
        session.sql(f"""
          UPDATE silver_it.skill_assessments
          SET level_score = {new_score}, needs_review = FALSE
          WHERE assessment_id = '{assessment_id}'
        """).collect()
        st.success("更新しました")
```

---

## 制約・注意事項

- **CLIは使用しない**。Snowsightの画面から直接アプリを作成・デプロイすること
- **9月末までは閲覧・データ修正のみ**。新規データの書き込み機能は対象外
- **AIはスコアを変更しない**。1–5のスキルスコアは人間の入力値をそのまま使う。AIは正規化フラグと信頼度スコアのみ付与する
- **Bronze層は不変**。修正はSilver層に対して行い、GoldビューはSilver修正後に再計算される
- **暗号化列を平文で扱わない**。`st.write()` やログに復号値を直接出力しない

---

## 参考リンク

- [Streamlit in Snowflake 公式ドキュメント](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Snowpark Python API](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Plotly Express ドキュメント](https://plotly.com/python/plotly-express/)
