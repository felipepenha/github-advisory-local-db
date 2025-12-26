# Default target
help:
	@echo "GitHub Advisory Local DB - Available Commands:"
	@echo ""
	@echo "  make sync-submodule   - Update the git submodule"
	@echo "  make init-db          - Build the local SQLite database"
	@echo "  make test  		   - Verify DB by querying for langchain-core"
	@echo "  make clean            - Remove the generated database files"
	@echo ""

.PHONY: help sync-submodule init-db test clean

sync-submodule:
	git submodule update --remote

init-db:
	python3 scripts/build_db.py

test:
	sqlite3 advisory.db "SELECT P.name, A.id, A.summary FROM affected_packages P JOIN advisories A ON P.advisory_id = A.id WHERE P.name = 'langchain-core';"

clean:
	rm -f advisory.db advisory.db-journal advisory.db-wal

all: clean sync-submodule init-db test