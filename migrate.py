import sqlite3
import os
from supabase import create_client
from dotenv import load_dotenv

# Load credentials
load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

def migrate_to_cloud():
    db_path = 'employees.db'
    
    if not os.path.exists(db_path):
        print("Error: SQLite file 'employees.db' nahi mili!")
        return

    try:
        # SQLite connect karna
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Data fetch karna
        rows = cursor.execute("SELECT * FROM employees").fetchall()
        
        print(f"Starting Secure Migration of {len(rows)} records...")

        for row in rows:
            payload = {
                "emp_id": str(row["emp_id"]),
                "name": row["name"],
                "role": row["role"],
                "email": row["email"],
                "address": row["address"],
                "mobile": row["mobile"]
            }
            # Secure API Insert to Cloud
            supabase.table("employees").insert(payload).execute()
            print(f"Migrated: {row['name']}")
            
        print("\n--- SUCCESS: Data is now on Supabase Cloud! ---")
        
    except Exception as e:
        print(f"Migration Failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_to_cloud()