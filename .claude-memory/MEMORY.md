# MEMORY (Windows / Cowork)

This directory mirrors the `memory/` directories used on Mac and Debian
(`~/.claude/projects/.../memory/`), but lives inside the repo because
`C:\Users\kazuy\.claude\` is a protected OS path that Cowork sessions cannot mount.

Update this file (and topic-specific `.md` files in this directory) at the end
of each conversation per the rules in `CLAUDE.md` → "Memory — Automatic Update Rules".

## Log

- 2026-06-07: 過去問転記スクリプト実施済み（対象Excelは private の kazuhayase/actuary リポジトリへ移動 2026-07-11）
  分類結果46件を追記（穴埋め18件 #281-298、記述24件 #266-289、計算4件 #155-158）。
  計算問題は画像貼付のため問題・解答欄は空欄、備考に追記予定の旨を記載。
  2004年「問題3(2)」(早期是正措置制度)と「問題2(1)」のレディントン条件式はOCR抽出範囲外の
  ためプレースホルダーあり、原本PDFでの確認が必要。
- 2026-06-07: Cowork環境ではOSの `.claude` フォルダにアクセスできないため、
  メモリ保存先をリポジトリ内 `.claude-memory/` に変更し、CLAUDE.md にルールを追記した。
- 2026-08-02: Windowsクローンの `master` が履歴書き換え前の古い系統のままで、`origin/master`
  と2017年まで遡る乖離（ローカル422 / origin310、うち299件は件名・日付が一致＝書き換え済み）に
  なっていた。ローカル固有の内容は `actuary/`（private kazuhayase/actuary へ移管済み）、
  `work/twitter-bot/token*.txt`（漏洩トークン、origin で削除済み）、`openai-quickstart-python`
  と `vcpkg`（GitHub Pages を壊す壊れた gitlink、origin で削除済み）のみで、push すべき成果物
  なし。**この乖離は merge してはいけない**（削除済みの秘密情報とactuary資料が復活するため）。
  `backup/master-prerewrite-20260802` を作成のうえ `git reset --mixed origin/master`
  ＋ `git checkout -- .` で同期（`--hard` は actuary の実ファイルを消すので使わない）。
  併せて `.claude/worktrees/` を `.gitignore` に追加（gitlink として誤ってステージされていた）。
- 2026-08-02: 主作業機は Mac。Win11 クローン（`C:\Users\kazuy\GitHub\study`）は `master` のみを
  origin に追随させる運用とし、過去セッション由来の `claude/*` ローカルブランチ4本を削除した
  （いずれも origin の方が新しく、内容は完全に吸収済みであることを確認のうえ実施）。
  Win11 では `.git/` 配下の削除が Permission denied になりやすく、`git worktree remove` や
  ブランチ削除後の空ディレクトリ掃除が失敗する。実害はないので放置可、消すなら手動 `rmdir`。
