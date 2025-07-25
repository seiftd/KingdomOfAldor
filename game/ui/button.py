"""
Kingdom of Aldoria - Button UI Component
Customizable button with hover effects and mobile support
"""

import pygame
from typing import Callable, Optional, Tuple

class Button:
    """A customizable button UI component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str = "",
                 font_size: int = 24, on_click: Optional[Callable] = None,
                 background_color: Tuple[int, int, int] = (100, 100, 150),
                 hover_color: Tuple[int, int, int] = (120, 120, 180),
                 pressed_color: Tuple[int, int, int] = (80, 80, 120),
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 border_width: int = 2,
                 border_color: Tuple[int, int, int] = (200, 200, 200)):
        """Initialize the button"""
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.on_click = on_click
        
        # Colors
        self.background_color = background_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.border_width = border_width
        self.border_color = border_color
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True
        
        # Animation
        self.hover_animation_time = 0
        self.press_animation_time = 0
        self.animation_speed = 5.0
        
        # Font (will be loaded when needed)
        self.font = None
        self.text_surface = None
        self.text_rect = None
        
        # Sound effects
        self.hover_sound_played = False
    
    def update(self, dt: float):
        """Update button animations"""
        # Update hover animation
        if self.is_hovered:
            self.hover_animation_time = min(1.0, self.hover_animation_time + self.animation_speed * dt)
        else:
            self.hover_animation_time = max(0.0, self.hover_animation_time - self.animation_speed * dt)
            self.hover_sound_played = False  # Reset hover sound
        
        # Update press animation
        if self.is_pressed:
            self.press_animation_time = min(1.0, self.press_animation_time + self.animation_speed * dt * 2)
        else:
            self.press_animation_time = max(0.0, self.press_animation_time - self.animation_speed * dt * 2)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events"""
        if not self.is_enabled:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Play hover sound when first hovering
        if self.is_hovered and not was_hovered and not self.hover_sound_played:
            self._play_hover_sound()
            self.hover_sound_played = True
        
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:  # Left click
                self.is_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                if self.is_pressed and self.is_hovered:
                    self._on_button_clicked()
                self.is_pressed = False
        
        # Handle touch events (mobile)
        elif event.type == pygame.FINGERDOWN:
            touch_pos = self._normalize_touch_position(event.x, event.y)
            if self.rect.collidepoint(touch_pos):
                self.is_pressed = True
                self.is_hovered = True
        
        elif event.type == pygame.FINGERUP:
            if self.is_pressed:
                touch_pos = self._normalize_touch_position(event.x, event.y)
                if self.rect.collidepoint(touch_pos):
                    self._on_button_clicked()
                self.is_pressed = False
                self.is_hovered = False
    
    def _normalize_touch_position(self, x: float, y: float) -> Tuple[int, int]:
        """Convert normalized touch coordinates to screen coordinates"""
        # Get screen size (assuming 1280x720 for now)
        screen_width, screen_height = 1280, 720
        screen_x = int(x * screen_width)
        screen_y = int(y * screen_height)
        return (screen_x, screen_y)
    
    def _on_button_clicked(self):
        """Handle button click"""
        self._play_click_sound()
        
        if self.on_click:
            self.on_click()
    
    def _play_hover_sound(self):
        """Play hover sound effect"""
        # This will be implemented when audio manager is available
        pass
    
    def _play_click_sound(self):
        """Play click sound effect"""
        # This will be implemented when audio manager is available
        pass
    
    def render(self, screen: pygame.Surface):
        """Render the button"""
        if not self.is_enabled:
            # Draw disabled button
            disabled_color = (60, 60, 60)
            pygame.draw.rect(screen, disabled_color, self.rect)
            if self.border_width > 0:
                pygame.draw.rect(screen, (40, 40, 40), self.rect, self.border_width)
        else:
            # Calculate current color based on state and animations
            current_color = self._get_current_color()
            
            # Draw button background with slight animation offset
            button_rect = self.rect.copy()
            if self.is_pressed:
                button_rect.y += 2  # Press effect
            
            pygame.draw.rect(screen, current_color, button_rect)
            
            # Draw border
            if self.border_width > 0:
                border_color = self._get_border_color()
                pygame.draw.rect(screen, border_color, button_rect, self.border_width)
        
        # Draw text
        self._draw_text(screen)
    
    def _get_current_color(self) -> Tuple[int, int, int]:
        """Get current button color based on state and animations"""
        if self.is_pressed:
            # Interpolate between hover and pressed color
            base_color = self.hover_color if self.is_hovered else self.background_color
            return self._interpolate_color(base_color, self.pressed_color, self.press_animation_time)
        elif self.is_hovered:
            # Interpolate between background and hover color
            return self._interpolate_color(self.background_color, self.hover_color, self.hover_animation_time)
        else:
            # Normal background color
            return self.background_color
    
    def _get_border_color(self) -> Tuple[int, int, int]:
        """Get current border color"""
        if self.is_hovered:
            # Brighter border when hovered
            brightness_boost = int(50 * self.hover_animation_time)
            return (
                min(255, self.border_color[0] + brightness_boost),
                min(255, self.border_color[1] + brightness_boost),
                min(255, self.border_color[2] + brightness_boost)
            )
        return self.border_color
    
    def _interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                          factor: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        factor = max(0.0, min(1.0, factor))  # Clamp factor
        
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        
        return (r, g, b)
    
    def _draw_text(self, screen: pygame.Surface):
        """Draw button text"""
        if not self.text:
            return
        
        # Load font if not already loaded
        if self.font is None:
            self.font = pygame.font.Font(None, self.font_size)
        
        # Create text surface if not already created or text changed
        if self.text_surface is None:
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Adjust text position for press effect
        text_pos = self.text_rect.topleft
        if self.is_pressed:
            text_pos = (text_pos[0], text_pos[1] + 2)
        
        # Draw text with subtle shadow if not disabled
        if self.is_enabled:
            # Shadow
            shadow_surface = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(shadow_surface, (text_pos[0] + 1, text_pos[1] + 1))
        
        # Main text
        text_color = self.text_color if self.is_enabled else (120, 120, 120)
        if self.text_surface is None or self.text_surface.get_at((0, 0))[:3] != text_color:
            self.text_surface = self.font.render(self.text, True, text_color)
        
        screen.blit(self.text_surface, text_pos)
    
    def set_text(self, new_text: str):
        """Change button text"""
        if self.text != new_text:
            self.text = new_text
            self.text_surface = None  # Force recreation
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the button"""
        self.is_enabled = enabled
        if not enabled:
            self.is_hovered = False
            self.is_pressed = False
    
    def set_position(self, x: int, y: int):
        """Set button position"""
        self.rect.x = x
        self.rect.y = y
        self.text_rect = None  # Force text position recalculation
    
    def set_size(self, width: int, height: int):
        """Set button size"""
        self.rect.width = width
        self.rect.height = height
        self.text_rect = None  # Force text position recalculation
    
    def get_rect(self) -> pygame.Rect:
        """Get button rectangle"""
        return self.rect.copy()
    
    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if point is inside button"""
        return self.rect.collidepoint(point)