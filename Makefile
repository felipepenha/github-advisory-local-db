# Default target
help:
	@echo "GitHub Advisory Local DB - Available Commands:"
	@echo ""
	@echo "  make sync             - Install uv and project dependencies"
	@echo "  make sync-submodule   - Initialize and update the git submodule"
	@echo "  make init-db          - Build the local SQLite database (uses uv run)"
	@echo "  make query-langchain  - Verify DB by querying for langchain-core"
	@echo "  make clean            - Remove the generated database files"
	@echo "  make all              - Run all recipes."
	@echo ""

.PHONY: help sync sync-submodule init-db query-langchain clean

sync:
	uv sync

sync-submodule:
	git submodule update --init --recursive

init-db: sync sync-submodule
	uv run scripts/build_db.py

query-langchain:
	@echo "----------------------------------------------------------------------"
	@echo "Querying for 'langchain-core' vulnerabilities..."
	@echo "----------------------------------------------------------------------"
	uv run scripts/test_query.py
	@echo "----------------------------------------------------------------------"

clean:
	rm -f advisory.db advisory.db-journal advisory.db-wal

all: clean sync sync-submodule init-db query-langchain