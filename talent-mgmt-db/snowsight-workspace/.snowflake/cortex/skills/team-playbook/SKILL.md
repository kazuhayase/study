# SKILL: team-playbook
# 作業開始時に呼び出す。参照順・出力形式・禁止事項を固定する。

## 使い方
作業開始時に「/team-playbook」と入力する。

## 作業開始チェックリスト（AIが自動実行）

### Step 1: ドキュメント参照
以下を順番に読み込む。

```
1. AGENTS.md               — Critical Rules確認
2. TEAM_DOCS/MEMORY.md     — 現状・既知問題
3. TEAM_DOCS/HANDOFF.md    — 前回からの引き継ぎ事項
4. TEAM_DOCS/DAILY_LOG/[今日の日付].md  — 当日ログ（なければスキップ）
```

### Step 2: 状況サマリー出力
以下の形式で出力する。

```
## 本日の作業開始サマリー

**現フェーズ**: （MEMORY.mdから）
**前回の続き**: （HANDOFF.mdから）
**本日のログ**: （あれば）
**注意事項**: （既知問題・ブロッカー）

準備完了。何から始めますか？
```

### Step 3: セッション準備
以下を案内する。

```sql
-- Snowsightで必ず最初に実行してください
SET passphrase = '（パスフレーズをここに入力）';
```

## 禁止事項（このセッション全体に適用）

- `raw_*` テーブルへの書き込み操作（Bronze immutable）
- `name_enc` / `score_enc` / `comment_enc` を平文で扱うSQL生成
- 1–5スコアのAI推定・修正
- パスフレーズをコードにハードコード

## 作業終了時

「まとめて」「終わり」「おわり」「ここまで」のいずれかが入力されたら：

1. `TEAM_DOCS/DAILY_LOG/YYYY-MM-DD.md` を更新（なければ作成）
2. `TEAM_DOCS/HANDOFF.md` を更新
3. 重要な設計判断があれば `TEAM_DOCS/DECISIONS.md` に追記
4. 必要に応じて `TEAM_DOCS/MEMORY.md` を更新
