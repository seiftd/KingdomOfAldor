"""
Kingdom of Aldoria - Panel UI Component
A panel for displaying information with backgrounds and borders
"""

import pygame
from typing import Tuple, Optional

class Panel:
    """A UI panel component for displaying content"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 background_color: Tuple[int, int, int, int] = (50, 50, 80, 200),
                 border_color: Optional[Tuple[int, int, int]] = (100, 100, 150),
                 border_width: int = 2,
                 corner_radius: int = 5):
        """Initialize the panel"""
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
        # Appearance
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        
        # Content padding
        self.padding = 10
        
        # Visibility
        self.visible = True
        
        # Animation
        self.animation_time = 0
        self.fade_in_duration = 0.5
        self.scale_animation = False
        
    def update(self, dt: float):
        """Update panel animations"""
        if self.animation_time < self.fade_in_duration:
            self.animation_time += dt
    
    def render(self, screen: pygame.Surface):
        """Render the panel"""
        if not self.visible:
            return
        
        # Calculate animation progress
        animation_progress = min(1.0, self.animation_time / self.fade_in_duration)
        
        # Create panel surface with transparency
        panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Apply background color with animation alpha
        bg_color = self.background_color
        if len(bg_color) == 4:  # RGBA
            animated_alpha = int(bg_color[3] * animation_progress)
            bg_color = (bg_color[0], bg_color[1], bg_color[2], animated_alpha)
        
        # Draw rounded rectangle background
        if self.corner_radius > 0:
            self._draw_rounded_rect(panel_surface, bg_color, 
                                  pygame.Rect(0, 0, self.width, self.height),
                                  self.corner_radius)
        else:
            panel_surface.fill(bg_color)
        
        # Draw border if specified
        if self.border_color and self.border_width > 0:
            border_alpha = int(255 * animation_progress)
            border_color = (*self.border_color, border_alpha)
            
            if self.corner_radius > 0:
                # Draw rounded border
                self._draw_rounded_rect_border(panel_surface, border_color,
                                             pygame.Rect(0, 0, self.width, self.height),
                                             self.corner_radius, self.border_width)
            else:
                pygame.draw.rect(panel_surface, border_color,
                               pygame.Rect(0, 0, self.width, self.height),
                               self.border_width)
        
        # Apply scale animation if enabled
        if self.scale_animation:
            scale_factor = 0.8 + 0.2 * animation_progress
            scaled_width = int(self.width * scale_factor)
            scaled_height = int(self.height * scale_factor)
            panel_surface = pygame.transform.scale(panel_surface, (scaled_width, scaled_height))
            
            # Center the scaled panel
            scaled_x = self.x + (self.width - scaled_width) // 2
            scaled_y = self.y + (self.height - scaled_height) // 2
            screen.blit(panel_surface, (scaled_x, scaled_y))
        else:
            screen.blit(panel_surface, (self.x, self.y))
    
    def _draw_rounded_rect(self, surface: pygame.Surface, color: Tuple[int, int, int, int],
                          rect: pygame.Rect, radius: int):
        """Draw a rounded rectangle"""
        # Create a temporary surface for the rounded rectangle
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Draw the main rectangle (without corners)
        main_rect = pygame.Rect(radius, 0, rect.width - 2 * radius, rect.height)
        temp_surface.fill(color, main_rect)
        
        # Draw the left and right rectangles
        left_rect = pygame.Rect(0, radius, radius, rect.height - 2 * radius)
        right_rect = pygame.Rect(rect.width - radius, radius, radius, rect.height - 2 * radius)
        temp_surface.fill(color, left_rect)
        temp_surface.fill(color, right_rect)
        
        # Draw the four corner circles
        corner_color = color[:3] if len(color) == 4 else color
        pygame.draw.circle(temp_surface, corner_color, (radius, radius), radius)
        pygame.draw.circle(temp_surface, corner_color, (rect.width - radius, radius), radius)
        pygame.draw.circle(temp_surface, corner_color, (radius, rect.height - radius), radius)
        pygame.draw.circle(temp_surface, corner_color, (rect.width - radius, rect.height - radius), radius)
        
        surface.blit(temp_surface, rect.topleft)
    
    def _draw_rounded_rect_border(self, surface: pygame.Surface, color: Tuple[int, int, int, int],
                                 rect: pygame.Rect, radius: int, border_width: int):
        """Draw a rounded rectangle border"""
        # Draw outer rounded rectangle
        outer_rect = rect
        self._draw_rounded_rect(surface, color, outer_rect, radius)
        
        # Draw inner rounded rectangle (to create border effect)
        inner_rect = pygame.Rect(
            border_width, border_width,
            rect.width - 2 * border_width,
            rect.height - 2 * border_width
        )
        
        if inner_rect.width > 0 and inner_rect.height > 0:
            # Create a mask by drawing a transparent rectangle
            inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
            inner_surface.fill((0, 0, 0, 0))  # Transparent
            
            # This is a simplified border - in a full implementation you'd need
            # to properly handle the rounded corners for the border
            pygame.draw.rect(surface, (0, 0, 0, 0), inner_rect)
    
    def set_position(self, x: int, y: int):
        """Set panel position"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width: int, height: int):
        """Set panel size"""
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height
    
    def get_content_rect(self) -> pygame.Rect:
        """Get the rectangle for content area (inside padding)"""
        return pygame.Rect(
            self.x + self.padding,
            self.y + self.padding,
            self.width - 2 * self.padding,
            self.height - 2 * self.padding
        )
    
    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if point is inside panel"""
        return self.rect.collidepoint(point)
    
    def set_visible(self, visible: bool):
        """Set panel visibility"""
        self.visible = visible
    
    def start_fade_in(self, duration: float = 0.5, with_scale: bool = False):
        """Start fade-in animation"""
        self.animation_time = 0
        self.fade_in_duration = duration
        self.scale_animation = with_scale
    
    def is_animation_complete(self) -> bool:
        """Check if fade-in animation is complete"""
        return self.animation_time >= self.fade_in_duration