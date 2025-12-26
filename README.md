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

#### Test Database

To verify the database by querying for `langchain` and `langchain-core` vulnerabilities:

```bash
make test
```

#### Check Package Vulnerabilities

To check a specific Python package (and its dependencies) for vulnerabilities using a temporary `uv` environment:

```bash
make check-package PACKAGE="name==version"
```

Example:
```bash
make check-package PACKAGE="langchain==1.2.0"

----------------------------------------------------------------------
Checking vulnerabilities for langchain==1.2.0...
----------------------------------------------------------------------
Checking 33 packages from /var/folders/t0/k8gt3srs7xqd5cppy9549_pc0000gn/T/tmp.uEtdx7az9L/uv.lock...
 - annotated-types 0.7.0
 - anyio 4.12.0
 - certifi 2025.11.12
 - charset-normalizer 3.4.4
 - h11 0.16.0
 - httpcore 1.0.9
 - httpx 0.28.1
 - idna 3.11
 - jsonpatch 1.33
 - jsonpointer 3.0.0
 - langchain 1.2.0
 - langchain-core 1.2.5
 - langgraph 1.0.5
 - langgraph-checkpoint 3.0.1
 - langgraph-prebuilt 1.0.5
 - langgraph-sdk 0.3.1
 - langsmith 0.5.1
 - orjson 3.11.5
 - ormsgpack 1.12.1
 - packaging 25.0
 - pydantic 2.12.5
 - pydantic-core 2.41.5
 - pyyaml 6.0.3
 - requests 2.32.5
 - requests-toolbelt 1.0.0
 - tenacity 9.1.2
 - tmp-uetdx7az9l 0.1.0
 - typing-extensions 4.15.0
 - typing-inspection 0.4.2
 - urllib3 2.6.2
 - uuid-utils 0.12.0
 - xxhash 3.6.0
 - zstandard 0.25.0
jsonpointer 3.0.0 | GHSA-282f-qqgm-c34q | ["CVE-2021-23807"] | 5.0.0 | Prototype Pollution in node-jsonpointer
langchain 1.2.0 | GHSA-fprp-p869-w6q2 | ["CVE-2023-29374"] | No fixed version | LangChain vulnerable to code injection
langchain 1.2.0 | GHSA-r399-636x-v7f6 | ["CVE-2025-68665"] | 1.2.3 | LangChain serialization injection vulnerability enables secret extraction
----------------------------------------------------------------------
```

The analysis is based on the temporary `uv.lock` file.

#### Check Vulnerability History for a Package

To list all known vulnerabilities for a specific package, sorted by fixed version:

```bash
make check-package-history PACKAGE="name"
```

Example:
```bash
make check-package-history PACKAGE="langchain"

----------------------------------------------------------------------
Checking vulnerability history for langchain...
----------------------------------------------------------------------
Vulnerability history for 'langchain':
--------------------------------------------------------------------------------
langchain | GHSA-r399-636x-v7f6 | ["CVE-2025-68665"] | 1.2.3 | LangChain serialization injection vulnerability enables secret extraction
langchain | GHSA-r399-636x-v7f6 | ["CVE-2025-68665"] | 0.3.37 | LangChain serialization injection vulnerability enables secret extraction
langchain | GHSA-3hjh-jh2h-vrg6 | ["CVE-2024-2965"] | 0.2.5 | Denial of service in langchain-community
langchain | GHSA-hc5w-c9f8-9cc4 | ["CVE-2024-7774"] | 0.2.19 | Langchain Path Traversal vulnerability
langchain | GHSA-45pg-36p6-83v9 | ["CVE-2024-8309"] | 0.2.0 | Langchain SQL Injection vulnerability
langchain | GHSA-h9j7-5xvc-qhg5 | ["CVE-2024-0243"] | 0.1.0 | langchain Server-Side Request Forgery vulnerability
langchain | GHSA-rgp8-pm28-3759 | ["CVE-2024-3571"] | 0.0.353 | langchain vulnerable to path traversal
langchain | GHSA-h59x-p739-982c | ["CVE-2024-28088"] | 0.0.339 | LangChain directory traversal vulnerability
langchain | GHSA-6h8p-4hx9-w66c | ["CVE-2023-32786"] | 0.0.329 | Langchain Server-Side Request Forgery vulnerability
langchain | GHSA-prgp-w7vf-ch62 | ["CVE-2023-39659"] | 0.0.325 | LangChain vulnerable to arbitrary code execution
langchain | GHSA-655w-fm8m-m478 | ["CVE-2023-46229"] | 0.0.317 | LangChain Server Side Request Forgery vulnerability
langchain | GHSA-7gfq-f96f-g85j | ["CVE-2023-36281"] | 0.0.312 | langchain vulnerable to arbitrary code execution
langchain | GHSA-f73w-4m7g-ch9x | ["CVE-2023-39631"] | 0.0.308 | Langchain vulnerable to arbitrary code execution via the evaluate function in the numexpr library
langchain | GHSA-8h5w-f6q9-wg35 | ["CVE-2023-32785"] | 0.0.247 | Langchain SQL Injection vulnerability
langchain | GHSA-2qmj-7962-cjq8 | ["CVE-2023-36258"] | 0.0.247 | langchain arbitrary code execution vulnerability
langchain | GHSA-7q94-qpjr-xpgm | ["CVE-2023-36189"] | 0.0.247 | langchain SQL Injection vulnerability
langchain | GHSA-fj32-q626-pjjc | ["CVE-2023-38860"] | 0.0.247 | LangChain vulnerable to arbitrary code execution
langchain | GHSA-6643-h7h5-x9wh | ["CVE-2023-34541"] | 0.0.247 | Langchain vulnerable to arbitrary code execution
langchain | GHSA-57fc-8q82-gfp3 | ["CVE-2023-36188"] | 0.0.236 | langchain vulnerable to arbitrary code execution
langchain | GHSA-92j5-3459-qgp4 | ["CVE-2023-38896"] | 0.0.236 | LangChain vulnerable to arbitrary code execution
langchain | GHSA-gwqq-6vq7-5j86 | ["CVE-2023-36095"] | 0.0.236 | langchain Code Injection vulnerability
langchain | GHSA-x32c-59v5-h7fg | ["CVE-2023-34540"] | 0.0.225 | Langchain OS Command Injection vulnerability
langchain | GHSA-fprp-p869-w6q2 | ["CVE-2023-29374"] |  | LangChain vulnerable to code injection
----------------------------------------------------------------------
Done.
```

#### Clean

To remove the generated database files:

```bash
make clean
```

### Development

#### Format Code

To run code formatting and static analysis with `isort`, `black`, and `mypy`:

```bash
make format
```