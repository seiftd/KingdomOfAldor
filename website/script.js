/**
 * Kingdom of Aldoria - Payment Website JavaScript
 * Handles package selection, payment methods, and RedotPay/Binance Pay integration
 */

// Payment Configuration
const PAYMENT_CONFIG = {
    redotpay: {
        merchantId: '1810350237',
        cardNumber: '4937280055579823',
        apiUrl: 'https://api.redotpay.com/v1/payments',
        publicKey: 'your_redotpay_public_key'
    },
    binance: {
        merchantId: '713636914',
        apiUrl: 'https://bpay.binanceapi.com/binancepay/openapi/v2/order',
        publicKey: 'your_binance_public_key'
    }
};

// Global State
let selectedPackage = null;
let selectedPaymentMethod = null;

// Payment processing status
let paymentInProgress = false;

// QR Code Generation and Download Functions
function generateQRCode() {
    const gameUrl = 'https://yourgame.com/download'; // Replace with actual download URL
    const qrCodeElement = document.getElementById('game-qr-code');
    
    // Generate QR code using QR.js library or similar
    // For now, we'll use a placeholder
    if (qrCodeElement) {
        // You can integrate with QR code generation library here
        console.log('QR Code generated for URL:', gameUrl);
    }
}

function downloadGame(platform) {
    const downloadUrls = {
        android: 'https://play.google.com/store/apps/details?id=com.aldoria.kingdom',
        ios: 'https://apps.apple.com/app/kingdom-of-aldoria/id123456789'
    };
    
    const url = downloadUrls[platform];
    if (url) {
        // Track download analytics
        trackEvent('game_download', {
            platform: platform,
            source: 'website_qr_section'
        });
        
        // Open download link
        window.open(url, '_blank');
        
        // Show success message
        showNotification(`🎮 Redirecting to ${platform === 'android' ? 'Google Play Store' : 'App Store'}...`, 'success');
    }
}

// Enhanced tracking for legendary item purchases
function trackLegendaryPurchase(itemId, price) {
    trackEvent('legendary_item_purchase', {
        item_id: itemId,
        price: price,
        currency: 'USD',
        item_category: 'legendary'
    });
}

// Modified selectPackage function to handle legendary items
function selectPackage(packageId, price) {
    if (paymentInProgress) {
        showNotification('⏳ Payment already in progress...', 'warning');
        return;
    }

    const packageData = {
        // Existing packages
        monthly_premium: { name: 'Royal Crown Membership', type: 'subscription' },
        weekly_premium: { name: 'Knight\'s Weekly Pass', type: 'subscription' },
        
        // Legendary Weapons
        godslayer_excalibur: { name: 'Godslayer Excalibur', type: 'legendary_weapon' },
        worldender_bow: { name: 'Worldender Bow', type: 'legendary_weapon' },
        omniscience_staff: { name: 'Staff of Omniscience', type: 'legendary_weapon' },
        
        // Legendary Skins
        dragon_lord_skin: { name: 'Dragon Lord Arin Skin', type: 'legendary_skin' },
        cosmic_emperor_skin: { name: 'Cosmic Emperor Arin Skin', type: 'legendary_skin' },
        
        // Ultimate Bundle
        godslayer_bundle: { name: 'Godslayer Complete Arsenal', type: 'ultimate_bundle' },
        
        // Gem packages (existing)
        gems_100: { name: '100 Gems', type: 'gems' },
        gems_500: { name: '500 Gems + 50 Bonus', type: 'gems' },
        gems_1200: { name: '1,200 Gems + 200 Bonus', type: 'gems' }
    };

    const selectedPackage = packageData[packageId];
    if (!selectedPackage) {
        showNotification('❌ Invalid package selected', 'error');
        return;
    }

    // Track legendary purchases
    if (selectedPackage.type.includes('legendary') || selectedPackage.type === 'ultimate_bundle') {
        trackLegendaryPurchase(packageId, price);
    }

    // Show package selection confirmation with enhanced UI for legendary items
    showPackageConfirmation(selectedPackage, price, packageId);
}

function showPackageConfirmation(packageData, price, packageId) {
    const isLegendary = packageData.type.includes('legendary') || packageData.type === 'ultimate_bundle';
    
    const confirmationHtml = `
        <div class="package-confirmation ${isLegendary ? 'legendary-confirmation' : ''}">
            <div class="confirmation-header">
                <h3>${isLegendary ? '🌟 LEGENDARY PURCHASE 🌟' : '📦 Package Confirmation'}</h3>
            </div>
            <div class="confirmation-content">
                <div class="package-info">
                    <h4>${packageData.name}</h4>
                    <div class="package-price ${isLegendary ? 'legendary-price' : ''}">$${price}</div>
                </div>
                
                ${isLegendary ? `
                    <div class="legendary-benefits">
                        <p>✨ You're about to unlock ultimate power!</p>
                        <div class="power-indicator">
                            <div class="power-bar"></div>
                        </div>
                    </div>
                ` : ''}
                
                <div class="confirmation-buttons">
                    <button class="confirm-btn ${isLegendary ? 'legendary-btn' : ''}" onclick="processPayment('${packageId}', ${price})">
                        ${isLegendary ? '⚔️ Claim Legendary Power' : '💳 Proceed to Payment'}
                    </button>
                    <button class="cancel-btn" onclick="closeConfirmation()">Cancel</button>
                </div>
            </div>
        </div>
    `;
    
    showModal(confirmationHtml);
}

// DOM Elements
const packageInfo = document.getElementById('selected-package-info');
const paymentForm = document.getElementById('payment-form');
const paymentDetails = document.getElementById('payment-details');
const loadingOverlay = document.getElementById('loading-overlay');

/**
 * Initialize the website
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏰 Kingdom of Aldoria Payment Portal Initialized');
    
    // Setup navigation
    setupNavigation();
    
    // Setup smooth scrolling
    setupSmoothScrolling();
    
    // Setup mobile menu
    setupMobileMenu();
    
    // Setup form validation
    setupFormValidation();
    
    // Add visual effects
    addVisualEffects();
    
    // Initialize QR code on page load
    generateQRCode();
    
    // Add legendary item hover effects
    addLegendaryEffects();
    
    console.log('✨ All systems ready for epic adventures!');
});

/**
 * Setup navigation functionality
 */
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a, .btn[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Setup smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Setup mobile menu toggle
 */
function setupMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

/**
 * Package Selection Functions
 */

/**
 * Select a package and update UI
 * @param {string} packageType - Type of package selected
 * @param {number} price - Price of the package
 */
function selectPackage(packageType, price) {
    console.log(`📦 Package selected: ${packageType} - $${price}`);
    
    selectedPackage = {
        type: packageType,
        price: price,
        name: getPackageName(packageType),
        description: getPackageDescription(packageType)
    };
    
    updateSelectedPackageDisplay();
    
    // Scroll to payment section
    document.getElementById('payment').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
    
    // Add selection animation
    addSelectionAnimation();
}

/**
 * Get human-readable package name
 * @param {string} packageType - Package type identifier
 * @returns {string} - Human-readable name
 */
function getPackageName(packageType) {
    const packageNames = {
        'monthly_premium': '👑 Royal Crown Membership',
        'weekly_premium': '⚔️ Knight\'s Weekly Pass',
        'monthly': '🏆 VIP Membership',
        'weekly': '⚔️ Weekly Pass',
        'starter': '🎮 Starter Pack',
        'void_scythe': '🌌 Void Scythe',
        'solar_sword': '🔥 Solar Flare Sword',
        'void_knight_skin': '🖤 Void Knight Skin',
        'gems_100': '💎 100 Gems',
        'gems_500': '💎 500 Gems (+50 Bonus)',
        'gems_1200': '💎 1,200 Gems (+200 Bonus)',
        'gems_3000': '💎 3,000 Gems (+700 Bonus)'
    };
    
    return packageNames[packageType] || packageType;
}

/**
 * Get package description
 * @param {string} packageType - Package type identifier
 * @returns {string} - Package description
 */
function getPackageDescription(packageType) {
    const descriptions = {
        'monthly_premium': 'Full VIP experience with 40 daily gems, max stamina 25, and exclusive benefits',
        'weekly_premium': 'Weekly knight pass with 25 daily gems, boosted stamina, and premium features',
        'monthly': 'Monthly VIP membership with daily gems and premium features',
        'weekly': 'Weekly subscription with enhanced gameplay benefits',
        'starter': 'Perfect starter bundle with exclusive skin, weapon, and resources',
        'void_scythe': 'Legendary cosmic weapon with +40 attack power and dark energy effects',
        'solar_sword': 'Blazing weapon with +35 fire damage and solar abilities',
        'void_knight_skin': 'Legendary dark armor with Time Rewind special ability',
        'gems_100': 'Perfect for small purchases and quick upgrades',
        'gems_500': 'Great value pack with bonus gems for serious players',
        'gems_1200': 'Premium gem package with substantial bonus rewards',
        'gems_3000': 'Ultimate gem package for the most dedicated adventurers'
    };
    
    return descriptions[packageType] || 'Premium game content package';
}

/**
 * Update the selected package display
 */
function updateSelectedPackageDisplay() {
    if (!selectedPackage) return;
    
    const packageHtml = `
        <div class="selected-package-details">
            <h4>${selectedPackage.name}</h4>
            <p class="package-description">${selectedPackage.description}</p>
            <div class="package-price-display">
                <span class="price-label">Price:</span>
                <span class="price-amount">$${selectedPackage.price}</span>
            </div>
            <div class="package-benefits">
                <span class="benefits-label">✨ Instant delivery to your game account</span>
            </div>
        </div>
    `;
    
    packageInfo.innerHTML = packageHtml;
    
    // Add golden glow effect
    packageInfo.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.4)';
    packageInfo.style.borderColor = '#FFD700';
}

/**
 * Add selection animation effect
 */
function addSelectionAnimation() {
    const effect = document.createElement('div');
    effect.className = 'selection-effect';
    effect.innerHTML = '✨ Package Selected! ✨';
    effect.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #0D0D0D;
        padding: 20px 40px;
        border-radius: 25px;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        font-size: 1.2rem;
        z-index: 10000;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
        animation: selectionPulse 2s ease-out forwards;
    `;
    
    document.body.appendChild(effect);
    
    setTimeout(() => {
        effect.remove();
    }, 2000);
}

/**
 * Tab switching functionality
 * @param {string} tabName - Name of tab to switch to
 */
function switchTab(tabName) {
    console.log(`🔄 Switching to tab: ${tabName}`);
    
    // Remove active class from all tabs and content
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.package-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    event.target.classList.add('active');
    document.getElementById(tabName).classList.add('active');
    
    // Add tab switch animation
    const activeContent = document.getElementById(tabName);
    activeContent.style.animation = 'tabFadeIn 0.5s ease-in-out';
}

/**
 * Payment Method Selection
 */

/**
 * Select payment method
 * @param {string} method - Payment method (redotpay, binance, card)
 */
function selectPaymentMethod(method) {
    console.log(`💳 Payment method selected: ${method}`);
    
    if (!selectedPackage) {
        showAlert('Please select a package first!', 'warning');
        return;
    }
    
    selectedPaymentMethod = method;
    
    // Update UI
    document.querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    event.currentTarget.classList.add('selected');
    
    // Show payment form
    paymentForm.style.display = 'block';
    
    // Load payment method specific details
    loadPaymentDetails(method);
    
    // Scroll to form
    paymentForm.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

/**
 * Load payment method specific details
 * @param {string} method - Payment method
 */
function loadPaymentDetails(method) {
    let detailsHtml = '';
    
    switch (method) {
        case 'redotpay':
            detailsHtml = `
                <div class="redotpay-details">
                    <h4>🔴 RedotPay Payment</h4>
                    <div class="payment-info-grid">
                        <div class="info-item">
                            <label>Merchant ID:</label>
                            <span>1810350237</span>
                        </div>
                        <div class="info-item">
                            <label>Supported Cards:</label>
                            <span>Visa, Mastercard, American Express</span>
                        </div>
                        <div class="info-item">
                            <label>Processing Time:</label>
                            <span>Instant</span>
                        </div>
                    </div>
                    <div class="security-notice">
                        <p>🔒 Secured by RedotPay's advanced encryption and fraud protection</p>
                    </div>
                </div>
            `;
            break;
            
        case 'binance':
            detailsHtml = `
                <div class="binance-details">
                    <h4>🟡 Binance Pay</h4>
                    <div class="payment-info-grid">
                        <div class="info-item">
                            <label>Merchant ID:</label>
                            <span>713636914</span>
                        </div>
                        <div class="info-item">
                            <label>Supported Crypto:</label>
                            <span>BTC, ETH, BNB, USDT, BUSD</span>
                        </div>
                        <div class="info-item">
                            <label>Network Fees:</label>
                            <span>Low fees with Binance Smart Chain</span>
                        </div>
                    </div>
                    <div class="crypto-notice">
                        <p>⚡ Fast crypto payments with instant confirmation</p>
                    </div>
                </div>
            `;
            break;
            
        case 'card':
            detailsHtml = `
                <div class="card-details">
                    <h4>💳 Credit/Debit Card</h4>
                    <div class="card-form">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="card-number">Card Number</label>
                                <input type="text" id="card-number" placeholder="1234 5678 9012 3456" maxlength="19">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="card-expiry">Expiry Date</label>
                                <input type="text" id="card-expiry" placeholder="MM/YY" maxlength="5">
                            </div>
                            <div class="form-group">
                                <label for="card-cvv">CVV</label>
                                <input type="text" id="card-cvv" placeholder="123" maxlength="4">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="card-name">Cardholder Name</label>
                            <input type="text" id="card-name" placeholder="John Doe">
                        </div>
                    </div>
                </div>
            `;
            break;
    }
    
    paymentDetails.innerHTML = detailsHtml;
    
    // Setup card input formatting if card method
    if (method === 'card') {
        setupCardInputFormatting();
    }
}

/**
 * Setup card input formatting
 */
function setupCardInputFormatting() {
    const cardNumber = document.getElementById('card-number');
    const cardExpiry = document.getElementById('card-expiry');
    const cardCvv = document.getElementById('card-cvv');
    
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });
    }
    
    if (cardExpiry) {
        cardExpiry.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
        });
    }
    
    if (cardCvv) {
        cardCvv.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }
}

/**
 * Form validation setup
 */
function setupFormValidation() {
    const form = document.getElementById('checkout-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            processPayment();
        });
    }
}

/**
 * Process payment based on selected method
 */
async function processPayment() {
    console.log('💰 Processing payment...');
    
    if (!selectedPackage || !selectedPaymentMethod) {
        showAlert('Please select a package and payment method!', 'error');
        return;
    }
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Show loading
    showLoading(true);
    
    try {
        let result;
        
        switch (selectedPaymentMethod) {
            case 'redotpay':
                result = await processRedotPayment();
                break;
            case 'binance':
                result = await processBinancePayment();
                break;
            case 'card':
                result = await processCardPayment();
                break;
            default:
                throw new Error('Invalid payment method');
        }
        
        if (result.success) {
            showPaymentSuccess(result);
        } else {
            showAlert(result.error || 'Payment failed. Please try again.', 'error');
        }
        
    } catch (error) {
        console.error('Payment error:', error);
        showAlert('An error occurred during payment. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Process RedotPay payment
 */
async function processRedotPayment() {
    console.log('🔴 Processing RedotPay payment...');
    
    const paymentData = {
        merchantId: PAYMENT_CONFIG.redotpay.merchantId,
        amount: selectedPackage.price,
        currency: 'USD',
        orderId: generateOrderId(),
        productName: selectedPackage.name,
        productDescription: selectedPackage.description,
        customerEmail: document.getElementById('email').value,
        playerId: document.getElementById('player-id').value || null,
        successUrl: `${window.location.origin}/success.html`,
        failUrl: `${window.location.origin}/failed.html`,
        notifyUrl: `${window.location.origin}/webhook/redotpay`
    };
    
    // Simulate API call (replace with actual RedotPay integration)
    await simulatePaymentProcessing();
    
    // For demo purposes, we'll redirect to RedotPay checkout
    const checkoutUrl = `https://checkout.redotpay.com/pay?` + 
        `merchant_id=${paymentData.merchantId}&` +
        `amount=${paymentData.amount}&` +
        `currency=${paymentData.currency}&` +
        `order_id=${paymentData.orderId}&` +
        `product_name=${encodeURIComponent(paymentData.productName)}&` +
        `email=${encodeURIComponent(paymentData.customerEmail)}&` +
        `success_url=${encodeURIComponent(paymentData.successUrl)}&` +
        `fail_url=${encodeURIComponent(paymentData.failUrl)}`;
    
    // In production, redirect to actual payment page
    // window.location.href = checkoutUrl;
    
    // For demo, simulate success
    return {
        success: true,
        transactionId: 'REDOT_' + generateOrderId(),
        method: 'RedotPay'
    };
}

/**
 * Process Binance Pay payment
 */
async function processBinancePayment() {
    console.log('🟡 Processing Binance Pay payment...');
    
    const paymentData = {
        merchantId: PAYMENT_CONFIG.binance.merchantId,
        merchantTradeNo: generateOrderId(),
        orderAmount: selectedPackage.price,
        currency: 'USDT', // Default to USDT for crypto
        goods: {
            goodsType: "02", // Virtual goods
            goodsCategory: "Game Items",
            referenceGoodsId: selectedPackage.type,
            goodsName: selectedPackage.name,
            goodsDetail: selectedPackage.description
        },
        buyerInfo: {
            buyerEmail: document.getElementById('email').value,
            buyerId: document.getElementById('player-id').value || 'guest'
        }
    };
    
    // Simulate API call (replace with actual Binance Pay integration)
    await simulatePaymentProcessing();
    
    // For demo purposes, create Binance Pay checkout URL
    const checkoutUrl = `https://pay.binance.com/checkout?` +
        `merchant_id=${paymentData.merchantId}&` +
        `trade_no=${paymentData.merchantTradeNo}&` +
        `amount=${paymentData.orderAmount}&` +
        `currency=${paymentData.currency}&` +
        `goods_name=${encodeURIComponent(paymentData.goods.goodsName)}`;
    
    // In production, redirect to actual payment page
    // window.location.href = checkoutUrl;
    
    // For demo, simulate success
    return {
        success: true,
        transactionId: 'BINANCE_' + generateOrderId(),
        method: 'Binance Pay'
    };
}

/**
 * Process regular card payment
 */
async function processCardPayment() {
    console.log('💳 Processing card payment...');
    
    // Simulate payment processing
    await simulatePaymentProcessing();
    
    return {
        success: true,
        transactionId: 'CARD_' + generateOrderId(),
        method: 'Credit Card'
    };
}

/**
 * Validate payment form
 */
function validateForm() {
    const email = document.getElementById('email').value;
    
    if (!email || !isValidEmail(email)) {
        showAlert('Please enter a valid email address!', 'error');
        return false;
    }
    
    // Additional validation for card payments
    if (selectedPaymentMethod === 'card') {
        const cardNumber = document.getElementById('card-number').value;
        const cardExpiry = document.getElementById('card-expiry').value;
        const cardCvv = document.getElementById('card-cvv').value;
        const cardName = document.getElementById('card-name').value;
        
        if (!cardNumber || cardNumber.replace(/\s/g, '').length < 13) {
            showAlert('Please enter a valid card number!', 'error');
            return false;
        }
        
        if (!cardExpiry || cardExpiry.length !== 5) {
            showAlert('Please enter a valid expiry date!', 'error');
            return false;
        }
        
        if (!cardCvv || cardCvv.length < 3) {
            showAlert('Please enter a valid CVV!', 'error');
            return false;
        }
        
        if (!cardName) {
            showAlert('Please enter the cardholder name!', 'error');
            return false;
        }
    }
    
    return true;
}

/**
 * Utility Functions
 */

/**
 * Generate unique order ID
 */
function generateOrderId() {
    return 'KOA_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Simulate payment processing delay
 */
function simulatePaymentProcessing() {
    return new Promise(resolve => {
        setTimeout(resolve, 2000 + Math.random() * 3000); // 2-5 seconds
    });
}

/**
 * Show loading overlay
 */
function showLoading(show) {
    if (loadingOverlay) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type}`;
    alertElement.innerHTML = `
        <div class="alert-content">
            <span class="alert-icon">${getAlertIcon(type)}</span>
            <span class="alert-message">${message}</span>
            <button class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    alertElement.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getAlertColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(alertElement);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertElement.parentNode) {
            alertElement.remove();
        }
    }, 5000);
}

/**
 * Get alert icon based on type
 */
function getAlertIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || 'ℹ️';
}

/**
 * Get alert color based on type
 */
function getAlertColor(type) {
    const colors = {
        success: '#00C851',
        error: '#FF3547',
        warning: '#FFA500',
        info: '#6495ED'
    };
    return colors[type] || '#6495ED';
}

/**
 * Show payment success page
 */
function showPaymentSuccess(result) {
    const successHtml = `
        <div class="payment-success">
            <div class="success-animation">
                <div class="checkmark">✓</div>
            </div>
            <h2>🎉 Payment Successful!</h2>
            <div class="success-details">
                <p><strong>Package:</strong> ${selectedPackage.name}</p>
                <p><strong>Amount:</strong> $${selectedPackage.price}</p>
                <p><strong>Transaction ID:</strong> ${result.transactionId}</p>
                <p><strong>Payment Method:</strong> ${result.method}</p>
            </div>
            <div class="success-message">
                <p>🏰 Welcome to Kingdom of Aldoria!</p>
                <p>Your purchase will be delivered to your game account within 5 minutes.</p>
                <p>Check your email for receipt and instructions.</p>
            </div>
            <div class="success-actions">
                <button class="btn btn-primary" onclick="window.location.reload()">Buy More</button>
                <button class="btn btn-secondary" onclick="window.close()">Close</button>
            </div>
        </div>
    `;
    
    // Replace entire page content with success page
    document.body.innerHTML = `
        <div class="success-container">
            ${successHtml}
        </div>
        <div class="stars-background"></div>
    `;
    
    // Add success page styles
    document.head.insertAdjacentHTML('beforeend', `
        <style>
            .success-container {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--gradient-mystic);
            }
            .payment-success {
                background: rgba(30, 30, 62, 0.9);
                padding: 3rem;
                border-radius: 20px;
                text-align: center;
                border: 2px solid #FFD700;
                box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
                max-width: 500px;
            }
            .success-animation {
                margin-bottom: 2rem;
            }
            .checkmark {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: #00C851;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                margin: 0 auto;
                animation: bounceIn 0.6s ease-out;
            }
            @keyframes bounceIn {
                0% { transform: scale(0); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            .success-details {
                background: rgba(0, 0, 0, 0.3);
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1.5rem 0;
                text-align: left;
            }
            .success-actions {
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin-top: 2rem;
            }
        </style>
    `);
}

/**
 * Add visual effects to the page
 */
function addVisualEffects() {
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes selectionPulse {
            0% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.5);
            }
            50% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1.1);
            }
            100% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(1);
            }
        }
        
        @keyframes tabFadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .payment-info-grid {
            display: grid;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        .info-item label {
            color: #FFD700;
            font-weight: 600;
        }
        
        .card-form .form-row {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .card-form .form-group {
            flex: 1;
        }
        
        .security-notice, .crypto-notice {
            background: rgba(0, 200, 81, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #00C851;
            margin-top: 1rem;
        }
        
        .alert-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .alert-close {
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            margin-left: auto;
        }
    `;
    document.head.appendChild(style);
}

// Export functions for global use
window.selectPackage = selectPackage;
window.switchTab = switchTab;
window.selectPaymentMethod = selectPaymentMethod;

console.log('🚀 Kingdom of Aldoria Payment System Ready!');