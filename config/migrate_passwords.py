import sqlite3
import shutil
import os
import sys

# Add parent directory to path so we can import config.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import hash_password

def migrate_passwords():
    db_path = 'resume_data.db'
    backup_path = 'resume_data.db.backup'
    
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    # Backup the database
    print(f"Backing up database to {backup_path}")
    shutil.copy2(db_path, backup_path)
    
    # Connect and migrate
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, email, password FROM admin")
        admins = cursor.fetchall()
        
        migrated_count = 0
        for admin_id, email, password in admins:
            # Check if it's already hashed (i.e. contains colon)
            if ':' not in password:
                print(f"Migrating password for admin: {email}")
                hashed = hash_password(password)
                cursor.execute("UPDATE admin SET password = ? WHERE id = ?", (hashed, admin_id))
                migrated_count += 1
            else:
                print(f"Admin {email} already has a hashed password.")
                
        conn.commit()
        print(f"Successfully migrated {migrated_count} admin accounts.")
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_passwords()
