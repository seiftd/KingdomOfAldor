import React, {useEffect, useState} from 'react';
import {
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Dimensions,
  View,
  Text,
} from 'react-native';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import Orientation from 'react-native-orientation-locker';
import KeepAwake from 'react-native-keep-awake';

// Game Components
import GameEngine from './src/components/GameEngine';
import LoadingScreen from './src/components/LoadingScreen';
import MainMenu from './src/screens/MainMenu';
import WorldMap from './src/screens/WorldMap';
import Shop from './src/screens/Shop';
import Battle from './src/screens/Battle';

// Game Systems
import {GameStateManager} from './src/systems/GameStateManager';
import {AudioManager} from './src/systems/AudioManager';
import {SaveManager} from './src/systems/SaveManager';

// Constants and Types
import {GameStates} from './src/constants/GameStates';
import {COLORS, GAME_CONFIG} from './src/constants/Config';

const {width: SCREEN_WIDTH, height: SCREEN_HEIGHT} = Dimensions.get('window');

interface GameState {
  currentState: GameStates;
  isLoading: boolean;
  gameData: any;
}

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    currentState: GameStates.LOADING,
    isLoading: true,
    gameData: null,
  });

  const [gameManagers, setGameManagers] = useState({
    stateManager: null as GameStateManager | null,
    audioManager: null as AudioManager | null,
    saveManager: null as SaveManager | null,
  });

  useEffect(() => {
    initializeGame();
    setupDeviceSettings();
    
    return () => {
      cleanup();
    };
  }, []);

  const setupDeviceSettings = () => {
    // Lock orientation to landscape for better gaming experience
    Orientation.lockToLandscape();
    
    // Keep screen awake during gameplay
    KeepAwake.activate();
    
    // Hide status bar for immersive experience
    StatusBar.setHidden(true);
  };

  const initializeGame = async () => {
    try {
      console.log('🏰 Initializing Kingdom of Aldoria Mobile...');

      // Initialize game managers
      const stateManager = new GameStateManager();
      const audioManager = new AudioManager();
      const saveManager = new SaveManager();

      // Initialize systems
      await audioManager.initialize();
      await saveManager.initialize();

      // Load game data
      const gameData = await saveManager.loadGameData();

      setGameManagers({
        stateManager,
        audioManager,
        saveManager,
      });

      setGameState({
        currentState: GameStates.MAIN_MENU,
        isLoading: false,
        gameData,
      });

      console.log('✅ Kingdom of Aldoria Mobile initialized successfully!');
    } catch (error) {
      console.error('❌ Failed to initialize game:', error);
    }
  };

  const cleanup = () => {
    KeepAwake.deactivate();
    gameManagers.audioManager?.cleanup();
  };

  const changeGameState = (newState: GameStates, data?: any) => {
    console.log(`🎮 Changing game state: ${gameState.currentState} → ${newState}`);
    
    setGameState(prev => ({
      ...prev,
      currentState: newState,
      gameData: data || prev.gameData,
    }));

    gameManagers.stateManager?.changeState(newState);
  };

  const renderCurrentScreen = () => {
    if (gameState.isLoading) {
      return (
        <LoadingScreen
          onLoadingComplete={() => {
            setGameState(prev => ({...prev, isLoading: false}));
          }}
        />
      );
    }

    const commonProps = {
      gameData: gameState.gameData,
      onStateChange: changeGameState,
      audioManager: gameManagers.audioManager,
      saveManager: gameManagers.saveManager,
    };

    switch (gameState.currentState) {
      case GameStates.MAIN_MENU:
        return <MainMenu {...commonProps} />;
        
      case GameStates.WORLD_MAP:
        return <WorldMap {...commonProps} />;
        
      case GameStates.SHOP:
        return <Shop {...commonProps} />;
        
      case GameStates.BATTLE:
        return <Battle {...commonProps} />;
        
      default:
        return <MainMenu {...commonProps} />;
    }
  };

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <StatusBar hidden={true} />
        
        {/* Game Container */}
        <View style={styles.gameContainer}>
          {renderCurrentScreen()}
        </View>

        {/* Game Status Overlay */}
        <View style={styles.statusOverlay}>
          <Text style={styles.statusText}>
            🎮 Kingdom of Aldoria • {gameState.currentState.toUpperCase()}
          </Text>
        </View>

        {/* FPS Counter (Debug) */}
        {__DEV__ && (
          <View style={styles.debugOverlay}>
            <Text style={styles.debugText}>
              📱 {SCREEN_WIDTH}x{SCREEN_HEIGHT} • React Native
            </Text>
          </View>
        )}
      </SafeAreaView>
    </SafeAreaProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.BACKGROUND_DARK,
  },
  gameContainer: {
    flex: 1,
    width: SCREEN_WIDTH,
    height: SCREEN_HEIGHT,
  },
  statusOverlay: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(0,0,0,0.7)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    zIndex: 1000,
  },
  statusText: {
    color: COLORS.SUCCESS,
    fontSize: 12,
    fontWeight: 'bold',
  },
  debugOverlay: {
    position: 'absolute',
    bottom: 10,
    left: 10,
    backgroundColor: 'rgba(0,0,0,0.7)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    zIndex: 1000,
  },
  debugText: {
    color: COLORS.ACCENT,
    fontSize: 10,
    fontFamily: 'monospace',
  },
});

export default App;