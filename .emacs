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
