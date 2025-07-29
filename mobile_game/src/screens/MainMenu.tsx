import React, {useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import HapticFeedback from 'react-native-haptic-feedback';

import {GameStates} from '../constants/GameStates';
import {COLORS, TYPOGRAPHY, SPACING, GAME_CONFIG} from '../constants/Config';
import {AnimatedBackground} from '../components/AnimatedBackground';
import {GameButton} from '../components/GameButton';

const {width: SCREEN_WIDTH, height: SCREEN_HEIGHT} = Dimensions.get('window');

interface MainMenuProps {
  gameData: any;
  onStateChange: (state: GameStates, data?: any) => void;
  audioManager?: any;
  saveManager?: any;
}

const MainMenu: React.FC<MainMenuProps> = ({
  gameData,
  onStateChange,
  audioManager,
  saveManager,
}) => {
  const titleAnimation = new Animated.Value(0);
  const buttonsAnimation = new Animated.Value(0);

  useEffect(() => {
    startAnimations();
    playBackgroundMusic();
  }, []);

  const startAnimations = () => {
    // Animated title entrance
    Animated.sequence([
      Animated.timing(titleAnimation, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.timing(buttonsAnimation, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const playBackgroundMusic = () => {
    audioManager?.playMusic('main_menu_theme', true);
  };

  const handleMenuAction = (action: string, state: GameStates) => {
    // Haptic feedback for touch
    HapticFeedback.trigger('impactMedium');
    
    // Audio feedback
    audioManager?.playSound('button_click');
    
    // State change
    onStateChange(state);
  };

  const titleTransform = {
    opacity: titleAnimation,
    transform: [
      {
        translateY: titleAnimation.interpolate({
          inputRange: [0, 1],
          outputRange: [-50, 0],
        }),
      },
      {
        scale: titleAnimation.interpolate({
          inputRange: [0, 1],
          outputRange: [0.8, 1],
        }),
      },
    ],
  };

  const buttonsTransform = {
    opacity: buttonsAnimation,
    transform: [
      {
        translateY: buttonsAnimation.interpolate({
          inputRange: [0, 1],
          outputRange: [100, 0],
        }),
      },
    ],
  };

  return (
    <View style={styles.container}>
      {/* Animated Background */}
      <AnimatedBackground />
      
      {/* Main Content */}
      <View style={styles.content}>
        {/* Game Title */}
        <Animated.View style={[styles.titleContainer, titleTransform]}>
          <Text style={styles.titleEmoji}>🏰</Text>
          <Text style={styles.title}>KINGDOM</Text>
          <Text style={styles.title}>OF ALDORIA</Text>
          <Text style={styles.titleEmoji}>👑</Text>
          <Text style={styles.subtitle}>Epic 2D Mobile RPG Adventure</Text>
        </Animated.View>

        {/* Menu Buttons */}
        <Animated.View style={[styles.menuContainer, buttonsTransform]}>
          <GameButton
            title="🗺️ EXPLORE WORLD"
            onPress={() => handleMenuAction('explore', GameStates.WORLD_MAP)}
            style={[styles.menuButton, {backgroundColor: COLORS.SUCCESS}]}
            textStyle={styles.menuButtonText}
          />
          
          <GameButton
            title="🛒 SHOP & INVENTORY"
            onPress={() => handleMenuAction('shop', GameStates.SHOP)}
            style={[styles.menuButton, {backgroundColor: COLORS.UI_BUTTON}]}
            textStyle={styles.menuButtonText}
          />
          
          <GameButton
            title="⚔️ BATTLE ARENA"
            onPress={() => handleMenuAction('battle', GameStates.BATTLE)}
            style={[styles.menuButton, {backgroundColor: COLORS.ERROR}]}
            textStyle={styles.menuButtonText}
          />
          
          <GameButton
            title="⚙️ SETTINGS"
            onPress={() => handleMenuAction('settings', GameStates.SETTINGS)}
            style={[styles.menuButton, styles.settingsButton]}
            textStyle={styles.menuButtonText}
          />
        </Animated.View>

        {/* Player Info */}
        <View style={styles.playerInfo}>
          <LinearGradient
            colors={[COLORS.OVERLAY_DARK, 'transparent']}
            style={styles.playerInfoGradient}
          >
            <Text style={styles.playerName}>Hero Arin • Level {gameData?.level || 1}</Text>
            <View style={styles.currencyContainer}>
              <Text style={styles.currency}>💰 {gameData?.gold || 1000}</Text>
              <Text style={styles.currency}>💎 {gameData?.gems || 50}</Text>
            </View>
          </LinearGradient>
        </View>

        {/* Game Status */}
        <View style={styles.statusContainer}>
          <Text style={styles.statusText}>
            ✅ Mobile Game Running Perfectly!
          </Text>
          <Text style={styles.versionText}>
            v{GAME_CONFIG.VERSION} • React Native
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.BACKGROUND_DARK,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: SPACING.LARGE,
  },
  titleContainer: {
    alignItems: 'center',
    marginBottom: SPACING.XXLARGE,
  },
  titleEmoji: {
    fontSize: 60,
    marginBottom: SPACING.SMALL,
  },
  title: {
    fontSize: TYPOGRAPHY.FONT_SIZE_HERO,
    fontWeight: 'bold',
    color: COLORS.PRIMARY,
    textAlign: 'center',
    textShadowColor: COLORS.BACKGROUND_DARK,
    textShadowOffset: {width: 2, height: 2},
    textShadowRadius: 4,
    lineHeight: TYPOGRAPHY.FONT_SIZE_HERO + 5,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_LARGE,
    color: COLORS.SECONDARY,
    textAlign: 'center',
    marginTop: SPACING.MEDIUM,
    fontWeight: '600',
  },
  menuContainer: {
    width: '100%',
    maxWidth: 400,
    gap: SPACING.MEDIUM,
  },
  menuButton: {
    height: 60,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 4},
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  settingsButton: {
    backgroundColor: COLORS.OVERLAY_DARK,
    borderWidth: 2,
    borderColor: COLORS.UI_BORDER,
  },
  menuButtonText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_LARGE,
    fontWeight: 'bold',
    color: COLORS.TEXT_PRIMARY,
    textAlign: 'center',
  },
  playerInfo: {
    position: 'absolute',
    top: SPACING.LARGE,
    left: 0,
    right: 0,
    paddingHorizontal: SPACING.LARGE,
  },
  playerInfoGradient: {
    padding: SPACING.MEDIUM,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  playerName: {
    fontSize: TYPOGRAPHY.FONT_SIZE_MEDIUM,
    fontWeight: 'bold',
    color: COLORS.TEXT_ACCENT,
  },
  currencyContainer: {
    flexDirection: 'row',
    gap: SPACING.MEDIUM,
  },
  currency: {
    fontSize: TYPOGRAPHY.FONT_SIZE_MEDIUM,
    fontWeight: '600',
    color: COLORS.TEXT_PRIMARY,
  },
  statusContainer: {
    position: 'absolute',
    bottom: SPACING.LARGE,
    alignItems: 'center',
  },
  statusText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_MEDIUM,
    fontWeight: 'bold',
    color: COLORS.SUCCESS,
    textAlign: 'center',
  },
  versionText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.TEXT_SECONDARY,
    marginTop: SPACING.SMALL,
    textAlign: 'center',
  },
});

export default MainMenu;