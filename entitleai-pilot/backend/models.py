from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='officer')
    district = db.Column(db.String(100), default='Villupuram')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Household(db.Model):
    __tablename__ = 'households'
    
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    income = db.Column(db.Integer, nullable=False)
    ration_type = db.Column(db.String(10), nullable=False)
    landholding = db.Column(db.Float, default=0)
    occupation = db.Column(db.String(50))
    disability = db.Column(db.String(50), default='None')
    village = db.Column(db.String(100))
    caste = db.Column(db.String(20))
    aadhaar_number = db.Column(db.String(12), unique=True)
    ration_card_number = db.Column(db.String(20))
    phone_number = db.Column(db.String(10))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class EnrolledScheme(db.Model):
    __tablename__ = 'enrolled_schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.String(20), db.ForeignKey('households.id'))
    scheme_name = db.Column(db.String(100))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.String(20), db.ForeignKey('households.id'))
    doc_type = db.Column(db.String(50))
    doc_number = db.Column(db.String(50))
    has_doc = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class InteractionLog(db.Model):
    __tablename__ = 'interaction_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.String(20), db.ForeignKey('households.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)