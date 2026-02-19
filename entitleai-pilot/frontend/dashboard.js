// Dashboard JavaScript
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
}