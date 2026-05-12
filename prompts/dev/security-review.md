---
title: コードセキュリティレビュー
category: dev
tags: [security, code-review, vulnerability]
created: 2026-05-12
models:
  claude: ★★★★★  # 脆弱性の説明・修正コード生成が精緻
  gemini: ★★★★☆  # Google Cloud環境との親和性が高い
---

# プロンプト（共通ベース）

```
以下のコードをセキュリティ観点でレビューしてください。

【言語・フレームワーク】{{例：Python / FastAPI}}
【コードの役割】{{例：外部APIからデータを受け取りDBに保存する処理}}

【チェック観点】（不要な項目は削除）
- OWASP Top 10（インジェクション、認証、XSS等）
- 機密情報のハードコーディング
- 依存ライブラリの既知CVE
- 入力バリデーション・サニタイズ
- エラーハンドリングの情報漏洩リスク
- 権限・アクセス制御

【コード】
---
{{code}}
---

出力形式：
1. 深刻度別の問題一覧（Critical / High / Medium / Low）
2. 各問題の説明と修正コード例
3. 問題なしと判断した観点
```

# モデル別バリエーション

## Claude向け

修正コードも含めて一気に出させる場合：

```
問題箇所を修正したコード全体も出力してください。
```

依存ライブラリのCVEチェックはCLI併用が確実：

```bash
# studyリポジトリのワークフロー
pip-audit -r requirements.txt
gh api repos/kazuhayase/study/dependabot/alerts --jq '.[] | select(.state=="open") | {pkg: .security_vulnerability.package.name, severity: .security_advisory.severity, summary: .security_advisory.summary}'
```

## Gemini向け

Google Cloud（Cloud Run / BigQuery）固有のセキュリティパターンを聞く場合に追加：

```
Google Cloud環境（Cloud Run + BigQuery）でのベストプラクティスも考慮してください。
```

# 使用メモ

- studyリポジトリでは pip-audit + Dependabot API の両方を実行するのが標準
- 修正後は必ずコミット＆プッシュまでセットで行う
- 機密情報（APIキー等）が含まれるコードは貼り付けない
