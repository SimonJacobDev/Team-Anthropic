import os
import subprocess
import sys

def create_project():
    """Create the entire EntitleAI-Pilot project structure"""
    
    print("🚀 Creating EntitleAI-Pilot project...")
    
    # Create main project directory
    os.makedirs("entitleai-pilot/backend", exist_ok=True)
    os.makedirs("entitleai-pilot/frontend", exist_ok=True)
    
    print("📁 Created project directories")
    
    # ------------------- BACKEND FILES -------------------
    
    # backend/requirements.txt
    with open("entitleai-pilot/backend/requirements.txt", "w") as f:
        f.write("""Flask==2.3.3
Flask-CORS==4.0.0""")
    
    # backend/init_db.py
    with open("entitleai-pilot/backend/init_db.py", "w", encoding="utf-8") as f:
        f.write("""import sqlite3
import random
from datetime import datetime

def init_database():
    \"\"\"Initialize database with 1000 households\"\"\"
    
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
""")
    
    # backend/rules_engine.py
    with open("entitleai-pilot/backend/rules_engine.py", "w", encoding="utf-8") as f:
        f.write("""class RulesEngine:
    \"\"\"Eligibility rules engine for welfare schemes\"\"\"
    
    def __init__(self):
        self.schemes = self.load_schemes()
    
    def load_schemes(self):
        \"\"\"Load scheme eligibility rules\"\"\"
        return {
            "Old Age Pension": {
                "name": "Indira Gandhi National Old Age Pension",
                "criteria": {
                    "min_age": 60,
                    "max_income": 5000,
                    "ration_type": ["PHH", "AAY"],
                    "exclusions": ["Already receiving pension"]
                },
                "documents": ["Age Proof", "Income Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹200 per month"
            },
            "Widow Pension": {
                "name": "Indira Gandhi National Widow Pension",
                "criteria": {
                    "gender": "Female",
                    "min_age": 40,
                    "max_age": 60,
                    "max_income": 5000,
                    "ration_type": ["PHH", "AAY"],
                    "marital_status": "Widow"
                },
                "documents": ["Age Proof", "Income Certificate", "Husband Death Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹200 per month"
            },
            "Disability Pension": {
                "name": "Indira Gandhi National Disability Pension",
                "criteria": {
                    "min_age": 18,
                    "max_age": 80,
                    "disability": ["Visual", "Physical", "Hearing", "Multiple"],
                    "max_income": 5000,
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Disability Certificate", "Age Proof", "Income Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹300 per month"
            },
            "PM-KISAN": {
                "name": "Pradhan Mantri Kisan Samman Nidhi",
                "criteria": {
                    "landholding": 2.0,
                    "occupation": ["Farmer"],
                    "exclusions": ["Income tax payer", "Government employee"]
                },
                "documents": ["Land Records", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹6000 per year"
            },
            "PMAY-G": {
                "name": "Pradhan Mantri Awas Yojana - Gramin",
                "criteria": {
                    "ration_type": ["PHH", "AAY"],
                    "landholding": 0,
                    "housing_status": "Kutcha house"
                },
                "documents": ["Land Records", "Income Certificate", "Aadhaar Card", "Ration Card"],
                "benefit": "₹1.2 lakh for house construction"
            },
            "MGNREGA": {
                "name": "Mahatma Gandhi National Rural Employment Guarantee Act",
                "criteria": {
                    "min_age": 18,
                    "max_age": 60,
                    "occupation": ["Daily Wage Labor", "Unemployed", "Farmer"],
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Job Card", "Bank Passbook", "Aadhaar Card"],
                "benefit": "100 days guaranteed work"
            },
            "PMMVY": {
                "name": "Pradhan Mantri Matru Vandana Yojana",
                "criteria": {
                    "gender": "Female",
                    "min_age": 19,
                    "pregnancy_status": "First live birth",
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Pregnancy Certificate", "Aadhaar Card", "Bank Passbook"],
                "benefit": "₹5000 cash incentive"
            },
            "Scholarship": {
                "name": "Post-Matric Scholarship for SC/ST",
                "criteria": {
                    "caste": ["SC", "ST"],
                    "min_age": 16,
                    "max_age": 30,
                    "education_level": "Post-matric",
                    "max_income": 250000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Previous Year Marksheet", "Aadhaar Card", "Bank Passbook"],
                "benefit": "Full tuition + maintenance allowance"
            },
            "Caste Certificate": {
                "name": "Community Certificate for SC/ST/BC",
                "criteria": {
                    "caste": ["SC", "ST", "BC", "MBC"],
                    "documents_required": True
                },
                "documents": ["Community Certificate of parents", "Birth Certificate", "Aadhaar Card"],
                "benefit": "Eligibility for reservations"
            }
        }
    
    def check_eligibility(self, household):
        \"\"\"Check household eligibility for all schemes\"\"\"
        eligible = []
        
        for scheme_id, scheme in self.schemes.items():
            criteria = scheme["criteria"]
            eligible_flag = True
            reasons = []
            
            # Age checks
            if "min_age" in criteria:
                if household['age'] < criteria["min_age"]:
                    eligible_flag = False
                    reasons.append(f"Age {household['age']} < minimum {criteria['min_age']}")
            
            if "max_age" in criteria:
                if household['age'] > criteria["max_age"]:
                    eligible_flag = False
                    reasons.append(f"Age {household['age']} > maximum {criteria['max_age']}")
            
            # Gender check
            if "gender" in criteria:
                if household['gender'] != criteria["gender"]:
                    eligible_flag = False
                    reasons.append(f"Gender {household['gender']} not eligible")
            
            # Income check
            if "max_income" in criteria:
                if household['income'] > criteria["max_income"]:
                    eligible_flag = False
                    reasons.append(f"Income ₹{household['income']} > maximum ₹{criteria['max_income']}")
            
            # Ration type check
            if "ration_type" in criteria:
                if household['ration_type'] not in criteria["ration_type"]:
                    eligible_flag = False
                    reasons.append(f"Ration type {household['ration_type']} not eligible")
            
            # Landholding check
            if "landholding" in criteria:
                if isinstance(criteria["landholding"], (int, float)):
                    if household['landholding'] > criteria["landholding"]:
                        eligible_flag = False
                        reasons.append(f"Landholding {household['landholding']}ha > limit {criteria['landholding']}ha")
                elif criteria["landholding"] == 0:
                    if household['landholding'] > 0:
                        eligible_flag = False
                        reasons.append("Scheme requires landless status")
            
            # Occupation check
            if "occupation" in criteria:
                if household['occupation'] not in criteria["occupation"]:
                    eligible_flag = False
                    reasons.append(f"Occupation {household['occupation']} not eligible")
            
            # Disability check
            if "disability" in criteria:
                if household['disability'] not in criteria["disability"]:
                    eligible_flag = False
                    reasons.append(f"Disability status {household['disability']} not eligible")
            
            # Caste check
            if "caste" in criteria:
                if household['caste'] not in criteria["caste"]:
                    eligible_flag = False
                    reasons.append(f"Caste {household['caste']} not eligible")
            
            if eligible_flag:
                eligible.append({
                    "scheme_id": scheme_id,
                    "scheme_name": scheme["name"],
                    "benefit": scheme["benefit"],
                    "required_docs": scheme["documents"]
                })
        
        return eligible
    
    def check_documents(self, household_id, household_docs, scheme_docs):
        \"\"\"Check if household has required documents for a scheme\"\"\"
        missing_docs = []
        present_docs = []
        
        for doc in scheme_docs:
            found = False
            for h_doc in household_docs:
                if h_doc['doc_type'] == doc and h_doc['has_doc']:
                    found = True
                    present_docs.append({
                        "doc_type": doc,
                        "doc_number": h_doc['doc_number']
                    })
                    break
            
            if not found:
                missing_docs.append(doc)
        
        return {
            "present": present_docs,
            "missing": missing_docs,
            "complete": len(missing_docs) == 0
        }
""")
    
    # backend/database.py
    with open("entitleai-pilot/backend/database.py", "w", encoding="utf-8") as f:
        f.write("""import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='entitleai.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_household(self, household_id):
        \"\"\"Get household details by ID\"\"\"
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, age, gender, income, ration_type, 
                   landholding, occupation, disability, village, caste
            FROM households WHERE id = ?
        ''', (household_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        household = {
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'income': row[4],
            'ration_type': row[5],
            'landholding': row[6],
            'occupation': row[7],
            'disability': row[8],
            'village': row[9],
            'caste': row[10]
        }
        
        # Get enrolled schemes
        cursor.execute('''
            SELECT scheme_name FROM enrolled_schemes WHERE household_id = ?
        ''', (household_id,))
        
        household['enrolled_schemes'] = [row[0] for row in cursor.fetchall()]
        
        # Get documents
        cursor.execute('''
            SELECT doc_type, has_doc, doc_number FROM documents WHERE household_id = ?
        ''', (household_id,))
        
        household['documents'] = [
            {'doc_type': row[0], 'has_doc': bool(row[1]), 'doc_number': row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return household
    
    def search_households(self, query):
        \"\"\"Search households by ID or name\"\"\"
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, village FROM households 
            WHERE id LIKE ? OR name LIKE ? 
            LIMIT 10
        ''', (f'%{query}%', f'%{query}%'))
        
        results = [{'id': row[0], 'name': row[1], 'village': row[2]} for row in cursor.fetchall()]
        conn.close()
        return results
    
    def log_interaction(self, household_id, action, details):
        \"\"\"Log any interaction\"\"\"
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interaction_logs (household_id, action, details, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (household_id, action, details, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_dashboard_stats(self):
        \"\"\"Get KPI data for dashboard\"\"\"
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total households
        cursor.execute('SELECT COUNT(*) FROM households')
        stats['total_households'] = cursor.fetchone()[0]
        
        # Average correction cycles
        cursor.execute('''
            SELECT COUNT(*) FROM interaction_logs WHERE action = 'correction_loop'
        ''')
        total_corrections = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT household_id) FROM interaction_logs')
        households_with_interactions = cursor.fetchone()[0]
        
        if households_with_interactions > 0:
            stats['avg_corrections'] = round(total_corrections / households_with_interactions, 1)
        else:
            stats['avg_corrections'] = 0
        
        # Top rejection reasons
        cursor.execute('''
            SELECT details, COUNT(*) as count FROM interaction_logs 
            WHERE action = 'rejection' 
            GROUP BY details 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        
        stats['top_rejections'] = [
            {'reason': row[0], 'count': row[1]} 
            for row in cursor.fetchall()
        ]
        
        # Households with gaps
        cursor.execute('''
            SELECT COUNT(DISTINCT h.id) 
            FROM households h
            LEFT JOIN enrolled_schemes e ON h.id = e.household_id
            WHERE e.household_id IS NULL OR 
                  (SELECT COUNT(*) FROM enrolled_schemes WHERE household_id = h.id) < 2
        ''')
        
        stats['households_with_gaps'] = cursor.fetchone()[0]
        
        # Weekly trend
        cursor.execute('''
            SELECT date(timestamp) as day, COUNT(*) 
            FROM interaction_logs 
            GROUP BY day 
            ORDER BY day DESC 
            LIMIT 7
        ''')
        
        stats['trend'] = [
            {'date': row[0], 'count': row[1]} 
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return stats
""")
    
    # backend/app.py
    with open("entitleai-pilot/backend/app.py", "w", encoding="utf-8") as f:
        f.write("""from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import Database
from rules_engine import RulesEngine
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

db = Database()
engine = RulesEngine()

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('../frontend', path)

# API Routes
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = db.search_households(query)
    return jsonify(results)

@app.route('/api/household/<household_id>', methods=['GET'])
def get_household(household_id):
    household = db.get_household(household_id)
    if not household:
        return jsonify({'error': 'Household not found'}), 404
    
    eligible_schemes = engine.check_eligibility(household)
    
    # Check document gaps
    doc_gaps = {}
    for scheme in eligible_schemes:
        doc_check = engine.check_documents(
            household_id, 
            household['documents'], 
            scheme['required_docs']
        )
        if not doc_check['complete']:
            doc_gaps[scheme['scheme_name']] = doc_check['missing']
    
    enrolled = set(household['enrolled_schemes'])
    eligible_names = {s['scheme_name'] for s in eligible_schemes}
    gap_schemes = list(eligible_names - enrolled)
    
    db.log_interaction(household_id, 'eligibility_check', f'Eligible: {len(eligible_schemes)}, Enrolled: {len(enrolled)}')
    
    return jsonify({
        'household': household,
        'eligible_schemes': eligible_schemes,
        'entitlement_gaps': gap_schemes,
        'document_gaps': doc_gaps,
        'enrolled': list(enrolled)
    })

@app.route('/api/validate-docs/<household_id>', methods=['POST'])
def validate_docs(household_id):
    data = request.json
    scheme_name = data.get('scheme_name')
    
    household = db.get_household(household_id)
    if not household:
        return jsonify({'error': 'Household not found'}), 404
    
    eligible_schemes = engine.check_eligibility(household)
    scheme = next((s for s in eligible_schemes if s['scheme_name'] == scheme_name), None)
    
    if not scheme:
        return jsonify({'error': 'Scheme not found'}), 404
    
    doc_check = engine.check_documents(household_id, household['documents'], scheme['required_docs'])
    
    return jsonify(doc_check)

@app.route('/api/submit-correction', methods=['POST'])
def submit_correction():
    data = request.json
    household_id = data.get('household_id')
    rejection_reason = data.get('rejection_reason')
    scheme_name = data.get('scheme_name')
    
    details = f"Rejected for {scheme_name}: {rejection_reason}"
    db.log_interaction(household_id, 'rejection', details)
    db.log_interaction(household_id, 'correction_loop', f'Correction needed: {rejection_reason}')
    
    # Generate correction checklist
    checklist = []
    if "name mismatch" in rejection_reason.lower():
        checklist.append("Get affidavit for name correction")
        checklist.append("Bring all original documents for verification")
    elif "income" in rejection_reason.lower():
        checklist.append("Get new income certificate from VAO")
    elif "age proof" in rejection_reason.lower():
        checklist.append("Bring birth certificate or school leaving certificate")
    elif "caste" in rejection_reason.lower():
        checklist.append("Get caste certificate from Tahsildar")
    else:
        checklist.append(f"Fix issue: {rejection_reason}")
        checklist.append("Visit again with corrected documents")
    
    return jsonify({
        'status': 'logged',
        'checklist': checklist,
        'message': 'Correction logged successfully'
    })

@app.route('/api/dashboard-stats', methods=['GET'])
def dashboard_stats():
    stats = db.get_dashboard_stats()
    return jsonify(stats)

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('entitleai.db'):
        print("Database not found. Running init_db.py first...")
        import init_db
        init_db.init_database()
    
    app.run(debug=True, port=5000)
""")
    
    # ------------------- FRONTEND FILES -------------------
    
    # frontend/index.html
    with open("entitleai-pilot/frontend/index.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EntitleAI-Pilot | Smart Eligibility System</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <h1>EntitleAI<span>-Pilot</span></h1>
                    <span class="badge">Villupuram District</span>
                </div>
                <nav>
                    <a href="/" class="active">Eligibility Check</a>
                    <a href="/dashboard">Dashboard</a>
                </nav>
            </div>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Search Section -->
            <section class="search-section">
                <div class="search-container">
                    <h2>Check Household Eligibility</h2>
                    <div class="search-box">
                        <input type="text" id="searchInput" placeholder="Enter Household ID (e.g., VILL001234) or Name...">
                        <button id="searchBtn" class="btn-primary">Search</button>
                    </div>
                    <div id="searchResults" class="search-results"></div>
                </div>
            </section>

            <!-- Household Profile Section -->
            <section id="profileSection" class="profile-section" style="display: none;">
                <div class="profile-header">
                    <h3>Household Profile</h3>
                    <span id="householdId" class="household-id"></span>
                </div>
                
                <div class="profile-grid">
                    <div class="profile-card">
                        <h4>Basic Details</h4>
                        <div class="details-grid">
                            <div class="detail-item">
                                <label>Name:</label>
                                <span id="profileName"></span>
                            </div>
                            <div class="detail-item">
                                <label>Age/Gender:</label>
                                <span id="profileAgeGender"></span>
                            </div>
                            <div class="detail-item">
                                <label>Village:</label>
                                <span id="profileVillage"></span>
                            </div>
                            <div class="detail-item">
                                <label>Ration Card:</label>
                                <span id="profileRation"></span>
                            </div>
                            <div class="detail-item">
                                <label>Income:</label>
                                <span id="profileIncome"></span>
                            </div>
                            <div class="detail-item">
                                <label>Occupation:</label>
                                <span id="profileOccupation"></span>
                            </div>
                            <div class="detail-item">
                                <label>Caste:</label>
                                <span id="profileCaste"></span>
                            </div>
                            <div class="detail-item">
                                <label>Disability:</label>
                                <span id="profileDisability"></span>
                            </div>
                        </div>
                    </div>

                    <div class="profile-card">
                        <h4>Currently Enrolled Schemes</h4>
                        <div id="enrolledSchemes" class="schemes-list"></div>
                    </div>
                </div>

                <!-- Voice Assistant -->
                <div class="voice-assistant">
                    <button id="voiceBtn" class="btn-voice">
                        <span>🔊</span> Read in Tamil
                    </button>
                </div>

                <!-- Eligibility Results -->
                <div class="results-section">
                    <div class="results-header">
                        <h3>Eligibility Analysis</h3>
                        <span class="badge" id="eligibleCount">0 schemes</span>
                    </div>

                    <div id="eligibleSchemes" class="schemes-container"></div>
                </div>

                <!-- Document Gaps -->
                <div id="gapsSection" class="gaps-section" style="display: none;">
                    <h3>Document Gaps Detected</h3>
                    <div id="documentGaps" class="gaps-container"></div>
                </div>

                <!-- Correction Modal -->
                <div id="correctionModal" class="modal">
                    <div class="modal-content">
                        <span class="close">&times;</span>
                        <h3>Document Correction Required</h3>
                        <p id="schemeNameDisplay"></p>
                        
                        <div class="form-group">
                            <label>Rejection Reason:</label>
                            <select id="rejectionReason">
                                <option value="">Select reason...</option>
                                <option value="Name mismatch in documents">Name mismatch in documents</option>
                                <option value="Missing income certificate">Missing income certificate</option>
                                <option value="Age proof not provided">Age proof not provided</option>
                                <option value="Caste certificate expired">Caste certificate expired</option>
                                <option value="Photo not matching">Photo not matching</option>
                                <option value="Wrong bank account details">Wrong bank account details</option>
                                <option value="Land records not updated">Land records not updated</option>
                            </select>
                        </div>

                        <button id="submitCorrection" class="btn-primary">Generate Correction Checklist</button>
                        
                        <div id="checklistOutput" class="checklist" style="display: none;">
                            <h4>📋 Correction Checklist</h4>
                            <ul id="checklistItems"></ul>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <p>EntitleAI-Pilot | Villupuram District Pilot | 1,000 Households</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>""")
    
    # frontend/dashboard.html
    with open("entitleai-pilot/frontend/dashboard.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - EntitleAI-Pilot</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="app-container">
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <h1>EntitleAI<span>-Pilot</span></h1>
                    <span class="badge">Dashboard</span>
                </div>
                <nav>
                    <a href="/">Eligibility Check</a>
                    <a href="/dashboard" class="active">Dashboard</a>
                </nav>
            </div>
        </header>

        <main class="main-content">
            <div class="dashboard-header">
                <h2>Pilot Performance Dashboard</h2>
                <p>Villupuram District | 1,000 Households | Jan-Jun 2027</p>
            </div>

            <!-- KPI Cards -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-icon">👥</div>
                    <div class="kpi-content">
                        <h3>Total Households</h3>
                        <div class="kpi-value" id="totalHouseholds">1,000</div>
                        <div class="kpi-label">Fixed denominator</div>
                    </div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-icon">🎯</div>
                    <div class="kpi-content">
                        <h3>With Entitlement Gaps</h3>
                        <div class="kpi-value" id="householdsWithGaps">0</div>
                        <div class="kpi-label">Eligible but not enrolled</div>
                    </div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-icon">🔄</div>
                    <div class="kpi-content">
                        <h3>Avg. Correction Cycles</h3>
                        <div class="kpi-value" id="avgCorrections">3.2</div>
                        <div class="kpi-label">Baseline: 3.0 → Target: ≤1.0</div>
                    </div>
                </div>

                <div class="kpi-card">
                    <div class="kpi-icon">✅</div>
                    <div class="kpi-content">
                        <h3>Rejection Reduction</h3>
                        <div class="kpi-value" id="rejectionReduction">42%</div>
                        <div class="kpi-label">Against baseline</div>
                    </div>
                </div>
            </div>

            <!-- Charts Row -->
            <div class="charts-row">
                <div class="chart-card">
                    <h3>Rejection Reasons</h3>
                    <canvas id="rejectionChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>Weekly Activity Trend</h3>
                    <canvas id="trendChart"></canvas>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="activity-section">
                <h3>Recent Rejections & Corrections</h3>
                <div class="activity-table-container">
                    <table class="activity-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Household ID</th>
                                <th>Action</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody id="activityTableBody">
                            <tr>
                                <td colspan="4" class="loading">Loading data...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <footer class="footer">
            <p>EntitleAI-Pilot | Real-time KPI tracking | Last updated: <span id="lastUpdated"></span></p>
        </footer>
    </div>

    <script src="dashboard.js"></script>
</body>
</html>""")
    
    # frontend/styles.css
    with open("entitleai-pilot/frontend/styles.css", "w", encoding="utf-8") as f:
        f.write("""* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: #f3f4f6;
    color: #1f2937;
    line-height: 1.5;
}

.app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header Styles */
.header {
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.logo h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #059669;
}

.logo h1 span {
    color: #6b7280;
    font-weight: 400;
}

.badge {
    background: #e5e7eb;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    color: #4b5563;
}

nav {
    display: flex;
    gap: 1rem;
}

nav a {
    text-decoration: none;
    color: #6b7280;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    transition: all 0.2s;
}

nav a:hover {
    background: #f3f4f6;
    color: #059669;
}

nav a.active {
    background: #059669;
    color: white;
}

/* Main Content */
.main-content {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
    flex: 1;
}

/* Search Section */
.search-section {
    background: white;
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.search-container h2 {
    margin-bottom: 1.5rem;
    color: #1f2937;
}

.search-box {
    display: flex;
    gap: 1rem;
}

.search-box input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.375rem;
    font-size: 1rem;
    transition: border-color 0.2s;
}

.search-box input:focus {
    outline: none;
    border-color: #059669;
}

.btn-primary {
    background: #059669;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-primary:hover {
    background: #047857;
}

.search-results {
    margin-top: 1rem;
    border-top: 1px solid #e5e7eb;
    padding-top: 1rem;
}

.result-item {
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.result-item:hover {
    background: #f9fafb;
    border-color: #059669;
}

.result-item strong {
    color: #059669;
}

/* Profile Section */
.profile-section {
    background: white;
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e5e7eb;
}

.household-id {
    font-family: monospace;
    background: #f3f4f6;
    padding: 0.25rem 0.75rem;
    border-radius: 0.375rem;
    font-weight: 600;
    color: #4b5563;
}

.profile-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.profile-card {
    background: #f9fafb;
    border-radius: 0.5rem;
    padding: 1.5rem;
}

.profile-card h4 {
    margin-bottom: 1rem;
    color: #4b5563;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

.detail-item {
    display: flex;
    flex-direction: column;
}

.detail-item label {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.detail-item span {
    font-weight: 500;
    color: #1f2937;
}

.schemes-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.scheme-tag {
    background: #e5e7eb;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    color: #4b5563;
}

/* Voice Assistant */
.voice-assistant {
    margin-bottom: 2rem;
}

.btn-voice {
    background: #2563eb;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: background 0.2s;
}

.btn-voice:hover {
    background: #1d4ed8;
}

/* Results Section */
.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.schemes-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.scheme-card {
    background: #f9fafb;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1.25rem;
    transition: all 0.2s;
}

.scheme-card.eligible {
    border-left: 4px solid #059669;
}

.scheme-card.enrolled {
    background: #e5e7eb;
    opacity: 0.7;
}

.scheme-card h4 {
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.scheme-benefit {
    color: #059669;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.scheme-docs {
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 1rem;
}

.btn-check-docs {
    background: none;
    border: 2px solid #059669;
    color: #059669;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
}

.btn-check-docs:hover {
    background: #059669;
    color: white;
}

/* Gaps Section */
.gaps-section {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #fee2e2;
    border-radius: 0.5rem;
    border: 1px solid #fecaca;
}

.gaps-section h3 {
    color: #991b1b;
    margin-bottom: 1rem;
}

.gap-item {
    background: white;
    padding: 1rem;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
    border: 1px solid #fecaca;
}

.gap-item strong {
    color: #991b1b;
}

.missing-docs {
    margin-top: 0.5rem;
    padding-left: 1.5rem;
    color: #b91c1c;
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 1000;
}

.modal-content {
    background: white;
    margin: 10% auto;
    padding: 2rem;
    border-radius: 0.5rem;
    max-width: 500px;
    position: relative;
}

.close {
    position: absolute;
    top: 1rem;
    right: 1.5rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
}

.form-group {
    margin: 1.5rem 0;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e5e7eb;
    border-radius: 0.375rem;
    font-size: 1rem;
}

.checklist {
    margin-top: 1.5rem;
    padding: 1.5rem;
    background: #f0fdf4;
    border-radius: 0.5rem;
    border: 1px solid #86efac;
}

.checklist h4 {
    color: #166534;
    margin-bottom: 1rem;
}

.checklist ul {
    list-style: none;
    padding: 0;
}

.checklist li {
    padding: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
}

.checklist li:before {
    content: "✓";
    color: #059669;
    position: absolute;
    left: 0;
}

/* Dashboard Styles */
.dashboard-header {
    margin-bottom: 2rem;
}

.dashboard-header h2 {
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.dashboard-header p {
    color: #6b7280;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.kpi-card {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.kpi-icon {
    font-size: 2.5rem;
    background: #f3f4f6;
    width: 4rem;
    height: 4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
}

.kpi-content h3 {
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 0.25rem;
}

.kpi-value {
    font-size: 1.875rem;
    font-weight: 700;
    color: #1f2937;
    line-height: 1.2;
}

.kpi-label {
    font-size: 0.75rem;
    color: #9ca3af;
}

.charts-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.chart-card {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.chart-card h3 {
    margin-bottom: 1rem;
    color: #4b5563;
    font-size: 1rem;
}

.activity-section {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.activity-section h3 {
    margin-bottom: 1rem;
    color: #4b5563;
}

.activity-table {
    width: 100%;
    border-collapse: collapse;
}

.activity-table th {
    text-align: left;
    padding: 0.75rem;
    background: #f9fafb;
    color: #6b7280;
    font-weight: 500;
    font-size: 0.875rem;
}

.activity-table td {
    padding: 0.75rem;
    border-bottom: 1px solid #e5e7eb;
}

.loading {
    text-align: center;
    color: #9ca3af;
    padding: 2rem;
}

/* Footer */
.footer {
    background: white;
    border-top: 1px solid #e5e7eb;
    padding: 1.5rem;
    text-align: center;
    color: #6b7280;
    font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    .profile-grid {
        grid-template-columns: 1fr;
    }
    
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .charts-row {
        grid-template-columns: 1fr;
    }
    
    .search-box {
        flex-direction: column;
    }
}""")
    
    # frontend/script.js
    with open("entitleai-pilot/frontend/script.js", "w", encoding="utf-8") as f:
        f.write("""// State management
let currentHousehold = null;
let currentEligibleSchemes = [];

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');
const profileSection = document.getElementById('profileSection');
const correctionModal = document.getElementById('correctionModal');
const voiceBtn = document.getElementById('voiceBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    searchBtn.addEventListener('click', performSearch);
    
    document.querySelector('.close').addEventListener('click', () => {
        correctionModal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === correctionModal) {
            correctionModal.style.display = 'none';
        }
    });
    
    voiceBtn.addEventListener('click', readAloud);
    
    document.getElementById('submitCorrection').addEventListener('click', submitCorrection);
});

// Search function
async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;
    
    searchResults.innerHTML = '<div class="loading">Searching...</div>';
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No households found</div>';
            return;
        }
        
        searchResults.innerHTML = results.map(hh => `
            <div class="result-item" onclick="loadHousehold('${hh.id}')">
                <strong>${hh.id}</strong> - ${hh.name}<br>
                <small>${hh.village}</small>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = '<div class="error">Error searching. Please try again.</div>';
    }
}

// Load household data
async function loadHousehold(householdId) {
    searchResults.innerHTML = '';
    searchInput.value = householdId;
    
    try {
        const response = await fetch(`/api/household/${householdId}`);
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        currentHousehold = data.household;
        currentEligibleSchemes = data.eligible_schemes;
        
        displayHousehold(data);
        profileSection.style.display = 'block';
        
        profileSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Load error:', error);
        alert('Error loading household data');
    }
}

// Display household data
function displayHousehold(data) {
    const hh = data.household;
    
    document.getElementById('householdId').textContent = hh.id;
    document.getElementById('profileName').textContent = hh.name;
    document.getElementById('profileAgeGender').textContent = `${hh.age} yrs / ${hh.gender}`;
    document.getElementById('profileVillage').textContent = hh.village;
    document.getElementById('profileRation').textContent = hh.ration_type;
    document.getElementById('profileIncome').textContent = `₹${hh.income}/month`;
    document.getElementById('profileOccupation').textContent = hh.occupation;
    document.getElementById('profileCaste').textContent = hh.caste;
    document.getElementById('profileDisability').textContent = hh.disability;
    
    const enrolledDiv = document.getElementById('enrolledSchemes');
    if (hh.enrolled_schemes && hh.enrolled_schemes.length > 0) {
        enrolledDiv.innerHTML = hh.enrolled_schemes.map(s => 
            `<span class="scheme-tag">${s}</span>`
        ).join('');
    } else {
        enrolledDiv.innerHTML = '<p class="text-gray">No schemes currently enrolled</p>';
    }
    
    document.getElementById('eligibleCount').textContent = `${data.eligible_schemes.length} schemes`;
    
    displayEligibleSchemes(data.eligible_schemes, hh.enrolled_schemes);
    
    if (Object.keys(data.document_gaps).length > 0) {
        displayDocumentGaps(data.document_gaps);
    } else {
        document.getElementById('gapsSection').style.display = 'none';
    }
}

// Display eligible schemes
function displayEligibleSchemes(schemes, enrolled) {
    const container = document.getElementById('eligibleSchemes');
    
    container.innerHTML = schemes.map(scheme => {
        const isEnrolled = enrolled.includes(scheme.scheme_name);
        const cardClass = isEnrolled ? 'scheme-card enrolled' : 'scheme-card eligible';
        
        return `
            <div class="${cardClass}">
                <h4>${scheme.scheme_name}</h4>
                <div class="scheme-benefit">${scheme.benefit}</div>
                <div class="scheme-docs">
                    <strong>Required:</strong> ${scheme.required_docs.join(', ')}
                </div>
                ${!isEnrolled ? `
                    <button class="btn-check-docs" onclick="checkDocuments('${scheme.scheme_name}')">
                        Check Documents
                    </button>
                ` : '<div class="enrolled-badge">✓ Already Enrolled</div>'}
            </div>
        `;
    }).join('');
}

// Display document gaps
function displayDocumentGaps(gaps) {
    const container = document.getElementById('documentGaps');
    const gapsSection = document.getElementById('gapsSection');
    
    container.innerHTML = Object.entries(gaps).map(([scheme, missing]) => `
        <div class="gap-item">
            <strong>${scheme}</strong>
            <div class="missing-docs">
                Missing: ${missing.join(', ')}
            </div>
        </div>
    `).join('');
    
    gapsSection.style.display = 'block';
}

// Check documents for a scheme
async function checkDocuments(schemeName) {
    if (!currentHousehold) return;
    
    try {
        const response = await fetch(`/api/validate-docs/${currentHousehold.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scheme_name: schemeName })
        });
        
        const result = await response.json();
        
        if (!result.complete) {
            document.getElementById('schemeNameDisplay').textContent = `Scheme: ${schemeName}`;
            document.getElementById('checklistOutput').style.display = 'none';
            document.getElementById('rejectionReason').value = '';
            correctionModal.style.display = 'block';
            
            correctionModal.dataset.schemeName = schemeName;
            correctionModal.dataset.missingDocs = JSON.stringify(result.missing);
        } else {
            alert('✅ All documents are present! This household is ready for application.');
        }
        
    } catch (error) {
        console.error('Document check error:', error);
        alert('Error checking documents');
    }
}

// Submit correction
async function submitCorrection() {
    const reason = document.getElementById('rejectionReason').value;
    if (!reason) {
        alert('Please select a rejection reason');
        return;
    }
    
    const schemeName = correctionModal.dataset.schemeName;
    
    try {
        const response = await fetch('/api/submit-correction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                household_id: currentHousehold.id,
                rejection_reason: reason,
                scheme_name: schemeName
            })
        });
        
        const result = await response.json();
        
        const checklistItems = document.getElementById('checklistItems');
        checklistItems.innerHTML = result.checklist.map(item => `<li>${item}</li>`).join('');
        document.getElementById('checklistOutput').style.display = 'block';
        
        console.log('Correction logged:', result);
        
        setTimeout(() => loadHousehold(currentHousehold.id), 1000);
        
    } catch (error) {
        console.error('Correction error:', error);
        alert('Error submitting correction');
    }
}

// Text to speech
function readAloud() {
    if (!currentHousehold || !currentEligibleSchemes) return;
    
    const hh = currentHousehold;
    const eligibleNames = currentEligibleSchemes.map(s => s.scheme_name).join(', ');
    const enrolled = hh.enrolled_schemes.join(', ') || 'none';
    const gaps = document.getElementById('documentGaps').innerText || 'No document gaps';
    
    const message = `
        Household ${hh.id}. Name ${hh.name}. Age ${hh.age}. Village ${hh.village}.
        Currently enrolled in: ${enrolled}.
        Eligible for additional schemes: ${eligibleNames}.
        Document status: ${gaps}.
    `;
    
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = 'ta-IN';
    utterance.rate = 0.9;
    
    window.speechSynthesis.speak(utterance);
}

// Make functions global
window.loadHousehold = loadHousehold;
window.checkDocuments = checkDocuments;""")
    
    # frontend/dashboard.js
    with open("entitleai-pilot/frontend/dashboard.js", "w", encoding="utf-8") as f:
        f.write("""// Dashboard JavaScript
let rejectionChart, trendChart;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
    
    setInterval(loadDashboardData, 30000);
});

async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-stats');
        const stats = await response.json();
        
        updateKPIs(stats);
        updateCharts(stats);
        loadRecentActivity();
        
    } catch (error) {
        console.error('Dashboard error:', error);
    }
}

function updateKPIs(stats) {
    document.getElementById('totalHouseholds').textContent = stats.total_households || 1000;
    document.getElementById('householdsWithGaps').textContent = stats.households_with_gaps || 0;
    document.getElementById('avgCorrections').textContent = stats.avg_corrections || '2.8';
    
    const baselineCorrections = 3.0;
    const currentCorrections = stats.avg_corrections || 2.8;
    const reduction = ((baselineCorrections - currentCorrections) / baselineCorrections * 100).toFixed(0);
    document.getElementById('rejectionReduction').textContent = `${reduction}%`;
}

function updateCharts(stats) {
    const rejectionCtx = document.getElementById('rejectionChart').getContext('2d');
    
    if (rejectionChart) {
        rejectionChart.destroy();
    }
    
    const rejectionData = stats.top_rejections || [
        { reason: 'Name mismatch', count: 45 },
        { reason: 'Missing income certificate', count: 32 },
        { reason: 'Age proof missing', count: 28 },
        { reason: 'Caste certificate expired', count: 19 },
        { reason: 'Bank details wrong', count: 15 }
    ];
    
    rejectionChart = new Chart(rejectionCtx, {
        type: 'bar',
        data: {
            labels: rejectionData.map(r => r.reason),
            datasets: [{
                label: 'Number of Rejections',
                data: rejectionData.map(r => r.count),
                backgroundColor: '#ef4444',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
    
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    
    if (trendChart) {
        trendChart.destroy();
    }
    
    const trendData = stats.trend || [
        { date: '2026-02-12', count: 24 },
        { date: '2026-02-13', count: 32 },
        { date: '2026-02-14', count: 28 },
        { date: '2026-02-15', count: 35 },
        { date: '2026-02-16', count: 42 },
        { date: '2026-02-17', count: 38 },
        { date: '2026-02-18', count: 45 }
    ];
    
    trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: trendData.map(d => d.date),
            datasets: [{
                label: 'Interactions',
                data: trendData.map(d => d.count),
                borderColor: '#059669',
                backgroundColor: 'rgba(5, 150, 105, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
}

async function loadRecentActivity() {
    const activities = generateSampleActivity();
    
    const tbody = document.getElementById('activityTableBody');
    tbody.innerHTML = activities.map(a => `
        <tr>
            <td>${a.timestamp}</td>
            <td><strong>${a.household_id}</strong></td>
            <td>
                <span class="badge ${a.action === 'rejection' ? 'badge-error' : 'badge-warning'}">
                    ${a.action}
                </span>
            </td>
            <td>${a.details}</td>
        </tr>
    `).join('');
}

function generateSampleActivity() {
    const actions = [
        { action: 'rejection', details: 'Name mismatch in documents' },
        { action: 'rejection', details: 'Missing income certificate' },
        { action: 'correction_loop', details: 'Age proof not provided' },
        { action: 'rejection', details: 'Caste certificate expired' },
        { action: 'correction_loop', details: 'Photo not matching' }
    ];
    
    const households = ['VILL001234', 'VILL004567', 'VILL007890', 'VILL002345', 'VILL006789'];
    
    return Array.from({ length: 5 }, (_, i) => {
        const now = new Date();
        now.setMinutes(now.getMinutes() - i * 15);
        
        return {
            timestamp: now.toLocaleString(),
            household_id: households[i % households.length],
            action: actions[i % actions.length].action,
            details: actions[i % actions.length].details
        };
    });
}""")
    
    # Create run.py (Windows-friendly runner)
    with open("entitleai-pilot/run.py", "w", encoding="utf-8") as f:
        f.write("""#!/usr/bin/env python
import os
import sys
import subprocess
import webbrowser
from time import sleep

def main():
    print("🚀 Starting EntitleAI-Pilot...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir('backend')
    
    # Check if database exists
    if not os.path.exists('entitleai.db'):
        print("📦 Initializing database with 1000 households...")
        subprocess.run([sys.executable, 'init_db.py'])
    
    # Open browser
    print("🌐 Opening browser in 3 seconds...")
    webbrowser.open('http://localhost:5000')
    webbrowser.open_new_tab('http://localhost:5000/dashboard')
    
    # Run Flask app
    print("🚀 Starting Flask server...")
    print("📊 Main app: http://localhost:5000")
    print("📈 Dashboard: http://localhost:5000/dashboard")
    print("=" * 50)
    print("Press Ctrl+C to stop")
    
    subprocess.run([sys.executable, 'app.py'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Shutting down...")
        sys.exit(0)
""")
    
    print("\n" + "="*50)
    print("✅ Project created successfully in 'entitleai-pilot' folder!")
    print("="*50)
    print("\nTo run the project:")
    print("1. Open VS Code")
    print("2. Open the 'entitleai-pilot' folder")
    print("3. Open terminal in VS Code (Ctrl + `)")
    print("4. Run these commands:")
    print("   cd backend")
    print("   pip install -r requirements.txt")
    print("   cd ..")
    print("   python run.py")
    print("\nOr simply double-click run.py to start!")
    print("="*50)

if __name__ == "__main__":
    create_project()