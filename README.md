# Kingdom of Aldoria - 2D Mobile RPG Game

A complete fantasy RPG game for Android devices built with Python and Pygame, featuring 10 unique worlds, 300 stages, character customization, and mobile monetization.

## 🎮 Game Features

### Core Gameplay
- **10 Fantasy Worlds**: Forest of Shadows, Desert of Souls, Ice Peaks, Volcanic Wastes, Mystic Swamps, Crystal Caverns, Sky Citadel, Dark Kingdom, Light Fortress, and Void Nexus
- **300 Total Stages**: 30 stages per world with progressive difficulty
- **Boss Battles**: Epic boss encounters every 5 stages that scale with player power
- **Real-time Combat**: Turn-based mechanics with skill timing and strategy

### Character System
- **Knight Arin**: Main character with customizable appearances
- **5 Unique Skins**: Each with special abilities
  - Default Knight (no special skill)
  - Forest Scout (Speed Boost - 5s duration)
  - Desert Nomad (Instant Heal - 30% HP)
  - Void Knight (Time Rewind - damage reversal)
  - Solar Paladin (Damage Doubler - 7s duration)
- **Weapon Collection**: 5 weapons with increasing power
- **Level Progression**: Stats increase with player level

### Mobile Features
- **Stamina System**: 1 stamina per stage, 20-minute recharge
- **Dual Currency**: Gold (earned) and Gems (premium)
- **Touch Controls**: Optimized for mobile devices
- **HD Graphics**: 1280x720 resolution with aspect ratio scaling

### Monetization
- **Subscriptions**:
  - Weekly ($4.99): 25 gems/day + max stamina 20
  - Monthly ($15.99): 40 gems/day + max stamina 25
- **In-App Purchases**:
  - Starter Pack ($0.99): Special skin + weapon
  - Legendary items ($3.99-$14.99)
- **Rewarded Ads**: 30 gems per 10 views (30 ads/day cap)
- **Interstitial Ads**: Between stages
- **Daily Login Rewards**: Streak bonuses

## 🛠️ Technical Requirements

### Development Environment
- Python 3.10+
- Pygame 2.5+
- Android SDK (for building APK)
- Buildozer (for Android packaging)

### Dependencies
```bash
pip install -r requirements.txt
```

### Asset Requirements
- Images: WebP format for optimization
- Audio: Ogg Vorbis format
- Fonts: TTF format
- Total size limit: 2GB maximum

## 🚀 Getting Started

### Local Development

1. **Clone the repository**:
```bash
git clone <repository-url>
cd KingdomOfAldoria
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the game**:
```bash
python main.py
```

### Building for Android

1. **Install Buildozer**:
```bash
pip install buildozer
```

2. **Initialize Buildozer** (first time only):
```bash
buildozer init
```

3. **Build debug APK**:
```bash
buildozer android debug
```

4. **Build release APK**:
```bash
buildozer android release
```

### ADB Testing

1. **Connect Android device** with USB debugging enabled

2. **Install debug APK**:
```bash
adb install bin/kingdomofaldoria-*-debug.apk
```

3. **View logs**:
```bash
adb logcat | grep python
```

## 📁 Project Structure

```
KingdomOfAldoria/
├── main.py                 # Main game entry point
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Android build configuration
├── README.md              # This file
├── game/                  # Game source code
│   ├── core/             # Core systems
│   │   ├── config.py     # Game configuration
│   │   ├── asset_manager.py  # Asset loading
│   │   ├── audio_manager.py  # Audio system
│   │   └── save_manager.py   # Save/load system
│   ├── states/           # Game states
│   │   ├── state_manager.py  # State management
│   │   ├── main_menu.py     # Main menu
│   │   ├── world_map.py     # World selection
│   │   ├── battle.py        # Combat screen
│   │   └── shop.py          # Shop system
│   ├── entities/         # Game entities
│   │   ├── player.py     # Player character
│   │   ├── enemy.py      # Enemy entities
│   │   └── items.py      # Items and equipment
│   ├── systems/          # Game systems
│   │   ├── combat.py     # Combat mechanics
│   │   ├── progression.py # Level/XP system
│   │   └── monetization.py # IAP and ads
│   ├── ui/               # User interface
│   │   ├── button.py     # Button component
│   │   ├── panel.py      # Panel component
│   │   └── hud.py        # Game HUD
│   └── utils/            # Utilities
│       └── mobile_utils.py # Mobile optimizations
└── assets/               # Game assets
    ├── images/           # Sprite graphics
    │   ├── characters/   # Character sprites
    │   ├── enemies/      # Enemy sprites
    │   ├── weapons/      # Weapon sprites
    │   ├── worlds/       # World backgrounds
    │   ├── ui/           # UI elements
    │   └── effects/      # Visual effects
    ├── audio/            # Sound and music
    │   ├── music/        # Background music
    │   └── sfx/          # Sound effects
    ├── fonts/            # Typography
    └── data/             # Game data files
```

## 🎯 Game Balance

### Progression Formula
- **XP Requirements**: Base 100 XP * 1.15^(level-1)
- **Enemy HP**: Base 100 * (1 + (world-1) * 0.3) * (1 + (stage-1) * 0.05) * (1 + (player_level-1) * 0.02)
- **Enemy Damage**: Base 50 * (1 + (world-1) * 0.25) * (1 + (stage-1) * 0.03) * (1 + (player_level-1) * 0.015)

### Currency Economy
- **Stage Gold Reward**: 10 + world*5 + stage*2
- **Stage XP Reward**: 25 + world*10 + stage*3
- **Gems from Ads**: 3 gems per ad, 30 ads/day max = 90 gems/day
- **Subscription Value**: Weekly provides 175 gems/week, Monthly provides 1200 gems/month

## 🎨 Art Style Requirements

All assets should follow a consistent fantasy art style:

### Characters
- **Resolution**: 64x64 to 128x128 pixels
- **Style**: Pixel art or high-resolution fantasy sprites
- **Animation**: Idle, attack, and special skill frames

### Enemies
- **Resolution**: 48x48 to 96x96 pixels
- **Style**: Fantasy creatures matching world themes
- **Variety**: 3 enemy types per world + boss variants

### Weapons
- **Resolution**: 32x48 to 48x64 pixels
- **Style**: Fantasy weapons with visual progression
- **Effects**: Glowing or particle effects for higher tiers

### World Backgrounds
- **Resolution**: 1280x720 (HD)
- **Style**: Fantasy landscapes with atmospheric effects
- **Parallax**: Multiple layers for depth

## 🔧 Mobile Optimizations

### Performance
- **Texture Atlases**: Reduce draw calls
- **Object Pooling**: Reuse enemy/projectile objects
- **Dynamic Loading**: Load/unload world assets as needed
- **Quality Settings**: Adjustable graphics quality

### Memory Management
- **Asset Caching**: LRU cache with configurable size
- **Compression**: WebP images, Ogg audio
- **Garbage Collection**: Aggressive GC settings for mobile

### Battery Optimization
- **Frame Rate**: Adaptive FPS based on performance
- **Background Pause**: Automatic pause when app is backgrounded
- **Reduced Effects**: Lower particle density on slower devices

## 📱 Platform Integration

### Android Features
- **Back Button**: Proper navigation handling
- **Lifecycle**: Pause/resume support
- **Permissions**: Minimal required permissions
- **Storage**: External storage for save data
- **Notifications**: Local notifications for stamina

### Ad Integration
- **AdMob**: Google AdMob integration
- **Rewarded Videos**: Gems and items
- **Interstitials**: Between levels
- **Banner Ads**: Optional bottom banner

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Performance Testing
- **FPS Monitoring**: Built-in performance metrics
- **Memory Usage**: Asset manager statistics
- **Battery Usage**: Profile with Android tools

### Device Testing
- **Target Devices**: Android 7.0+ (API 24+)
- **Screen Sizes**: 5" to 7" tablets and phones
- **Performance**: 30+ FPS on mid-range devices

## 📊 Analytics and Metrics

### Player Engagement
- **Session Length**: Average play time
- **Retention**: Day 1, 7, 30 retention rates
- **Progression**: Stage completion rates
- **Currency**: Gold/gem earning and spending

### Monetization
- **ARPU**: Average revenue per user
- **Conversion**: Free to paid conversion rates
- **LTV**: Lifetime value calculations
- **Ad Performance**: CTR and completion rates

## 🚢 Deployment

### Build Process
1. **Asset Optimization**: Compress all assets
2. **Code Minification**: Remove debug code
3. **Testing**: Full regression testing
4. **Signing**: Sign APK with release key
5. **Upload**: Google Play Console

### Release Checklist
- [ ] All placeholder assets replaced
- [ ] Ad network IDs updated
- [ ] Analytics tracking enabled
- [ ] Privacy policy included
- [ ] Store listing prepared
- [ ] Screenshots and videos ready

## 📄 License

This project is proprietary. All rights reserved.

## 🤝 Contributing

This is a closed-source project. For bug reports or feature requests, please contact the development team.

## 📞 Support

For technical support or business inquiries:
- Email: support@kingdomofaldoria.com
- Website: https://www.kingdomofaldoria.com

---

**Kingdom of Aldoria** - Embark on an epic fantasy adventure! ⚔️✨
