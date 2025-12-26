# github-advisory-local-db

Spin up your own local database for: security vulnerabilities inclusive of CVEs and GitHub originated security advisories from the world of open source software.


## Workflow

This project uses `make` and `uv` to automate common tasks.

### Prerequisites

- [uv](https://github.com/astral-sh/uv) must be installed.

### Quickstart

To get started, clone the repository, sync dependencies, and build the database:

```bash
git clone --recursive https://github.com/fcpenha/github-advisory-local-db.git
cd github-advisory-local-db
make init-db
```

### Commands

#### Sync Dependencies

To install `uv` (if not present) and sync project dependencies:

```bash
make sync
```

#### Sync Submodule

To update the submodule to the latest commit:

```bash
make sync-submodule
```

#### Initialize Database

This command syncs dependencies, updates the submodule, and builds the SQLite database using the `scripts/build_db.py` script:

```bash
make init-db
```

#### Query Database

To verify the database by querying for `langchain-core` vulnerabilities:

```bash
make query-langchain
```

#### Clean

To remove the generated database files:

```bash
make clean
```