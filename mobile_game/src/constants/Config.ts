import {Dimensions} from 'react-native';

const {width: SCREEN_WIDTH, height: SCREEN_HEIGHT} = Dimensions.get('window');

// Game Configuration
export const GAME_CONFIG = {
  VERSION: '1.0.0',
  TITLE: 'Kingdom of Aldoria',
  
  // Display Settings
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  FPS: 60,
  
  // Game Mechanics
  PLAYER_START_LEVEL: 1,
  PLAYER_START_HP: 100,
  PLAYER_START_GOLD: 1000,
  PLAYER_START_GEMS: 50,
  
  // Weapon System
  WEAPON_MAX_LEVEL: 120,
  WEAPON_LEVEL_COST_BASE: 100,
  WEAPON_ETHER_COST: 5,
  
  // Battle System
  BATTLE_TURN_DURATION: 30000, // 30 seconds
  SKILL_COOLDOWN: 3000, // 3 seconds
  
  // Mobile Specific
  TOUCH_FEEDBACK_DURATION: 100,
  HAPTIC_ENABLED: true,
  LANDSCAPE_ONLY: true,
  KEEP_SCREEN_AWAKE: true,
};

// Color Palette
export const COLORS = {
  // Primary Colors
  PRIMARY: '#FFD700',        // Gold
  SECONDARY: '#87CEEB',      // Sky Blue
  ACCENT: '#FF6B6B',         // Coral Red
  SUCCESS: '#90EE90',        // Light Green
  WARNING: '#FFA500',        // Orange
  ERROR: '#DC143C',          // Crimson
  
  // Backgrounds
  BACKGROUND_DARK: '#1a1a2e',
  BACKGROUND_MEDIUM: '#16213e',
  BACKGROUND_LIGHT: '#0f3460',
  
  // UI Elements
  UI_BACKGROUND: 'rgba(20, 25, 40, 0.9)',
  UI_PANEL: 'rgba(255,255,255,0.1)',
  UI_BUTTON: '#4169E1',
  UI_BUTTON_HOVER: '#6495ED',
  UI_BORDER: '#FFD700',
  
  // Text Colors
  TEXT_PRIMARY: '#FFFFFF',
  TEXT_SECONDARY: '#E0E0E0',
  TEXT_ACCENT: '#FFD700',
  TEXT_SUCCESS: '#90EE90',
  TEXT_ERROR: '#FF6B6B',
  
  // Weapon Ranks
  WOOD: '#8B4513',
  IRON: '#708090',
  SILVER: '#C0C0C0',
  GOLD: '#FFD700',
  PLATINUM: '#E5E4E2',
  EMERALD: '#50C878',
  DIAMOND: '#B9F2FF',
  ELITE: '#9400D3',
  HYPER: '#FF1493',
  LEGENDARY: '#FF4500',
  
  // Transparent Overlays
  OVERLAY_DARK: 'rgba(0,0,0,0.7)',
  OVERLAY_LIGHT: 'rgba(255,255,255,0.1)',
  OVERLAY_SUCCESS: 'rgba(34, 139, 34, 0.3)',
  OVERLAY_ERROR: 'rgba(220, 20, 60, 0.3)',
};

// Typography
export const TYPOGRAPHY = {
  FONT_FAMILY_REGULAR: 'System',
  FONT_FAMILY_BOLD: 'System',
  FONT_FAMILY_MONO: 'monospace',
  
  // Font Sizes (Mobile Optimized)
  FONT_SIZE_TINY: 10,
  FONT_SIZE_SMALL: 12,
  FONT_SIZE_MEDIUM: 16,
  FONT_SIZE_LARGE: 20,
  FONT_SIZE_XLARGE: 24,
  FONT_SIZE_TITLE: 32,
  FONT_SIZE_HERO: 40,
};

// Spacing
export const SPACING = {
  TINY: 4,
  SMALL: 8,
  MEDIUM: 16,
  LARGE: 24,
  XLARGE: 32,
  XXLARGE: 48,
};

// Game Data
export const WEAPONS_DATA = [
  {
    id: 'wooden_sword',
    name: 'Wooden Sword',
    rank: 'Wood',
    price: 100,
    level: 1,
    maxLevel: 120,
    color: COLORS.WOOD,
    attack: 10,
    description: 'A basic training sword made of sturdy oak.',
  },
  {
    id: 'iron_blade',
    name: 'Iron Blade',
    rank: 'Iron',
    price: 500,
    level: 1,
    maxLevel: 120,
    color: COLORS.IRON,
    attack: 25,
    description: 'A reliable iron sword for seasoned warriors.',
  },
  {
    id: 'silver_edge',
    name: 'Silver Edge',
    rank: 'Silver',
    price: 1000,
    level: 1,
    maxLevel: 120,
    color: COLORS.SILVER,
    attack: 50,
    description: 'Blessed silver blade that gleams in moonlight.',
  },
  {
    id: 'golden_destroyer',
    name: 'Golden Destroyer',
    rank: 'Gold',
    price: 2500,
    level: 1,
    maxLevel: 120,
    color: COLORS.GOLD,
    attack: 100,
    description: 'Forged from pure gold with devastating power.',
  },
  {
    id: 'platinum_slayer',
    name: 'Platinum Slayer',
    rank: 'Platinum',
    price: 5000,
    level: 1,
    maxLevel: 120,
    color: COLORS.PLATINUM,
    attack: 200,
    description: 'Ultra-rare platinum weapon of legends.',
  },
  {
    id: 'emerald_fury',
    name: 'Emerald Fury',
    rank: 'Emerald',
    price: 10000,
    level: 1,
    maxLevel: 120,
    color: COLORS.EMERALD,
    attack: 400,
    description: 'Infused with emerald magic and nature\'s wrath.',
  },
  {
    id: 'diamond_edge',
    name: 'Diamond Edge',
    rank: 'Diamond',
    price: 25000,
    level: 1,
    maxLevel: 120,
    color: COLORS.DIAMOND,
    attack: 800,
    description: 'Crystalline perfection that cuts through reality.',
  },
  {
    id: 'elite_devastator',
    name: 'Elite Devastator',
    rank: 'Elite',
    price: 50000,
    level: 1,
    maxLevel: 120,
    color: COLORS.ELITE,
    attack: 1600,
    description: 'Reserved for the elite warriors of the kingdom.',
  },
  {
    id: 'hyper_annihilator',
    name: 'Hyper Annihilator',
    rank: 'Hyper',
    price: 100000,
    level: 1,
    maxLevel: 120,
    color: COLORS.HYPER,
    attack: 3200,
    description: 'Transcends mortal understanding of power.',
  },
  {
    id: 'legendary_worldbreaker',
    name: 'Legendary Worldbreaker',
    rank: 'Legendary',
    price: 250000,
    level: 1,
    maxLevel: 120,
    color: COLORS.LEGENDARY,
    attack: 6400,
    description: 'The ultimate weapon capable of shattering worlds.',
  },
];

export const HEROES_DATA = [
  {
    id: 'pyromancer',
    name: 'Pyromancer',
    ability: 'Fireburst',
    price: 5000,
    description: 'Master of flame magic who burns enemies to ash.',
    color: COLORS.ERROR,
    element: 'Fire',
    hp: 120,
    attack: 80,
    defense: 60,
  },
  {
    id: 'void_assassin',
    name: 'Void Assassin',
    ability: 'Shadow Strike',
    price: 7500,
    description: 'Teleports through shadows to deliver critical strikes.',
    color: COLORS.ELITE,
    element: 'Void',
    hp: 100,
    attack: 120,
    defense: 40,
  },
  {
    id: 'ice_warden',
    name: 'Ice Warden',
    ability: 'Frost Prison',
    price: 6000,
    description: 'Freezes enemies solid with arctic magic.',
    color: COLORS.SECONDARY,
    element: 'Ice',
    hp: 140,
    attack: 70,
    defense: 90,
  },
  {
    id: 'storm_caller',
    name: 'Storm Caller',
    ability: 'Lightning Bolt',
    price: 8000,
    description: 'Commands the fury of storms and thunder.',
    color: COLORS.PRIMARY,
    element: 'Lightning',
    hp: 110,
    attack: 100,
    defense: 70,
  },
  {
    id: 'earth_guardian',
    name: 'Earth Guardian',
    ability: 'Stone Shield',
    price: 5500,
    description: 'Protects allies with the strength of mountains.',
    color: COLORS.WOOD,
    element: 'Earth',
    hp: 160,
    attack: 60,
    defense: 120,
  },
];

export const WORLD_REGIONS = [
  {
    id: 'royal_castle',
    name: '🏰 Royal Castle',
    description: 'The heart of the kingdom where your journey begins.',
    unlocked: true,
    stages: 10,
    difficulty: 1,
    rewards: ['gold', 'experience'],
  },
  {
    id: 'mystic_forest',
    name: '🌲 Mystic Forest',
    description: 'Ancient woods filled with magical creatures.',
    unlocked: true,
    stages: 15,
    difficulty: 2,
    rewards: ['gems', 'weapons'],
  },
  {
    id: 'ice_peaks',
    name: '🏔️ Ice Peaks',
    description: 'Frozen mountains where ice elementals dwell.',
    unlocked: true,
    stages: 20,
    difficulty: 3,
    rewards: ['rare_items', 'heroes'],
  },
  {
    id: 'desert_souls',
    name: '🏜️ Desert of Souls',
    description: 'Scorching sands haunted by ancient spirits.',
    unlocked: false,
    stages: 25,
    difficulty: 4,
    rewards: ['legendary_weapons', 'elite_gems'],
  },
  {
    id: 'volcanic_realm',
    name: '🌋 Volcanic Realm',
    description: 'Molten depths where fire demons rule.',
    unlocked: false,
    stages: 30,
    difficulty: 5,
    rewards: ['hyper_weapons', 'premium_heroes'],
  },
  {
    id: 'abyssal_trench',
    name: '🌊 Abyssal Trench',
    description: 'Deepest underwater realm of ultimate challenges.',
    unlocked: false,
    stages: 50,
    difficulty: 6,
    rewards: ['legendary_heroes', 'worldbreaker_weapons'],
  },
];

// Mobile Specific Settings
export const MOBILE_CONFIG = {
  // Touch Controls
  TOUCH_AREA_SIZE: 80,
  BUTTON_MIN_SIZE: 44, // iOS Human Interface Guidelines
  GESTURE_SENSITIVITY: 1.0,
  
  // Performance
  ANIMATION_DURATION: 300,
  FRAME_SKIP_THRESHOLD: 16.67, // 60 FPS target
  
  // Storage
  MAX_SAVE_SLOTS: 3,
  AUTO_SAVE_INTERVAL: 30000, // 30 seconds
  
  // Notifications
  ENABLE_PUSH_NOTIFICATIONS: true,
  DAILY_REMINDER_TIME: '09:00',
  
  // Haptic Feedback
  HAPTIC_LIGHT: 'impactLight',
  HAPTIC_MEDIUM: 'impactMedium',
  HAPTIC_HEAVY: 'impactHeavy',
};