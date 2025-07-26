# Kingdom of Aldoria - Offline/Online Integration Guide

## 🎯 **System Overview**

This guide explains how to integrate the offline/online system, code redemption, and sync management for Kingdom of Aldoria.

## 📊 **Data Flow Architecture**

```mermaid
flowchart LR
    A[Player] -->|Online| B[Firebase: UserID, Gems, Ads, IAPs]
    A -->|Offline| C[SQLite: Progress, Inventory]
    B <-->|Sync| D[Conflict Resolution: Keep newest timestamp]
    C <-->|Sync| D
    E[Admin Dashboard] -->|Monitor| B
    E -->|Monitor| C
    F[Promo Codes] -->|Rewards| C
    F -->|Analytics| E
```

## 🔧 **Integration Steps**

### 1. **Initialize Database Systems**

```python
# In main.py
from src.systems.database_manager import DatabaseManager
from src.systems.code_manager import CodeManager

def initialize_game():
    game = Game()
    
    # Initialize database manager (handles both SQLite and Firebase)
    db_manager = DatabaseManager(game)
    game.add_system('database_manager', db_manager)
    
    # Initialize code manager
    code_manager = CodeManager(game)
    game.add_system('code_manager', code_manager)
    
    return game
```

### 2. **Player Login & Sync**

```python
# Player login process
def login_player(user_id: str):
    db_manager = game.get_system('database_manager')
    
    # Create user if doesn't exist
    if not db_manager.get_player_data(user_id):
        db_manager.create_user(user_id)
    
    # Login handles stamina update, daily rewards, and sync
    success = db_manager.login_user(user_id)
    
    if success:
        print(f"✅ Player {user_id} logged in successfully")
        
        # Check sync status
        sync_status = db_manager.get_sync_status(user_id)
        if sync_status['is_online']:
            print("🌐 Online mode - data will sync to Firebase")
        else:
            print("📱 Offline mode - data stored locally")
```

### 3. **Code Redemption Integration**

```python
# In-game code redemption
def redeem_promo_code(user_id: str, code: str):
    code_manager = game.get_system('code_manager')
    
    result = code_manager.redeem_code(user_id, code)
    
    if result['success']:
        rewards = result['rewards']
        message = f"Code redeemed! Rewards: "
        
        if 'gems' in rewards:
            message += f"{rewards['gems']} gems "
        if 'gold' in rewards:
            message += f"{rewards['gold']} gold "
        
        show_reward_popup(message)
    else:
        show_error_popup(result['message'])
```

### 4. **Admin Dashboard Integration**

The admin dashboard provides comprehensive management through:

#### **Code Management**
- **Create Codes**: Set rewards, limits, and expiration
- **Monitor Usage**: Track redemptions and analytics
- **Manage Lifecycle**: Edit, disable, or delete codes

#### **Sync Monitoring**
- **Real-time Status**: Online/offline player counts
- **Sync Events**: Track successful/failed sync operations
- **Conflict Resolution**: Monitor and resolve data conflicts
- **Emergency Controls**: Force offline mode if needed

## 🔄 **Sync Process Details**

### **Automatic Sync Triggers**
1. **Login**: Player connects → sync player data
2. **Currency Changes**: Gems/gold earned → queue for sync
3. **Inventory Updates**: New items → queue for sync
4. **Progress Updates**: Stage completion → queue for sync
5. **Periodic**: Every 5 minutes if online

### **Conflict Resolution**
```python
# Timestamp-based conflict resolution
def resolve_conflicts(local_data, remote_data):
    local_timestamp = local_data.get('updated_at', 0)
    remote_timestamp = remote_data.get('updated_at', 0)
    
    if remote_timestamp > local_timestamp:
        # Remote is newer, update local
        return remote_data
    else:
        # Local is newer, push to remote
        return local_data
```

## 📱 **Offline Mode Features**

### **Fully Functional Offline**
- ✅ Stage progression and combat
- ✅ Inventory management
- ✅ Currency earning (gold from battles)
- ✅ Stamina regeneration (device clock)
- ✅ Player progression and leveling
- ✅ Local save with encryption

### **Online-Only Features**
- 🌐 Rewarded ads for gems
- 🌐 IAP validation and gem purchases
- 🌐 Daily login streaks
- 🌐 Promo code redemption
- 🌐 Multiplayer/guild features
- 🌐 Cloud save backup

## 🎫 **Promo Code System**

### **Code Types & Rewards**
- **Welcome**: 100 gems, 1000 gold
- **Daily**: 25 gems, 500 gold
- **Weekly**: 100 gems, 2000 gold
- **Event**: 500 gems, 5000 gold
- **Premium**: 1000 gems, 10000 gold
- **VIP**: 2500 gems, 25000 gold

### **Default Codes Created**
- `WELCOME2024`: Welcome bonus (1000 uses)
- `LAUNCH50`: Launch celebration (500 uses)
- `SEIFVIP`: Creator special (100 uses)

### **Admin Code Management**
```javascript
// Create new code via dashboard
function createCode() {
    const codeData = {
        code: 'NEWYEAR2024',
        name: 'New Year Special',
        description: 'Celebrate the new year!',
        type: 'event',
        rewardGems: 500,
        rewardGold: 5000,
        usageLimit: 1000,
        durationDays: 30
    };
    
    // API call to create code
    createPromoCode(codeData);
}
```

## 🔐 **Security Features**

### **Data Protection**
- SQLite database encryption
- Firebase security rules
- Code validation and rate limiting
- Admin authentication (seiftouatilol@gmail.com)

### **Anti-Cheat Measures**
- Server-side validation for critical operations
- Encrypted save files with checksums
- Timestamp verification for offline progress
- Usage limits for promo codes

## 📊 **Analytics & Monitoring**

### **Available Metrics**
- Player activity (DAU/WAU/MAU)
- Revenue tracking by source
- Ad performance and conversion rates
- Code redemption analytics
- Sync success/failure rates
- Online vs offline player distribution

### **Dashboard Access**
- **URL**: `website/admin/dashboard.html`
- **Login**: seiftouatilol@gmail.com / seif0662
- **Features**: Real-time monitoring, code management, sync controls

## 🚀 **Deployment Checklist**

### **Firebase Setup**
1. Create Firebase project
2. Enable Firestore Database
3. Set up authentication
4. Configure security rules
5. Add service account key

### **Database Configuration**
1. Ensure SQLite database creation
2. Test sync functionality
3. Verify code redemption system
4. Configure ad reward validation

### **Admin Dashboard**
1. Deploy website with admin section
2. Test login functionality
3. Verify code management
4. Check sync monitoring

## 🔧 **Production Configuration**

### **Firebase Config (firebase-config.json)**
```json
{
  "type": "service_account",
  "project_id": "kingdom-of-aldoria-prod",
  "private_key_id": "your_private_key_id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk@kingdom-of-aldoria-prod.iam.gserviceaccount.com",
  "client_id": "your_client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

### **Environment Variables**
```bash
# Production settings
FIREBASE_CONFIG_PATH=/path/to/firebase-config.json
ADMIN_EMAIL=seiftouatilol@gmail.com
ADMIN_PASSWORD_HASH=your_hashed_password
DATABASE_ENCRYPTION_KEY=your_32_byte_key
```

## 🎮 **Game Integration Examples**

### **Shop Integration**
```python
# When player tries to buy premium item
def purchase_premium_item(user_id: str, item_id: str):
    if is_online():
        # Redirect to payment website
        web_integration.open_store_website(f'item_{item_id}')
    else:
        show_message("Premium purchases require internet connection")
```

### **Ad Rewards Integration**
```python
# When player watches ad
def watch_rewarded_ad(user_id: str):
    if is_online():
        ad_manager = game.get_system('ad_manager')
        result = ad_manager.show_rewarded_ad()
        
        if result['success']:
            # Rewards automatically added to database
            show_reward_popup(result['message'])
    else:
        show_message("Ads require internet connection")
```

## 🏆 **Best Practices**

1. **Always check online status** before sync operations
2. **Queue offline changes** for sync when connection returns
3. **Validate all transactions** server-side
4. **Encrypt sensitive data** in local storage
5. **Monitor sync conflicts** and resolve promptly
6. **Test offline mode** thoroughly
7. **Use timestamp-based** conflict resolution
8. **Implement graceful degradation** for offline features

This integration provides a robust foundation for Kingdom of Aldoria's offline/online hybrid system with comprehensive admin controls and real-time monitoring capabilities.