# github-advisory-local-db

Spin up your own local database for: security vulnerabilities inclusive of CVEs and GitHub originated security advisories from the world of open source software.

## Workflow

This project includes the [GitHub Advisory Database](https://github.com/github/advisory-database) as a git submodule in the `advisory-database` directory.

### Quickstart

To get started, you can clone this repository and build the local SQLite database:

```bash
git clone --recursive https://github.com/fcpenha/github-advisory-local-db.git
make all
```

### Step-by-step

#### Cloning the Repository

When cloning this repository, you need to initialize the submodule:

```bash
git clone --recursive https://github.com/fcpenha/github-advisory-local-db.git
```

#### Updating the Submodule

To update the advisory database to the latest version:

```bash
make sync-submodule
```

#### Initialize Database

To sync the submodule and build the local SQLite database:

```bash
make init-db
```

This will create an `advisory.db` file in the root directory.

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