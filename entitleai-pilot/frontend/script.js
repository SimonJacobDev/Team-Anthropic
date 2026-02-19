// State management
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
window.checkDocuments = checkDocuments;