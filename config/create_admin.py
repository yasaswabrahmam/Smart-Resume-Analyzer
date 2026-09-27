"""
Create a new admin account with a securely hashed password.

USAGE:
    python config/create_admin.py

This script prompts for an email and password, hashes the password
using PBKDF2-HMAC-SHA512, and inserts the admin record into the database.

Run this once during initial setup to create your admin account.
"""

import sys
import os
import getpass
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database_connection, hash_password, init_database


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def main():
    print("=" * 60)
    print(" Create Admin Account")
    print("=" * 60)
    print()

    # Ensure database is initialized
    init_database()

    # Get email
    while True:
        email = input("  Admin email: ").strip().lower()
        if not email:
            print("  Email cannot be empty.\n")
            continue
        if not is_valid_email(email):
            print("  Please enter a valid email address.\n")
            continue
        break

    # Get password (with confirmation)
    while True:
        try:
            pwd = getpass.getpass("  Password (min 8 characters): ")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)

        if len(pwd) < 8:
            print("  Password must be at least 8 characters.\n")
            continue

        try:
            pwd2 = getpass.getpass("  Confirm password: ")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)

        if pwd != pwd2:
            print("  Passwords do not match. Try again.\n")
            continue
        break

    # Hash and insert
    hashed = hash_password(pwd)

    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO admin (email, password) VALUES (?, ?)",
            (email, hashed)
        )
        conn.commit()
        print(f"\n  ✅  Admin account created for: {email}")
        print("  You can now log in with this account.")
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            print(f"\n  ❌  An admin account with email '{email}' already exists.")
            print("  To reset the password, delete the account and re-create it.")
        else:
            print(f"\n  ❌  Error creating admin: {e}")
    finally:
        conn.close()

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
