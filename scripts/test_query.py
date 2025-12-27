import os
import sqlite3

DB_NAME = "advisory.db"


def run_query():
    if not os.path.exists(DB_NAME):
        print(f"Error: {DB_NAME} not found. Run 'make init-db' first.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT P.name, A.id, A.aliases, P.fixed_version, A.summary, P.ecosystem
    FROM affected_packages P 
    JOIN advisories A ON P.advisory_id = A.id 
    WHERE P.name = 'langchain'
    ORDER BY P.fixed_version DESC;
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            # Output format: name|ecosystem|id|aliases|fixed_version|summary
            print(f"{row[0]}|{row[5]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_query()
