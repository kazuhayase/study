;; <leaf-install-code>
(eval-and-compile
  (customize-set-variable
   'package-archives '(("org" . "https://orgmode.org/elpa/")
                       ("melpa" . "https://melpa.org/packages/")
                       ("gnu" . "https://elpa.gnu.org/packages/")))
  (package-initialize)
  (unless (package-installed-p 'leaf)
    (package-refresh-contents)
    (package-install 'leaf))

  (leaf leaf-keywords
    :ensure t
    :init
    ;; optional packages if you want to use :hydra, :el-get, :blackout,,,
    (leaf hydra :ensure t)
    (leaf el-get :ensure t)
    (leaf blackout :ensure t)

    :config
    ;; initialize leaf-keywords.el
    (leaf-keywords-init)))
;; </leaf-install-code>

;; Now you can use leaf!


;; customizations written in custom.el
(leaf cus-edit
  :doc "tools for customizing Emacs and Lisp packages"
  :tag "builtin" "faces" "help"
  :custom `((custom-file . ,(locate-user-emacs-file "custom.el"))))

(leaf autorevert
  :doc "revert buffers when files on disk change"
  :tag "builtin"
  :custom ((auto-revert-interval . 0.1))
  :global-minor-mode global-auto-revert-mode)

;; from older .emacs.d (before leaf)

(leaf mozc
  :doc "minor mode to input Japanese with Mozc"
  :tag "input method" "multilingual" "mule"
  :added "2023-05-28"
  :ensure t)

(leaf mozc-temp
  :doc "Use mozc temporarily"
  :req "emacs-24" "dash-2.10.0" "mozc-0"
  :tag "emacs>=24"
  :url "https://github.com/HKey/mozc-temp"
  :added "2023-05-28"
  :emacs>= 24
  :ensure t
  :after mozc
  :bind (("C-j" . mozc-temp-convert)))

(leaf magit
  :doc "A Git porcelain inside Emacs."
  :req "emacs-25.1" "compat-29.1.3.4" "dash-20221013" "git-commit-20230101" "magit-section-20230101" "transient-20230201" "with-editor-20230118"
  :tag "vc" "tools" "git" "emacs>=25.1"
  :url "https://github.com/magit/magit"
  :added "2023-05-29"
  :emacs>= 25.1
  :ensure t
  :after compat git-commit magit-section with-editor)

(leaf desktop
  :doc "save partial status of Emacs when killed"
  :tag "builtin"
  :added "2023-05-29")

(leaf pdf-tools
  :doc "Support library for PDF documents"
  :req "emacs-26.3" "tablist-1.0" "let-alist-1.0.4"
  :tag "multimedia" "files" "emacs>=26.3"
  :url "http://github.com/vedang/pdf-tools/"
  :added "2023-05-30"
  :emacs>= 26.3
  :ensure t
  :after tablist)


(leaf company
  :doc "Modular text completion framework"
  :req "emacs-25.1"
  :tag "matching" "convenience" "abbrev" "emacs>=25.1"
  :url "http://company-mode.github.io/"
  :added "2023-05-30"
  :emacs>= 25.1
  :ensure t)

(leaf math-symbol-lists
  :doc "Lists of Unicode math symbols and latex commands"
  :tag "mathematics" "symbols" "unicode"
  :url "https://github.com/vspinu/math-symbol-lists"
  :added "2023-05-30"
  :ensure t)

(leaf company-math
  :doc "Completion backends for unicode math symbols and latex tags"
  :req "company-0.8.0" "math-symbol-lists-1.3"
  :tag "completion" "symbols" "unicode"
  :url "https://github.com/vspinu/company-math"
  :added "2023-05-30"
  :ensure t
  :after company math-symbol-lists)

(leaf smartchr
  :tag "out-of-MELPA"
  :added "2023-05-30"
  :el-get imakado/emacs-smartchr
  :require t)

;(require 'tex-jp)
;(require 'tex-wizard)

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
    (local-set-key (kbd "\")  (smartchr '("\" "\\" "\[`!!'\]")))
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

(leaf default
  :bind (("C-h" . delete-backward-char)
         ("C-x g" . magit-status)
         ("C-x C-g" . goto-line)
         ("C-x V" . view-file)
         ("C-x B" . buffer-menu)
         ("C-x C-m" . manual-entry)
         ("C-x M" . compile)
         ("C-x H" . help-for-help)
         ))

;; ...

(provide 'init)

;; Local Variables:
;; indent-tabs-mode: nil
;; End:

;;; init.el ends here
