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
        case 'codes':
            updateCodesData();
            break;
        case 'sync':
            updateSyncData();
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

// Promo Codes Management
function updateCodesData() {
    // Simulate code data
    const codesData = {
        totalCodes: 15,
        activeCodes: 12,
        totalRedemptions: 1847,
        totalGemsDistributed: 125340,
        codes: [
            {
                code: 'WELCOME2024',
                name: 'Welcome to Kingdom of Aldoria',
                type: 'welcome',
                rewardGems: 100,
                rewardGold: 1000,
                currentUsage: 456,
                usageLimit: 1000,
                status: 'active',
                expiresFormatted: '2024-12-31'
            },
            {
                code: 'LAUNCH50',
                name: 'Game Launch Celebration',
                type: 'event',
                rewardGems: 500,
                rewardGold: 5000,
                currentUsage: 234,
                usageLimit: 500,
                status: 'active',
                expiresFormatted: '2024-02-15'
            },
            {
                code: 'SEIFVIP',
                name: 'Creator Special',
                type: 'vip',
                rewardGems: 2500,
                rewardGold: 25000,
                currentUsage: 67,
                usageLimit: 100,
                status: 'active',
                expiresFormatted: '2024-04-10'
            }
        ]
    };
    
    // Update statistics
    document.getElementById('total-codes').textContent = codesData.totalCodes;
    document.getElementById('active-codes').textContent = codesData.activeCodes;
    document.getElementById('total-redemptions').textContent = codesData.totalRedemptions.toLocaleString();
    document.getElementById('total-gems-distributed').textContent = codesData.totalGemsDistributed.toLocaleString();
    
    // Update codes table
    updateCodesTable(codesData.codes);
}

function updateCodesTable(codes) {
    const tableBody = document.getElementById('codes-table-body');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    codes.forEach(code => {
        const row = document.createElement('tr');
        
        const statusColor = code.status === 'active' ? 'var(--success-green)' : 
                           code.status === 'expired' ? 'var(--error-red)' : 'var(--warning-orange)';
        
        row.innerHTML = `
            <td><strong>${code.code}</strong></td>
            <td>${code.name}</td>
            <td><span class="code-type ${code.type}">${code.type}</span></td>
            <td>💎 ${code.rewardGems} | 🪙 ${code.rewardGold}</td>
            <td>${code.currentUsage}/${code.usageLimit}</td>
            <td><span style="color: ${statusColor}">${code.status}</span></td>
            <td>${code.expiresFormatted}</td>
            <td>
                <button class="action-btn edit" onclick="editCode('${code.code}')">Edit</button>
                <button class="action-btn delete" onclick="deleteCode('${code.code}')">Delete</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

function showCreateCodeModal() {
    document.getElementById('code-modal').style.display = 'flex';
    
    // Setup form submission
    const form = document.getElementById('create-code-form');
    form.onsubmit = function(e) {
        e.preventDefault();
        createNewCode();
    };
}

function closeCodeModal() {
    document.getElementById('code-modal').style.display = 'none';
    document.getElementById('create-code-form').reset();
}

function createNewCode() {
    const formData = {
        code: document.getElementById('code-name').value.toUpperCase(),
        displayName: document.getElementById('code-display-name').value,
        description: document.getElementById('code-description').value,
        type: document.getElementById('code-type').value,
        rewardGems: parseInt(document.getElementById('reward-gems').value),
        rewardGold: parseInt(document.getElementById('reward-gold').value),
        usageLimit: parseInt(document.getElementById('usage-limit').value),
        durationDays: parseInt(document.getElementById('duration-days').value)
    };
    
    // Validate code format
    if (!/^[A-Z0-9_-]{3,20}$/.test(formData.code)) {
        showAlert('error', 'Code must be 3-20 characters, uppercase letters and numbers only');
        return;
    }
    
    console.log('🎫 Creating code:', formData);
    
    // Simulate API call
    setTimeout(() => {
        showAlert('success', `Code ${formData.code} created successfully!`);
        closeCodeModal();
        updateCodesData(); // Refresh the table
    }, 1000);
}

function editCode(code) {
    console.log('✏️ Editing code:', code);
    showAlert('info', `Editing code ${code} (feature coming soon)`);
}

function deleteCode(code) {
    if (confirm(`Are you sure you want to delete code ${code}? This action cannot be undone.`)) {
        console.log('🗑️ Deleting code:', code);
        showAlert('success', `Code ${code} deleted successfully!`);
        updateCodesData(); // Refresh the table
    }
}

// Data Sync Management
function updateSyncData() {
    // Simulate sync data
    const syncData = {
        onlinePlayers: 423,
        offlinePlayers: 1654,
        pendingSyncs: 12,
        firebaseStatus: 'connected',
        recentSyncs: [
            { player: 'DragonSlayer93', type: 'Player Data', status: 'success', time: '2 minutes ago' },
            { player: 'MysticMage', type: 'Inventory', status: 'success', time: '3 minutes ago' },
            { player: 'ShadowKnight', type: 'Stage Progress', status: 'conflict', time: '5 minutes ago' },
            { player: 'IceQueen42', type: 'Player Data', status: 'success', time: '7 minutes ago' },
            { player: 'FireWizard', type: 'Currency', status: 'failed', time: '10 minutes ago' }
        ]
    };
    
    // Update status cards
    document.getElementById('online-players').textContent = syncData.onlinePlayers.toLocaleString();
    document.getElementById('offline-players').textContent = syncData.offlinePlayers.toLocaleString();
    document.getElementById('pending-syncs').textContent = syncData.pendingSyncs;
    
    const firebaseStatusEl = document.getElementById('firebase-status');
    firebaseStatusEl.textContent = '●';
    firebaseStatusEl.style.color = syncData.firebaseStatus === 'connected' ? 'var(--success-green)' : 'var(--error-red)';
    
    // Update recent syncs
    updateRecentSyncs(syncData.recentSyncs);
    
    // Initialize sync charts
    initializeSyncCharts();
}

function updateRecentSyncs(syncs) {
    const syncsList = document.getElementById('sync-events-list');
    if (!syncsList) return;
    
    syncsList.innerHTML = '';
    
    syncs.forEach(sync => {
        const syncItem = document.createElement('div');
        syncItem.className = 'sync-event-item';
        
        const statusColor = sync.status === 'success' ? 'var(--success-green)' :
                           sync.status === 'conflict' ? 'var(--warning-orange)' : 'var(--error-red)';
        
        syncItem.innerHTML = `
            <div class="sync-event-player">${sync.player}</div>
            <div class="sync-event-type">${sync.type}</div>
            <div class="sync-event-status" style="color: ${statusColor}">${sync.status}</div>
            <div class="sync-event-time">${sync.time}</div>
        `;
        
        syncsList.appendChild(syncItem);
    });
}

function initializeSyncCharts() {
    // Sync Activity Chart
    const syncCtx = document.getElementById('sync-activity-chart');
    if (syncCtx && !charts.syncActivity) {
        charts.syncActivity = new Chart(syncCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: generateHourLabels(24),
                datasets: [{
                    label: 'Sync Events',
                    data: generateSyncActivityData(24),
                    borderColor: CONFIG.charts.colors.blue,
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
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
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Data Distribution Chart
    const dataCtx = document.getElementById('data-distribution-chart');
    if (dataCtx && !charts.dataDistribution) {
        charts.dataDistribution = new Chart(dataCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['SQLite (Offline)', 'Firebase (Online)', 'Pending Sync'],
                datasets: [{
                    data: [65, 30, 5],
                    backgroundColor: [
                        CONFIG.charts.colors.green,
                        CONFIG.charts.colors.blue,
                        CONFIG.charts.colors.orange
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
}

function generateHourLabels(hours) {
    const labels = [];
    for (let i = hours - 1; i >= 0; i--) {
        const date = new Date();
        date.setHours(date.getHours() - i);
        labels.push(date.getHours() + ':00');
    }
    return labels;
}

function generateSyncActivityData(hours) {
    const data = [];
    for (let i = 0; i < hours; i++) {
        data.push(Math.floor(Math.random() * 50) + 10);
    }
    return data;
}

function forceSyncAll() {
    console.log('🔄 Forcing sync for all players...');
    showAlert('info', 'Initiating sync for all players...');
    
    // Simulate sync process
    setTimeout(() => {
        showAlert('success', 'All players synced successfully!');
        updateSyncData();
    }, 2000);
}

function clearSyncCache() {
    console.log('🗑️ Clearing sync cache...');
    showAlert('info', 'Sync cache cleared');
}

function resetConflictData() {
    if (confirm('This will reset all conflict resolution data. Continue?')) {
        console.log('🔄 Resetting conflict data...');
        showAlert('success', 'Conflict data reset successfully');
        updateSyncData();
    }
}

function emergencyOfflineMode() {
    if (confirm('This will force all players into offline mode. Are you sure?')) {
        console.log('🚨 Emergency offline mode activated');
        showAlert('warning', 'Emergency offline mode activated');
    }
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

// Add these functions at the end of the file

// Events Management Functions
function showCreateEventModal() {
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>🎉 Create New Event</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                
                <form id="create-event-form" onsubmit="createEvent(event)">
                    <div class="form-group">
                        <label for="event-name">Event Name</label>
                        <input type="text" id="event-name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="event-type">Event Type</label>
                        <select id="event-type" name="type" required>
                            <option value="daily_login">Daily Login Bonus</option>
                            <option value="weekly_quest">Weekly Quest</option>
                            <option value="special_event">Special Event</option>
                            <option value="seasonal">Seasonal Event</option>
                            <option value="competition">Competition</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="event-description">Description</label>
                        <textarea id="event-description" name="description" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="event-start">Start Date & Time</label>
                        <input type="datetime-local" id="event-start" name="startDate" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="event-end">End Date & Time</label>
                        <input type="datetime-local" id="event-end" name="endDate" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="event-rewards">Rewards (JSON format)</label>
                        <textarea id="event-rewards" name="rewards" rows="4" 
                                  placeholder='{"gems": 100, "weapons": ["silver_sword"], "experience": 500}'></textarea>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="form-btn secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="form-btn primary">Create Event</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function createEvent(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const eventData = Object.fromEntries(formData.entries());
    
    try {
        eventData.rewards = JSON.parse(eventData.rewards || '{}');
    } catch (e) {
        showNotification('❌ Invalid rewards JSON format', 'error');
        return;
    }
    
    // Simulate API call
    console.log('Creating event:', eventData);
    showNotification('✅ Event created successfully!', 'success');
    closeModal();
    refreshEvents();
}

function createEventFromTemplate(templateType) {
    const templates = {
        double_xp: {
            name: 'Double XP Weekend',
            type: 'special_event',
            description: 'Get 2x experience points from all battles during this weekend!',
            rewards: { experience_multiplier: 2 }
        },
        gem_rain: {
            name: 'Gem Rain Event',
            type: 'special_event',
            description: 'Earn extra gems from all sources for a limited time!',
            rewards: { gems_multiplier: 1.5, bonus_gems: 50 }
        },
        boss_rush: {
            name: 'Boss Rush Challenge',
            type: 'competition',
            description: 'Face powerful bosses in succession for legendary rewards!',
            rewards: { legendary_weapon: 'random', gems: 500, rare_materials: 10 }
        },
        login_bonus: {
            name: '7-Day Login Bonus',
            type: 'daily_login',
            description: 'Login daily for 7 days to receive progressive rewards!',
            rewards: { 
                day1: { gems: 50 },
                day2: { gems: 75 },
                day3: { gems: 100, weapons: ['silver_sword'] },
                day7: { gems: 500, legendary_weapon: 'random' }
            }
        }
    };
    
    const template = templates[templateType];
    if (template) {
        // Auto-fill form with template data
        showCreateEventModal();
        setTimeout(() => {
            document.getElementById('event-name').value = template.name;
            document.getElementById('event-type').value = template.type;
            document.getElementById('event-description').value = template.description;
            document.getElementById('event-rewards').value = JSON.stringify(template.rewards, null, 2);
        }, 100);
    }
}

function refreshEvents() {
    loadEventsData();
    showNotification('🔄 Events data refreshed', 'info');
}

function filterEvents() {
    const filter = document.getElementById('event-filter').value;
    console.log('Filtering events by:', filter);
    // Implement filtering logic
}

function filterEventsByType() {
    const filter = document.getElementById('event-type-filter').value;
    console.log('Filtering events by type:', filter);
    // Implement filtering logic
}

// Weapons Management Functions
function showCreateWeaponModal() {
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>⚔️ Add New Weapon</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                
                <form id="create-weapon-form" onsubmit="createWeapon(event)">
                    <div class="form-group">
                        <label for="weapon-name">Weapon Name</label>
                        <input type="text" id="weapon-name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-type">Weapon Type</label>
                        <select id="weapon-type" name="type" required>
                            <option value="sword">Sword</option>
                            <option value="bow">Bow</option>
                            <option value="staff">Staff</option>
                            <option value="dagger">Dagger</option>
                            <option value="hammer">Hammer</option>
                            <option value="scythe">Scythe</option>
                            <option value="orb">Orb</option>
                            <option value="gauntlets">Gauntlets</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-rarity">Rarity</label>
                        <select id="weapon-rarity" name="rarity" required>
                            <option value="wood">Wood</option>
                            <option value="iron">Iron</option>
                            <option value="silver">Silver</option>
                            <option value="gold">Gold</option>
                            <option value="platinum">Platinum</option>
                            <option value="emerald">Emerald</option>
                            <option value="diamond">Diamond</option>
                            <option value="elite">Elite</option>
                            <option value="hyper">Hyper</option>
                            <option value="legendary">Legendary</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-attack">Attack Power</label>
                        <input type="number" id="weapon-attack" name="attack" min="1" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-price">Price (Gems/USD)</label>
                        <input type="number" id="weapon-price" name="price" min="0" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-description">Description</label>
                        <textarea id="weapon-description" name="description" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="weapon-special">Special Abilities (JSON)</label>
                        <textarea id="weapon-special" name="special" rows="3" 
                                  placeholder='{"crit_chance": 0.25, "fire_damage": 50}'></textarea>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="form-btn secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="form-btn primary">Add Weapon</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function createWeapon(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const weaponData = Object.fromEntries(formData.entries());
    
    try {
        weaponData.special = JSON.parse(weaponData.special || '{}');
    } catch (e) {
        showNotification('❌ Invalid special abilities JSON format', 'error');
        return;
    }
    
    // Simulate API call
    console.log('Creating weapon:', weaponData);
    showNotification('✅ Weapon added successfully!', 'success');
    closeModal();
    loadWeaponsData();
}

function searchWeapons() {
    const query = document.getElementById('weapon-search').value;
    console.log('Searching weapons:', query);
    // Implement search logic
}

function filterWeaponsByRarity() {
    const rarity = document.getElementById('weapon-rarity-filter').value;
    console.log('Filtering weapons by rarity:', rarity);
    // Implement filtering logic
}

function filterWeaponsByType() {
    const type = document.getElementById('weapon-type-filter').value;
    console.log('Filtering weapons by type:', type);
    // Implement filtering logic
}

function exportWeapons() {
    // Simulate data export
    const weaponsData = generateSampleWeaponsData();
    downloadJSON(weaponsData, 'weapons_export.json');
    showNotification('📊 Weapons data exported successfully!', 'success');
}

// Heroes Management Functions
function showCreateHeroModal() {
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>🦸 Add New Hero</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                
                <form id="create-hero-form" onsubmit="createHero(event)">
                    <div class="form-group">
                        <label for="hero-name">Hero Name</label>
                        <input type="text" id="hero-name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-class">Hero Class</label>
                        <select id="hero-class" name="class" required>
                            <option value="knight">Knight</option>
                            <option value="mage">Mage</option>
                            <option value="archer">Archer</option>
                            <option value="assassin">Assassin</option>
                            <option value="berserker">Berserker</option>
                            <option value="paladin">Paladin</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-rarity">Rarity</label>
                        <select id="hero-rarity" name="rarity" required>
                            <option value="common">Common</option>
                            <option value="rare">Rare</option>
                            <option value="epic">Epic</option>
                            <option value="legendary">Legendary</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-health">Health Points</label>
                        <input type="number" id="hero-health" name="health" min="100" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-attack">Attack Power</label>
                        <input type="number" id="hero-attack" name="attack" min="10" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-price">Price (Gems/USD)</label>
                        <input type="number" id="hero-price" name="price" min="0" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-description">Description</label>
                        <textarea id="hero-description" name="description" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="hero-abilities">Abilities (comma-separated)</label>
                        <input type="text" id="hero-abilities" name="abilities" 
                               placeholder="Fireball, Heal, Shield Block">
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="form-btn secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="form-btn primary">Add Hero</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function createHero(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const heroData = Object.fromEntries(formData.entries());
    
    // Process abilities
    heroData.abilities = heroData.abilities.split(',').map(a => a.trim()).filter(a => a);
    
    // Simulate API call
    console.log('Creating hero:', heroData);
    showNotification('✅ Hero added successfully!', 'success');
    closeModal();
    loadHeroesData();
}

function searchHeroes() {
    const query = document.getElementById('hero-search').value;
    console.log('Searching heroes:', query);
    // Implement search logic
}

function filterHeroesByClass() {
    const heroClass = document.getElementById('hero-class-filter').value;
    console.log('Filtering heroes by class:', heroClass);
    // Implement filtering logic
}

function filterHeroesByRarity() {
    const rarity = document.getElementById('hero-rarity-filter').value;
    console.log('Filtering heroes by rarity:', rarity);
    // Implement filtering logic
}

function exportHeroes() {
    // Simulate data export
    const heroesData = generateSampleHeroesData();
    downloadJSON(heroesData, 'heroes_export.json');
    showNotification('📊 Heroes data exported successfully!', 'success');
}

// Enhanced VIP Management Functions
function searchVIPs() {
    const query = document.getElementById('vip-search').value;
    console.log('Searching VIPs:', query);
    // Implement search logic
}

function filterVIPs() {
    const filter = document.getElementById('vip-filter').value;
    console.log('Filtering VIPs:', filter);
    // Implement filtering logic
}

function exportSubscriptions() {
    // Simulate data export
    const vipData = generateSampleVIPData();
    downloadJSON(vipData, 'vip_subscriptions_export.json');
    showNotification('📊 VIP data exported successfully!', 'success');
}

function refreshSubscriptions() {
    loadVIPData();
    showNotification('🔄 VIP data refreshed', 'info');
}

function extendVIP(userId) {
    console.log('Extending VIP for user:', userId);
    showNotification(`✅ VIP extended for user ${userId}`, 'success');
    // Implement VIP extension logic
}

function removeVIP(userId) {
    if (confirm('Are you sure you want to remove VIP status for this user?')) {
        console.log('Removing VIP for user:', userId);
        showNotification(`❌ VIP removed for user ${userId}`, 'success');
        // Implement VIP removal logic
    }
}

// Utility Functions
function closeModal(event) {
    if (event && event.target !== event.currentTarget) return;
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
    }
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Data Loading Functions
function loadEventsData() {
    // Simulate loading events data
    const eventsContainer = document.getElementById('events-container');
    if (eventsContainer) {
        eventsContainer.innerHTML = generateSampleEventsHTML();
    }
    
    // Update stats
    updateElementById('active-events', '3');
    updateElementById('scheduled-events', '5');
    updateElementById('event-participation', '78%');
}

function loadWeaponsData() {
    // Simulate loading weapons data
    const weaponsGrid = document.getElementById('weapons-grid');
    if (weaponsGrid) {
        weaponsGrid.innerHTML = generateSampleWeaponsHTML();
    }
    
    // Update stats
    updateElementById('total-weapons', '45');
    updateElementById('legendary-weapons', '8');
    updateElementById('popular-weapon', 'Godslayer Excalibur');
}

function loadHeroesData() {
    // Simulate loading heroes data
    const heroesGrid = document.getElementById('heroes-grid');
    if (heroesGrid) {
        heroesGrid.innerHTML = generateSampleHeroesHTML();
    }
    
    // Update stats
    updateElementById('total-heroes', '12');
    updateElementById('premium-heroes', '4');
    updateElementById('popular-hero', 'Dragon Lord Arin');
}

function loadVIPData() {
    // Simulate loading VIP data
    const vipList = document.getElementById('vip-list');
    if (vipList) {
        vipList.innerHTML = generateSampleVIPHTML();
    }
    
    // Update stats
    updateElementById('active-vips', '156');
    updateElementById('vip-revenue', '$2,480');
    updateElementById('retention-rate', '87%');
}

// Sample Data Generators
function generateSampleEventsHTML() {
    return `
        <div class="event-card">
            <div class="event-header">
                <h4>⚡ Double XP Weekend</h4>
                <div class="event-status active">Active</div>
            </div>
            <p>Get 2x experience from all battles this weekend!</p>
            <div class="event-details">
                <small>Ends: Tomorrow 23:59 | Participants: 1,247</small>
            </div>
        </div>
        
        <div class="event-card">
            <div class="event-header">
                <h4>💎 Gem Rain Event</h4>
                <div class="event-status scheduled">Scheduled</div>
            </div>
            <p>Extra gems from all sources for 3 days!</p>
            <div class="event-details">
                <small>Starts: Monday 00:00 | Expected: 2,000+ players</small>
            </div>
        </div>
    `;
}

function generateSampleWeaponsHTML() {
    return `
        <div class="weapon-card">
            <div class="weapon-rarity legendary">LEGENDARY</div>
            <div class="weapon-image">⚔️</div>
            <h4>Godslayer Excalibur</h4>
            <div class="weapon-stats">
                <div class="weapon-stat">Attack: 150</div>
                <div class="weapon-stat">Crit: 35%</div>
            </div>
            <div class="weapon-actions">
                <button class="weapon-action-btn edit">Edit</button>
                <button class="weapon-action-btn delete">Delete</button>
            </div>
        </div>
        
        <div class="weapon-card">
            <div class="weapon-rarity legendary">LEGENDARY</div>
            <div class="weapon-image">🏹</div>
            <h4>Worldender Bow</h4>
            <div class="weapon-stats">
                <div class="weapon-stat">Attack: 140</div>
                <div class="weapon-stat">Range: 50%</div>
            </div>
            <div class="weapon-actions">
                <button class="weapon-action-btn edit">Edit</button>
                <button class="weapon-action-btn delete">Delete</button>
            </div>
        </div>
    `;
}

function generateSampleHeroesHTML() {
    return `
        <div class="hero-card">
            <div class="hero-class">Knight</div>
            <div class="hero-avatar">🦸</div>
            <h4>Dragon Lord Arin</h4>
            <div class="hero-abilities">
                <h5>Abilities:</h5>
                <div class="ability-list">
                    <span class="ability-tag">Dragon Breath</span>
                    <span class="ability-tag">Fire Shield</span>
                </div>
            </div>
            <div class="hero-pricing">
                <span class="hero-price">$24.99</span>
            </div>
            <div class="hero-actions">
                <button class="hero-action-btn edit">Edit</button>
                <button class="hero-action-btn delete">Delete</button>
            </div>
        </div>
        
        <div class="hero-card">
            <div class="hero-class">Mage</div>
            <div class="hero-avatar">🧙</div>
            <h4>Cosmic Emperor Arin</h4>
            <div class="hero-abilities">
                <h5>Abilities:</h5>
                <div class="ability-list">
                    <span class="ability-tag">Stellar Nova</span>
                    <span class="ability-tag">Gravity Control</span>
                </div>
            </div>
            <div class="hero-pricing">
                <span class="hero-price">$26.99</span>
            </div>
            <div class="hero-actions">
                <button class="hero-action-btn edit">Edit</button>
                <button class="hero-action-btn delete">Delete</button>
            </div>
        </div>
    `;
}

function generateSampleVIPHTML() {
    return `
        <div class="vip-item">
            <div class="vip-info">
                <div class="vip-name">Player_123</div>
                <div class="vip-details">Royal Crown • Expires: Dec 25, 2024 • $15.99/month</div>
            </div>
            <div class="vip-status active">Active</div>
            <div class="vip-actions">
                <button class="vip-action-btn extend" onclick="extendVIP('player_123')">Extend</button>
                <button class="vip-action-btn remove" onclick="removeVIP('player_123')">Remove</button>
            </div>
        </div>
        
        <div class="vip-item">
            <div class="vip-info">
                <div class="vip-name">DragonSlayer99</div>
                <div class="vip-details">Knight's Weekly • Expires: Dec 15, 2024 • $4.99/week</div>
            </div>
            <div class="vip-status expiring">Expiring Soon</div>
            <div class="vip-actions">
                <button class="vip-action-btn extend" onclick="extendVIP('dragonslayer99')">Extend</button>
                <button class="vip-action-btn remove" onclick="removeVIP('dragonslayer99')">Remove</button>
            </div>
        </div>
    `;
}

// Data generation functions for export
function generateSampleWeaponsData() {
    return [
        {
            id: 1,
            name: "Godslayer Excalibur",
            type: "sword",
            rarity: "legendary",
            attack: 150,
            price: 29.99,
            special_abilities: { crit_chance: 0.35, fire_damage: 75 }
        },
        {
            id: 2,
            name: "Worldender Bow",
            type: "bow",
            rarity: "legendary",
            attack: 140,
            price: 27.99,
            special_abilities: { void_damage: 80, piercing: true }
        }
    ];
}

function generateSampleHeroesData() {
    return [
        {
            id: 1,
            name: "Dragon Lord Arin",
            class: "knight",
            rarity: "legendary",
            health: 500,
            attack: 120,
            price: 24.99,
            abilities: ["Dragon Breath", "Fire Shield", "Dragon Wings"]
        },
        {
            id: 2,
            name: "Cosmic Emperor Arin",
            class: "mage",
            rarity: "legendary",
            health: 400,
            attack: 150,
            price: 26.99,
            abilities: ["Stellar Nova", "Gravity Control", "Cosmic Speed"]
        }
    ];
}

function generateSampleVIPData() {
    return [
        {
            user_id: "player_123",
            username: "Player_123",
            subscription_type: "monthly",
            start_date: "2024-11-01",
            end_date: "2024-12-25",
            price: 15.99,
            status: "active"
        },
        {
            user_id: "dragonslayer99",
            username: "DragonSlayer99",
            subscription_type: "weekly",
            start_date: "2024-12-08",
            end_date: "2024-12-15",
            price: 4.99,
            status: "expiring"
        }
    ];
}

// Initialize new tabs when switching
const originalSwitchTab = window.switchTab;
window.switchTab = function(tabName) {
    originalSwitchTab(tabName);
    
    // Load data for new tabs
    switch(tabName) {
        case 'events':
            loadEventsData();
            break;
        case 'weapons':
            loadWeaponsData();
            break;
        case 'heroes':
            loadHeroesData();
            break;
        case 'subscriptions':
            loadVIPData();
            break;
        case 'pixellab':
            loadPixelLabData();
            break;
    }
};

// PixelLab.ai API Configuration
const PIXELLAB_API_BASE = 'http://localhost:5001/api/pixellab';

// PixelLab.ai Functions
async function loadPixelLabData() {
    try {
        // Check PixelLab.ai status
        await checkPixelLabStatus();
        
        // Load generated assets
        await refreshAssetGallery();
        
        // Update stats
        await updatePixelLabStats();
        
    } catch (error) {
        console.error('Failed to load PixelLab data:', error);
        showNotification('❌ Failed to load PixelLab.ai data', 'error');
    }
}

async function checkPixelLabStatus() {
    try {
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        
        // Set checking state
        statusIndicator.className = 'status-indicator checking';
        statusText.textContent = 'Checking connection...';
        
        const response = await fetch(`${PIXELLAB_API_BASE}/status`);
        const data = await response.json();
        
        if (response.ok && data.status === 'online') {
            statusIndicator.className = 'status-indicator online';
            statusText.textContent = `PixelLab.ai Online - ${data.version}`;
            showNotification('✅ PixelLab.ai connection established', 'success');
        } else {
            throw new Error(data.message || 'Service unavailable');
        }
        
    } catch (error) {
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        
        statusIndicator.className = 'status-indicator offline';
        statusText.textContent = `Offline - ${error.message}`;
        showNotification('❌ PixelLab.ai connection failed', 'error');
    }
}

async function generateFromTemplate(category, index) {
    try {
        showGenerationProgress(`Generating ${category} template...`);
        
        const response = await fetch(`${PIXELLAB_API_BASE}/generate/template`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template_category: category,
                template_index: index
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification(`✅ Generated ${data.template_used} successfully!`, 'success');
            await refreshAssetGallery();
            await updatePixelLabStats();
        } else {
            throw new Error(data.error || 'Generation failed');
        }
        
    } catch (error) {
        console.error('Template generation failed:', error);
        showNotification(`❌ Template generation failed: ${error.message}`, 'error');
    } finally {
        hideGenerationProgress();
    }
}

async function generateCustomAsset() {
    try {
        const assetType = document.getElementById('asset-type-select').value;
        const rarity = document.getElementById('rarity-select').value;
        const style = document.getElementById('style-select').value;
        const name = document.getElementById('asset-name').value;
        const description = document.getElementById('asset-description').value;
        const width = parseInt(document.getElementById('asset-width').value);
        const height = parseInt(document.getElementById('asset-height').value);
        
        if (!name || !description) {
            showNotification('❌ Please fill in asset name and description', 'error');
            return;
        }
        
        showGenerationProgress(`Generating ${name}...`);
        
        const response = await fetch(`${PIXELLAB_API_BASE}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                asset_type: assetType,
                name: name,
                description: description,
                rarity: rarity,
                style: style,
                width: width,
                height: height
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification(`✅ Generated ${name} successfully!`, 'success');
            await refreshAssetGallery();
            await updatePixelLabStats();
            
            // Clear form
            clearGenerationForm();
        } else {
            throw new Error(data.error || 'Generation failed');
        }
        
    } catch (error) {
        console.error('Asset generation failed:', error);
        showNotification(`❌ Asset generation failed: ${error.message}`, 'error');
    } finally {
        hideGenerationProgress();
    }
}

async function generateAssetSet() {
    try {
        const assetType = document.getElementById('asset-type-select').value;
        const name = document.getElementById('asset-name').value;
        const rarity = document.getElementById('rarity-select').value;
        
        if (!name) {
            showNotification('❌ Please fill in asset name', 'error');
            return;
        }
        
        showGenerationProgress(`Generating ${name} asset set...`);
        
        let endpoint = '';
        let payload = {};
        
        switch (assetType) {
            case 'weapon':
                endpoint = 'weapon-set';
                payload = { weapon_name: name, rarity: rarity };
                break;
            case 'hero':
                endpoint = 'hero-set';
                payload = { 
                    hero_name: name, 
                    transformations: ['base', 'dragon_lord', 'cosmic_emperor', 'void_knight']
                };
                break;
            case 'map':
                endpoint = 'map-set';
                payload = { 
                    map_name: name, 
                    areas: ['main', 'entrance', 'depths', 'boss_area']
                };
                break;
            default:
                throw new Error('Asset sets not supported for this type');
        }
        
        const response = await fetch(`${PIXELLAB_API_BASE}/generate/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            const setData = data.weapon_set || data.hero_set || data.map_set;
            showNotification(`✅ Generated ${setData.assets.length} assets for ${name}!`, 'success');
            await refreshAssetGallery();
            await updatePixelLabStats();
        } else {
            throw new Error(data.error || 'Set generation failed');
        }
        
    } catch (error) {
        console.error('Asset set generation failed:', error);
        showNotification(`❌ Asset set generation failed: ${error.message}`, 'error');
    } finally {
        hideGenerationProgress();
    }
}

async function refreshAssetGallery() {
    try {
        const gallery = document.getElementById('assets-gallery');
        const filter = document.getElementById('gallery-filter').value;
        
        const url = filter === 'all' ? 
            `${PIXELLAB_API_BASE}/assets` : 
            `${PIXELLAB_API_BASE}/assets?type=${filter}`;
            
        const response = await fetch(url);
        const data = await response.json();
        
        if (response.ok && data.success) {
            renderAssetGallery(data.assets);
        } else {
            throw new Error(data.error || 'Failed to load assets');
        }
        
    } catch (error) {
        console.error('Failed to refresh asset gallery:', error);
        const gallery = document.getElementById('assets-gallery');
        gallery.innerHTML = '<p>Failed to load assets</p>';
    }
}

function renderAssetGallery(assets) {
    const gallery = document.getElementById('assets-gallery');
    
    if (assets.length === 0) {
        gallery.innerHTML = `
            <div class="no-assets">
                <p>No assets generated yet</p>
                <p>Use the templates or custom generation to create your first asset!</p>
            </div>
        `;
        return;
    }
    
    gallery.innerHTML = assets.map(asset => `
        <div class="asset-item">
            <div class="asset-type-badge ${asset.type}">${asset.type.toUpperCase()}</div>
            <div class="asset-preview">
                <img src="${asset.url}" alt="${asset.name}" onerror="this.style.display='none'">
                <div class="asset-placeholder" style="display: none;">
                    <span class="asset-icon">${getAssetTypeIcon(asset.type)}</span>
                </div>
            </div>
            <div class="asset-info">
                <h5>${asset.name}</h5>
                <p>Created: ${new Date(asset.created_at).toLocaleDateString()}</p>
                <p>Type: ${asset.type} | Status: ${asset.status}</p>
            </div>
            <div class="asset-actions">
                <button class="asset-action-btn download" onclick="downloadAsset('${asset.id}')">
                    📥 Download
                </button>
                <button class="asset-action-btn view" onclick="viewAsset('${asset.id}')">
                    👁️ View
                </button>
            </div>
        </div>
    `).join('');
}

function getAssetTypeIcon(type) {
    const icons = {
        weapon: '⚔️',
        hero: '🦸',
        map: '🗺️',
        gem: '💎',
        icon: '🎯',
        skin: '🎭',
        boss: '🐉'
    };
    return icons[type] || '🎨';
}

async function downloadAsset(assetId) {
    try {
        const response = await fetch(`${PIXELLAB_API_BASE}/assets/${assetId}/download`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = assetId;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showNotification('📥 Asset downloaded successfully!', 'success');
        } else {
            throw new Error('Download failed');
        }
        
    } catch (error) {
        showNotification('❌ Failed to download asset', 'error');
    }
}

async function viewAsset(assetId) {
    try {
        const response = await fetch(`${PIXELLAB_API_BASE}/assets/${assetId}`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show asset details in modal
            showAssetDetailsModal(data.asset);
        } else {
            throw new Error(data.error || 'Failed to load asset details');
        }
        
    } catch (error) {
        showNotification('❌ Failed to view asset details', 'error');
    }
}

function showAssetDetailsModal(asset) {
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content asset-details-modal" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>🎨 Asset Details</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                
                <div class="asset-details">
                    <div class="asset-preview-large">
                        <img src="${asset.path}" alt="Asset Preview">
                    </div>
                    
                    <div class="asset-metadata">
                        <div class="metadata-item">
                            <label>Asset ID:</label>
                            <span>${asset.id}</span>
                        </div>
                        <div class="metadata-item">
                            <label>File Size:</label>
                            <span>${formatFileSize(asset.size)}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Created:</label>
                            <span>${new Date(asset.created_at).toLocaleString()}</span>
                        </div>
                        <div class="metadata-item">
                            <label>Modified:</label>
                            <span>${new Date(asset.modified_at).toLocaleString()}</span>
                        </div>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button class="form-btn primary" onclick="downloadAsset('${asset.id}')">
                        📥 Download Asset
                    </button>
                    <button class="form-btn secondary" onclick="closeModal()">
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function updatePixelLabStats() {
    try {
        // Get asset count
        const assetsResponse = await fetch(`${PIXELLAB_API_BASE}/assets`);
        const assetsData = await assetsResponse.json();
        
        if (assetsResponse.ok && assetsData.success) {
            updateElementById('total-generated-assets', assetsData.assets.length.toString());
        }
        
        // Update other stats (mock data for now)
        updateElementById('active-generations', '0');
        updateElementById('generation-success-rate', '98.5%');
        
    } catch (error) {
        console.error('Failed to update PixelLab stats:', error);
    }
}

async function showBatchGenerationModal() {
    const modalHtml = `
        <div class="modal-overlay" onclick="closeModal(event)">
            <div class="modal-content batch-modal" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>📦 Batch Asset Generation</h3>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                
                <div class="batch-form">
                    <div class="form-group">
                        <label>Generation Template</label>
                        <select id="batch-template">
                            <option value="weapon_pack">⚔️ Complete Weapon Pack (10 weapons)</option>
                            <option value="hero_pack">🦸 Hero Transformation Pack (4 forms)</option>
                            <option value="map_pack">🗺️ Environment Pack (6 maps)</option>
                            <option value="ui_pack">🎮 UI Elements Pack (15 icons)</option>
                            <option value="complete_game">🎯 Complete Game Assets (50+ items)</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Game Theme</label>
                        <select id="batch-theme">
                            <option value="fantasy">🏰 Fantasy Medieval</option>
                            <option value="sci-fi">🚀 Sci-Fi Futuristic</option>
                            <option value="dark">🌑 Dark Gothic</option>
                            <option value="cartoon">🎨 Cartoon Style</option>
                        </select>
                    </div>
                    
                    <div class="batch-preview" id="batch-preview">
                        <!-- Preview will be populated based on selection -->
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button class="form-btn primary" onclick="startBatchGeneration()">
                        🚀 Start Batch Generation
                    </button>
                    <button class="form-btn secondary" onclick="closeModal()">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    updateBatchPreview();
}

async function generateGameAssetPack() {
    try {
        showBatchProgress();
        
        const gameAssets = [
            // Legendary Weapons
            { asset_type: 'weapon', name: 'Godslayer Excalibur', description: 'Epic holy sword', rarity: 'legendary' },
            { asset_type: 'weapon', name: 'Worldender Bow', description: 'Cosmic void bow', rarity: 'legendary' },
            { asset_type: 'weapon', name: 'Staff of Omniscience', description: 'Reality-bending staff', rarity: 'legendary' },
            
            // Hero Forms
            { asset_type: 'hero', name: 'Dragon Lord Arin', description: 'Dragon transformation', rarity: 'legendary' },
            { asset_type: 'hero', name: 'Cosmic Emperor Arin', description: 'Cosmic ascension', rarity: 'legendary' },
            { asset_type: 'hero', name: 'Void Knight Arin', description: 'Dark void form', rarity: 'legendary' },
            
            // Environments
            { asset_type: 'map', name: 'Forest of Shadows', description: 'Dark mystical forest' },
            { asset_type: 'map', name: 'Ice Peaks', description: 'Frozen mountain peaks' },
            { asset_type: 'map', name: 'Volcanic Wasteland', description: 'Hellscape environment' },
            
            // Gems and UI
            { asset_type: 'gem', name: 'Crystal Gem', description: 'Game currency gem' },
            { asset_type: 'icon', name: 'Health Potion', description: 'Healing item icon' },
            { asset_type: 'icon', name: 'Mana Crystal', description: 'Magic item icon' }
        ];
        
        const response = await fetch(`${PIXELLAB_API_BASE}/batch-generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requests: gameAssets
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification(`✅ Generated ${data.successful} assets successfully!`, 'success');
            if (data.failed > 0) {
                showNotification(`⚠️ ${data.failed} assets failed to generate`, 'warning');
            }
            await refreshAssetGallery();
            await updatePixelLabStats();
        } else {
            throw new Error(data.error || 'Batch generation failed');
        }
        
    } catch (error) {
        console.error('Game asset pack generation failed:', error);
        showNotification(`❌ Game asset pack generation failed: ${error.message}`, 'error');
    } finally {
        hideBatchProgress();
    }
}

function showGenerationProgress(message) {
    // Add loading state to buttons
    const buttons = document.querySelectorAll('.template-btn, .generate-btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('generating');
    });
    
    showNotification(`🎨 ${message}`, 'info');
}

function hideGenerationProgress() {
    // Remove loading state from buttons
    const buttons = document.querySelectorAll('.template-btn, .generate-btn');
    buttons.forEach(btn => {
        btn.disabled = false;
        btn.classList.remove('generating');
    });
}

function showBatchProgress() {
    const batchStatus = document.getElementById('batch-status');
    const progressFill = document.getElementById('batch-progress');
    const batchCurrent = document.getElementById('batch-current');
    const batchTotal = document.getElementById('batch-total');
    
    batchStatus.style.display = 'block';
    batchTotal.textContent = '12';
    batchCurrent.textContent = '0';
    progressFill.style.width = '0%';
    
    // Simulate progress
    let current = 0;
    const interval = setInterval(() => {
        current++;
        batchCurrent.textContent = current.toString();
        progressFill.style.width = `${(current / 12) * 100}%`;
        
        if (current >= 12) {
            clearInterval(interval);
            setTimeout(() => {
                batchStatus.style.display = 'none';
            }, 2000);
        }
    }, 500);
}

function hideBatchProgress() {
    const batchStatus = document.getElementById('batch-status');
    batchStatus.style.display = 'none';
}

function clearGenerationForm() {
    document.getElementById('asset-name').value = '';
    document.getElementById('asset-description').value = '';
}

function filterAssetGallery() {
    refreshAssetGallery();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Auto-update dimensions based on asset type
document.addEventListener('DOMContentLoaded', function() {
    const assetTypeSelect = document.getElementById('asset-type-select');
    const widthInput = document.getElementById('asset-width');
    const heightInput = document.getElementById('asset-height');
    
    if (assetTypeSelect && widthInput && heightInput) {
        assetTypeSelect.addEventListener('change', function() {
            const dimensions = {
                weapon: { width: 1024, height: 1024 },
                hero: { width: 512, height: 768 },
                map: { width: 1920, height: 1080 },
                gem: { width: 256, height: 256 },
                icon: { width: 512, height: 512 },
                skin: { width: 512, height: 768 },
                boss: { width: 1024, height: 1024 }
            };
            
            const dim = dimensions[this.value] || { width: 1024, height: 1024 };
            widthInput.value = dim.width;
            heightInput.value = dim.height;
        });
    }
});