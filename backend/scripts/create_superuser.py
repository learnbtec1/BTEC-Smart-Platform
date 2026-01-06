#!/usr/bin/env python3
"""
Example create_superuser helper.
Run inside backend container:
docker compose exec backend python scripts/create_superuser.py
Adjust imports according to your project structure.
"""
import getpass
try:
    from app import crud, database, schemas
    db = database.SessionLocal()
except Exception:
    print("Warning: could not import project modules directly. Run inside backend container.")
    raise

def main():
    email = input("Email for admin: ").strip()
    pwd = getpass.getpass("Password: ")
    user = crud.get_user_by_email(db, email=email)
    if user:
        print("User exists, updating to superuser...")
        try:
            crud.update_user_to_superuser(db, user)
            print("Updated.")
        except Exception as ex:
            print("Update failed:", ex)
    else:
        try:
            crud.create_user(db, schemas.UserCreate(email=email, password=pwd, is_superuser=True))
            print("Created superuser.")
        except Exception as ex:
            print("Create failed:", ex)

if __name__ == "__main__":
    main()
