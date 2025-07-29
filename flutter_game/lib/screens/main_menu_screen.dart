import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

// Core
import '../core/app_config.dart';
import '../core/theme.dart';

// Widgets
import '../widgets/game_button.dart';
import '../widgets/animated_background.dart';
import '../widgets/player_info_card.dart';

// Providers
import '../providers/game_state_provider.dart';
import '../providers/player_provider.dart';

// Services
import '../services/audio_service.dart';
import '../services/haptic_service.dart';

// Models
import '../models/game_screen.dart';

class MainMenuScreen extends ConsumerStatefulWidget {
  const MainMenuScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<MainMenuScreen> createState() => _MainMenuScreenState();
}

class _MainMenuScreenState extends ConsumerState<MainMenuScreen>
    with TickerProviderStateMixin {
  
  late AnimationController _titleController;
  late AnimationController _buttonsController;
  late AnimationController _particlesController;
  
  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _playBackgroundMusic();
  }
  
  @override
  void dispose() {
    _titleController.dispose();
    _buttonsController.dispose();
    _particlesController.dispose();
    super.dispose();
  }
  
  void _initializeAnimations() {
    _titleController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    
    _buttonsController = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    );
    
    _particlesController = AnimationController(
      duration: const Duration(seconds: 20),
      vsync: this,
    )..repeat();
    
    // Start animations with delay
    Future.delayed(const Duration(milliseconds: 300), () {
      _titleController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 800), () {
      _buttonsController.forward();
    });
  }
  
  void _playBackgroundMusic() {
    AudioService.instance.playBackgroundMusic('main_menu_theme');
  }
  
  void _handleMenuAction(GameScreen screen) {
    // Haptic feedback
    HapticService.instance.lightImpact();
    
    // Audio feedback
    AudioService.instance.playSound('button_click');
    
    // Navigate to screen
    ref.read(gameStateProvider.notifier).changeScreen(screen);
  }

  @override
  Widget build(BuildContext context) {
    final player = ref.watch(playerProvider);
    
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
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
        child: Stack(
          children: [
            // Animated Background
            const AnimatedBackground(),
            
            // Main Content
            SafeArea(
              child: Padding(
                padding: EdgeInsets.all(24.w),
                child: Column(
                  children: [
                    // Player Info Card
                    PlayerInfoCard(player: player)
                        .animate()
                        .slideY(begin: -1, duration: 800.ms)
                        .fadeIn(duration: 600.ms),
                    
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          // Game Title
                          _buildGameTitle(),
                          
                          SizedBox(height: 60.h),
                          
                          // Menu Buttons
                          _buildMenuButtons(),
                        ],
                      ),
                    ),
                    
                    // Game Status
                    _buildGameStatus(),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildGameTitle() {
    return Column(
      children: [
        // Castle Emoji
        Text(
          '🏰',
          style: TextStyle(fontSize: 80.sp),
        ).animate()
          .scale(begin: const Offset(0.5, 0.5), duration: 1000.ms)
          .then()
          .shake(duration: 500.ms),
        
        SizedBox(height: 20.h),
        
        // Main Title
        AnimatedTextKit(
          animatedTexts: [
            TyperAnimatedText(
              'KINGDOM OF ALDORIA',
              textStyle: GoogleFonts.cinzel(
                fontSize: 48.sp,
                fontWeight: FontWeight.bold,
                color: AppTheme.goldColor,
                shadows: [
                  Shadow(
                    color: AppTheme.goldColor.withOpacity(0.5),
                    blurRadius: 20,
                    offset: const Offset(0, 0),
                  ),
                ],
              ),
              speed: const Duration(milliseconds: 100),
            ),
          ],
          totalRepeatCount: 1,
        ),
        
        SizedBox(height: 16.h),
        
        // Crown Emoji
        Text(
          '👑',
          style: TextStyle(fontSize: 60.sp),
        ).animate()
          .scale(begin: const Offset(0.3, 0.3), duration: 800.ms, delay: 1500.ms)
          .then()
          .shimmer(duration: 2000.ms),
        
        SizedBox(height: 20.h),
        
        // Subtitle
        Text(
          'Epic 2D Mobile RPG Adventure',
          style: GoogleFonts.orbitron(
            fontSize: 20.sp,
            color: AppTheme.skyBlueColor,
            fontWeight: FontWeight.w600,
          ),
        ).animate()
          .fadeIn(duration: 800.ms, delay: 2000.ms)
          .slideY(begin: 0.5, duration: 600.ms),
      ],
    );
  }
  
  Widget _buildMenuButtons() {
    final buttons = [
      {
        'title': '🗺️ EXPLORE WORLD',
        'color': AppTheme.successColor,
        'screen': GameScreen.worldMap,
      },
      {
        'title': '🛒 SHOP & INVENTORY',
        'color': AppTheme.primaryBlue,
        'screen': GameScreen.shop,
      },
      {
        'title': '⚔️ BATTLE ARENA',
        'color': AppTheme.errorColor,
        'screen': GameScreen.battle,
      },
      {
        'title': '⚙️ SETTINGS',
        'color': AppTheme.neutralGray,
        'screen': GameScreen.settings,
      },
    ];
    
    return Column(
      children: buttons.asMap().entries.map((entry) {
        final index = entry.key;
        final button = entry.value;
        
        return Padding(
          padding: EdgeInsets.only(bottom: 16.h),
          child: SizedBox(
            width: 400.w,
            child: GameButton(
              title: button['title'] as String,
              color: button['color'] as Color,
              onPressed: () => _handleMenuAction(button['screen'] as GameScreen),
              gradient: true,
              elevation: 8,
            ).animate()
              .slideX(
                begin: index.isEven ? -1 : 1,
                duration: 600.ms,
                delay: Duration(milliseconds: 300 + (index * 150)),
              )
              .fadeIn(duration: 400.ms),
          ),
        );
      }).toList(),
    );
  }
  
  Widget _buildGameStatus() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 12.h),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppTheme.successColor.withOpacity(0.2),
            AppTheme.successColor.withOpacity(0.1),
          ],
        ),
        borderRadius: BorderRadius.circular(25.r),
        border: Border.all(
          color: AppTheme.successColor.withOpacity(0.5),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Status Indicator
          Container(
            width: 8.w,
            height: 8.h,
            decoration: BoxDecoration(
              color: AppTheme.successColor,
              borderRadius: BorderRadius.circular(4.r),
            ),
          ).animate()
            .scale(duration: 1000.ms)
            .then()
            .scale(begin: const Offset(1.5, 1.5), duration: 1000.ms)
            .then()
            .scale(begin: const Offset(0.8, 0.8), duration: 1000.ms),
          
          SizedBox(width: 12.w),
          
          // Status Text
          Text(
            'FLUTTER GAME RUNNING PERFECTLY!',
            style: GoogleFonts.orbitron(
              fontSize: 14.sp,
              color: AppTheme.successColor,
              fontWeight: FontWeight.bold,
            ),
          ),
          
          SizedBox(width: 8.w),
          
          // Flutter Logo
          Text(
            '🚀',
            style: TextStyle(fontSize: 16.sp),
          ).animate()
            .rotate(duration: 2000.ms)
            .then()
            .rotate(begin: 1, duration: 2000.ms),
        ],
      ),
    ).animate()
      .fadeIn(duration: 1000.ms, delay: 3000.ms)
      .slideY(begin: 1, duration: 600.ms);
  }
}