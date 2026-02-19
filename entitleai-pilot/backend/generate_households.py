import sqlite3
import random
from datetime import datetime, timedelta
import json

def generate_realistic_households():
    """Generate 1000 realistic household records with proper demographics"""
    
    # Connect to database
    conn = sqlite3.connect('entitleai.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS households (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            income INTEGER,
            ration_type TEXT,
            landholding REAL,
            occupation TEXT,
            disability TEXT,
            village TEXT,
            caste TEXT,
            aadhaar_number TEXT,
            ration_card_number TEXT,
            phone_number TEXT,
            created_at TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrolled_schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id TEXT,
            scheme_name TEXT,
            enrollment_date TIMESTAMP,
            status TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id TEXT,
            doc_type TEXT,
            doc_number TEXT,
            has_doc BOOLEAN,
            verified BOOLEAN
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM households')
    cursor.execute('DELETE FROM enrolled_schemes')
    cursor.execute('DELETE FROM documents')
    
    # ========== REALISTIC DATA POOLS ==========
    
    # Tamil names by gender and age group
    male_names_young = ["Kumar", "Raja", "Sekar", "Mani", "Balu", "Gopi", "Suresh", "Ramesh", "Dinesh", "Vignesh"]
    male_names_middle = ["Muthu", "Kannan", "Murugan", "Selvam", "Velu", "Perumal", "Karuppu", "Mari", "Ayya", "Pandi"]
    male_names_old = ["Kaliannan", "Muthu", "Karuppan", "Velayudham", "Chinnasamy", "Palani", "Subramani", "Dorai", "Rangasamy", "Goundar"]
    
    female_names_young = ["Priya", "Divya", "Kavitha", "Malar", "Thenmozhi", "Anitha", "Selvi", "Vasanthi", "Mallika", "Deepa"]
    female_names_middle = ["Lakshmi", "Parvathi", "Meena", "Rani", "Sarasu", "Kamala", "Maragatham", "Alamelu", "Dhanam", "Pappathi"]
    female_names_old = ["Kaliammal", "Thangam", "Palaniyammal", "Karuppayi", "Mariyammal", "Velammal", "Chinnapillai", "Rengammal", "Ayyammal", "Goundammal"]
    
    # Villages in Villupuram district
    villages = [
        "Villupuram", "Tindivanam", "Gingee", "Vanur", "Marakkanam", 
        "Melmalayanur", "Koliyanur", "Kandamangalam", "Vikravandi", 
        "Thirukoilur", "Ulundurpettai", "Sankarapuram", "Rishivandiyam",
        "Mugaiyur", "Thiruvennainallur", "Valavanur", "Ananthapuram",
        "Avalurpet", "Salamedu", "Kilpudupakkam", "Olakkur", "Periyakapulur"
    ]
    
    # Occupations
    occupations = [
        "Farmer", "Daily Wage Labor", "Fisherman", "Weaver", 
        "Construction Worker", "Domestic Help", "Street Vendor", 
        "Cobbler", "Potter", "Blacksmith", "Carpenter", "Mason",
        "Auto Driver", "Farm Labor", "Beedi Worker", "Unemployed"
    ]
    
    # Castes (weighted towards SC/ST for realistic poverty data)
    castes = ["SC", "SC", "SC", "ST", "ST", "BC", "BC", "BC", "BC", "MBC", "MBC", "OC"]
    
    # Disability types
    disabilities = ["None", "Visual", "Physical", "Hearing", "Multiple"]
    
    # Ration card types
    ration_types = ["PHH", "PHH", "PHH", "PHH", "AAY", "AAY"]
    
    print("🚀 Generating 1000 realistic households...")
    
    for i in range(1, 1001):
        # Generate household ID
        household_id = f"VILL{str(i).zfill(6)}"
        
        # ===== REALISTIC AGE DISTRIBUTION =====
        age_group = random.choices(
            ['young', 'middle', 'old'],
            weights=[30, 40, 30],
            k=1
        )[0]
        
        if age_group == 'young':
            age = random.randint(18, 35)
        elif age_group == 'middle':
            age = random.randint(36, 59)
        else:
            age = random.randint(60, 85)
        
        # ===== GENDER =====
        gender = random.choices(['Male', 'Female'], weights=[45, 55])[0]
        
        # ===== NAME BASED ON AGE AND GENDER =====
        if gender == 'Male':
            if age < 35:
                name = random.choice(male_names_young)
            elif age < 60:
                name = random.choice(male_names_middle)
            else:
                name = random.choice(male_names_old)
        else:
            if age < 35:
                name = random.choice(female_names_young)
            elif age < 60:
                name = random.choice(female_names_middle)
            else:
                name = random.choice(female_names_old)
        
        # Add surname/father's name for realism
        father_names = ["Muthu", "Kumar", "Raja", "Selvam", "Perumal", "Kaliannan", "Chinnasamy", "Palani", "Subramani"]
        if random.random() > 0.3:  # 70% have father/husband name
            name = f"{name} {random.choice(father_names)}"
        
        # ===== INCOME DISTRIBUTION =====
        income_bracket = random.choices(
            ['very_low', 'low', 'medium', 'high'],
            weights=[40, 35, 20, 5]
        )[0]
        
        if income_bracket == 'very_low':
            income = random.randint(0, 2000)
        elif income_bracket == 'low':
            income = random.randint(2001, 5000)
        elif income_bracket == 'medium':
            income = random.randint(5001, 10000)
        else:
            income = random.randint(10001, 20000)
        
        # ===== RATION TYPE (based on income) =====
        if income < 3000:
            ration_type = "AAY"
        elif income < 8000:
            ration_type = "PHH"
        else:
            ration_type = "NPHH"
        
        # ===== LANDHOLDING =====
        if random.random() < 0.6:  # 60% landless
            landholding = 0
        elif random.random() < 0.3:  # 30% marginal farmers
            landholding = round(random.uniform(0.1, 1.0), 2)
        else:  # 10% small farmers
            landholding = round(random.uniform(1.1, 2.5), 2)
        
        # ===== OCCUPATION =====
        if landholding > 0:
            occupation = random.choice(["Farmer", "Farm Labor"])
        elif gender == 'Female' and age > 40:
            occupation = random.choice(["Domestic Help", "Street Vendor", "Daily Wage Labor"])
        else:
            occupation = random.choice(occupations)
        
        # ===== DISABILITY (FIXED VERSION) =====
        # 5% chance of having a disability
        if random.random() < 0.05:
            disability = random.choice(["Visual", "Physical", "Hearing", "Multiple"])
        else:
            disability = "None"
        
        # ===== CASTE =====
        caste = random.choice(castes)
        
        # ===== VILLAGE =====
        village = random.choice(villages)
        
        # ===== AADHAAR NUMBER =====
        aadhaar = f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
        
        # ===== RATION CARD NUMBER =====
        ration_card = f"RC/{random.randint(2020,2023)}/{random.randint(100,999)}"
        
        # ===== PHONE NUMBER =====
        if random.random() < 0.6:
            phone = f"9{random.randint(100000000, 999999999)}"
        else:
            phone = None
        
        # Insert household
        cursor.execute('''
            INSERT INTO households (
                id, name, age, gender, income, ration_type, landholding,
                occupation, disability, village, caste, aadhaar_number,
                ration_card_number, phone_number, created_at, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            household_id, name, age, gender, income, ration_type, landholding,
            occupation, disability, village, caste, aadhaar, ration_card,
            phone, datetime.now(), 1
        ))
        
        # ===== ENROLLED SCHEMES =====
        all_schemes = [
            "Old Age Pension", "Widow Pension", "Disability Pension",
            "PM-KISAN", "PMAY-G", "MGNREGA", "PMMVY", "Scholarship"
        ]
        
        enrolled_schemes = []
        
        # Check eligibility for schemes
        if age >= 60 and random.random() < 0.7:
            enrolled_schemes.append("Old Age Pension")
        
        if gender == 'Female' and age > 40 and random.random() < 0.3:
            enrolled_schemes.append("Widow Pension")
        
        if disability != 'None' and random.random() < 0.4:
            enrolled_schemes.append("Disability Pension")
        
        if landholding > 0 and occupation == 'Farmer' and random.random() < 0.4:
            enrolled_schemes.append("PM-KISAN")
        
        if ration_type in ['PHH', 'AAY'] and landholding < 0.5 and random.random() < 0.2:
            enrolled_schemes.append("PMAY-G")
        
        if occupation in ['Daily Wage Labor', 'Farm Labor'] and random.random() < 0.5:
            enrolled_schemes.append("MGNREGA")
        
        if gender == 'Female' and 19 <= age <= 35 and random.random() < 0.15:
            enrolled_schemes.append("PMMVY")
        
        if caste in ['SC', 'ST'] and age < 25 and random.random() < 0.2:
            enrolled_schemes.append("Scholarship")
        
        # Remove duplicates
        enrolled_schemes = list(set(enrolled_schemes))
        
        # Insert enrolled schemes
        for scheme in enrolled_schemes:
            enrollment_date = datetime.now() - timedelta(days=random.randint(30, 365))
            cursor.execute('''
                INSERT INTO enrolled_schemes (household_id, scheme_name, enrollment_date, status)
                VALUES (?, ?, ?, ?)
            ''', (household_id, scheme, enrollment_date, 'active'))
        
        # ===== DOCUMENTS =====
        documents = [
            ("Aadhaar Card", aadhaar, random.random() < 0.95),
            ("Ration Card", ration_card, True),
            ("Income Certificate", f"INC/{random.randint(100,999)}", random.random() < 0.4),
            ("Caste Certificate", f"CAST/{random.randint(100,999)}", random.random() < 0.5),
            ("Age Proof", f"AGE/{random.randint(100,999)}", random.random() < 0.6),
            ("Bank Passbook", f"ACC{random.randint(100000,999999)}", random.random() < 0.7),
        ]
        
        # Disability certificate if disabled
        if disability != 'None':
            documents.append(("Disability Certificate", f"DIS/{random.randint(100,999)}", random.random() < 0.3))
        
        # Land records if have land
        if landholding > 0:
            documents.append(("Land Records", f"PAT/{random.randint(100,999)}", random.random() < 0.4))
        
        for doc_type, doc_number, has_doc in documents:
            cursor.execute('''
                INSERT INTO documents (household_id, doc_type, doc_number, has_doc, verified)
                VALUES (?, ?, ?, ?, ?)
            ''', (household_id, doc_type, doc_number, has_doc, has_doc and random.random() < 0.7))
        
        # Progress indicator
        if i % 100 == 0:
            print(f"✅ Generated {i} households...")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("🎉 SUCCESS! Generated 1000 realistic households")
    print("="*50)
    
    # Show sample
    show_sample_data()

def show_sample_data():
    """Display some sample households"""
    conn = sqlite3.connect('entitleai.db')
    cursor = conn.cursor()
    
    print("\n📋 SAMPLE HOUSEHOLDS:")
    print("-"*80)
    
    cursor.execute('''
        SELECT id, name, age, gender, income, village, ration_type 
        FROM households LIMIT 5
    ''')
    
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | {row[1]} | Age: {row[2]} | {row[3]} | Income: ₹{row[4]} | {row[5]} | {row[6]}")
    
    print("\n📊 STATISTICS:")
    cursor.execute('SELECT COUNT(*) FROM households')
    total = cursor.fetchone()[0]
    print(f"Total Households: {total}")
    
    cursor.execute('SELECT COUNT(*) FROM households WHERE age >= 60')
    elderly = cursor.fetchone()[0]
    print(f"Elderly (60+): {elderly}")
    
    cursor.execute('SELECT COUNT(*) FROM households WHERE gender = "Female"')
    female = cursor.fetchone()[0]
    print(f"Female: {female}")
    
    cursor.execute('SELECT AVG(income) FROM households')
    avg_income = cursor.fetchone()[0]
    print(f"Average Income: ₹{avg_income:.0f}")
    
    cursor.execute('SELECT COUNT(*) FROM households WHERE income < 5000')
    below_poverty = cursor.fetchone()[0]
    print(f"Below Poverty Line (₹5000): {below_poverty}")
    
    conn.close()

if __name__ == '__main__':
    generate_realistic_households()