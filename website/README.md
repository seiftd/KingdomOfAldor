# Kingdom of Aldoria - Payment Website

Beautiful fantasy-themed payment portal for Kingdom of Aldoria mobile RPG game.

## 🏰 Features

- **Fantasy Theme**: Beautiful dark fantasy design with gold accents and magical effects
- **Multiple Payment Methods**: RedotPay, Binance Pay, and traditional card payments
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Game Integration**: Seamless connection with the mobile game
- **Secure Payments**: Industry-standard security with SSL encryption

## 💳 Payment Integration

### RedotPay Integration
- **Merchant ID**: `1810350237`
- **Card Number**: `4937280055579823`
- **Features**: Instant processing, global coverage, fraud protection

### Binance Pay Integration  
- **Merchant ID**: `713636914`
- **Features**: Cryptocurrency payments, low fees, fast transactions
- **Supported Coins**: BTC, ETH, BNB, USDT, BUSD

## 🚀 Quick Start

### 1. Local Development
```bash
# Clone or download the website files
cd website/

# Open in browser (simple method)
open index.html

# Or serve with a local server
python3 -m http.server 8000
# Visit: http://localhost:8000
```

### 2. Production Deployment

#### Option A: Static Hosting (GitHub Pages, Netlify, Vercel)
1. Upload all files to your hosting platform
2. Update the payment URLs in `script.js`
3. Configure your domain DNS settings

#### Option B: Traditional Web Hosting
1. Upload files via FTP/SFTP to your web server
2. Ensure HTTPS is enabled for secure payments
3. Update payment configurations

## 🔧 Configuration

### Payment Settings
Edit `script.js` and update the payment configuration:

```javascript
const PAYMENT_CONFIG = {
    redotpay: {
        merchantId: '1810350237',        // Your RedotPay merchant ID
        apiUrl: 'https://api.redotpay.com/v1/payments',
        publicKey: 'your_redotpay_public_key'
    },
    binance: {
        merchantId: '713636914',         // Your Binance Pay merchant ID  
        apiUrl: 'https://bpay.binanceapi.com/binancepay/openapi/v2/order',
        publicKey: 'your_binance_public_key'
    }
};
```

### Website URL
In the game's web integration system (`src/systems/web_integration.py`):

```python
self.website_url = "https://yourdomain.com"  # Update with your actual URL
```

## 📱 Game Integration

The website automatically integrates with the Kingdom of Aldoria mobile game:

### Automatic Package Selection
When players click "Buy Gems" or subscription buttons in the game, they're redirected to the website with the appropriate package pre-selected.

### Player Data Transfer
Player information is passed via URL parameters:
- Player ID (for purchase tracking)
- Current level
- Current gem/gold amounts
- Suggested packages

### Purchase Completion
After successful payment, players receive their items automatically in-game within 5 minutes.

## 🎨 Customization

### Colors & Theme
Edit `styles.css` to customize the fantasy theme:

```css
:root {
    --primary-gold: #FFD700;      /* Main gold color */
    --royal-purple: #4B0082;      /* Purple accents */
    --mystic-blue: #6495ED;       /* Blue highlights */
    /* ... more colors */
}
```

### Package Pricing
Update package prices in `index.html` and corresponding reward values in the game code.

### Payment Methods
Add or remove payment options by modifying the payment methods section in `index.html` and updating the corresponding JavaScript handlers.

## 🔒 Security

### SSL Certificate
**Required**: All payment processing requires HTTPS. Ensure your domain has a valid SSL certificate.

### Payment Data
- No sensitive payment data is stored on the website
- All transactions are processed through secure payment gateways
- Player data is minimal and encrypted where possible

### API Keys
- Keep all API keys and merchant secrets secure
- Use environment variables in production
- Never commit sensitive keys to version control

## 📊 Analytics & Tracking

### Built-in Tracking
The website includes purchase tracking:
- Package selection analytics
- Payment method preferences  
- Conversion rates
- Player behavior flows

### Integration Options
Add your preferred analytics:
- Google Analytics
- Facebook Pixel
- Custom tracking solutions

## 🛠️ Troubleshooting

### Common Issues

**Payment Not Processing**
1. Check SSL certificate is valid
2. Verify merchant IDs are correct
3. Ensure payment gateway is properly configured

**Website Not Loading** 
1. Check file permissions
2. Verify all assets are uploaded
3. Check browser console for errors

**Game Integration Issues**
1. Verify website URL in game settings
2. Check URL parameter parsing
3. Test with different browsers

### Debug Mode
Enable debug mode by adding `?debug=true` to the URL for additional console logging.

## 📞 Support

### For Players
- **Email**: support@kingdomofaldoria.com
- **Live Chat**: Available for premium members
- **FAQ**: Check the game's help section

### For Developers  
- Check browser console for error messages
- Review payment gateway documentation
- Test with payment gateway sandbox environments

## 🚀 Performance

### Optimization Features
- **Compressed Assets**: WebP images, minified CSS/JS
- **Caching**: Optimized cache headers
- **CDN Ready**: All assets can be served via CDN
- **Mobile Optimized**: Fast loading on mobile devices

### Best Practices
- Enable gzip compression on your server
- Use a CDN for static assets
- Monitor Core Web Vitals
- Test on various devices and connections

## 📄 License

Copyright © 2024 Kingdom of Aldoria. All rights reserved.

This payment portal is proprietary software for Kingdom of Aldoria game monetization.

## 🎮 About Kingdom of Aldoria

Kingdom of Aldoria is an epic 2D fantasy mobile RPG featuring:
- 10 unique fantasy worlds to explore
- 300 challenging stages with boss battles
- Character customization with special abilities
- Strategic turn-based combat
- Fair free-to-play progression

Download the game and begin your legendary adventure today!

---

*May your adventures in Aldoria be filled with glory and treasure!* ⚔️✨