OS := $(shell uname -s 2>/dev/null || echo Windows)

.PHONY: setup install-gitleaks install-pre-commit

## 初回セットアップ: make setup
setup: install-gitleaks install-pre-commit
	pre-commit install
	@echo ""
	@echo "Setup complete! gitleaks pre-commit hook is now active."

install-gitleaks:
ifeq ($(OS), Darwin)
	brew install gitleaks
else ifeq ($(OS), Linux)
	@echo "Installing gitleaks (latest) for Linux..."
	@LATEST=$$(curl -fsSL https://api.github.com/repos/gitleaks/gitleaks/releases/latest \
	  | grep '"tag_name"' | sed 's/.*"v\([^"]*\)".*/\1/'); \
	curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v$${LATEST}/gitleaks_$${LATEST}_linux_x64.tar.gz" \
	  | tar -xz -C /tmp gitleaks; \
	sudo mv /tmp/gitleaks /usr/local/bin/gitleaks; \
	echo "gitleaks $${LATEST} installed."
else
	@echo "Windows detected. Run manually: winget install gitleaks"
endif

install-pre-commit:
	pip install pre-commit

## 手動でスキャン実行: make scan
scan:
	gitleaks detect --source . --config .gitleaks.toml --verbose

## git 全履歴をスキャン: make scan-all
scan-all:
	gitleaks detect --source . --config .gitleaks.toml --log-opts="--all" --verbose
