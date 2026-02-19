import sqlite3

def view_data():
    conn = sqlite3.connect('entitleai.db')
    cursor = conn.cursor()
    
    print("="*80)
    print("📋 DATABASE CONTENTS")
    print("="*80)
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\n📊 TABLES: {[t[0] for t in tables]}")
    
    # Show households
    print("\n👥 HOUSEHOLDS:")
    print("-"*80)
    cursor.execute('''
        SELECT id, name, age, gender, income, village 
        FROM households LIMIT 15
    ''')
    households = cursor.fetchall()
    for h in households:
        print(f"ID: {h[0]} | {h[1]} | Age:{h[2]} | {h[3]} | ₹{h[4]} | {h[5]}")
    
    print(f"\n📊 Total households: {len(households)} shown (first 15)")
    
    # Show enrolled schemes
    print("\n📋 ENROLLED SCHEMES:")
    print("-"*80)
    cursor.execute('''
        SELECT household_id, scheme_name FROM enrolled_schemes LIMIT 10
    ''')
    schemes = cursor.fetchall()
    for s in schemes:
        print(f"{s[0]} → {s[1]}")
    
    # Count households with schemes
    cursor.execute('SELECT COUNT(DISTINCT household_id) FROM enrolled_schemes')
    count = cursor.fetchone()[0]
    print(f"\n📊 Households with schemes: {count}")
    
    conn.close()

if __name__ == "__main__":
    view_data()