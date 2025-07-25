/**
 * Kingdom of Aldoria Admin Dashboard JavaScript
 * Handles authentication, data visualization, and dashboard functionality
 */

// Global variables
let currentUser = null;
let dashboardData = {};
let updateInterval = null;
let charts = {};

// Configuration
const CONFIG = {
    adminEmail: 'seiftouatilol@gmail.com',
    adminPassword: 'seif0662',
    updateInterval: 30000, // 30 seconds
    charts: {
        colors: {
            primary: '#FFD700',
            blue: '#3B82F6',
            green: '#10B981',
            red: '#EF4444',
            purple: '#8B5CF6',
            orange: '#F59E0B'
        }
    }
};

// Initialize dashboard when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    console.log('🎮 Kingdom of Aldoria Admin Dashboard initializing...');
    
    // Set up login form
    setupLoginForm();
    
    // Load mock data
    loadMockData();
    
    // Check if already logged in
    const savedSession = localStorage.getItem('koa_admin_session');
    if (savedSession) {
        try {
            const session = JSON.parse(savedSession);
            if (Date.now() - session.timestamp < 86400000) { // 24 hours
                handleSuccessfulLogin();
                return;
            }
        } catch (e) {
            localStorage.removeItem('koa_admin_session');
        }
    }
    
    // Show login screen
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('dashboard').style.display = 'none';
}

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', handleLogin);
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    const loginBtn = document.querySelector('.login-btn');
    const loginText = document.querySelector('.login-text');
    const loginLoading = document.querySelector('.login-loading');
    
    // Clear previous errors
    errorDiv.style.display = 'none';
    
    // Show loading state
    loginText.style.display = 'none';
    loginLoading.style.display = 'inline';
    loginBtn.disabled = true;
    
    // Simulate authentication delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    if (email === CONFIG.adminEmail && password === CONFIG.adminPassword) {
        // Successful login
        const session = {
            email: email,
            timestamp: Date.now(),
            sessionId: generateSessionId()
        };
        
        localStorage.setItem('koa_admin_session', JSON.stringify(session));
        currentUser = { email, name: 'Seif Touati' };
        
        handleSuccessfulLogin();
    } else {
        // Failed login
        errorDiv.textContent = 'Invalid email or password. Please try again.';
        errorDiv.style.display = 'block';
        
        // Reset button state
        loginText.style.display = 'inline';
        loginLoading.style.display = 'none';
        loginBtn.disabled = false;
    }
}

function handleSuccessfulLogin() {
    console.log('✅ Admin login successful');
    
    // Hide login screen and show dashboard
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('dashboard').style.display = 'flex';
    
    // Initialize dashboard components
    initializeDashboardComponents();
    
    // Start data refresh interval
    startDataRefresh();
    
    // Update last updated time
    updateLastUpdatedTime();
}

function initializeDashboardComponents() {
    // Set up tab switching
    setupTabSwitching();
    
    // Initialize charts
    initializeCharts();
    
    // Load initial data
    updateDashboardData();
    
    // Setup real-time updates
    setupRealTimeUpdates();
    
    console.log('📊 Dashboard components initialized');
}

function setupTabSwitching() {
    // Add click event listeners to nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.onclick.toString().match(/switchTab\('(.+?)'\)/)[1];
            switchTab(tab);
        });
    });
}

function switchTab(tabName) {
    // Update navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Load tab-specific data
    loadTabData(tabName);
    
    console.log(`📋 Switched to ${tabName} tab`);
}

function loadTabData(tabName) {
    switch(tabName) {
        case 'overview':
            updateOverviewData();
            break;
        case 'revenue':
            updateRevenueData();
            break;
        case 'ads':
            updateAdsData();
            break;
        case 'players':
            updatePlayersData();
            break;
        case 'subscriptions':
            updateSubscriptionsData();
            break;
        case 'settings':
            loadSettings();
            break;
    }
}

function initializeCharts() {
    Chart.defaults.color = '#B0B9C9';
    Chart.defaults.borderColor = '#2A3441';
    Chart.defaults.backgroundColor = 'rgba(59, 130, 246, 0.1)';
    
    // Revenue Trend Chart
    const revenueCtx = document.getElementById('revenue-chart').getContext('2d');
    charts.revenue = new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Daily Revenue',
                data: [],
                borderColor: CONFIG.charts.colors.primary,
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
    
    // Player Activity Chart
    const activityCtx = document.getElementById('activity-chart').getContext('2d');
    charts.activity = new Chart(activityCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Daily Active Users',
                data: [],
                backgroundColor: CONFIG.charts.colors.blue,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Revenue Source Chart
    const sourceCtx = document.getElementById('revenue-source-chart');
    if (sourceCtx) {
        charts.revenueSource = new Chart(sourceCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Subscriptions', 'In-App Purchases', 'Ads'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        CONFIG.charts.colors.primary,
                        CONFIG.charts.colors.blue,
                        CONFIG.charts.colors.green
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    console.log('📈 Charts initialized');
}

function loadMockData() {
    // Simulate realistic game data
    dashboardData = {
        overview: {
            totalRevenue: 45230.50,
            activePlayers: 1247,
            adsToday: 8934,
            conversionRate: 3.2
        },
        revenue: {
            subscription: 28500.00,
            iap: 14230.50,
            ads: 2500.00,
            weekly: 18200.00,
            monthly: 10300.00,
            legendary: 8900.50,
            starter: 5330.00,
            rewardedAds: 1800.00,
            interstitial: 700.00
        },
        ads: {
            dailyViews: 8934,
            successRate: 94.2,
            rpm: 2.80,
            fillRate: 96.5,
            sources: {
                'AdMob': { attempts: 3250, successes: 3088, revenue: 850 },
                'Unity Ads': { attempts: 2100, successes: 1995, revenue: 520 },
                'AppLovin': { attempts: 1800, successes: 1692, revenue: 480 },
                'IronSource': { attempts: 1500, successes: 1425, revenue: 390 },
                'Vungle': { attempts: 1200, successes: 1116, revenue: 310 },
                'Facebook Audience Network': { attempts: 980, successes: 901, revenue: 250 },
                'TikTok Ads': { attempts: 750, successes: 668, revenue: 180 },
                'Chartboost': { attempts: 650, successes: 585, revenue: 160 }
            }
        },
        players: {
            total: 15634,
            dau: 1247,
            wau: 4892,
            mau: 12456
        },
        subscriptions: {
            weekly: {
                active: 186,
                revenue: 18200.00,
                conversion: 4.1
            },
            monthly: {
                active: 64,
                revenue: 10300.00,
                conversion: 2.8
            },
            expiring: [
                { player: 'DragonSlayer93', type: 'Monthly VIP', expires: '2024-01-15' },
                { player: 'MysticMage', type: 'Weekly Pass', expires: '2024-01-12' },
                { player: 'ShadowKnight', type: 'Monthly VIP', expires: '2024-01-16' },
                { player: 'IceQueen42', type: 'Weekly Pass', expires: '2024-01-13' }
            ]
        },
        recentActivity: [
            { text: 'New player registered: DragonMaster2024', time: '2 minutes ago' },
            { text: 'Legendary weapon purchased: Excalibur ($14.99)', time: '5 minutes ago' },
            { text: 'Monthly VIP subscription renewed: ShadowKnight', time: '8 minutes ago' },
            { text: 'Ad campaign performance alert: Unity Ads above target', time: '12 minutes ago' },
            { text: 'Weekly Pass purchased: MysticWizard ($4.99)', time: '15 minutes ago' }
        ],
        charts: {
            revenue: {
                labels: generateDateLabels(30),
                data: generateMockRevenueData(30)
            },
            activity: {
                labels: generateDateLabels(7),
                data: generateMockActivityData(7)
            }
        }
    };
}

function generateDateLabels(days) {
    const labels = [];
    for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    }
    return labels;
}

function generateMockRevenueData(days) {
    const data = [];
    let baseRevenue = 1200;
    for (let i = 0; i < days; i++) {
        // Add some realistic variation
        const variation = (Math.random() - 0.5) * 600;
        const weekendBoost = (i % 7 === 0 || i % 7 === 6) ? 200 : 0;
        data.push(Math.max(0, baseRevenue + variation + weekendBoost));
    }
    return data;
}

function generateMockActivityData(days) {
    const data = [];
    let baseActivity = 1000;
    for (let i = 0; i < days; i++) {
        const variation = (Math.random() - 0.5) * 400;
        const weekendBoost = (i % 7 === 0 || i % 7 === 6) ? 300 : 0;
        data.push(Math.max(0, Math.round(baseActivity + variation + weekendBoost)));
    }
    return data;
}

function updateDashboardData() {
    updateOverviewData();
    updateChartsData();
    updateRecentActivity();
}

function updateOverviewData() {
    const data = dashboardData.overview;
    
    document.getElementById('total-revenue').textContent = '$' + data.totalRevenue.toLocaleString();
    document.getElementById('active-players').textContent = data.activePlayers.toLocaleString();
    document.getElementById('ads-today').textContent = data.adsToday.toLocaleString();
    document.getElementById('conversion-rate').textContent = data.conversionRate + '%';
}

function updateChartsData() {
    // Update revenue chart
    if (charts.revenue) {
        charts.revenue.data.labels = dashboardData.charts.revenue.labels;
        charts.revenue.data.datasets[0].data = dashboardData.charts.revenue.data;
        charts.revenue.update();
    }
    
    // Update activity chart
    if (charts.activity) {
        charts.activity.data.labels = dashboardData.charts.activity.labels;
        charts.activity.data.datasets[0].data = dashboardData.charts.activity.data;
        charts.activity.update();
    }
}

function updateRecentActivity() {
    const activityList = document.getElementById('recent-activity');
    if (!activityList) return;
    
    activityList.innerHTML = '';
    
    dashboardData.recentActivity.forEach(activity => {
        const item = document.createElement('div');
        item.className = 'activity-item';
        item.innerHTML = `
            <div class="activity-text">${activity.text}</div>
            <div class="activity-time">${activity.time}</div>
        `;
        activityList.appendChild(item);
    });
}

function updateRevenueData() {
    const data = dashboardData.revenue;
    
    document.getElementById('subscription-revenue').textContent = '$' + data.subscription.toLocaleString();
    document.getElementById('iap-revenue').textContent = '$' + data.iap.toLocaleString();
    document.getElementById('ad-revenue').textContent = '$' + data.ads.toLocaleString();
    
    document.getElementById('weekly-revenue').textContent = '$' + data.weekly.toLocaleString();
    document.getElementById('monthly-revenue').textContent = '$' + data.monthly.toLocaleString();
    document.getElementById('legendary-revenue').textContent = '$' + data.legendary.toLocaleString();
    document.getElementById('starter-revenue').textContent = '$' + data.starter.toLocaleString();
    document.getElementById('rewarded-ad-revenue').textContent = '$' + data.rewardedAds.toLocaleString();
    document.getElementById('interstitial-revenue').textContent = '$' + data.interstitial.toLocaleString();
    
    // Update revenue source chart
    if (charts.revenueSource) {
        charts.revenueSource.data.datasets[0].data = [
            data.subscription,
            data.iap,
            data.ads
        ];
        charts.revenueSource.update();
    }
    
    // Update top spenders
    updateTopSpenders();
}

function updateTopSpenders() {
    const spendersList = document.getElementById('top-spenders-list');
    if (!spendersList) return;
    
    const topSpenders = [
        { name: 'DragonSlayer93', spent: '$89.95', vip: true },
        { name: 'MysticMage', spent: '$67.45', vip: true },
        { name: 'ShadowKnight', spent: '$54.90', vip: false },
        { name: 'IceQueen42', spent: '$43.25', vip: true },
        { name: 'FireWizard', spent: '$38.80', vip: false }
    ];
    
    spendersList.innerHTML = '';
    
    topSpenders.forEach((spender, index) => {
        const item = document.createElement('div');
        item.className = 'spender-item';
        item.innerHTML = `
            <div class="spender-rank">#${index + 1}</div>
            <div class="spender-name">${spender.name} ${spender.vip ? '👑' : ''}</div>
            <div class="spender-amount">${spender.spent}</div>
        `;
        spendersList.appendChild(item);
    });
}

function updateAdsData() {
    const data = dashboardData.ads;
    
    document.getElementById('daily-ad-views').textContent = data.dailyViews.toLocaleString();
    document.getElementById('ad-success-rate').textContent = data.successRate + '%';
    document.getElementById('ad-rpm').textContent = '$' + data.rpm.toFixed(2);
    document.getElementById('ad-fill-rate').textContent = data.fillRate + '%';
    
    // Update source performance table
    updateSourcePerformanceTable();
}

function updateSourcePerformanceTable() {
    const tableContainer = document.getElementById('source-performance-table');
    if (!tableContainer) return;
    
    let tableHTML = `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 2px solid var(--border-color);">
                    <th style="padding: 12px; text-align: left; color: var(--text-secondary);">Source</th>
                    <th style="padding: 12px; text-align: center; color: var(--text-secondary);">Attempts</th>
                    <th style="padding: 12px; text-align: center; color: var(--text-secondary);">Success Rate</th>
                    <th style="padding: 12px; text-align: center; color: var(--text-secondary);">Revenue</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    Object.entries(dashboardData.ads.sources).forEach(([source, data]) => {
        const successRate = ((data.successes / data.attempts) * 100).toFixed(1);
        tableHTML += `
            <tr style="border-bottom: 1px solid var(--border-color);">
                <td style="padding: 12px; color: var(--text-primary);">${source}</td>
                <td style="padding: 12px; text-align: center; color: var(--text-secondary);">${data.attempts.toLocaleString()}</td>
                <td style="padding: 12px; text-align: center; color: var(--success-green);">${successRate}%</td>
                <td style="padding: 12px; text-align: center; color: var(--primary-gold);">$${data.revenue.toLocaleString()}</td>
            </tr>
        `;
    });
    
    tableHTML += '</tbody></table>';
    tableContainer.innerHTML = tableHTML;
}

function updatePlayersData() {
    const data = dashboardData.players;
    
    document.getElementById('total-players').textContent = data.total.toLocaleString();
    document.getElementById('dau').textContent = data.dau.toLocaleString();
    document.getElementById('wau').textContent = data.wau.toLocaleString();
    document.getElementById('mau').textContent = data.mau.toLocaleString();
}

function updateSubscriptionsData() {
    const data = dashboardData.subscriptions;
    
    document.getElementById('weekly-subs').textContent = data.weekly.active.toLocaleString();
    document.getElementById('weekly-monthly-revenue').textContent = '$' + data.weekly.revenue.toLocaleString();
    document.getElementById('weekly-conversion').textContent = data.weekly.conversion + '%';
    
    document.getElementById('monthly-subs').textContent = data.monthly.active.toLocaleString();
    document.getElementById('monthly-monthly-revenue').textContent = '$' + data.monthly.revenue.toLocaleString();
    document.getElementById('monthly-conversion').textContent = data.monthly.conversion + '%';
    
    // Update expiring subscriptions
    updateExpiringSubscriptions();
}

function updateExpiringSubscriptions() {
    const expiringList = document.getElementById('expiring-subscriptions-list');
    if (!expiringList) return;
    
    expiringList.innerHTML = '';
    
    dashboardData.subscriptions.expiring.forEach(sub => {
        const item = document.createElement('div');
        item.className = 'expiring-item';
        item.innerHTML = `
            <div class="expiring-player">${sub.player}</div>
            <div class="expiring-type">${sub.type}</div>
            <div class="expiring-date">${sub.expires}</div>
        `;
        expiringList.appendChild(item);
    });
}

function startDataRefresh() {
    updateInterval = setInterval(() => {
        // Simulate real-time data updates
        simulateDataUpdates();
        updateLastUpdatedTime();
    }, CONFIG.updateInterval);
    
    console.log('🔄 Data refresh started');
}

function simulateDataUpdates() {
    // Simulate small changes in metrics
    dashboardData.overview.activePlayers += Math.floor((Math.random() - 0.5) * 10);
    dashboardData.overview.adsToday += Math.floor(Math.random() * 50);
    dashboardData.overview.totalRevenue += Math.random() * 100;
    
    // Update displays
    updateOverviewData();
}

function updateLastUpdatedTime() {
    const timeElement = document.getElementById('last-updated');
    if (timeElement) {
        timeElement.textContent = new Date().toLocaleString();
    }
}

// Dashboard control functions
function changeAdSource() {
    const select = document.getElementById('active-ad-source');
    const newSource = select.value;
    console.log(`📺 Ad source changed to: ${newSource}`);
    showAlert('success', `Ad source changed to ${newSource}`);
}

function refreshAds() {
    console.log('🔄 Refreshing ads...');
    showAlert('info', 'Ad refresh initiated');
}

function updateAdLimit() {
    const limit = document.getElementById('daily-ad-limit').value;
    console.log(`📺 Daily ad limit updated to: ${limit}`);
    showAlert('success', `Daily ad limit updated to ${limit}`);
}

function updateAdCooldown() {
    const cooldown = document.getElementById('ad-cooldown').value;
    console.log(`⏱️ Ad cooldown updated to: ${cooldown} seconds`);
    showAlert('success', `Ad cooldown updated to ${cooldown} seconds`);
}

function searchPlayer() {
    const query = document.getElementById('player-search-input').value;
    console.log(`🔍 Searching for player: ${query}`);
    
    const resultsContainer = document.getElementById('player-search-results');
    if (query.trim()) {
        resultsContainer.innerHTML = `
            <div class="search-result">
                <h4>Search Results for "${query}"</h4>
                <div class="player-result">
                    <div class="player-info">
                        <strong>Player ID:</strong> ${query}_12345<br>
                        <strong>Level:</strong> 45<br>
                        <strong>Total Spent:</strong> $23.50<br>
                        <strong>Last Active:</strong> 2 hours ago<br>
                        <strong>VIP Status:</strong> Weekly Pass
                    </div>
                </div>
            </div>
        `;
    } else {
        resultsContainer.innerHTML = '';
    }
}

function saveGameSettings() {
    console.log('💾 Saving game settings...');
    showAlert('success', 'Game settings saved successfully');
}

function savePricingSettings() {
    console.log('💾 Saving pricing settings...');
    showAlert('success', 'Pricing settings saved successfully');
}

function clearAdCache() {
    console.log('🗑️ Clearing ad cache...');
    showAlert('info', 'Ad cache cleared');
}

function resetDailyLimits() {
    console.log('🔄 Resetting daily limits...');
    showAlert('info', 'Daily limits reset');
}

function exportAnalytics() {
    console.log('📊 Exporting analytics...');
    showAlert('success', 'Analytics exported successfully');
}

function emergencyStop() {
    if (confirm('Are you sure you want to initiate emergency stop? This will temporarily disable all ads and purchases.')) {
        console.log('🚨 Emergency stop initiated');
        showAlert('warning', 'Emergency stop activated');
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('koa_admin_session');
        if (updateInterval) {
            clearInterval(updateInterval);
        }
        location.reload();
    }
}

// Utility functions
function generateSessionId() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

function showAlert(type, message) {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    switch(type) {
        case 'success':
            alert.style.background = '#10B981';
            break;
        case 'error':
            alert.style.background = '#EF4444';
            break;
        case 'warning':
            alert.style.background = '#F59E0B';
            break;
        case 'info':
            alert.style.background = '#3B82F6';
            break;
    }
    
    alert.textContent = message;
    document.body.appendChild(alert);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(alert);
        }, 300);
    }, 3000);
}

// Setup real-time updates simulation
function setupRealTimeUpdates() {
    // Simulate new activity every 30 seconds
    setInterval(() => {
        const activities = [
            'New player registered: GameMaster' + Math.floor(Math.random() * 1000),
            'Legendary skin purchased: Dragon Emperor ($19.99)',
            'Weekly Pass renewed: Knight' + Math.floor(Math.random() * 100),
            'Ad milestone reached: 10,000 views today',
            'Monthly VIP subscription started: Wizard' + Math.floor(Math.random() * 100)
        ];
        
        const newActivity = {
            text: activities[Math.floor(Math.random() * activities.length)],
            time: 'Just now'
        };
        
        dashboardData.recentActivity.unshift(newActivity);
        dashboardData.recentActivity = dashboardData.recentActivity.slice(0, 5);
        
        updateRecentActivity();
    }, 30000);
}

function loadSettings() {
    // Load current settings into form fields
    console.log('⚙️ Loading settings...');
}

// CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    .spender-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid var(--primary-gold);
    }
    .expiring-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid var(--warning-orange);
    }
    .search-result {
        background: var(--bg-card);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-top: 16px;
    }
    .player-result {
        margin-top: 12px;
        padding: 12px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
    }
`;
document.head.appendChild(style);

console.log('🎮 Kingdom of Aldoria Admin Dashboard loaded successfully!');