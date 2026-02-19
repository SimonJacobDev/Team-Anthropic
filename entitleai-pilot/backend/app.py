from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from rules_engine import RulesEngine
import os
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entitleai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize rules engine
engine = RulesEngine()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    # Create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@entitleai.gov.in',
            role='admin',
            district='Villupuram'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created - username: admin, password: admin123")

# ==================== DATABASE HELPER FUNCTIONS ====================
# Direct SQLite access for your existing data

def get_db_connection():
    conn = sqlite3.connect('entitleai.db')
    conn.row_factory = sqlite3.Row
    return conn

def search_households(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, village FROM households 
        WHERE id LIKE ? OR name LIKE ? 
        LIMIT 10
    ''', (f'%{query}%', f'%{query}%'))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_household(household_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get household details
    cursor.execute('''
        SELECT id, name, age, gender, income, ration_type, landholding, 
               occupation, disability, village, caste
        FROM households WHERE id = ?
    ''', (household_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    household = dict(row)
    
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

def log_interaction(household_id, action, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interaction_logs (household_id, action, details, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (household_id, action, details, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    stats = {}
    
    cursor.execute('SELECT COUNT(*) FROM households')
    stats['total_households'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT household_id) FROM enrolled_schemes')
    stats['households_with_schemes'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM households WHERE age >= 60')
    stats['elderly'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(income) FROM households')
    stats['avg_income'] = cursor.fetchone()[0]
    
    conn.close()
    return stats

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and API"""
    if request.method == 'GET':
        return send_from_directory('../frontend', 'login.html')
    
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'district': user.district
            }
        })
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

# ==================== FRONTEND ROUTES ====================

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/ai-insights')
def ai_insights():
    return send_from_directory('../frontend', 'ai-insights.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('../frontend', path)

# ==================== API ROUTES ====================

@app.route('/api/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '')
    results = search_households(query)
    return jsonify(results)

@app.route('/api/household/<household_id>', methods=['GET'])
@login_required
def get_household_api(household_id):
    household = get_household(household_id)
    if not household:
        return jsonify({'error': 'Household not found'}), 404
    
    # Check eligibility using rules engine
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
    
    log_interaction(household_id, 'eligibility_check', f'Eligible: {len(eligible_schemes)}, Enrolled: {len(enrolled)}')
    
    return jsonify({
        'household': household,
        'eligible_schemes': eligible_schemes,
        'entitlement_gaps': gap_schemes,
        'document_gaps': doc_gaps,
        'enrolled': list(enrolled)
    })

@app.route('/api/validate-docs/<household_id>', methods=['POST'])
@login_required
def validate_docs(household_id):
    data = request.json
    scheme_name = data.get('scheme_name')
    
    household = get_household(household_id)
    if not household:
        return jsonify({'error': 'Household not found'}), 404
    
    eligible_schemes = engine.check_eligibility(household)
    scheme = next((s for s in eligible_schemes if s['scheme_name'] == scheme_name), None)
    
    if not scheme:
        return jsonify({'error': 'Scheme not found'}), 404
    
    doc_check = engine.check_documents(household_id, household['documents'], scheme['required_docs'])
    
    return jsonify(doc_check)

@app.route('/api/submit-correction', methods=['POST'])
@login_required
def submit_correction():
    data = request.json
    household_id = data.get('household_id')
    rejection_reason = data.get('rejection_reason')
    scheme_name = data.get('scheme_name')
    
    details = f"Rejected for {scheme_name}: {rejection_reason}"
    log_interaction(household_id, 'rejection', details)
    log_interaction(household_id, 'correction_loop', f'Correction needed: {rejection_reason}')
    
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
@login_required
def dashboard_stats():
    stats = get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/test')
def test_api():
    return jsonify({'status': 'API is working', 'message': 'Success!'})
if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('entitleai.db'):
        print("📦 Database not found. Generating fresh data...")
        import generate_households
        generate_households.generate_realistic_households()
    
    app.run(debug=True, port=5000)