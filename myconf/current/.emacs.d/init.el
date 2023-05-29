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

(require 'tex-jp)
(require 'tex-wizard)

(leaf tex-jp
  :after t
  :require t tex-wizard
  :hook ((LaTeX-mode-hook . japanese-latex-mode))
  :setq ((japanese-TeX-engine-default quote uptex)
	 (japanese-LaTeX-default-style . "jlreq")
	 (TeX-engine quote uptex)
	 (TeX-PDF-from-DVI . "Dvipdfmx")
	 (TeX-view-program-selection quote
				     ((output-pdf "Evince")))
	 (TeX-source-correlate-method quote synctex)
	 (TeX-source-correlate-start-server . t)
	 (TeX-source-correlate-mode . t)
	 (reftex-plug-into-AUCTeX . t))
  :config
  (dolist (command
;;	   '("pTeX" "pLaTeX" "pBibTeX" "jTeX" "jLaTeX" "jBibTeX" "Mendex"))
    	   '("upTeX" "upLaTeX" "upBibTeX" "jTeX" "jLaTeX" "jBibTeX" "Mendex"))
    (delq
     (assoc command TeX-command-list)
     TeX-command-list))
  (with-eval-after-load 'tex-jp
    (add-hook 'LaTeX-mode-hook 'LaTeX-math-mode))

  (add-hook 'LaTeX-mode-hook
	    #'(lambda nil
		(add-to-list 'TeX-command-list
			     '("Latexmk" "latexmk %t" TeX-run-TeX nil
			       (latex-mode)
			       :help "Run Latexmk"))
		(add-to-list 'TeX-command-list
			     '("Latexmk-upLaTeX" "latexmk -e '$latex=q/uplatex %%O %(file-line-error) %(extraopts) %S %(mode) %%S/' -e '$bibtex=q/upbibtex %%O %%B/' -e '$biber=q/biber %%O --bblencoding=utf8 -u -U --output_safechars %%B/' -e '$makeindex=q/upmendex %%O -o %%D %%S/' -e '$dvipdf=q/dvipdfmx %%O -o %%D %%S/' -norc -gg -pdfdvi %t" TeX-run-TeX nil
			       (latex-mode)
			       :help "Run Latexmk-upLaTeX"))
		(add-to-list 'TeX-command-list
			     '("Latexmk-LuaLaTeX" "latexmk -e '$lualatex=q/lualatex %%O %(file-line-error) %(extraopts) %S %(mode) %%S/' -e '$bibtex=q/upbibtex %%O %%B/' -e '$biber=q/biber %%O --bblencoding=utf8 -u -U --output_safechars %%B/' -e '$makeindex=q/upmendex %%O -o %%D %%S/' -norc -gg -pdflua %t" TeX-run-TeX nil
			       (latex-mode)
			       :help "Run Latexmk-LuaLaTeX"))
		(add-to-list 'TeX-command-list
			     '("Xdg-open" "xdg-open %s.pdf" TeX-run-discard-or-function t t :help "Run xdg-open"))
		(add-to-list 'TeX-command-list
		;	     '("Evince" "TeX-evince-sync-view" TeX-run-discard-or-function t t :help "Forward search with Evince"))
                             '("Evince" "synctex view -i \"%n:0:%b\" -o %s.pdf -x \"evince -i %%{page+1} %%{output}\"" TeX-run-discard-or-function t t :help "Forward search with Evince"))
		(add-to-list 'TeX-command-list
			     '("Fwdevince" "fwdevince %s.pdf %n \"%b\"" TeX-run-discard-or-function t t :help "Forward search with fwdevince"))
		(add-to-list 'TeX-command-list
			     '("Atril" "TeX-atril-sync-view" TeX-run-discard-or-function t t :help "Forward search with Atril"))
		(add-to-list 'TeX-command-list
			     '("Okular" "okular --unique \"file:\"%s.pdf\"#src:%n %a\"" TeX-run-discard-or-function t t :help "Forward search with Okular"))
		(add-to-list 'TeX-command-list
			     '("Zathura" "zathura -x \"emacsclient --no-wait +%%{line} %%{input}\" --synctex-forward \"%n:0:%b\" %s.pdf" TeX-run-discard-or-function t t :help "Forward and inverse search with zathura"))
		(add-to-list 'TeX-command-list
			     '("Qpdfview" "qpdfview --unique \"\"%s.pdf\"#src:%b:%n:0\"" TeX-run-discard-or-function t t :help "Forward search with qpdfview"))
		(add-to-list 'TeX-command-list
			     '("TeXworks" "synctex view -i \"%n:0:%b\" -o %s.pdf -x \"texworks --position=%%{page+1} %%{output}\"" TeX-run-discard-or-function t t :help "Forward search with TeXworks"))
		(add-to-list 'TeX-command-list
			     '("TeXstudio" "synctex view -i \"%n:0:%b\" -o %s.pdf -x \"texstudio --pdf-viewer-only --page %%{page+1} %%{output}\"" TeX-run-discard-or-function t t :help "Forward search with TeXstudio"))
		(add-to-list 'TeX-command-list
			     '("MuPDF" "mupdf %s.pdf" TeX-run-discard-or-function t t :help "Run MuPDF"))
		(add-to-list 'TeX-command-list
			     '("Firefox" "firefox -new-window %s.pdf" TeX-run-discard-or-function t t :help "Run Mozilla Firefox"))
		(add-to-list 'TeX-command-list
			     '("Chromium" "chromium --new-window %s.pdf" TeX-run-discard-or-function t t :help "Run Chromium"))
		(add-to-list 'TeX-command-list
			     '("Acrobat" "wine64 cmd /c start Acrobat.exe %s.pdf" TeX-run-discard-or-function t t :help "Run Adobe Acrobat Reader"))))
  (with-eval-after-load 'tex-jp
    (add-hook 'LaTeX-mode-hook 'turn-on-reftex)))


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
