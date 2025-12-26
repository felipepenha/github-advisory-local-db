.PHONY: help sync sync-submodule init-db test clean check-package format

help:
	@echo "GitHub Advisory Local DB - Available Commands:"
	@echo ""
	@echo "  make sync             - Install uv and project dependencies"
	@echo "  make sync-submodule   - Initialize and update the git submodule"
	@echo "  make init-db          - Build the local SQLite database (uses uv run)"
	@echo "  make test             - Verify DB by querying for langchain-core"
	@echo "  make format           - Check code format using black, isort, mypy"
	@echo "  make clean            - Remove the generated database files"
	@echo "  make check-package PACKAGE=\"name==ver\" PYTHON_VERSION=\"3.xx\" - Check a specific package version"
	@echo "  make check-package-history PACKAGE=\"name\" - Check vulnerability history for a package"
	@echo "  make all              - Run all recipes."
	@echo ""

.PHONY: help sync sync-submodule init-db test clean check-package format check-package-history

sync:
	uv sync

sync-submodule:
	git submodule update --init --recursive

init-db: sync sync-submodule
	uv run scripts/build_db.py

test:
	@echo "----------------------------------------------------------------------"
	@echo "Querying for 'langchain-core' vulnerabilities..."
	@echo "----------------------------------------------------------------------"
	uv run scripts/test_query.py
	@echo "----------------------------------------------------------------------"

clean:
	rm -f advisory.db advisory.db-journal advisory.db-wal

check-package:
	@if [ -z "$(PACKAGE)" ]; then echo "PACKAGE variable not set. Use make check-package PACKAGE=\"name==version\" PYTHON_VERSION=\"3.xx\""; exit 1; fi
	@if [ -z "$(PYTHON_VERSION)" ]; then echo "PYTHON_VERSION variable not set. Use make check-package PACKAGE=\"name==version\" PYTHON_VERSION=\"3.xx\""; exit 1; fi
	@TEMP_DIR=$$(mktemp -d); \
	echo "Created temp dir: $$TEMP_DIR"; \
	(cd $$TEMP_DIR && uv init --python $(PYTHON_VERSION) --no-workspace > /dev/null 2>&1 && uv add "$(PACKAGE)" > /dev/null 2>&1); \
	echo "----------------------------------------------------------------------"; \
	echo "Checking vulnerabilities for $(PACKAGE)..."; \
	echo -n "Environment Python: "; (cd $$TEMP_DIR && uv run python --version); \
	echo "----------------------------------------------------------------------"; \
	uv run scripts/check_uv_package.py --lock-file "$$TEMP_DIR/uv.lock"; \
	rm -rf $$TEMP_DIR; \
	echo "----------------------------------------------------------------------"; \
	echo "Done."

check-package-history:
	@if [ -z "$(PACKAGE)" ]; then echo "PACKAGE variable not set. Use make check-package-history PACKAGE=\"name\""; exit 1; fi
	@echo "----------------------------------------------------------------------"; \
	echo "Checking vulnerability history for $(PACKAGE)..."; \
	echo "----------------------------------------------------------------------"; \
	uv run scripts/check_package_history.py "$(PACKAGE)"; \
	echo "----------------------------------------------------------------------"; \
	echo "Done."

all: clean sync sync-submodule init-db test check-package

format:
	isort ./scripts/*.py
	black ./scripts/*.py
	mypy ./scripts/*.py