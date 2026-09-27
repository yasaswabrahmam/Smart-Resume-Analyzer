"""
Migrate plaintext admin passwords to PBKDF2-HMAC-SHA512 hashes.

USAGE:
    python config/migrate_admin_passwords.py

This script:
1. Creates a backup of resume_data.db before any changes
2. Finds all admin accounts with plaintext passwords
3. Prompts you to confirm the password for each account (or skips)
4. Hashes and updates the password in-place
5. Reports what was migrated

If you do not know the original password for an account, use
    python config/create_admin.py
to create a fresh admin account.
"""

import sys
import os
import shutil
import getpass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database_connection, hash_password, verify_password


def main():
    print("=" * 60)
    print(" Admin Password Migration: Plaintext → PBKDF2")
    print("=" * 60)
    print()

    # --- 1. Backup ---
    db_path = "resume_data.db"
    backup_path = db_path + ".backup_migration"

    if not os.path.exists(db_path):
        print(f"ERROR: Database '{db_path}' not found.")
        print("Make sure you run this script from the project root directory.")
        sys.exit(1)

    shutil.copy2(db_path, backup_path)
    print(f"✅  Backup created: {backup_path}")
    print()

    # --- 2. Find plaintext accounts ---
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password FROM admin ORDER BY id")
    admins = cursor.fetchall()

    if not admins:
        print("No admin accounts found in the database.")
        conn.close()
        return

    print(f"Found {len(admins)} admin account(s):\n")

    migrated = 0
    skipped = 0

    for admin_id, email, stored_pwd in admins:
        # Detect if already hashed
        is_hashed = ":" in stored_pwd
        status = "ALREADY HASHED" if is_hashed else "PLAINTEXT"
        print(f"  [{admin_id}] {email}  — {status}")

        if is_hashed:
            skipped += 1
            continue

        print(f"\n  Migrating '{email}'...")
        print("  Enter the current plaintext password to migrate it, or press ENTER to skip.")
        try:
            pwd = getpass.getpass(f"  Password for '{email}': ")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            conn.close()
            sys.exit(0)

        if not pwd:
            print(f"  Skipped (no password entered).\n")
            skipped += 1
            continue

        # Verify the supplied password matches what's in DB (plaintext compare)
        if pwd != stored_pwd:
            print(f"  ❌  Password does not match the stored plaintext. Skipping.\n")
            skipped += 1
            continue

        # Hash and update
        new_hash = hash_password(pwd)
        cursor.execute("UPDATE admin SET password = ? WHERE id = ?", (new_hash, admin_id))
        conn.commit()
        print(f"  ✅  Password hashed and saved.\n")
        migrated += 1

    conn.close()

    print("=" * 60)
    print(f"Migration complete: {migrated} migrated, {skipped} skipped.")
    if migrated > 0:
        print(f"Backup is at: {backup_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
