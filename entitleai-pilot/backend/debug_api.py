import sqlite3
import json
from flask import Flask, jsonify
from rules_engine import RulesEngine

app = Flask(__name__)
engine = RulesEngine()

def test_database():
    print("\n🔍 TESTING DATABASE CONNECTION")
    print("="*50)
    
    try:
        conn = sqlite3.connect('entitleai.db')
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[t[0] for t in tables]}")
        
        # Check households
        cursor.execute("SELECT COUNT(*) FROM households")
        count = cursor.fetchone()[0]
        print(f"👥 Total households: {count}")
        
        if count > 0:
            # Show sample
            cursor.execute("SELECT id, name, age, income FROM households LIMIT 3")
            print("\n📋 Sample households:")
            for row in cursor.fetchall():
                print(f"  {row[0]}: {row[1]}, Age:{row[2]}, ₹{row[3]}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_eligibility():
    print("\n🔍 TESTING ELIGIBILITY ENGINE")
    print("="*50)
    
    test_household = {
        'age': 65,
        'gender': 'Female',
        'income': 2000,
        'ration_type': 'PHH',
        'landholding': 0,
        'occupation': 'Daily Wage Labor',
        'disability': 'None',
        'caste': 'SC'
    }
    
    try:
        eligible = engine.check_eligibility(test_household)
        print(f"✅ Eligible schemes found: {len(eligible)}")
        for i, scheme in enumerate(eligible[:5]):  # Show first 5
            print(f"  {i+1}. {scheme['scheme_name']}")
        return True
    except Exception as e:
        print(f"❌ Eligibility engine error: {e}")
        return False

if __name__ == "__main__":
    db_ok = test_database()
    if db_ok:
        test_eligibility()
    
    print("\n" + "="*50)
    print("📝 NEXT STEPS:")
    print("1. Make sure Flask is running: python app.py")
    print("2. Test in browser: http://127.0.0.1:5000/api/household/VILL000001")
    print("3. Check for error messages in the Flask console")