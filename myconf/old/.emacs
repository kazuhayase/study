(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(compile-command "g++ -g -O0")
 '(exec-path (quote ("/usr/bin" "/bin" "/usr/sbin" "/sbin" "/Applications/Emacs.app/Contents/MacOS/libexec" "/Applications/Emacs.app/Contents/MacOS/bin" "/usr/local/bin")))
 '(kill-whole-line t))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

(setq inhibit-splash-screen t)
(cd "~/")

;; key definitions
(define-key global-map "\C-x\C-g" 'goto-line)
(define-key global-map "\C-xV" 'view-file)
(define-key global-map "\C-xB" 'buffer-menu)
(define-key global-map "\C-xI" 'ispell-buffer)
(define-key global-map "\C-x\C-m" 'manual-entry)
;;(define-key global-map "\C-xG" 'gdb)
(define-key global-map "\C-xG" 'gud-gdb)
(define-key global-map "\C-xM" 'compile)

(global-set-key "\C-xH" 'help-for-help)

;; add 'buffer name' to compile command
;;http://forums.devshed.com/other-programming-languages-139/emacs-lisp-buffer-name-as-part-of-compile-command-390389.html

(add-hook 'java-mode-hook
	  (lambda()
	    (set (make-local-variable 'compile-command) (concat "javac " (buffer-name)))))
(add-hook 'c++-mode-hook
	  (lambda()
	    (set (make-local-variable 'compile-command) (concat "g++ -g -O0 " (buffer-name)))))

;; Mac用フォント設定
;; http://tcnksm.sakura.ne.jp/blog/2012/04/02/emacs/

 ;; 英語
 (set-face-attribute 'default nil
             :family "Menlo" ;; font
             :height 150)    ;; font size

;; 日本語
(set-fontset-font
 nil 'japanese-jisx0208
;; (font-spec :family "Hiragino Mincho Pro")) ;; font
  (font-spec :family "Hiragino Kaku Gothic ProN")) ;; font

;; 半角と全角の比を1:2にしたければ
(setq face-font-rescale-alist
;;        '((".*Hiragino_Mincho_pro.*" . 1.2)))
      '((".*Hiragino_Kaku_Gothic_ProN.*" . 1.2)));; Mac用フォント設定

;; 2014/09/15
;; auto-complete-mode
;; http://cx4a.org/software/auto-complete/manual.ja.html
(add-to-list 'load-path "~/.emacs.d/")
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "~/.emacs.d//ac-dict")
(ac-config-default)
