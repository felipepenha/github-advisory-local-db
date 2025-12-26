import argparse
import os
import sqlite3
import sys
import tomllib

from packaging.version import parse

DB_NAME = "advisory.db"


def check_package(lock_file):
    if not os.path.exists(DB_NAME):
        print(f"Error: {DB_NAME} not found. Run 'make init-db' first.")
        return

    if not os.path.exists(lock_file):
        print(f"Error: {lock_file} not found.")
        return

    # Parse uv.lock to get package names
    try:
        with open(lock_file, "rb") as f:
            data = tomllib.load(f)

        # uv.lock 'package' is a list of tables (dicts)
        packages = data.get("package", [])

        if not packages:
            print("No packages found in lock file.")
            return

        # Create map of package name -> version
        package_versions = {p["name"]: p["version"] for p in packages}
        package_names = list(package_versions.keys())

    except Exception as e:
        print(f"Error reading lock file: {e}")
        return

    print(f"Checking {len(package_names)} packages from {lock_file}...")
    for pkg, ver in package_versions.items():
        print(f" - {pkg} {ver}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Construct SQL query with IN clause
    placeholders = ",".join(["?"] * len(package_names))
    query = f"""
    SELECT P.name, A.id, A.aliases, P.fixed_version, A.summary 
    FROM affected_packages P 
    JOIN advisories A ON P.advisory_id = A.id 
    WHERE P.name IN ({placeholders})
    ORDER BY P.name, A.id, A.aliases, P.fixed_version;
    """

    try:
        cursor.execute(query, package_names)
        rows = cursor.fetchall()

        if not rows:
            print("No vulnerabilities found for the specified packages.")
            conn.close()
            return

        for row in rows:
            pkg_name = row[0]
            advisory_id = row[1]
            aliases = row[2]
            fixed_version_str = row[3]
            summary = row[4]

            # Get version from lock file map
            current_version_str = package_versions.get(pkg_name)

            if not current_version_str:
                # Should not happen given the query filter
                continue

            if not fixed_version_str:
                # If no fixed version is specified, it might be always vulnerable or data is missing.
                # Report it to be safe.
                print(
                    f"{pkg_name} {current_version_str} | {advisory_id} | {aliases} | No fixed version | {summary}"
                )
                continue

            # Compare versions
            try:
                is_vulnerable = False
                fixed_versions = [v.strip() for v in fixed_version_str.split(",")]

                # Heuristic: If the current version is smaller than a fixed version, flag it.
                for fv_str in fixed_versions:
                    if parse(current_version_str) < parse(fv_str):
                        is_vulnerable = True
                        break

                if is_vulnerable:
                    print(
                        f"{pkg_name} {current_version_str} | {advisory_id} | {aliases} | {fixed_version_str} | {summary}"
                    )

            except Exception as e:
                print(f"Error comparing versions for {pkg_name}: {e}")
                # Fallback to reporting
                print(
                    f"[CHECK MANUAL] {pkg_name} {current_version_str} | {advisory_id} | {aliases} | Fixed: {fixed_version_str}"
                )

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check uv.lock packages against vulnerability database."
    )
    parser.add_argument("--lock-file", required=True, help="Path to uv.lock file")
    args = parser.parse_args()

    check_package(args.lock_file)
