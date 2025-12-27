import argparse
import os
import sqlite3

DB_NAME = "advisory.db"


def check_history(package_name):
    if not os.path.exists(DB_NAME):
        print(f"Error: {DB_NAME} not found. Run 'make init-db' first.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT P.name, A.id, A.aliases, P.fixed_version, A.summary, P.ecosystem
    FROM affected_packages P 
    JOIN advisories A ON P.advisory_id = A.id 
    WHERE P.name = ?
    ORDER BY P.fixed_version DESC;
    """

    try:
        cursor.execute(query, (package_name,))
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No known vulnerabilities found for package '{package_name}' in the local database.")
            return

        print(f"Vulnerability history for '{package_name}':")
        print("-" * 80)
        for row in rows:
            # Output format: name|ecosystem|id|aliases|fixed_version|summary
            print(f"{row[0]} | {row[5]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check vulnerability history for a specific package.")
    parser.add_argument("package", help="Name of the package to check")
    args = parser.parse_args()

    check_history(args.package)
