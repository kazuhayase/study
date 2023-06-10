;; this enables this running method
;;   emacs -q -l ~/.debug.emacs.d/{{pkg}}/init.el
(eval-and-compile
  (when (or load-file-name byte-compile-current-file)
    (setq user-emacs-directory
          (expand-file-name
           (file-name-directory (or load-file-name byte-compile-current-file))))))

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

(leaf leaf
  :config
  (leaf leaf-convert :ensure t)
  (leaf leaf-tree
    :ensure t
    :custom ((imenu-list-size . 30)
             (imenu-list-position . 'left))))

(leaf macrostep
  :ensure t
  :bind (("C-c e" . macrostep-expand)))

;; customizations written in custom.el

(setq custom-file "~/.emacs.d/custom.el")
(load custom-file)

;; (leaf cus-edit
;;   :doc "tools for customizing Emacs and Lisp packages"
;;   :tag "builtin" "faces" "help"
;;   :custom `((custom-file . ,(locate-user-emacs-file "custom.el"))))

(leaf autorevert
  :doc "revert buffers when files on disk change"
  :tag "builtin"
  :custom ((auto-revert-interval . 0.1))
  :global-minor-mode global-auto-revert-mode)

;; from older .emacs.d (before leaf)

(leaf migemo
  :doc "Japanese incremental search through dynamic pattern expansion"
  :req "cl-lib-0.5"
  :url "https://github.com/emacs-jp/migemo"
  :added "2023-06-03"
  :ensure t)

(leaf leaf-convert
  :require migemo
  :setq ((migemo-command . "cmigemo")
	 (migemo-options quote
			 ("-q" "--emacs"))
	 (migemo-dictionary . "/usr/share/cmigemo/utf-8/migemo-dict")
	 (migemo-user-dictionary)
	 (migemo-regex-dictionary)
	 (migemo-coding-system quote utf-8-unix))
  :config
  (load-library "migemo")
  (migemo-init))


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

(leaf leaf-convert
  :bind (([zenkaku-hankaku]
	  . toggle-input-method))
  :require mozc
  :setq ((default-input-method . "japanese-mozc"))
  :config
  (set-language-environment "Japanese"))

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


;;(require 'yatex)
;;(require 'reftex)
;;(require 'company)

(leaf leaf-convert
  :config
  (leaf company
    :ensure t
    :bind ((company-active-map
	    ("C-n" . company-select-next)
	    ("C-p" . company-select-previous)
	    ("C-s" . company-filter-candidates)
	    ("<tab>" . company-complete-selection))
	   (company-search-map
	    ("C-n" . company-select-next)
	    ("C-p" . company-select-previous)))
    :config
    (with-eval-after-load 'company
      (global-company-mode)
      (setq company-idle-delay 0)
      (setq company-minimum-prefix-length 2)
      (setq company-selection-wrap-around t)
      (setq company-show-quick-access t)))

  (leaf company-tabnine
    :ensure t
    :require t
    :config
    (add-to-list 'company-backends #'company-tabnine)))


(leaf yatex
  :doc "Yet Another tex-mode for emacs //野鳥//"
  :added "2023-05-30"
  :ensure t)
(leaf reftex
  :doc "minor mode for doing \\label, \\ref, \\cite, \\index in LaTeX"
  :tag "builtin"
  :added "2023-05-30")

(leaf yatex
  :ensure t
  :mode ("\\.tex$" "\\.ltx$" "\\.cls$" "\\.sty$" "\\.clo$" "\\.bbl$")
  :setq ((YaTeX-inhibit-prefix-letter . t))
  :config
  (with-eval-after-load 'yatex
    (setq YaTeX-kanji-code nil)
    (setq YaTeX-latex-message-code 'utf-8)
    (setq YaTeX-use-LaTeX2e t)
    (setq YaTeX-use-AMS-LaTeX t)
    (setq tex-command "/usr/local/texlive/current/bin/x86_64-linux/latexmk")
    (setq tex-pdfview-command "evince")
    (auto-fill-mode 0)
    (set
     (make-local-variable 'company-backends)
     '(company-tabnine))))

(leaf latex-math-preview
  :doc "preview LaTeX mathematical expressions."
  :tag "tex" "latex"
  :url "https://gitlab.com/latex-math-preview/latex-math-preview"
  :added "2023-06-09"
  :ensure t)

; https://www.emacswiki.org/emacs/LaTeXMathPreview

(add-hook 'yatex-mode-hook
         '(lambda ()
         (YaTeX-define-key "\C-p" 'latex-math-preview-expression)
;         (YaTeX-define-key "\C-p" 'latex-math-preview-save-image-file)
         (YaTeX-define-key "\C-j" 'latex-math-preview-insert-symbol)
;         (YaTeX-define-key "\C-j" 'latex-math-preview-last-symbol-again)
         (YaTeX-define-key "\C-b" 'latex-math-preview-beamer-frame)))
(setq latex-math-preview-in-math-mode-p-func 'YaTeX-in-math-mode-p)

; https://qiita.com/sinnershiki/items/73eff367bf0803ab585f#fn1

(leaf popwin
  :doc "Popup Window Manager"
  :req "emacs-24.3"
  :tag "convenience" "emacs>=24.3"
  :url "https://github.com/emacsorphanage/popwin"
  :added "2023-06-10"
  :emacs>= 24.3
  :ensure t)

(require 'popwin)
(setq display-buffer-function 'popwin:display-buffer)
(setq popwin:popup-window-position 'bottom)
;(push '("*quickrun*") popwin:special-display-config)
;(push '("*Google Translate*") popwin:special-display-config)
(push '("*latex-math-preview-expression*") popwin:special-display-config)

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
