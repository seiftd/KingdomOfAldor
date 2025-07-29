import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:wakelock/wakelock.dart';
import 'package:google_fonts/google_fonts.dart';

// Core
import 'core/app_config.dart';
import 'core/theme.dart';
import 'core/routes.dart';

// Services
import 'services/audio_service.dart';
import 'services/save_service.dart';
import 'services/haptic_service.dart';

// Providers
import 'providers/game_state_provider.dart';
import 'providers/player_provider.dart';

// Screens
import 'screens/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive for local storage
  await Hive.initFlutter();
  await Hive.openBox('gameData');
  await Hive.openBox('settings');
  
  // Lock orientation to landscape for gaming
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  
  // Hide status bar for immersive gaming
  await SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: Colors.transparent,
    ),
  );
  
  // Keep screen awake during gameplay
  await Wakelock.enable();
  
  // Initialize services
  await AudioService.instance.initialize();
  await SaveService.instance.initialize();
  await HapticService.instance.initialize();
  
  runApp(const ProviderScope(child: KingdomOfAldoriaApp()));
}

class KingdomOfAldoriaApp extends ConsumerWidget {
  const KingdomOfAldoriaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ScreenUtilInit(
      designSize: const Size(1280, 720), // Game design resolution
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return MaterialApp(
          title: AppConfig.appName,
          debugShowCheckedModeBanner: false,
          theme: AppTheme.gameTheme,
          onGenerateRoute: AppRoutes.generateRoute,
          initialRoute: '/',
          home: const SplashScreen(),
          builder: (context, widget) {
            return MediaQuery(
              // Ensure text doesn't scale beyond reasonable limits
              data: MediaQuery.of(context).copyWith(textScaleFactor: 1.0),
              child: widget!,
            );
          },
        );
      },
    );
  }
}

class GameApp extends ConsumerStatefulWidget {
  const GameApp({Key? key}) : super(key: key);

  @override
  ConsumerState<GameApp> createState() => _GameAppState();
}

class _GameAppState extends ConsumerState<GameApp> 
    with WidgetsBindingObserver {
  
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _initializeGame();
  }
  
  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _cleanupGame();
    super.dispose();
  }
  
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    
    switch (state) {
      case AppLifecycleState.paused:
        _pauseGame();
        break;
      case AppLifecycleState.resumed:
        _resumeGame();
        break;
      case AppLifecycleState.detached:
        _saveGameState();
        break;
      default:
        break;
    }
  }
  
  Future<void> _initializeGame() async {
    try {
      // Load game data
      await ref.read(saveServiceProvider).loadGameData();
      
      // Initialize player data
      await ref.read(playerProvider.notifier).loadPlayerData();
      
      // Start background music
      await AudioService.instance.playBackgroundMusic('main_theme');
      
      // Set game as initialized
      ref.read(gameStateProvider.notifier).setInitialized(true);
      
      debugPrint('🏰 Kingdom of Aldoria Flutter initialized successfully!');
    } catch (e) {
      debugPrint('❌ Failed to initialize game: $e');
    }
  }
  
  void _pauseGame() {
    AudioService.instance.pauseBackgroundMusic();
    ref.read(gameStateProvider.notifier).pauseGame();
    _saveGameState();
  }
  
  void _resumeGame() {
    AudioService.instance.resumeBackgroundMusic();
    ref.read(gameStateProvider.notifier).resumeGame();
  }
  
  Future<void> _saveGameState() async {
    await SaveService.instance.saveGameData();
    debugPrint('💾 Game state saved');
  }
  
  Future<void> _cleanupGame() async {
    await AudioService.instance.dispose();
    await Wakelock.disable();
    await SaveService.instance.saveGameData();
  }

  @override
  Widget build(BuildContext context) {
    final gameState = ref.watch(gameStateProvider);
    
    return Scaffold(
      backgroundColor: AppTheme.backgroundDark,
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppTheme.backgroundDark,
              AppTheme.backgroundMedium,
              AppTheme.backgroundLight,
            ],
          ),
        ),
        child: SafeArea(
          child: _buildGameContent(gameState),
        ),
      ),
    );
  }
  
  Widget _buildGameContent(GameState gameState) {
    if (!gameState.isInitialized) {
      return const SplashScreen();
    }
    
    return Stack(
      children: [
        // Main game content
        AppRoutes.getScreenWidget(gameState.currentScreen),
        
        // Game overlay UI
        Positioned(
          top: 16.h,
          right: 16.w,
          child: _buildGameStatus(gameState),
        ),
        
        // Debug info (only in debug mode)
        if (AppConfig.isDebugMode)
          Positioned(
            bottom: 16.h,
            left: 16.w,
            child: _buildDebugInfo(),
          ),
      ],
    );
  }
  
  Widget _buildGameStatus(GameState gameState) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12.w, vertical: 6.h),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.7),
        borderRadius: BorderRadius.circular(8.r),
        border: Border.all(color: AppTheme.goldColor, width: 1),
      ),
      child: Text(
        '🎮 ${gameState.currentScreen.name.toUpperCase()}',
        style: GoogleFonts.orbitron(
          fontSize: 12.sp,
          color: AppTheme.successColor,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
  
  Widget _buildDebugInfo() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 4.h),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.5),
        borderRadius: BorderRadius.circular(4.r),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Flutter ${AppConfig.version}',
            style: TextStyle(
              fontSize: 10.sp,
              color: AppTheme.accentColor,
              fontFamily: 'monospace',
            ),
          ),
          Text(
            'FPS: 60 | Screen: ${1.sw.toInt()}x${1.sh.toInt()}',
            style: TextStyle(
              fontSize: 10.sp,
              color: AppTheme.accentColor,
              fontFamily: 'monospace',
            ),
          ),
        ],
      ),
    );
  }
}