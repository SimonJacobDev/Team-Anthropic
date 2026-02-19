import sqlite3

def fix_database():
    print("🔧 Fixing database schema...")
    
    conn = sqlite3.connect('entitleai.db')
    cursor = conn.cursor()
    
    # Check existing tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"📋 Existing tables: {tables}")
    
    # Create missing tables
    
    # 1. Create interaction_logs table
    if 'interaction_logs' not in tables:
        print("➕ Creating interaction_logs table...")
        cursor.execute('''
            CREATE TABLE interaction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id TEXT,
                action TEXT,
                details TEXT,
                timestamp DATETIME
            )
        ''')
        print("✅ interaction_logs table created")
    
    # 2. Check if households table has all columns
    if 'households' in tables:
        cursor.execute("PRAGMA table_info(households)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 households columns: {columns}")
        
        # Add missing columns if needed
        if 'aadhaar_number' not in columns:
            cursor.execute("ALTER TABLE households ADD COLUMN aadhaar_number TEXT")
            print("✅ Added aadhaar_number column")
        if 'ration_card_number' not in columns:
            cursor.execute("ALTER TABLE households ADD COLUMN ration_card_number TEXT")
            print("✅ Added ration_card_number column")
        if 'phone_number' not in columns:
            cursor.execute("ALTER TABLE households ADD COLUMN phone_number TEXT")
            print("✅ Added phone_number column")
        if 'created_at' not in columns:
            cursor.execute("ALTER TABLE households ADD COLUMN created_at TIMESTAMP")
            print("✅ Added created_at column")
    
    # 3. Check enrolled_schemes table
    if 'enrolled_schemes' not in tables:
        print("➕ Creating enrolled_schemes table...")
        cursor.execute('''
            CREATE TABLE enrolled_schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id TEXT,
                scheme_name TEXT,
                enrollment_date DATETIME,
                status TEXT
            )
        ''')
        print("✅ enrolled_schemes table created")
    
    # 4. Check documents table
    if 'documents' not in tables:
        print("➕ Creating documents table...")
        cursor.execute('''
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id TEXT,
                doc_type TEXT,
                doc_number TEXT,
                has_doc BOOLEAN,
                verified BOOLEAN
            )
        ''')
        print("✅ documents table created")
    
    conn.commit()
    
    # Verify tables now exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\n📋 Tables after fix: {tables}")
    
    conn.close()
    print("\n✅ Database fix complete!")

if __name__ == "__main__":
    fix_database()