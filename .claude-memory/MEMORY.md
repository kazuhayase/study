# Memory Index

全マシン共通のメモリ。Mac / Debian は OS 側のパスからこのディレクトリへシンボリックリンク、
Cowork は直接参照する。運用ルールはリポジトリルートの `CLAUDE.md` →「Memory」を参照。

- [project_windows_environment.md](project_windows_environment.md) — **Win11/Cowork固有**: master乖離は**merge禁止**・actuaryはsibling clone・**openpyxlは埋め込み画像を失う→win32com DispatchEx**・G-Drive共有ブックが正本・**この機体はhaya001/github(小文字)でkazuy/GitHub前提の記述と不一致**・**setxは実行中プロセスに反映されない**・**auto mode classifierがgit push/reset --hardを一律ブロック(ユーザー実行が必要)**・**gh CLI/git-filter-repo導入済み(2026-08-25)**
- [project_repo_setup.md](project_repo_setup.md) — studyリポ設定＋**actuary分離(2026-07-11: private別リポ・同一パスにネスト・他マシン要再クローン)**・gh CLI導入済み・**Cyber/はgit完全対象外化(2026-08-25実施: private分離→撤回・削除→study履歴からfilter-repo除去+force-push完了)**
- [project_security_scan.md](project_security_scan.md) — セキュリティスキャン手法（OSV API）・既知CVE・週次ルーティン詳細（trig_01NTDkYt1CRMm9R47ULyoRfQ）
- **(ローカル限定・git管理外)** talent-mgmt-db の進捗メモは勤務先環境の情報を含むため公開リポジトリには置かない。Macローカルの `.claude-memory/` にのみ存在し、`.claude-memory/.gitignore` で除外している
- [project_podcast_agent.md](project_podcast_agent.md) — Podcast要約エージェント（scripts/podcast/）の構成・設計判断・ハマりどころ
- [project_actuary_transcription.md](project_actuary_transcription.md) — 生保2過去問(2019/2018/2005/2004)のExcel転記スクリプト・注意点・手動確認事項
- [project_cyber_vulndb.md](project_cyber_vulndb.md) — Cyber/vulndb: BOD 26-04脆弱性優先度DB構築＋**全38万件ロード完了**(2026-08-25, このWindows機で実測: silver.cve 382,270件)・**DuckDBのexecutemanyは1800行/秒で激遅→bulk_insert必須**・cisa.govはUA必須・NVDがSSVC同梱・SSVCカバレッジは年次で13〜99%と激差・**ベンダーアドバイザリ(AWS/MS/Broadcom/IBM)実装**(gold非統合)・MSRCはAccept:application/json必須・**http.pyにIncompleteRead/JSON truncation retry・NVD/IBMにレジューム機能を追加**(2026-08-25)・**Cyber/は git 完全対象外(private repoも撤回)、CI(`cyber-vulndb-update.yml`)は要対応**
- [project_seiho2_yosou.md](project_seiho2_yosou.md) — 生保2予想問題: Phase 7監査・配布パッケージ完了(2026-07-09)・表記ポリシー・コーパス実態(ページオフセット実測/pdf_direct_read)・全工程完了(2026-07-10)・e-Gov法令API突合ノウハウ・ミラーの払戻積立金欠落に注意
