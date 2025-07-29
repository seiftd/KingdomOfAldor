import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ViewStyle,
  TextStyle,
  Animated,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import HapticFeedback from 'react-native-haptic-feedback';

import {COLORS, TYPOGRAPHY, SPACING, MOBILE_CONFIG} from '../constants/Config';

interface GameButtonProps {
  title: string;
  onPress: () => void;
  style?: ViewStyle;
  textStyle?: TextStyle;
  disabled?: boolean;
  hapticType?: 'light' | 'medium' | 'heavy';
  gradient?: boolean;
  gradientColors?: string[];
}

const GameButton: React.FC<GameButtonProps> = ({
  title,
  onPress,
  style,
  textStyle,
  disabled = false,
  hapticType = 'medium',
  gradient = false,
  gradientColors = [COLORS.UI_BUTTON, COLORS.UI_BUTTON_HOVER],
}) => {
  const scaleAnimation = new Animated.Value(1);

  const handlePressIn = () => {
    if (!disabled) {
      // Visual feedback - scale down
      Animated.spring(scaleAnimation, {
        toValue: 0.95,
        useNativeDriver: true,
      }).start();

      // Haptic feedback
      const hapticTypes = {
        light: MOBILE_CONFIG.HAPTIC_LIGHT,
        medium: MOBILE_CONFIG.HAPTIC_MEDIUM,
        heavy: MOBILE_CONFIG.HAPTIC_HEAVY,
      };
      
      HapticFeedback.trigger(hapticTypes[hapticType]);
    }
  };

  const handlePressOut = () => {
    if (!disabled) {
      // Visual feedback - scale back to normal
      Animated.spring(scaleAnimation, {
        toValue: 1,
        useNativeDriver: true,
      }).start();
    }
  };

  const buttonContent = (
    <Animated.View
      style={[
        styles.button,
        style,
        disabled && styles.disabled,
        {transform: [{scale: scaleAnimation}]},
      ]}
    >
      <Text style={[styles.text, textStyle, disabled && styles.disabledText]}>
        {title}
      </Text>
    </Animated.View>
  );

  if (gradient && !disabled) {
    return (
      <TouchableOpacity
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={disabled}
        activeOpacity={0.8}
      >
        <LinearGradient
          colors={gradientColors}
          style={[styles.button, style]}
          start={{x: 0, y: 0}}
          end={{x: 1, y: 1}}
        >
          <Animated.View style={{transform: [{scale: scaleAnimation}]}}>
            <Text style={[styles.text, textStyle]}>{title}</Text>
          </Animated.View>
        </LinearGradient>
      </TouchableOpacity>
    );
  }

  return (
    <TouchableOpacity
      onPress={onPress}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      disabled={disabled}
      activeOpacity={0.8}
    >
      {buttonContent}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    minHeight: MOBILE_CONFIG.BUTTON_MIN_SIZE,
    paddingHorizontal: SPACING.LARGE,
    paddingVertical: SPACING.MEDIUM,
    backgroundColor: COLORS.UI_BUTTON,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.UI_BORDER,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  text: {
    fontSize: TYPOGRAPHY.FONT_SIZE_LARGE,
    fontWeight: 'bold',
    color: COLORS.TEXT_PRIMARY,
    textAlign: 'center',
  },
  disabled: {
    backgroundColor: COLORS.OVERLAY_DARK,
    borderColor: COLORS.TEXT_SECONDARY,
    opacity: 0.6,
  },
  disabledText: {
    color: COLORS.TEXT_SECONDARY,
  },
});

export {GameButton};