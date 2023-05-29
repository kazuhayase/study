;;; mozc-temp-autoloads.el --- automatically extracted autoloads
;;
;;; Code:

(add-to-list 'load-path (directory-file-name
                         (or (file-name-directory #$) (car load-path))))


;;;### (autoloads nil "mozc-temp" "mozc-temp.el" (0 0 0 0))
;;; Generated autoloads from mozc-temp.el

(autoload 'mozc-temp-convert "mozc-temp" "\
Convert the current word with mozc.

\(fn)" t nil)

(autoload 'mozc-temp-convert-dwim "mozc-temp" "\
Convert the current word or start a mozc-temp session.
If there is a prefix string, this function calls `mozc-temp-convert'.
If not, this function starts a mozc-temp session.

\(fn)" t nil)

(if (fboundp 'register-definition-prefixes) (register-definition-prefixes "mozc-temp" '("mozc-temp-")))

;;;***

;; Local Variables:
;; version-control: never
;; no-byte-compile: t
;; no-update-autoloads: t
;; coding: utf-8
;; End:
;;; mozc-temp-autoloads.el ends here
