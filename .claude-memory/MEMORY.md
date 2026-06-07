# MEMORY (Windows / Cowork)

This directory mirrors the `memory/` directories used on Mac and Debian
(`~/.claude/projects/.../memory/`), but lives inside the repo because
`C:\Users\kazuy\.claude\` is a protected OS path that Cowork sessions cannot mount.

Update this file (and topic-specific `.md` files in this directory) at the end
of each conversation per the rules in `CLAUDE.md` → "Memory — Automatic Update Rules".

## Log

- 2026-06-07: actuary/2026/2026年度生保2暗記集.xlsx に過去問(2019・2018・2005・2004年)の
  分類結果46件を追記（穴埋め18件 #281-298、記述24件 #266-289、計算4件 #155-158）。
  計算問題は画像貼付のため問題・解答欄は空欄、備考に追記予定の旨を記載。
  2004年「問題3(2)」(早期是正措置制度)と「問題2(1)」のレディントン条件式はOCR抽出範囲外の
  ためプレースホルダーあり、原本PDFでの確認が必要。
- 2026-06-07: Cowork環境ではOSの `.claude` フォルダにアクセスできないため、
  メモリ保存先をリポジトリ内 `.claude-memory/` に変更し、CLAUDE.md にルールを追記した。
