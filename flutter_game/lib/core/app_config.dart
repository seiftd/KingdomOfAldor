import 'package:flutter/foundation.dart';

class AppConfig {
  // App Information
  static const String appName = 'Kingdom of Aldoria';
  static const String version = '1.0.0';
  static const String description = 'Epic 2D Mobile RPG Adventure - Flutter Edition';
  
  // Debug Settings
  static const bool isDebugMode = kDebugMode;
  static const bool enableLogging = true;
  static const bool enablePerformanceMonitoring = true;
  
  // Game Configuration
  static const double gameWidth = 1280.0;
  static const double gameHeight = 720.0;
  static const int targetFPS = 60;
  
  // Player Starting Values
  static const int startingLevel = 1;
  static const int startingHP = 100;
  static const int startingGold = 1000;
  static const int startingGems = 50;
  static const String startingWeapon = 'Bronze Sword';
  
  // Game Mechanics
  static const int maxWeaponLevel = 120;
  static const int weaponUpgradeCostBase = 100;
  static const int etherCostPerUpgrade = 5;
  static const int battleTurnDuration = 30; // seconds
  static const int skillCooldownDuration = 3; // seconds
  
  // Mobile Specific
  static const int hapticFeedbackDuration = 100; // milliseconds
  static const bool enableHaptics = true;
  static const bool landscapeOnly = true;
  static const bool keepScreenAwake = true;
  static const int autoSaveInterval = 30; // seconds
  
  // Audio Settings
  static const double defaultMusicVolume = 0.7;
  static const double defaultSFXVolume = 0.8;
  static const bool enableBackgroundMusic = true;
  static const bool enableSoundEffects = true;
  
  // Animation Settings
  static const int defaultAnimationDuration = 300; // milliseconds
  static const int fastAnimationDuration = 150; // milliseconds
  static const int slowAnimationDuration = 600; // milliseconds
  
  // UI Settings
  static const double buttonMinSize = 44.0; // iOS guidelines
  static const double touchAreaSize = 80.0;
  static const double borderRadius = 12.0;
  static const double cardElevation = 8.0;
  
  // Performance Settings
  static const int maxParticles = 100;
  static const bool enableParticleEffects = true;
  static const bool enableShadows = true;
  static const bool enableBlur = true;
  
  // Storage Settings
  static const String gameDataBoxName = 'gameData';
  static const String settingsBoxName = 'settings';
  static const String playerDataKey = 'playerData';
  static const String gameStateKey = 'gameState';
  static const String settingsKey = 'settings';
  
  // Platform Features
  static const bool enableNotifications = true;
  static const String dailyReminderTime = '09:00';
  static const bool enableAnalytics = false; // Privacy focused
  
  // Game Content
  static const int totalWeaponRanks = 10;
  static const int totalHeroes = 5;
  static const int totalWorldRegions = 6;
  static const int maxInventorySlots = 50;
  
  // Monetization (Future)
  static const bool enableInAppPurchases = false;
  static const bool enableAds = false;
  static const bool enablePremiumFeatures = false;
  
  // Network (Future)
  static const bool enableOnlineFeatures = false;
  static const bool enableLeaderboards = false;
  static const bool enableMultiplayer = false;
  
  // Security
  static const bool enableDataEncryption = true;
  static const bool enableAntiCheat = true;
  static const bool validateGameData = true;
  
  // Accessibility
  static const bool enableColorblindSupport = true;
  static const bool enableTextScaling = true;
  static const bool enableHighContrast = false;
  
  // Development
  static const bool enableDevConsole = kDebugMode;
  static const bool enableCheatCodes = kDebugMode;
  static const bool showFPSCounter = kDebugMode;
  static const bool logPlayerActions = kDebugMode;
  
  // Error Handling
  static const bool enableCrashReporting = !kDebugMode;
  static const bool enableErrorDialogs = kDebugMode;
  static const int maxErrorLogs = 100;
  
  // Cache Settings
  static const int maxCacheSize = 100; // MB
  static const int cacheExpirationDays = 7;
  static const bool enableImageCaching = true;
  static const bool enableAudioCaching = true;
  
  // Validation
  static bool get isValidConfiguration {
    return gameWidth > 0 &&
           gameHeight > 0 &&
           targetFPS > 0 &&
           startingGold >= 0 &&
           startingGems >= 0 &&
           maxWeaponLevel > 0;
  }
  
  // Environment Detection
  static bool get isProduction => !kDebugMode;
  static bool get isDevelopment => kDebugMode;
  
  // Feature Flags
  static bool get showDebugInfo => kDebugMode && enableLogging;
  static bool get enableAdvancedFeatures => isProduction;
  static bool get enableExperimentalFeatures => kDebugMode;
  
  // Game Balance
  static double getWeaponPriceMultiplier(int rank) {
    return [1.0, 5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0][rank.clamp(0, 9)];
  }
  
  static int getRegionDifficulty(int regionIndex) {
    return [1, 2, 3, 4, 5, 6][regionIndex.clamp(0, 5)];
  }
  
  static int getRegionStageCount(int regionIndex) {
    return [10, 15, 20, 25, 30, 50][regionIndex.clamp(0, 5)];
  }
  
  // Utility Methods
  static String getFormattedVersion() => 'v$version';
  
  static String getAppTitle() => '$appName ${getFormattedVersion()}';
  
  static Duration get animationDuration => Duration(milliseconds: defaultAnimationDuration);
  
  static Duration get fastAnimation => Duration(milliseconds: fastAnimationDuration);
  
  static Duration get slowAnimation => Duration(milliseconds: slowAnimationDuration);
  
  static Duration get autoSave => Duration(seconds: autoSaveInterval);
  
  // Debug Methods
  static void logConfig() {
    if (!kDebugMode) return;
    
    print('🏰 Kingdom of Aldoria Configuration:');
    print('   App: $appName v$version');
    print('   Resolution: ${gameWidth}x$gameHeight');
    print('   Target FPS: $targetFPS');
    print('   Debug Mode: $isDebugMode');
    print('   Features: Haptics($enableHaptics), Audio($enableBackgroundMusic)');
    print('   Performance: Particles($enableParticleEffects), Shadows($enableShadows)');
  }
  
  static Map<String, dynamic> toJson() {
    return {
      'appName': appName,
      'version': version,
      'gameResolution': '${gameWidth}x$gameHeight',
      'targetFPS': targetFPS,
      'isDebugMode': isDebugMode,
      'enableHaptics': enableHaptics,
      'enableAudio': enableBackgroundMusic,
      'autoSaveInterval': autoSaveInterval,
    };
  }
}