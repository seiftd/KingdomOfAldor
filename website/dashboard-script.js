/**
 * Kingdom of Aldoria - Admin Dashboard JavaScript
 * Handles authentication, navigation, and data visualization
 */

// Admin credentials (in production, this should be handled server-side)
const ADMIN_CREDENTIALS = {
    email: 'seiftouatilol@gmail.com',
    password: 'seif0662'
};

// Mock data for dashboard (in production, this would come from API)
const dashboardData = {
    revenue: {
        total: 12847.50,
        breakdown: {
            subscriptions: 8450.00,
            gems: 3120.50,
            items: 1277.00
        },
        paymentMethods: {
            redotpay: 7230.25,
            binance: 4120.75,
            cards: 1496.50
        }
    },
    players: {
        active: 2847,
        vip: 342,
        total: 15420
    },
    ads: {
        revenue: 2847.92,
        impressions: 847291,
        ctr: 3.2,
        rpm: 3.36,
        sources: {
            admob: { revenue: 1542.30, percentage: 54.2 },
            unity: { revenue: 892.15, percentage: 31.3 },
            ironsource: { revenue: 413.47, percentage: 14.5 }
        }
    },
    subscriptions: [
        {
            id: 'PLR_001',
            name: 'DragonSlayer_99',
            type: 'Monthly',
            startDate: '2024-01-15',
            endDate: '2024-02-15',
            status: 'active'
        },
        {
            id: 'PLR_002',
            name: 'MysticKnight_42',
            type: 'Weekly',
            startDate: '2024-01-20',
            endDate: '2024-01-27',
            status: 'ending'
        },
        {
            id: 'PLR_003',
            name: 'ShadowMage_77',
            type: 'Monthly',
            startDate: '2024-01-10',
            endDate: '2024-02-10',
            status: 'active'
        },
        {
            id: 'PLR_004',
            name: 'FireWarrior_23',
            type: 'Weekly',
            startDate: '2024-01-18',
            endDate: '2024-01-25',
            status: 'expired'
        }
    ],
    vipPlayers: [
        {
            id: 'PLR_001',
            name: 'DragonSlayer_99',
            level: 85,
            spent: 250.00,
            joinDate: '2024-01-15'
        },
        {
            id: 'PLR_003',
            name: 'ShadowMage_77',
            level: 72,
            spent: 180.50,
            joinDate: '2024-01-10'
        },
        {
            id: 'PLR_005',
            name: 'IceQueen_88',
            level: 91,
            spent: 320.75,
            joinDate: '2024-01-08'
        },
        {
            id: 'PLR_007',
            name: 'ThunderLord_55',
            level: 67,
            spent: 145.25,
            joinDate: '2024-01-12'
        }
    ]
};

// Chart instances
let revenueChart = null;
let activityChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeLogin();
    initializeNavigation();
    initializeDashboard();
});

// Login functionality
function initializeLogin() {
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (email === ADMIN_CREDENTIALS.email && password === ADMIN_CREDENTIALS.password) {
            // Successful login
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('dashboard-content').style.display = 'flex';
            loadDashboardData();
        } else {
            // Failed login
            loginError.style.display = 'block';
            setTimeout(() => {
                loginError.style.display = 'none';
            }, 3000);
        }
    });
    
    // Logout functionality
    document.getElementById('logout-btn').addEventListener('click', function() {
        document.getElementById('login-screen').style.display = 'flex';
        document.getElementById('dashboard-content').style.display = 'none';
        
        // Clear form
        document.getElementById('email').value = '';
        document.getElementById('password').value = '';
    });
}

// Navigation functionality
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.dashboard-section');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetSection = this.dataset.section;
            
            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(`${targetSection}-section`).classList.add('active');
            
            // Load section-specific data
            loadSectionData(targetSection);
        });
    });
}

// Initialize dashboard components
function initializeDashboard() {
    // Set up chart containers
    setupCharts();
}

// Load dashboard data
function loadDashboardData() {
    updateOverviewStats();
    updateRevenueData();
    updateAdsData();
    updateSubscriptionsData();
    updateUsersData();
    updateAnalyticsData();
    createCharts();
}

// Update overview statistics
function updateOverviewStats() {
    document.getElementById('total-revenue').textContent = `$${dashboardData.revenue.total.toLocaleString()}`;
    document.getElementById('active-players').textContent = dashboardData.players.active.toLocaleString();
    document.getElementById('vip-subscribers').textContent = dashboardData.players.vip.toLocaleString();
    document.getElementById('ad-impressions').textContent = dashboardData.ads.impressions.toLocaleString();
}

// Update revenue data
function updateRevenueData() {
    // This would typically fetch data from an API
    console.log('Revenue data updated');
}

// Update ads data
function updateAdsData() {
    // This would typically fetch data from an API
    console.log('Ads data updated');
}

// Update subscriptions data
function updateSubscriptionsData() {
    const subscriptionList = document.getElementById('subscription-list');
    subscriptionList.innerHTML = '';
    
    dashboardData.subscriptions.forEach(sub => {
        const row = document.createElement('tr');
        const statusClass = `status-${sub.status}`;
        
        row.innerHTML = `
            <td>${sub.id}</td>
            <td>${sub.name}</td>
            <td>${sub.type}</td>
            <td>${sub.startDate}</td>
            <td>${sub.endDate}</td>
            <td class="${statusClass}">${sub.status.charAt(0).toUpperCase() + sub.status.slice(1)}</td>
        `;
        
        subscriptionList.appendChild(row);
    });
}

// Update users data
function updateUsersData() {
    const vipList = document.getElementById('vip-list');
    vipList.innerHTML = '';
    
    dashboardData.vipPlayers.forEach(player => {
        const card = document.createElement('div');
        card.className = 'vip-card';
        
        card.innerHTML = `
            <div class="player-name">${player.name}</div>
            <div class="player-info">Level ${player.level}</div>
            <div class="player-info">Spent: $${player.spent}</div>
            <div class="player-info">Joined: ${player.joinDate}</div>
        `;
        
        vipList.appendChild(card);
    });
}

// Update analytics data
function updateAnalyticsData() {
    // This would typically fetch data from an API
    console.log('Analytics data updated');
}

// Load section-specific data
function loadSectionData(section) {
    switch(section) {
        case 'overview':
            updateOverviewStats();
            break;
        case 'revenue':
            updateRevenueData();
            break;
        case 'ads':
            updateAdsData();
            break;
        case 'subscriptions':
            updateSubscriptionsData();
            break;
        case 'users':
            updateUsersData();
            break;
        case 'analytics':
            updateAnalyticsData();
            break;
    }
}

// Setup chart containers
function setupCharts() {
    // Ensure Chart.js is available (would be loaded from CDN in production)
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded. Charts will not be displayed.');
        return;
    }
}

// Create charts
function createCharts() {
    createRevenueChart();
    createActivityChart();
}

// Create revenue trend chart
function createRevenueChart() {
    const ctx = document.getElementById('revenue-chart');
    if (!ctx || typeof Chart === 'undefined') return;
    
    // Generate sample data for the last 30 days
    const labels = [];
    const data = [];
    const today = new Date();
    
    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        // Generate realistic revenue data with some variation
        const baseRevenue = 400 + (Math.sin(i / 5) * 100) + (Math.random() * 200);
        data.push(Math.round(baseRevenue * 100) / 100);
    }
    
    if (revenueChart) {
        revenueChart.destroy();
    }
    
    revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Revenue ($)',
                data: data,
                borderColor: '#FFD700',
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#F8F8FF'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#F8F8FF'
                    },
                    grid: {
                        color: 'rgba(255, 215, 0, 0.2)'
                    }
                },
                y: {
                    ticks: {
                        color: '#F8F8FF',
                        callback: function(value) {
                            return '$' + value;
                        }
                    },
                    grid: {
                        color: 'rgba(255, 215, 0, 0.2)'
                    }
                }
            }
        }
    });
}

// Create player activity chart
function createActivityChart() {
    const ctx = document.getElementById('activity-chart');
    if (!ctx || typeof Chart === 'undefined') return;
    
    const hours = [];
    const players = [];
    
    // Generate 24-hour activity data
    for (let i = 0; i < 24; i++) {
        hours.push(`${i}:00`);
        
        // Simulate realistic player activity (higher during evening hours)
        let baseActivity;
        if (i >= 6 && i <= 9) {
            baseActivity = 150 + (Math.random() * 50); // Morning peak
        } else if (i >= 18 && i <= 23) {
            baseActivity = 200 + (Math.random() * 100); // Evening peak
        } else if (i >= 0 && i <= 5) {
            baseActivity = 50 + (Math.random() * 30); // Night
        } else {
            baseActivity = 100 + (Math.random() * 80); // Day
        }
        
        players.push(Math.round(baseActivity));
    }
    
    if (activityChart) {
        activityChart.destroy();
    }
    
    activityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hours,
            datasets: [{
                label: 'Active Players',
                data: players,
                backgroundColor: 'rgba(75, 0, 130, 0.7)',
                borderColor: '#4B0082',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#F8F8FF'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#F8F8FF'
                    },
                    grid: {
                        color: 'rgba(255, 215, 0, 0.2)'
                    }
                },
                y: {
                    ticks: {
                        color: '#F8F8FF'
                    },
                    grid: {
                        color: 'rgba(255, 215, 0, 0.2)'
                    }
                }
            }
        }
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Auto-refresh dashboard data every 5 minutes
setInterval(() => {
    if (document.getElementById('dashboard-content').style.display !== 'none') {
        loadDashboardData();
        console.log('Dashboard data refreshed');
    }
}, 5 * 60 * 1000);

// Export for potential external use
window.DashboardManager = {
    loadDashboardData,
    updateOverviewStats,
    updateSubscriptionsData,
    updateUsersData
};