import sqlite3
import json
import os
import glob

DB_NAME = "advisory.db"
ADVISORY_DIR = "advisory-database/advisories"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS advisories (
            id TEXT PRIMARY KEY,
            summary TEXT,
            details TEXT,
            published TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS affected_packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            advisory_id TEXT,
            ecosystem TEXT,
            name TEXT,
            FOREIGN KEY(advisory_id) REFERENCES advisories(id)
        )
    ''')
    
    conn.commit()
    return conn

def process_advisories(conn):
    cursor = conn.cursor()
    
    # Walk through both github-reviewed and unreviewed directories
    files = glob.glob(os.path.join(ADVISORY_DIR, "**/*.json"), recursive=True)
    
    print(f"Found {len(files)} advisory files. Processing...")
    
    count = 0
    for file_path in files:
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                
                advisory_id = data.get('id')
                if not advisory_id:
                    continue
                
                # Insert advisory
                cursor.execute('''
                    INSERT OR IGNORE INTO advisories (id, summary, details, published)
                    VALUES (?, ?, ?, ?)
                ''', (
                    advisory_id,
                    data.get('summary', ''),
                    data.get('details', ''),
                    data.get('published', '')
                ))
                
                # Insert affected packages
                affected = data.get('affected', [])
                for item in affected:
                    package = item.get('package', {})
                    cursor.execute('''
                        INSERT INTO affected_packages (advisory_id, ecosystem, name)
                        VALUES (?, ?, ?)
                    ''', (
                        advisory_id,
                        package.get('ecosystem', ''),
                        package.get('name', '')
                    ))
                
                count += 1
                if count % 1000 == 0:
                    print(f"Processed {count} advisories...")
                    conn.commit()
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    conn.commit()
    print(f"Finished processing. Total {count} advisories imported.")

if __name__ == "__main__":
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = init_db()
    process_advisories(conn)
    conn.close()
