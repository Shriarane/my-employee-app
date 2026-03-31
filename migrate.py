import sqlite3
from supabase import create_client

# Yahan apni details paste karo
SUPABASE_URL = "https://jhhxjthrpdngwxpuodgq.supabase.co"
SUPABASE_KEY = "sb_secret_rbT1M125PxwbOwPyauRGhQ_wCvRRSZM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def migrate_to_cloud():
    try:
        # SQLite se data read karna
        conn = sqlite3.connect('employees.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if table exists
        rows = cursor.execute("SELECT * FROM employees").fetchall()
        
        if not rows:
            print("No data found in SQLite to migrate.")
            return

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
            # Secure API Insert
            supabase.table("employees").insert(payload).execute()
            print(f"Successfully migrated: {row['name']}")
            
        print("\n--- MIGRATION SUCCESSFUL: Check Supabase Table Editor! ---")
        
    except Exception as e:
        print(f"Migration Failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_to_cloud()