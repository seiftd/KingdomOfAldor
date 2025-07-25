# Kingdom of Aldoria 🏰⚔️

A complete 2D mobile RPG game built with Python and Pygame featuring 10 fantasy worlds, 300 stages, character customization, and monetization systems.

## 🎮 Game Features

### Core Gameplay
- **10 Fantasy Worlds**: Forest of Shadows, Desert of Souls, Ice Peaks, Dark Kingdom, Light Fortress, and more
- **300 Stages**: 30 stages per world with progressive difficulty
- **Boss Battles**: Epic fights every 5 stages that scale with player power
- **Hero Character**: Knight Arin with customizable appearances

### Game Systems
- **Stamina System**: 1 stamina per stage, 20-min recharge, max 10 stamina
- **Dual Currency**: Gold (earned) and Gems (premium)
- **Player Progression**: Leveling system with stat increases
- **Real-time Combat**: Turn-based mechanics with strategy

### Character Customization
- **Unique Skins** with special abilities:
  - Speed Boost (5s duration)
  - Instant Heal (30% HP recovery)
  - Time Rewind (damage reversal)
  - Damage Doubler (7s power boost)
- **Weapons**: Different attack values and visual effects
- **Visual Upgrades**: Enhance appearance and stats

### Monetization
- **Subscriptions**: Weekly ($5) and Monthly ($16) with premium benefits
- **In-App Purchases**: Starter packs ($1) to Legendary items ($14.99)
- **Ad System**: Rewarded ads for gems, interstitials, and revive options

## 🛠️ Technical Specifications

### Requirements
- Python 3.10+
- Pygame 2.5+
- HD Resolution: 1280x720 with scaling
- File Size: Under 2GB

### Asset Optimization
- **Images**: WebP format for compression
- **Audio**: Ogg Vorbis for quality/size balance
- **Dynamic Loading**: Efficient memory management

## 🚀 Installation & Setup

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

## 📱 Android Build Instructions

### Prerequisites
- Android SDK
- Buildozer
- ADB for testing

### Build Steps
1. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

2. **Initialize build**:
   ```bash
   buildozer android debug
   ```

3. **Deploy to device**:
   ```bash
   buildozer android deploy run
   ```

## 🎨 Asset Generation

All game assets are AI-generated using consistent fantasy art style:

### Character Sprites
- Forest Scout (ranger with bow)
- Desert Nomad (warrior with scimitar)
- Void Knight (cosmic dark armor)

### Enemies
- Shadow Wolf (spectral with glowing eyes)
- Sand Pharaoh (mummy with golden artifacts)
- Ice Yeti (frost-covered giant)

### Weapons
- Bronze Sword (simple metal blade)
- Void Scythe (cosmic purple energy)
- Solar Flare Sword (golden fire weapon)

## 🏗️ Architecture

### Core Systems
- **Game Loop**: State machine with multiple screens
- **Player System**: Stats, inventory, skill management
- **Combat System**: Turn-based with real-time elements
- **World Manager**: Stage progression and difficulty scaling
- **Ad Manager**: Reward tracking and ad placement

### Class Structure
```
src/
├── core/
│   ├── game.py          # Main game loop
│   ├── state_manager.py # Game state handling
│   └── config.py        # Game configuration
├── systems/
│   ├── player.py        # Player management
│   ├── combat.py        # Battle system
│   ├── stamina.py       # Stamina mechanics
│   ├── currency.py      # Gold/Gems system
│   └── ads.py           # Advertisement system
├── ui/
│   ├── main_menu.py     # Main menu interface
│   ├── battle_ui.py     # Combat interface
│   ├── shop.py          # Store system
│   └── world_map.py     # World selection
├── entities/
│   ├── player.py        # Player character
│   ├── enemy.py         # Enemy entities
│   └── skills.py        # Skill system
└── world/
    ├── world_manager.py # World progression
    ├── stage.py         # Individual stages
    └── boss.py          # Boss battles
```

## 🔧 Testing & Development

### ADB Testing Configuration
```bash
# Enable developer options on Android device
adb devices
adb install -r bin/KingdomOfAldoria-debug.apk
adb logcat | grep pygame
```

### Debug Mode
Set `DEBUG = True` in `src/core/config.py` for:
- Console logging
- FPS display
- Debug UI overlays
- Skip monetization checks

## 🌍 Localization

Supported languages:
- English (default)
- Arabic
- French

Language files located in `assets/localization/`

## 💾 Save System

- Local save files
- Cloud save integration points
- Automatic backup system
- Cross-device synchronization support

## 🎯 Performance Optimization

- **Texture Atlases**: Sprite batching for efficiency
- **Object Pooling**: Reuse enemies and projectiles
- **Background Loading**: Async asset loading
- **Memory Management**: Mobile-optimized cleanup

## 📊 Economy Balance

### Currency Rates
- **Gold**: Base currency for upgrades
- **Gems**: Premium currency (1 gem = $0.05 USD equivalent)
- **Conversion**: 100 gold = 1 gem (emergency only)

### Progression Balance
- **Linear XP Growth**: Level * 100 base XP required
- **Stat Scaling**: +5% per level across all stats
- **Difficulty Curve**: Enemy power scales at 110% per stage

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🎖️ Credits

- **Game Design**: Kingdom of Aldoria Team
- **Art Assets**: AI-generated with custom prompts
- **Audio**: Royalty-free fantasy music and SFX
- **Engine**: Built with Pygame

---

*Embark on an epic journey through the Kingdom of Aldoria!* ⚔️🏰
