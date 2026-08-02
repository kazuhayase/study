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
- 2026-08-02: `actuary/` は study.git とは**独立したリポジトリ** `kazuhayase/actuary`（private）で、
  study 側では `.gitignore` により除外＋Mac ではネストした clone として配置されている。
  よって seiho2-anaume 等の作業には actuary.git を別途 clone/pull する必要があり、
  study の pull だけでは `actuary/` 配下は一切更新されない。
  Win11 では **`C:\Users\kazuy\GitHub\actuary` に sibling として clone 済み**（Mac のネスト構成とは
  異なる。study 配下の旧 `actuary/` を触らずに済むためこちらを採用）。
  study 配下にあった移管前の取り残しファイル群（175ファイル / 88.6 MB）は照合の結果、
  `2026年度生保2暗記集_local.xlsx` の blob が actuary.git の `807c2c9`（2026-06-28）と完全一致し、
  その後 2026-07-10 の編集2件（`c3503f9`, `c1bddf2`）で上書きされているため固有の内容なしと確認、削除した。
  照合には SHA256 ではなく `git hash-object` と `git rev-parse <commit>:<path>` の blob 比較が有効
  （xlsx は zip のため内容が同じでも保存時刻で SHA256 が変わる）。
- 2026-08-02: 「Mac が cd2cd3e のまま」という話は **study.git ではなく actuary.git のコミット**だった。
  マシン間でコミットハッシュの話をするときは、study と actuary のどちらのリポジトリかを必ず確認すること。
  actuary.git には `session_lessons.md` があり、セッション開始時に読み・終了時に更新する運用が
  リポジトリ側で指示されている（コミット `e1bc1f7`）。actuary 側の作業時は確認すること。
- 2026-08-02: **xlsx を openpyxl で保存すると埋め込み画像が失われる**。暗記集Excelは実際に
  画像60枚→21枚に欠落していた（計算問題は画像貼付のため実害大）。Win11 には Excel 2016 と
  pywin32 があるので、画像・図形を保つ書き換えは `win32com.client.DispatchEx('Excel.Application')`
  を使う（`DispatchEx` はユーザーが開いている Excel セッションと分離した新インスタンスになる）。
  検証は zip 内 `xl/media/` の数と `xl/drawings/_rels/*.rels` の Relationship 数で行う。
  openpyxl が無い場合は `python -m pip install openpyxl` で入る（pip 24.0 / Python 3.11）。
- 2026-08-02: アク研の暗記集Excelの**正本は G-Drive 上の共有ブック**
  `G:\マイドライブ\アク研生保2次資料\2026年度_v2\生保2\2026年度生保2暗記集.xlsx` で、
  actuary リポジトリの `_local` はその派生コピー。共有ブックには他担当者の追記が入り続けるため、
  `_local` を丸ごと書き戻してはいけない。詳細な運用は actuary.git の
  `2026/seiho2-anaume/pipeline/output/inventory/session_lessons.md` に記載（コミット `2c40ab3`）。
  G-Drive のファイルは別プロセスがロックしていることがあり、`Copy-Item` が失敗する場合は
  `[System.IO.File]::Open($src,'Open','Read','ReadWrite')` の共有読み取りでコピーできる。
