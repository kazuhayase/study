(eval-when-compile
  (require 'latex-math-preview nil t)
  (require 'reftex nil t)
  (require 'tex nil t)
  (require 'tex-jp nil t)
  (require 'preview nil t))

(eval-when-compile (setq byte-compile-warnings '(cl-functions)))

;; https://mytexpert.osdn.jp/index.php?Emacs/AUCTeX#fd84843a
(setq TeX-auto-save t) ; Enable parse on load.
(setq TeX-parse-self t) ; Enable parse on save.
;; (setq-default TeX-master nil) ;; 単一のtexを触る場合は特に設定せずともよい

;; 日本語設定
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (setq TeX-default-mode 'japanese-latex-mode)
              (setq japanese-TeX-engine-default 'uptex)))

;; LaTeXでタイプセット→Dvipdfmx→Viewの流れが基本の処理の流れ
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (setq TeX-PDF-mode t)
              (setq TeX-PDF-from-DVI "Dvipdfmx")))

;; コンパイル後にビューワー表示の自動リフレッシュ
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (add-hook 'TeX-after-compilation-finished-functions
                        #'TeX-revert-document-buffer)))

;; pdf-toolsと連携する場合のビューワー設定 (C-c C-v)
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (setq TeX-view-program-selection
                    '((output-pdf "PDF Tools")))
              (setq TeX-view-program-list
                    '(("PDF Tools" TeX-pdf-tools-sync-view)))))

;; 以下を有効にする w/ pdf-tools
;; - forward search (texソースから対応するPDF位置にジャンプ)
;; - backward search (PDFから対応するtexソースまでジャンプ)
;; forward search は C-c C-g
;; backward searchは Ctrl + 左クリック
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (setq TeX-source-correlate-method 'synctex)
              (setq TeX-source-correlate-start-server t)

              ;; pdf-toolsと連携する場合
              (with-eval-after-load "pdf-sync"
                (define-key TeX-source-correlate-map (kbd "C-c C-g")
                  'pdf-sync-forward-search))))
(add-hook 'TeX-mode-hook #'TeX-source-correlate-mode)

;; Evinceと連携する場合のビューワー設定 (C-c C-v)
;; (add-hook 'TeX-mode-hook
;;           #'(lambda ()
;;               (setq TeX-view-program-selection
;;                     '((output-pdf "Evince")))))

;; AUCTeX で PDF をコマンド一つで生成する
;; https://qiita.com/tm_tn/items/cbc813028d7f5951b165
;; https://github.com/tom-tan/auctex-latexmk
;; (require 'auctex-latexmk)
;; (auctex-latexmk-setup)
;; (add-hook 'TeX-mode-hook 'auctex-latexmk-setup)
;; (add-hook 'TeX-mode-hook
;;           #'(lambda ()
;;               (setq TeX-command-default "LatexMk")))

;; 単にlatexmkを走らせる目的ならば以下を追記してLatexmkコマンドとして使う
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (add-to-list
               'TeX-command-list
               '("Latexmk"
                 "latexmk %t"
                 TeX-run-TeX nil (latex-mode) :help "Run Latexmk"))))

;; スペルチェック
(add-hook 'TeX-mode-hook #'flyspell-mode)

;; 数学記号まわり
(add-hook 'TeX-mode-hook #'LaTeX-math-mode)

;; 画像挿入
(add-hook 'TeX-mode-hook #'auto-image-file-mode)

;; rextex
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (turn-on-reftex)
              (setq reftex-plug-into-AUCTeX t)
              (setq reftex-toc-split-windows-horizontally t)
              (setq reftex-toc-split-windows-fraction 0.3)))

;; アウトラインモード （sectionやsubsectionなどの見出し確認・折りたたみ）
(add-hook 'TeX-mode-hook #'(lambda () (outline-minor-mode t)))

;; 要dvipng
(with-eval-after-load 'latex-math-preview
  (setq latex-math-preview-in-math-mode-p-func
        'latex-math-preview-in-math-mode-p)
  (setq latex-math-preview-tex-to-png-for-preview '(platex dvipng))
  (setq latex-math-preview-tex-to-png-for-save '(platex dvipng))
  (setq latex-math-preview-tex-to-eps-for-save '(platex dvips-to-eps))
  (setq latex-math-preview-beamer-to-png '(platex dvipdfmx gs-to-png)))

;; 数学記号の補完
(eval-when-compile (require 'company-math))
(defun company-math-mode-setup ()
  (require 'company-math)
  (setq-local company-backends
              (append '((company-math-symbols-latex company-latex-commands))
                      company-backends)))
(add-hook 'TeX-mode-hook #'company-math-mode-setup)

;; インライン数式を入力する際、
;; タイプが煩わしいのでバックスラッシュや左ブレース連打で展開できるようにしたい
;; →smartchrを用いて実現
(eval-when-compile (require 'smartchr))
(declare-function smartchr "smartchr")
(when (require 'smartchr nil t)
  (defun smartchr-keybindings-auctex ()
    (local-set-key (kbd "\\")  (smartchr '("\\" "\\\\" "\\[`!!'\\]")))
    (local-set-key (kbd "{")  (smartchr '("{`!!'}"))))
  (add-hook 'TeX-mode-hook #'smartchr-keybindings-auctex))

;; インラインプレビュー時にdvipngを用いて高速化
(add-hook 'TeX-mode-hook #'(lambda ()
                             (setq preview-image-type 'dvipng)))

;; インラインプレビュー時におけるsectionの文字化けを回避
(add-hook 'TeX-mode-hook
          #'(lambda ()
              (setq preview-default-option-list
                    '("displaymath" "floats" "graphics"
                      "textmath" "footnotes"))))
