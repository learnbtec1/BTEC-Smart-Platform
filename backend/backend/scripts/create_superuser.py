#!/usr/bin/env python3
import getpass
import os
import sys

try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from app import database, crud, schemas
    db = database.SessionLocal()
except Exception as e:
    print("Run this script from repository root with installed dependencies. Error:", e)
    raise SystemExit(1)

def main():
    email = input("Email for admin: ").strip()
    pwd = getpass.getpass("Password: ")
    existing = crud.get_user_by_email(db, email)
    if existing:
        print("User exists, updating to superuser.")
        existing.is_superuser = True
        db.add(existing)
        db.commit()
        print("Updated.")
    else:
        user = schemas.UserCreate(email=email, password=pwd)
        crud.create_user(db, user, is_superuser=True)
        print("Created superuser.")

if __name__ == "__main__":
    main()
