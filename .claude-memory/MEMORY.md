# Memory Index

全マシン共通のメモリ。Mac / Debian は OS 側のパスからこのディレクトリへシンボリックリンク、
Cowork は直接参照する。運用ルールはリポジトリルートの `CLAUDE.md` →「Memory」を参照。

- [project_windows_environment.md](project_windows_environment.md) — **Win11/Cowork固有**: master乖離は**merge禁止**・actuaryはsibling clone・**openpyxlは埋め込み画像を失う→win32com DispatchEx**・G-Drive共有ブックが正本・**この機体はhaya001/github(小文字)でkazuy/GitHub前提の記述と不一致**・**setxは実行中プロセスに反映されない**・**auto mode classifierがgit push/reset --hardを一律ブロック(ユーザー実行が必要)**・**gh CLI/git-filter-repo導入済み(2026-08-25)**・**別ユーザープロファイルのファイルへの生スクリプト書き込みもブロックされるが、CLIコマンド経由なら通る(2026-09-14)**
- [project_repo_setup.md](project_repo_setup.md) — studyリポ設定＋**actuary分離(2026-07-11: private別リポ・同一パスにネスト・他マシン要再クローン)**・gh CLI導入済み・**Cyber/は2026-08-25に一度git完全対象外化したが、2026-10-13に再度private分離(`kazuhayase/Cyber`)へ方針転換・実施済み**
- [project_security_scan.md](project_security_scan.md) — セキュリティスキャン手法（OSV API）・既知CVE・週次ルーティン詳細（trig_01NTDkYt1CRMm9R47ULyoRfQ）
- **(ローカル限定・git管理外)** talent-mgmt-db の進捗メモは勤務先環境の情報を含むため公開リポジトリには置かない。Macローカルの `.claude-memory/` にのみ存在し、`.claude-memory/.gitignore` で除外している
- [project_podcast_agent.md](project_podcast_agent.md) — Podcast要約エージェント（scripts/podcast/）の構成・設計判断・ハマりどころ
- [project_actuary_transcription.md](project_actuary_transcription.md) — 生保2過去問(2019/2018/2005/2004)のExcel転記スクリプト・注意点・手動確認事項
- **(ローカル限定・git管理外)** Cyber/vulndb のプロジェクトメモは `kazuhayase/Cyber`（private repo）の `.claude-memory/project_cyber_vulndb.md` に移行済み（2026-10-13）。詳細は [[project-repo-setup]] 参照
- [project_seiho2_yosou.md](project_seiho2_yosou.md) — 生保2予想問題: Phase 7監査・配布パッケージ完了(2026-07-09)・表記ポリシー・コーパス実態(ページオフセット実測/pdf_direct_read)・全工程完了(2026-07-10)・e-Gov法令API突合ノウハウ・ミラーの払戻積立金欠落に注意
