import sqlite3
import random
from datetime import datetime

def init_database():
    """Initialize database with 1000 households"""
    
    conn = sqlite3.connect('entitleai.db')
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute('DROP TABLE IF EXISTS households')
    cursor.execute('DROP TABLE IF EXISTS enrolled_schemes')
    cursor.execute('DROP TABLE IF EXISTS documents')
    cursor.execute('DROP TABLE IF EXISTS interaction_logs')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE households (
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
            caste TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE enrolled_schemes (
            household_id TEXT,
            scheme_name TEXT,
            FOREIGN KEY(household_id) REFERENCES households(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE documents (
            household_id TEXT,
            doc_type TEXT,
            has_doc BOOLEAN,
            doc_number TEXT,
            FOREIGN KEY(household_id) REFERENCES households(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE interaction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id TEXT,
            action TEXT,
            details TEXT,
            timestamp DATETIME
        )
    ''')
    
    # Sample data pools
    first_names_male = ["Muthu", "Kannan", "Murugan", "Kumar", "Velu", "Selvam", "Ramesh", "Suresh", "Babu", "Raj"]
    first_names_female = ["Kaliammal", "Selvi", "Rani", "Lakshmi", "Parvathi", "Meena", "Vasanthi", "Mallika", "Sarasu", "Devi"]
    villages = ["Villupuram", "Tindivanam", "Gingee", "Vanur", "Marakkanam", "Melmalayanur", "Koliyanur", "Kandamangalam", "Vikravandi", "Thirukoilur"]
    occupations = ["Farmer", "Daily Wage Labor", "Fisherman", "Weaver", "Construction Worker", "Domestic Help", "Street Vendor", "Unemployed", "Cobbler", "Potter"]
    castes = ["SC", "ST", "BC", "MBC", "OC", "SC", "BC", "BC", "MBC", "SC"]
    
    print("Generating 1000 households...")
    
    # Generate 1000 households
    for i in range(1, 1001):
        household_id = f"VILL{str(i).zfill(6)}"
        
        # Generate gender and appropriate name
        gender = random.choice(["Male", "Female", "Female", "Male", "Female"])
        if gender == "Male":
            name = random.choice(first_names_male)
        else:
            name = random.choice(first_names_female)
        
        age = random.randint(22, 85)
        income = random.choice([0, 1000, 2500, 4000, 6000, 8000, 10000, 12000])
        ration_type = random.choice(["PHH", "PHH", "PHH", "AAY", "PHH"])
        landholding = random.choice([0, 0, 0, 0.5, 1.0, 1.5, 2.0])
        occupation = random.choice(occupations)
        disability = random.choice(["None", "None", "None", "None", "Visual", "Physical", "Hearing", "Multiple"])
        village = random.choice(villages)
        caste = random.choice(castes)
        
        cursor.execute('''
            INSERT INTO households (id, name, age, gender, income, ration_type, landholding, occupation, disability, village, caste)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (household_id, name, age, gender, income, ration_type, landholding, occupation, disability, village, caste))
        
        # Add enrolled schemes
        all_schemes = ["PM-KISAN", "Old Age Pension", "Widow Pension", "Disability Pension", 
                      "PMJJBY", "PMAY-G", "MGNREGA", "PMMVY", "Scholarship", "Caste Certificate"]
        
        if random.random() < 0.7:
            num_enrolled = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
            enrolled = random.sample(all_schemes, min(num_enrolled, len(all_schemes)))
            
            for scheme in enrolled:
                cursor.execute('''
                    INSERT INTO enrolled_schemes (household_id, scheme_name)
                    VALUES (?, ?)
                ''', (household_id, scheme))
        
        # Add documents
        docs = [
            ("Aadhaar Card", random.random() > 0.08, f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"),
            ("Ration Card", True, f"RC/{random.randint(2020,2023)}/{random.randint(100,999)}"),
            ("Income Certificate", random.random() > 0.35, f"INC/{random.randint(2020,2023)}/{random.randint(100,999)}"),
            ("Caste Certificate", random.random() > 0.40, f"CAST/{random.randint(2020,2023)}/{random.randint(100,999)}"),
            ("Age Proof", random.random() > 0.25, f"AGE/{random.randint(2020,2023)}/{random.randint(100,999)}"),
            ("Bank Passbook", random.random() > 0.20, f"ACC{random.randint(100000,999999)}"),
            ("Disability Certificate", True if disability != "None" else random.random() > 0.90, f"DIS/{random.randint(2020,2023)}/{random.randint(100,999)}"),
            ("Land Records", True if landholding > 0 else random.random() > 0.70, f"PAT/{random.randint(2020,2023)}/{random.randint(100,999)}")
        ]
        
        for doc_name, has_doc, doc_num in docs:
            cursor.execute('''
                INSERT INTO documents (household_id, doc_type, has_doc, doc_number)
                VALUES (?, ?, ?, ?)
            ''', (household_id, doc_name, has_doc, doc_num if has_doc else ""))
        
        if i % 100 == 0:
            print(f"Generated {i} households...")
    
    # Add rejection logs
    rejection_reasons = [
        "Name mismatch in documents",
        "Missing income certificate",
        "Age proof not provided",
        "Caste certificate expired",
        "Photo not matching",
        "Incomplete application form",
        "Wrong bank account details",
        "Land records not updated"
    ]
    
    for i in range(1, 101):
        household_id = f"VILL{str(i).zfill(6)}"
        if random.random() < 0.5:
            num_rejections = random.randint(1, 3)
            for _ in range(num_rejections):
                reason = random.choice(rejection_reasons)
                timestamp = datetime.now().isoformat()
                cursor.execute('''
                    INSERT INTO interaction_logs (household_id, action, details, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (household_id, "rejection", reason, timestamp))
    
    conn.commit()
    conn.close()
    print("Database initialization complete! 1000 households generated.")

if __name__ == "__main__":
    init_database()
