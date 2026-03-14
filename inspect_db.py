"""Quick script to print users from e2ee_messaging.db. Run from project root: python inspect_db.py"""
import sqlite3

conn = sqlite3.connect("e2ee_messaging.db")
conn.row_factory = sqlite3.Row
cur = conn.execute("SELECT id, username, display_name, id_pub_key, dh_pub_key FROM users")
rows = cur.fetchall()
conn.close()

if not rows:
    print("No users in database.")
else:
    for r in rows:
        print(dict(r))
    print(f"\nTotal: {len(rows)} user(s)")
