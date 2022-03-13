;;
;; Emacs共通設定
;;
(set-language-environment 'Japanese)    ; 日本語環境
(set-default-coding-systems 'utf-8-unix)    ; UTF-8 が基本
(set-terminal-coding-system 'utf-8-unix)    ; emacs -nw も文字化けしない
(setq default-file-name-coding-system 'utf-8)
(setq default-process-coding-system '(utf-8 . utf-8))
(prefer-coding-system 'utf-8-unix)
(setq mouse-drag-copy-region t); mouse dragだけでコピー.(m1(st)＋m3(ed)の後M-wは面倒


;; splash screenを無効にする
(setq inhibit-splash-screen t)

;; C-hをbackspaceにする
(global-set-key (kbd "C-h") 'delete-backward-char)

;; キーバインド定義
(define-key global-map (kbd "C-z") 'scroll-down-command)
(define-key global-map (kbd "C-c z") 'suspend-frame)
(define-key global-map (kbd "C-c C-SPC") 'kill-ring-save)

;; ロックファイル / バックアップファイルを作成しない
(setq create-lockfiles nil)
(setq make-backup-files nil)
(setq delete-auto-save-files t)

;; 自動保存ファイルを作成しない
(setq auto-save-default nil)

;; テーマを設定する
(load-theme 'manoj-dark t)

;; 対応するカッコを強調表示
(show-paren-mode t)

;; 時間も表示させる。
;;(display-time)

;; 行番号を常に表示させる
(global-linum-mode)
(setq linum-format "%4d ")
(column-number-mode t)               ; 行番号と列番号を表示する

;; コンパイル時に画面スクロールする
(setq compilation-scroll-output t)

;; .grep拡張子はにgrepモードにする
(add-to-list 'auto-mode-alist
	     (cons "\\.grep$" 'grep-mode))

;; yesと入力するのは面倒なのでyで十分
(defalias 'yes-or-no-p 'y-or-n-p)

;; 行頭でC-kを実行した時に1行削除にする
(setq kill-whole-line t)

;;
;; CUI時の設定
;;
(if (not window-system) (progn
			  ;; 現在行をアンダーライン
			  (setq hl-line-face 'underline)     ; 現在行をアンダーライン
			  (global-hl-line-mode)

			  ))

;;
;; GUI時の設定
;;
(if window-system (progn
		    ;; 現在行に色をつける
		    (global-hl-line-mode t)            ;現在行に色をつける
		    (set-face-background 'hl-line "gray20")

		    ;; 初期フレームの設定
		    (setq initial-frame-alist
			  '((width . 86) (height . 45)))

		    ;; 新規フレームのデフォルト設定
		    (setq default-frame-alist
			  '((width . 86) (height . 45)))

		    ))

;;
;; C/C++言語の設定
;;
(defun my-c-mode-common-init ()
  "C, C++ mode set up function"
  (setq tab-width 4)
  ;; <- 追加
  )

(add-hook 'c-mode-hook 'my-c-mode-common-init)
(add-hook 'c++-mode-hook 'my-c-mode-common-init)

;;
;; パッケージ管理(package.el)を有効にする
;;
(require 'package)
;;(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
;;(add-to-list 'package-archives '("melpa" . "http://melpa.milkbox.net/packages/") t)
;;(add-to-list 'package-archives '("marmalade" . "http://marmalade-repo.org/packages/") t)
(package-initialize)

;;
;; undo-treeの設定
;;
;; undo-tree を読み込む
;;(require 'undo-tree)

;; undo-tree を起動時に有効にする
;;(global-undo-tree-mode t)

;; M-/ をredo に設定する。
;;(global-set-key (kbd "M-/") 'undo-tree-redo)



;;
;; Windows Emacsでの設定
;;
(when (eq system-type 'windows-nt) ; Windows

  ;; markdownビューワの指定
  ;;  (setq markdown-open-command "c:/Tools/MarkCat-win32-x64/MarkCat")
  (setq markdown-open-command "c:/Tools/markcat.bat")

  ;; (set-language-environment "UTF-8") ;; UTF-8 でも問題ないので適宜コメントアウトしてください
  (setq default-input-method "W32-IME")
  (setq-default w32-ime-mode-line-state-indicator "[--]")
  (setq w32-ime-mode-line-state-indicator-list '("[--]" "[あ]" "[--]"))
  (w32-ime-initialize)
  ;; 日本語入力時にカーソルの色を変える設定 (色は適宜変えてください)
  (add-hook 'w32-ime-on-hook '(lambda () (set-cursor-color "coral4")))
  (add-hook 'w32-ime-off-hook '(lambda () (set-cursor-color "black")))

  ;; 以下はお好みで設定してください
  ;; 全てバッファ内で日本語入力中に特定のコマンドを実行した際の日本語入力無効化処理です
  ;; もっと良い設定方法がありましたら issue などあげてもらえると助かります

  ;; ミニバッファに移動した際は最初に日本語入力が無効な状態にする
  (add-hook 'minibuffer-setup-hook 'deactivate-input-method)

  ;; isearch に移行した際に日本語入力を無効にする
  (add-hook 'isearch-mode-hook '(lambda ()
				  (deactivate-input-method)
				  (setq w32-ime-composition-window (minibuffer-window))))
  (add-hook 'isearch-mode-end-hook '(lambda () (setq w32-ime-composition-window nil)))

  ;; helm 使用中に日本語入力を無効にする
  (advice-add 'helm :around '(lambda (orig-fun &rest args)
			       (let ((select-window-functions nil)
				     (w32-ime-composition-window (minibuffer-window)))
				 (deactivate-input-method)
				 (apply orig-fun args))))

  (custom-set-variables
   ;; custom-set-variables was added by Custom.
   ;; If you edit it by hand, you could mess it up, so be careful.
   ;; Your init file should contain only one such instance.
   ;; If there is more than one, they won't work right.
   '(display-time-mode t)
   '(show-paren-mode t))
  (custom-set-faces
   ;; custom-set-faces was added by Custom.
   ;; If you edit it by hand, you could mess it up, so be careful.
   ;; Your init file should contain only one such instance.
   ;; If there is more than one, they won't work right.
   '(default ((t (:family #("ＭＳ ゴシック" 0 7 (charset cp932-2-byte)) :foundry "outline" :slant normal :weight normal :height 120 :width normal)))))
  )

;;
;; macOS Emacsでの設定
;;
(when (eq system-type 'darwin)
  (setq ns-command-modifier (quote meta))

  ;; markdownビューワの指定
  ;;  (setq markdown-open-command "markcat")
  (setq markdown-open-command "marked2")
  )

;;;mozc
(require 'mozc)
(setq default-input-method "japanese-mozc")
;;(global-set-key (kbd "C-j") 'toggle-input-mod)
;;;mozc-temp
(require 'mozc-temp)
(global-set-key (kbd "C-j") #'mozc-temp-convert)

;;; yatex
(require 'yatex)                ;; パッケージ読み込み
(add-to-list 'auto-mode-alist
	     '("\\.tex\\'" . yatex-mode)
	     ) ;;auto-mode-alistへの追加
(add-to-list 'auto-mode-alist
	     '("\\.anki\\'" . yatex-mode)
	     ) ;;auto-mode-alistへの追加

(setq tex-command "latex")       ;; 自分の環境に合わせて""内を変えてください
(setq bibtex-command "bibtex")    ;; 自分の環境に合わせて""内を変えてください
;;reftex-mode
(add-hook 'yatex-mode-hook
          #'(lambda ()
              (reftex-mode 1)
              (define-key reftex-mode-map
                (concat YaTeX-prefix ">") 'YaTeX-comment-region)
              (define-key reftex-mode-map
                (concat YaTeX-prefix "<") 'YaTeX-uncomment-region)))
(setq YaTeX-use-AMS-LaTeX t)



(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(display-time-mode t)
 '(package-archives
   (quote
    (("gnu" . "https://elpa.gnu.org/packages/")
     ("melpa" . "https://melpa.org/packages/"))))
 '(package-selected-packages
   (quote
    (mozc-temp yatex mozc markdown-mode undo-tree auto-complete)))
 '(show-paren-mode t))

(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
