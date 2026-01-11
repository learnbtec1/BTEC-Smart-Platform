#!/usr/bin/env python3
"""
Reset superuser password for a given email in a sqlite DB used by the project.
Usage:
  # set PYTHONPATH so `app` package is importable, then:
  $env:NEW_SUPERUSER_PASSWORD = "YourNewPassHere"
  python backend/scripts/reset_superuser_password.py --email "you@example.com"
Optionally pass --db to target a specific sqlite file path.
"""
import os
import sqlite3
import argparse
import sys
from getpass import getpass

# Import hashing helper from project (requires PYTHONPATH to include backend/)
try:
    from app.core.security import get_password_hash
except Exception as e:
    print("ERROR: could not import get_password_hash from app.core.security:", e)
    print("Ensure you set PYTHONPATH to include the backend folder, e.g.:")
    print(r'  $env:PYTHONPATH = "$PWD\backend"  (PowerShell)')
    sys.exit(2)

parser = argparse.ArgumentParser()
parser.add_argument("--email", required=True, help="User email to update")
parser.add_argument("--db", default=None, help="Path to sqlite DB file (optional)")
args = parser.parse_args()

email = args.email
new_password = os.environ.get("NEW_SUPERUSER_PASSWORD")
if not new_password:
    # Prompt securely if not provided via env
    new_password = getpass("New password (input hidden): ")
    if not new_password:
        print("No password provided, aborting.")
        sys.exit(3)

candidates = []
if args.db:
    candidates.append(args.db)
# common candidate locations relative to repo root and backend
candidates += [
    "backend/dev.db",
    "dev.db",
    "backend/btec.db",
    "btec.db",
    "backend/database.db",
    "backend/data/dev.db",
]

updated = False
for rel in candidates:
    path = os.path.abspath(rel)
    if not os.path.exists(path):
        continue
    print("Checking DB:", path)
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        # ensure users table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cur.fetchone():
            print("  no users table in", path)
            conn.close()
            continue
        # find user
        cur.execute("SELECT id, email FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        if not row:
            print("  user not found in", path)
            conn.close()
            continue
        # update hashed password
        hashpw = get_password_hash(new_password)
        cur.execute("UPDATE users SET hashed_password=? WHERE email=?", (hashpw, email))
        conn.commit()
        print("SUCCESS: updated password for", email, "in", path)
        conn.close()
        updated = True
        break
    except Exception as e:
        print("  ERROR operating on", path, ":", e)
        try:
            conn.close()
        except:
            pass

if not updated:
    print("User not found in candidate DB files. To list all .db files run in PowerShell:")
    print(r'  Get-ChildItem -Path . -Filter *.db -Recurse')
    sys.exit(1)
sys.exit(0)