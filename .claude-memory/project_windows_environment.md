---
name: project-windows-environment
description: Win11クローンの運用方針・master乖離の扱い・Windows固有のExcel/Git注意点（Mac側には無い知見）
metadata:
  type: project
---

Windows (Win11, `C:\Users\kazuy\GitHub\study`) と Cowork 環境の固有事項。
2026-08-21 に `.claude-memory/MEMORY.md` のログ形式から、ファイル単位の規約へ移行したもの。
**主作業機は Mac**。Windows は補助。

## Git 運用

- **Win11 クローンは `master` のみを origin に追随させる**運用。過去セッション由来の
  `claude/*` ローカルブランチ4本は削除済み（origin の方が新しく内容も吸収済みと確認のうえ実施）
- **2026-08-02 の master 乖離は絶対に merge してはいけない。** Windows の `master` が履歴書き換え
  前の古い系統のままで、`origin/master` と2017年まで遡る乖離（ローカル422 / origin 310、うち
  299件は件名・日付が一致＝書き換え済み）になっていた。merge すると
  **削除済みの漏洩トークンと actuary 資料が復活する**
  - ローカル固有だったのは `actuary/`（private リポへ移管済み）、
    `work/twitter-bot/token*.txt`（漏洩トークン、origin で削除済み）、
    `openai-quickstart-python` と `vcpkg`（GitHub Pages を壊す壊れた gitlink、origin で削除済み）
    のみで push すべき成果物は無かった
  - 対処: `backup/master-prerewrite-20260802` を作成のうえ `git reset --mixed origin/master`
    ＋ `git checkout -- .` で同期。**`--hard` は actuary の実ファイルを消すので使わない**
  - 併せて `.claude/worktrees/` を `.gitignore` に追加（gitlink として誤ってステージされていた）
- Win11 では `.git/` 配下の削除が Permission denied になりやすく、`git worktree remove` や
  ブランチ削除後の空ディレクトリ掃除が失敗する。実害は無いので放置可、消すなら手動 `rmdir`

## actuary リポジトリの配置がMacと違う

`actuary/` は study.git とは**独立した private リポジトリ** `kazuhayase/actuary`。
study の pull だけでは `actuary/` 配下は一切更新されない。

- **Win11: `C:\Users\kazuy\GitHub\actuary` に sibling として clone 済み**
  （Mac のネスト構成とは異なる。study 配下の旧 `actuary/` を触らずに済むためこちらを採用）
- study 配下にあった移管前の取り残し（175ファイル / 88.6 MB）は照合のうえ削除済み
- **xlsx の同一性照合に SHA256 を使わないこと**（zip なので内容が同じでも保存時刻でハッシュが変わる）。
  `git hash-object` と `git rev-parse <commit>:<path>` の blob 比較を使う
- 「Mac が cd2cd3e のまま」という話は **study.git ではなく actuary.git のコミット**だった。
  マシン間でコミットハッシュを話題にするときは、study と actuary のどちらかを必ず確認する
- actuary.git には `session_lessons.md` があり、セッション開始時に読み・終了時に更新する運用が
  リポジトリ側で指示されている（コミット `e1bc1f7`）

## Excel: openpyxl は埋め込み画像を失う

**`xlsx` を openpyxl で保存すると埋め込み画像が失われる。** 暗記集Excelで実際に
画像60枚→21枚に欠落した（計算問題は画像貼付のため実害大）。

- Win11 には Excel 2016 と pywin32 があるので、画像・図形を保つ書き換えは
  `win32com.client.DispatchEx('Excel.Application')` を使う
  （`DispatchEx` はユーザーが開いている Excel セッションと分離した新インスタンスになる）
- 検証は zip 内 `xl/media/` の数と `xl/drawings/_rels/*.rels` の Relationship 数で行う
- openpyxl が無い場合は `python -m pip install openpyxl`（pip 24.0 / Python 3.11）

## アク研暗記集の正本は G-Drive 側

正本は **G-Drive 上の共有ブック**
`G:\マイドライブ\アク研生保2次資料\2026年度_v2\生保2\2026年度生保2暗記集.xlsx`。
actuary リポジトリの `_local` はその派生コピー。

- 共有ブックには**他担当者の追記が入り続けるため、`_local` を丸ごと書き戻してはいけない**
- 詳細な運用は actuary.git の
  `2026/seiho2-anaume/pipeline/output/inventory/session_lessons.md` に記載（コミット `2c40ab3`）
- G-Drive のファイルは別プロセスがロックしていることがあり、`Copy-Item` が失敗する場合は
  `[System.IO.File]::Open($src,'Open','Read','ReadWrite')` の共有読み取りでコピーできる

## 過去問転記の状況（2026-06-07 時点）

対象Excelは private の `kazuhayase/actuary` へ移動済み（2026-07-11）。
分類結果46件を追記（穴埋め18件 #281-298、記述24件 #266-289、計算4件 #155-158）。
計算問題は画像貼付のため問題・解答欄は空欄で、備考に追記予定の旨を記載。
2004年「問題3(2)」（早期是正措置制度）と「問題2(1)」のレディントン条件式は
OCR抽出範囲外のためプレースホルダーあり、**原本PDFでの確認が必要**。

## この Windows 機はパスが従来メモリの記述と違う

これまでのメモリ/`CLAUDE.md` の Windows 向け記述は `C:\Users\kazuy\GitHub\study`
(ユーザー名 `kazuy`)を前提にしているが、**この機体は `C:\Users\haya001\github\study`**
(ユーザー名 `haya001`、`github` は小文字)。同一人物の別アカウント名と思われる。

- `.claude\projects\...\memory` への symlink 用コマンド(`CLAUDE.md` 記載)はこのパス前提の
  ままだと動かない。実際に `mklink` を試みたところ auto mode の classifier に拒否された
  (`.claude\projects` 配下への rmdir/mklink が risky 判定)ため、この機体では symlink 化を
  諦めて `.claude-memory/` を直接読み書きする運用にした(`CLAUDE.md` の fallback方針どおり)
- セッションの実 cwd は `C:\Users\haya001\github`(study の親)で起動されており、
  ハーネス組み込みの自動メモリは `C:\Users\haya001\.claude\projects\C--Users-haya001-github\memory`
  に対応する — study 固有ではなく `github` 配下全体で共有される点に注意
- python は `py` ランチャー経由(`C:\Users\haya001\AppData\Local\Python\pythoncore-3.14-64\`)。
  Git Bash から素の `python`/`python3` を呼ぶと Microsoft Store のスタブが応答し失敗する。
  Bash からは PowerShell 経由で `py` を叩くか、`.venv/Scripts/python.exe` を直接パス指定する
- `uv` は未インストール。`python -m venv` + `pip install` で代用可能(Python 3.14 は
  pyproject.toml の `>=3.13` を満たす)

## NVD_API_KEY の setx は既存プロセスに効かない

`setx NVD_API_KEY "..."` はレジストリ(`HKCU\Environment`)に書き込むだけで、**既に起動済みの
プロセスには一切反映されない**。Claude Code のツール実行シェル(このセッションの
PowerShell/Bash)もその一つで、そこから子プロセスとして新しい `powershell` を起動しても
親の古い環境を引き継ぐため反映されない(実際に試して確認済み、2026-08-21)。

- 反映させるには、このツールとは無関係に**新しく開いたターミナルウィンドウ**か、
  Claude Code セッション自体の再起動が必要
- レジストリに正しく書き込まれたかどうかは
  `[System.Environment]::GetEnvironmentVariable("NVD_API_KEY", "User")` で(子プロセスを
  介さず)直接確認できる — こちらは即座に反映を見られる
- 今のセッション内だけで使いたい場合は `$env:NVD_API_KEY = "..."` で都度設定する

## Cowork 環境

OS の `C:\Users\kazuy\.claude\` は保護されたパスで Cowork セッションにマウントできない。
そのため `.claude-memory/` をリポジトリ内に置く方式を 2026-06-07 に採用した。
2026-08-21 に全マシンがこの方式へ統一された（Mac/Debian は OS パスからのシンボリックリンク）。

関連: [[project-repo-setup]] [[project-actuary-transcription]] [[project-seiho2-yosou]]
