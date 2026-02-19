class RulesEngine:
    """Eligibility rules engine for ALL Indian welfare schemes"""
    
    def __init__(self):
        self.schemes = self.load_all_schemes()
    
    def load_all_schemes(self):
        """Load ALL 40+ government schemes with eligibility criteria"""
        return {
            # ========== PENSION SCHEMES (5) ==========
            "Indira Gandhi National Old Age Pension": {
                "name": "IGNOAPS - Old Age Pension",
                "category": "Pension",
                "ministry": "Ministry of Rural Development",
                "criteria": {
                    "min_age": 60,
                    "max_income": 5000,  # BPL threshold
                    "ration_type": ["PHH", "AAY"],
                    "bpl_required": True
                },
                "documents": ["Age Proof", "BPL Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹200-500/month + State top-up",
                "reference": "NSAP"
            },
            
            "Indira Gandhi National Widow Pension": {
                "name": "IGNWPS - Widow Pension",
                "category": "Pension",
                "criteria": {
                    "gender": "Female",
                    "min_age": 40,
                    "max_age": 79,
                    "marital_status": "Widow",
                    "max_income": 5000,
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Age Proof", "BPL Certificate", "Husband Death Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹300-500/month",
                "reference": "NSAP"
            },
            
            "Indira Gandhi National Disability Pension": {
                "name": "IGNDPS - Disability Pension",
                "category": "Pension",
                "criteria": {
                    "min_age": 18,
                    "max_age": 79,
                    "disability": ["Visual", "Physical", "Hearing", "Multiple"],
                    "max_income": 5000,
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Disability Certificate", "Age Proof", "BPL Certificate", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹300-500/month",
                "reference": "NSAP"
            },
            
            "Pradhan Mantri Shram Yogi Maan-dhan": {
                "name": "PM-SYM - Pension for Unorganised Workers",
                "category": "Pension",
                "criteria": {
                    "min_age": 18,
                    "max_age": 40,
                    "occupation": ["Daily Wage Labor", "Street Vendor", "Construction Worker", 
                                 "Rickshaw Puller", "Domestic Help", "Fisherman", "Cobbler", 
                                 "Farm Labor", "Beedi Worker", "Weaver"],
                    "max_income": 15000
                },
                "documents": ["Aadhaar Card", "Bank Passbook", "Age Proof"],
                "benefit": "₹3,000/month after 60 years",
                "reference": "Ministry of Labour"
            },
            
            "National Pension Scheme for Traders": {
                "name": "NPS - Traders and Self-Employed",
                "category": "Pension",
                "criteria": {
                    "min_age": 18,
                    "max_age": 40,
                    "occupation": ["Shopkeeper", "Small Business Owner", "Street Vendor", "Cobbler", "Potter"]
                },
                "documents": ["Aadhaar Card", "Bank Passbook", "Age Proof", "Business Proof"],
                "benefit": "₹3,000/month after 60 years",
                "reference": "Ministry of Labour"
            },
            
            # ========== INSURANCE SCHEMES (4) ==========
            "Pradhan Mantri Jeevan Jyoti Bima Yojana": {
                "name": "PMJJBY - Life Insurance",
                "category": "Insurance",
                "criteria": {
                    "min_age": 18,
                    "max_age": 50,
                    "bank_account": True
                },
                "documents": ["Aadhaar Card", "Bank Passbook"],
                "benefit": "Life cover of ₹2 lakh",
                "premium": "₹436/year",
                "reference": "Ministry of Finance"
            },
            
            "Pradhan Mantri Suraksha Bima Yojana": {
                "name": "PMSBY - Accident Insurance",
                "category": "Insurance",
                "criteria": {
                    "min_age": 18,
                    "max_age": 70,
                    "bank_account": True
                },
                "documents": ["Aadhaar Card", "Bank Passbook"],
                "benefit": "Accidental death: ₹2 lakh, Partial disability: ₹1 lakh",
                "premium": "₹20/year",
                "reference": "Ministry of Finance"
            },
            
            "Ayushman Bharat - PM Jan Arogya Yojana": {
                "name": "PM-JAY - Health Insurance",
                "category": "Health Insurance",
                "criteria": {
                    "max_income": 5000,
                    "caste": ["SC", "ST"],
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Aadhaar Card", "Ration Card"],
                "benefit": "Health cover of ₹5 lakh/family/year",
                "reference": "National Health Authority"
            },
            
            "PM RAHAT Scheme": {
                "name": "PM RAHAT - Accident Care",
                "category": "Health Insurance",
                "criteria": {},
                "documents": ["Aadhaar Card", "Accident Report"],
                "benefit": "Cashless treatment up to ₹1.5 lakh",
                "reference": "PMO"
            },
            
            # ========== FOOD & NUTRITION (3) ==========
            "National Food Security Act": {
                "name": "NFSA - Food Security",
                "category": "Food Security",
                "criteria": {
                    "ration_type": ["PHH", "AAY"]
                },
                "documents": ["Ration Card", "Aadhaar Card"],
                "benefit": "5 kg grain/person/month at subsidized rates",
                "reference": "Ministry of Food"
            },
            
            "Pradhan Mantri Matru Vandana Yojana": {
                "name": "PMMVY - Maternity Benefit",
                "category": "Women & Child",
                "criteria": {
                    "gender": "Female",
                    "min_age": 19,
                    "pregnancy_status": "Pregnant"
                },
                "documents": ["Aadhaar Card", "Pregnancy Certificate", "Bank Passbook"],
                "benefit": "₹5,000 in 3 installments",
                "reference": "Ministry of Women & Child Development"
            },
            
            "Mid-Day Meal Scheme": {
                "name": "Mid-Day Meal",
                "category": "Food Security",
                "criteria": {
                    "student": True,
                    "max_age": 14
                },
                "documents": ["School Enrollment"],
                "benefit": "Free cooked meal at school",
                "reference": "Ministry of Education"
            },
            
            # ========== HOUSING SCHEMES (3) ==========
            "Pradhan Mantri Awas Yojana - Gramin": {
                "name": "PMAY-G - Rural Housing",
                "category": "Housing",
                "criteria": {
                    "ration_type": ["PHH", "AAY"],
                    "landholding": 0.5,
                    "rural": True,
                    "max_income": 5000
                },
                "documents": ["Aadhaar Card", "Ration Card", "Land Records"],
                "benefit": "₹1.20 lakh for house construction",
                "reference": "Ministry of Rural Development"
            },
            
            "Pradhan Mantri Awas Yojana - Urban": {
                "name": "PMAY-U - Urban Housing",
                "category": "Housing",
                "criteria": {
                    "urban": True,
                    "max_income": 300000
                },
                "documents": ["Aadhaar Card", "Income Certificate"],
                "benefit": "Interest subsidy on housing loans",
                "reference": "Ministry of Housing"
            },
            
            "Pradhan Mantri Ujjwala Yojana": {
                "name": "PMUY - Free LPG Connection",
                "category": "Energy",
                "criteria": {
                    "ration_type": ["PHH", "AAY"],
                    "max_income": 5000
                },
                "documents": ["Aadhaar Card", "Ration Card"],
                "benefit": "Free LPG connection with first cylinder",
                "reference": "Ministry of Petroleum"
            },
            
            # ========== FARMER SCHEMES (4) ==========
            "PM-KISAN": {
                "name": "PM-KISAN - Farmer Income Support",
                "category": "Farmer Support",
                "criteria": {
                    "landholding": 2.0,
                    "occupation": ["Farmer"]
                },
                "documents": ["Land Records", "Bank Passbook", "Aadhaar Card"],
                "benefit": "₹6,000 per year (₹2,000 x 3 installments)",
                "reference": "Ministry of Agriculture"
            },
            
            "Pradhan Mantri Fasal Bima Yojana": {
                "name": "PMFBY - Crop Insurance",
                "category": "Farmer Support",
                "criteria": {
                    "occupation": ["Farmer"],
                    "landholding": 0.1
                },
                "documents": ["Land Records", "Aadhaar Card", "Bank Passbook"],
                "benefit": "Crop insurance at nominal premium",
                "reference": "Ministry of Agriculture"
            },
            
            "Kisan Credit Card": {
                "name": "KCC - Agricultural Credit",
                "category": "Farmer Support",
                "criteria": {
                    "occupation": ["Farmer", "Fisherman"],
                    "min_age": 18
                },
                "documents": ["Land Records", "Aadhaar Card", "Bank Passbook"],
                "benefit": "Short-term loans at subsidized interest",
                "reference": "Ministry of Agriculture"
            },
            
            "Agriculture Infrastructure Fund": {
                "name": "AIF - Farm Infrastructure",
                "category": "Farmer Support",
                "criteria": {
                    "occupation": ["Farmer"],
                    "landholding": 0.5
                },
                "documents": ["Land Records", "Aadhaar Card", "Project Report"],
                "benefit": "Loans for post-harvest infrastructure",
                "reference": "Ministry of Agriculture"
            },
            
            # ========== EMPLOYMENT SCHEMES (3) ==========
            "Mahatma Gandhi NREGA": {
                "name": "MGNREGA - Rural Employment",
                "category": "Employment",
                "criteria": {
                    "min_age": 18,
                    "max_age": 60,
                    "rural": True,
                    "occupation": ["Daily Wage Labor", "Unemployed", "Farm Labor"]
                },
                "documents": ["Aadhaar Card", "Job Card", "Bank Passbook"],
                "benefit": "100 days guaranteed work per year",
                "reference": "Ministry of Rural Development"
            },
            
            "Deen Dayal Upadhyaya Grameen Kaushalya Yojana": {
                "name": "DDU-GKY - Skill Training",
                "category": "Employment",
                "criteria": {
                    "min_age": 15,
                    "max_age": 35,
                    "rural": True,
                    "education_level": ["8th", "9th", "10th", "12th", "Graduate"]
                },
                "documents": ["Aadhaar Card", "Education Certificate", "Bank Passbook"],
                "benefit": "Free skill training with placement assistance",
                "reference": "Ministry of Rural Development"
            },
            
            "PM SVANidhi": {
                "name": "PM SVANidhi - Street Vendor Loan",
                "category": "Employment",
                "criteria": {
                    "occupation": ["Street Vendor"],
                    "urban": True
                },
                "documents": ["Aadhaar Card", "Vending Certificate"],
                "benefit": "Working capital loan up to ₹10,000",
                "reference": "Ministry of Housing"
            },
            
            # ========== EDUCATION SCHEMES (6) ==========
            "Pre-Matric Scholarship for SC Students": {
                "name": "Pre-Matric Scholarship (SC)",
                "category": "Education",
                "criteria": {
                    "caste": ["SC"],
                    "min_age": 14,
                    "max_age": 18,
                    "max_income": 250000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Aadhaar Card", "Bank Passbook"],
                "benefit": "₹350-750/month + other allowances",
                "reference": "Ministry of Social Justice"
            },
            
            "Pre-Matric Scholarship for ST Students": {
                "name": "Pre-Matric Scholarship (ST)",
                "category": "Education",
                "criteria": {
                    "caste": ["ST"],
                    "min_age": 14,
                    "max_age": 18,
                    "max_income": 250000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Aadhaar Card", "Bank Passbook"],
                "benefit": "₹350-750/month + other allowances",
                "reference": "Ministry of Tribal Affairs"
            },
            
            "Pre-Matric Scholarship for OBC Students": {
                "name": "Pre-Matric Scholarship (OBC)",
                "category": "Education",
                "criteria": {
                    "caste": ["OBC", "BC"],
                    "min_age": 14,
                    "max_age": 18,
                    "max_income": 200000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Aadhaar Card", "Bank Passbook"],
                "benefit": "₹350-750/month + other allowances",
                "reference": "Ministry of Social Justice"
            },
            
            "Post-Matric Scholarship for SC Students": {
                "name": "Post-Matric Scholarship (SC)",
                "category": "Education",
                "criteria": {
                    "caste": ["SC"],
                    "min_age": 18,
                    "max_income": 250000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Aadhaar Card", "Bank Passbook", "Admission Proof"],
                "benefit": "Full tuition + maintenance allowance",
                "reference": "Ministry of Social Justice"
            },
            
            "Post-Matric Scholarship for ST Students": {
                "name": "Post-Matric Scholarship (ST)",
                "category": "Education",
                "criteria": {
                    "caste": ["ST"],
                    "min_age": 18,
                    "max_income": 250000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Aadhaar Card", "Bank Passbook", "Admission Proof"],
                "benefit": "Full tuition + maintenance allowance",
                "reference": "Ministry of Tribal Affairs"
            },
            
            "National Overseas Scholarship": {
                "name": "National Overseas Scholarship",
                "category": "Education",
                "criteria": {
                    "caste": ["SC", "ST"],
                    "education_level": "Post Graduate",
                    "max_income": 800000
                },
                "documents": ["Caste Certificate", "Income Certificate", "Marksheet", "Passport", "Admission Letter"],
                "benefit": "Full tuition + living expenses for study abroad",
                "reference": "Ministry of Social Justice"
            },
            
            # ========== WOMEN SCHEMES (4) ==========
            "Ladli Laxmi Yojana": {
                "name": "Ladli Laxmi Yojana",
                "category": "Women & Child",
                "criteria": {
                    "gender": "Female",
                    "max_age": 5,
                    "max_income": 5000
                },
                "documents": ["Birth Certificate", "Aadhaar Card", "BPL Certificate"],
                "benefit": "₹1.20 lakh from birth to 21 years",
                "reference": "MP Government"
            },
            
            "Sukanya Samriddhi Yojana": {
                "name": "Sukanya Samriddhi Yojana",
                "category": "Women & Child",
                "criteria": {
                    "gender": "Female",
                    "max_age": 10
                },
                "documents": ["Birth Certificate", "Aadhaar Card"],
                "benefit": "High-interest savings scheme with tax benefits",
                "reference": "Ministry of Finance"
            },
            
            "Lakhpati Didi Scheme": {
                "name": "Lakhpati Didi",
                "category": "Women Empowerment",
                "criteria": {
                    "gender": "Female",
                    "rural": True
                },
                "documents": ["Aadhaar Card", "Bank Passbook"],
                "benefit": "Income support to become 'Lakhpati'",
                "reference": "Ministry of Rural Development"
            },
            
            "Rani Lakshmi Bai Scooty Yojana": {
                "name": "RLB Scooty Yojana",
                "category": "Women Empowerment",
                "criteria": {
                    "gender": "Female",
                    "min_age": 17,
                    "max_age": 21,
                    "education_level": "12th",
                    "state": "Uttar Pradesh"
                },
                "documents": ["Aadhaar Card", "Marksheet", "Admission Proof"],
                "benefit": "Free scooty for college education",
                "reference": "UP Government"
            },
            
            # ========== SPECIAL COMMUNITY SCHEMES (3) ==========
            "Scheme for Economic Empowerment of DNTs": {
                "name": "SEED for DNT Communities",
                "category": "Special Community",
                "criteria": {
                    "community": ["DNT"],
                    "max_income": 800000
                },
                "documents": ["Community Certificate", "Income Certificate", "Aadhaar Card"],
                "benefit": "Coaching for competitive exams + Health insurance",
                "reference": "DWBDNC"
            },
            
            "Vanbandhu Kalyan Yojana": {
                "name": "Vanbandhu Kalyan Yojana",
                "category": "Special Community",
                "criteria": {
                    "caste": ["ST"]
                },
                "documents": ["Caste Certificate", "Aadhaar Card"],
                "benefit": "Comprehensive tribal development package",
                "reference": "Ministry of Tribal Affairs"
            },
            
            "National Safai Karamcharis Finance & Development Corporation": {
                "name": "NSKFDC - Safai Karamchari Welfare",
                "category": "Special Community",
                "criteria": {
                    "occupation": ["Safai Karamchari"]
                },
                "documents": ["Identity Card", "Aadhaar Card", "Bank Passbook"],
                "benefit": "Loans for income generation + Skill training",
                "reference": "Ministry of Social Justice"
            },
            
            # ========== BUSINESS SCHEMES (3) ==========
            "PM Mudra Yojana": {
                "name": "Pradhan Mantri Mudra Yojana",
                "category": "Business",
                "criteria": {
                    "business_type": "Micro enterprise"
                },
                "documents": ["Aadhaar Card", "Business Plan", "Bank Passbook"],
                "benefit": "Loans up to ₹10 lakh",
                "reference": "Ministry of Finance"
            },
            
            "Stand-Up India": {
                "name": "Stand-Up India",
                "category": "Business",
                "criteria": {
                    "caste": ["SC", "ST"],
                    "gender": "Female"
                },
                "documents": ["Aadhaar Card", "Caste Certificate", "Business Plan"],
                "benefit": "Bank loans (₹10 lakh to ₹1 crore)",
                "reference": "Ministry of Finance"
            },
            
            "Startup India Fund of Funds 2.0": {
                "name": "Startup India Fund of Funds",
                "category": "Business",
                "criteria": {
                    "business_type": "Startup"
                },
                "documents": ["DPIIT Recognition", "Business Plan"],
                "benefit": "Fund of Funds support from ₹10,000 crore corpus",
                "reference": "DPIIT"
            }
        }
    
    def check_eligibility(self, household):
        """Check household eligibility for ALL schemes"""
        eligible = []
        
        for scheme_id, scheme in self.schemes.items():
            criteria = scheme["criteria"]
            eligible_flag = True
            
            # Age checks
            if "min_age" in criteria:
                if household.get('age', 0) < criteria["min_age"]:
                    eligible_flag = False
            
            if "max_age" in criteria:
                if household.get('age', 0) > criteria["max_age"]:
                    eligible_flag = False
            
            # Gender check
            if "gender" in criteria:
                if household.get('gender') != criteria["gender"]:
                    eligible_flag = False
            
            # Income check
            if "max_income" in criteria:
                if household.get('income', 999999) > criteria["max_income"]:
                    eligible_flag = False
            
            # Ration type check
            if "ration_type" in criteria:
                if household.get('ration_type') not in criteria["ration_type"]:
                    eligible_flag = False
            
            # Landholding check
            if "landholding" in criteria:
                if isinstance(criteria["landholding"], (int, float)):
                    if household.get('landholding', 999) > criteria["landholding"]:
                        eligible_flag = False
                elif criteria["landholding"] == 0:
                    if household.get('landholding', 1) > 0:
                        eligible_flag = False
            
            # Occupation check
            if "occupation" in criteria:
                if household.get('occupation') not in criteria["occupation"]:
                    eligible_flag = False
            
            # Disability check
            if "disability" in criteria:
                if household.get('disability') not in criteria["disability"]:
                    eligible_flag = False
            
            # Caste check
            if "caste" in criteria:
                if household.get('caste') not in criteria["caste"]:
                    eligible_flag = False
            
            # Marital status check
            if "marital_status" in criteria:
                if household.get('marital_status') != criteria["marital_status"]:
                    eligible_flag = False
            
            if eligible_flag:
                eligible.append({
                    "scheme_id": scheme_id,
                    "scheme_name": scheme["name"],
                    "category": scheme.get("category", "General"),
                    "benefit": scheme["benefit"],
                    "required_docs": scheme["documents"],
                    "reference": scheme.get("reference", "")
                })
        
        return eligible
    
    def check_documents(self, household_id, household_docs, scheme_docs):
        """Check if household has required documents for a scheme"""
        missing_docs = []
        present_docs = []
        
        for doc in scheme_docs:
            found = False
            for h_doc in household_docs:
                if h_doc['doc_type'] == doc and h_doc.get('has_doc', False):
                    found = True
                    present_docs.append({
                        "doc_type": doc,
                        "doc_number": h_doc.get('doc_number', '')
                    })
                    break
            
            if not found:
                missing_docs.append(doc)
        
        return {
            "present": present_docs,
            "missing": missing_docs,
            "complete": len(missing_docs) == 0
        }