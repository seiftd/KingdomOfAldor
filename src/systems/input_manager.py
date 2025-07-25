"""
Kingdom of Aldoria - Input Manager
Handles touch input, gestures, and input events for mobile gameplay
"""

import pygame
import logging
import time
from typing import Tuple, List, Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum

from ..core.config import Config

class GestureType(Enum):
    """Types of gestures"""
    TAP = "tap"
    LONG_PRESS = "long_press"
    DOUBLE_TAP = "double_tap"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    PINCH = "pinch"
    ZOOM = "zoom"

@dataclass
class TouchPoint:
    """Represents a touch point"""
    id: int
    x: float
    y: float
    start_time: float
    start_x: float
    start_y: float
    last_x: float
    last_y: float
    is_moving: bool = False

@dataclass
class GestureEvent:
    """Represents a gesture event"""
    gesture_type: GestureType
    position: Tuple[float, float]
    start_position: Tuple[float, float]
    duration: float
    distance: float
    direction: Tuple[float, float]
    additional_data: Dict[str, Any]

class InputManager:
    """Manages input handling for mobile gameplay"""
    
    def __init__(self):
        """Initialize the input manager"""
        self.logger = logging.getLogger(__name__)
        
        # Touch tracking
        self.active_touches: Dict[int, TouchPoint] = {}
        self.gesture_callbacks: Dict[GestureType, List[Callable]] = {}
        
        # Input state
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False
        self.keys_pressed = set()
        
        # Gesture detection parameters
        self.tap_max_duration = 0.3  # seconds
        self.tap_max_distance = 20   # pixels
        self.long_press_duration = Config.LONG_PRESS_DURATION
        self.double_tap_interval = Config.DOUBLE_TAP_MAX_INTERVAL
        self.swipe_min_distance = 50  # pixels
        self.deadzone = Config.TOUCH_DEADZONE
        
        # Gesture state
        self.last_tap_time = 0
        self.last_tap_pos = (0, 0)
        self.pending_taps = []
        
        # Virtual buttons for mobile
        self.virtual_buttons: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("InputManager initialized")
        self._setup_virtual_buttons()
    
    def _setup_virtual_buttons(self):
        """Setup virtual buttons for mobile interface"""
        button_size = 80
        margin = 20
        
        self.virtual_buttons = {
            "attack": {
                "rect": pygame.Rect(
                    Config.SCREEN_WIDTH - button_size - margin,
                    Config.SCREEN_HEIGHT - button_size - margin,
                    button_size, button_size
                ),
                "pressed": False,
                "color": Config.RED,
                "alpha": 0.7
            },
            "skill": {
                "rect": pygame.Rect(
                    Config.SCREEN_WIDTH - (button_size * 2) - (margin * 2),
                    Config.SCREEN_HEIGHT - button_size - margin,
                    button_size, button_size
                ),
                "pressed": False,
                "color": Config.BLUE,
                "alpha": 0.7
            },
            "menu": {
                "rect": pygame.Rect(
                    margin, margin, button_size // 2, button_size // 2
                ),
                "pressed": False,
                "color": Config.GRAY,
                "alpha": 0.7
            }
        }
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.KEYDOWN:
            self._handle_key_down(event)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event)
        
        # Handle touch events if available
        elif hasattr(pygame, 'FINGERDOWN') and event.type == pygame.FINGERDOWN:
            self._handle_finger_down(event)
        elif hasattr(pygame, 'FINGERUP') and event.type == pygame.FINGERUP:
            self._handle_finger_up(event)
        elif hasattr(pygame, 'FINGERMOTION') and event.type == pygame.FINGERMOTION:
            self._handle_finger_motion(event)
    
    def _handle_mouse_down(self, event):
        """Handle mouse button down (simulates touch)"""
        self.mouse_pressed = True
        pos = event.pos
        
        # Check virtual buttons
        for button_name, button_data in self.virtual_buttons.items():
            if button_data["rect"].collidepoint(pos):
                button_data["pressed"] = True
                self._trigger_button_event(button_name, True)
                return
        
        # Create touch point for gesture detection
        touch_id = 0  # Use 0 for mouse
        current_time = time.time()
        
        self.active_touches[touch_id] = TouchPoint(
            id=touch_id,
            x=pos[0], y=pos[1],
            start_time=current_time,
            start_x=pos[0], start_y=pos[1],
            last_x=pos[0], last_y=pos[1]
        )
    
    def _handle_mouse_up(self, event):
        """Handle mouse button up"""
        self.mouse_pressed = False
        pos = event.pos
        
        # Release virtual buttons
        for button_name, button_data in self.virtual_buttons.items():
            if button_data["pressed"]:
                button_data["pressed"] = False
                self._trigger_button_event(button_name, False)
        
        # Process gesture for mouse
        touch_id = 0
        if touch_id in self.active_touches:
            self._process_touch_end(touch_id, pos)
    
    def _handle_mouse_motion(self, event):
        """Handle mouse motion"""
        self.mouse_pos = event.pos
        
        # Update touch tracking for mouse
        touch_id = 0
        if touch_id in self.active_touches:
            touch = self.active_touches[touch_id]
            touch.last_x, touch.last_y = touch.x, touch.y
            touch.x, touch.y = event.pos
            
            # Check if moving
            distance = self._calculate_distance(
                (touch.start_x, touch.start_y), event.pos
            )
            if distance > self.deadzone:
                touch.is_moving = True
    
    def _handle_key_down(self, event):
        """Handle keyboard key down"""
        self.keys_pressed.add(event.key)
    
    def _handle_key_up(self, event):
        """Handle keyboard key up"""
        self.keys_pressed.discard(event.key)
    
    def _handle_finger_down(self, event):
        """Handle touch finger down"""
        # Convert normalized coordinates to screen coordinates
        x = int(event.x * Config.SCREEN_WIDTH)
        y = int(event.y * Config.SCREEN_HEIGHT)
        touch_id = event.touch_id
        current_time = time.time()
        
        self.active_touches[touch_id] = TouchPoint(
            id=touch_id,
            x=x, y=y,
            start_time=current_time,
            start_x=x, start_y=y,
            last_x=x, last_y=y
        )
    
    def _handle_finger_up(self, event):
        """Handle touch finger up"""
        x = int(event.x * Config.SCREEN_WIDTH)
        y = int(event.y * Config.SCREEN_HEIGHT)
        touch_id = event.touch_id
        
        if touch_id in self.active_touches:
            self._process_touch_end(touch_id, (x, y))
    
    def _handle_finger_motion(self, event):
        """Handle touch finger motion"""
        x = int(event.x * Config.SCREEN_WIDTH)
        y = int(event.y * Config.SCREEN_HEIGHT)
        touch_id = event.touch_id
        
        if touch_id in self.active_touches:
            touch = self.active_touches[touch_id]
            touch.last_x, touch.last_y = touch.x, touch.y
            touch.x, touch.y = x, y
            
            # Check if moving
            distance = self._calculate_distance(
                (touch.start_x, touch.start_y), (x, y)
            )
            if distance > self.deadzone:
                touch.is_moving = True
    
    def _process_touch_end(self, touch_id: int, end_pos: Tuple[int, int]):
        """Process end of touch and detect gestures
        
        Args:
            touch_id: Touch identifier
            end_pos: Final touch position
        """
        if touch_id not in self.active_touches:
            return
        
        touch = self.active_touches[touch_id]
        current_time = time.time()
        duration = current_time - touch.start_time
        
        start_pos = (touch.start_x, touch.start_y)
        distance = self._calculate_distance(start_pos, end_pos)
        direction = self._calculate_direction(start_pos, end_pos)
        
        # Detect gesture type
        gesture_type = None
        additional_data = {}
        
        if not touch.is_moving and distance <= self.tap_max_distance:
            if duration <= self.tap_max_duration:
                # Check for double tap
                if (current_time - self.last_tap_time <= self.double_tap_interval and
                    self._calculate_distance(self.last_tap_pos, end_pos) <= self.tap_max_distance):
                    gesture_type = GestureType.DOUBLE_TAP
                else:
                    gesture_type = GestureType.TAP
                    self.last_tap_time = current_time
                    self.last_tap_pos = end_pos
            elif duration >= self.long_press_duration:
                gesture_type = GestureType.LONG_PRESS
        
        elif distance >= self.swipe_min_distance:
            # Determine swipe direction
            if abs(direction[0]) > abs(direction[1]):
                if direction[0] > 0:
                    gesture_type = GestureType.SWIPE_RIGHT
                else:
                    gesture_type = GestureType.SWIPE_LEFT
            else:
                if direction[1] > 0:
                    gesture_type = GestureType.SWIPE_DOWN
                else:
                    gesture_type = GestureType.SWIPE_UP
        
        # Create and trigger gesture event
        if gesture_type:
            gesture_event = GestureEvent(
                gesture_type=gesture_type,
                position=end_pos,
                start_position=start_pos,
                duration=duration,
                distance=distance,
                direction=direction,
                additional_data=additional_data
            )
            
            self._trigger_gesture(gesture_event)
        
        # Remove touch from tracking
        del self.active_touches[touch_id]
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate distance between two points"""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return (dx * dx + dy * dy) ** 0.5
    
    def _calculate_direction(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> Tuple[float, float]:
        """Calculate direction vector between two points"""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return (dx, dy)
    
    def _trigger_gesture(self, gesture_event: GestureEvent):
        """Trigger gesture event callbacks
        
        Args:
            gesture_event: Gesture event data
        """
        gesture_type = gesture_event.gesture_type
        if gesture_type in self.gesture_callbacks:
            for callback in self.gesture_callbacks[gesture_type]:
                try:
                    callback(gesture_event)
                except Exception as e:
                    self.logger.error(f"Error in gesture callback: {e}")
    
    def _trigger_button_event(self, button_name: str, pressed: bool):
        """Trigger virtual button event
        
        Args:
            button_name: Name of the button
            pressed: Whether button was pressed or released
        """
        self.logger.debug(f"Virtual button {button_name}: {'pressed' if pressed else 'released'}")
        
        # You can add button-specific logic here or use callbacks
        event_name = f"button_{button_name}_{'down' if pressed else 'up'}"
        
        # Trigger any registered callbacks for this button
        if hasattr(self, 'button_callbacks') and event_name in self.button_callbacks:
            for callback in self.button_callbacks[event_name]:
                try:
                    callback()
                except Exception as e:
                    self.logger.error(f"Error in button callback: {e}")
    
    def register_gesture_callback(self, gesture_type: GestureType, callback: Callable):
        """Register callback for gesture events
        
        Args:
            gesture_type: Type of gesture to listen for
            callback: Function to call when gesture occurs
        """
        if gesture_type not in self.gesture_callbacks:
            self.gesture_callbacks[gesture_type] = []
        
        self.gesture_callbacks[gesture_type].append(callback)
        self.logger.debug(f"Registered callback for gesture: {gesture_type}")
    
    def unregister_gesture_callback(self, gesture_type: GestureType, callback: Callable):
        """Unregister gesture callback
        
        Args:
            gesture_type: Type of gesture
            callback: Callback function to remove
        """
        if gesture_type in self.gesture_callbacks:
            try:
                self.gesture_callbacks[gesture_type].remove(callback)
                self.logger.debug(f"Unregistered callback for gesture: {gesture_type}")
            except ValueError:
                self.logger.warning(f"Callback not found for gesture: {gesture_type}")
    
    def render_virtual_buttons(self, screen: pygame.Surface):
        """Render virtual buttons on screen
        
        Args:
            screen: Surface to render to
        """
        for button_name, button_data in self.virtual_buttons.items():
            rect = button_data["rect"]
            color = button_data["color"]
            alpha = button_data["alpha"]
            
            # Create surface with alpha
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            
            # Draw button background
            if button_data["pressed"]:
                # Darker when pressed
                pressed_color = tuple(int(c * 0.7) for c in color)
                pygame.draw.rect(button_surface, (*pressed_color, int(255 * alpha)), 
                               (0, 0, rect.width, rect.height))
            else:
                pygame.draw.rect(button_surface, (*color, int(255 * alpha)), 
                               (0, 0, rect.width, rect.height))
            
            # Draw button border
            pygame.draw.rect(button_surface, (255, 255, 255, int(255 * alpha)), 
                           (0, 0, rect.width, rect.height), 2)
            
            # Draw button label
            font = pygame.font.Font(None, 24)
            text = font.render(button_name.upper(), True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect.width // 2, rect.height // 2))
            button_surface.blit(text, text_rect)
            
            # Blit to screen
            screen.blit(button_surface, rect.topleft)
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if key is pressed
        """
        return key in self.keys_pressed
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get current mouse position
        
        Returns:
            Mouse position tuple
        """
        return self.mouse_pos
    
    def is_mouse_pressed(self) -> bool:
        """Check if mouse is pressed
        
        Returns:
            True if mouse button is down
        """
        return self.mouse_pressed
    
    def get_active_touch_count(self) -> int:
        """Get number of active touches
        
        Returns:
            Number of active touch points
        """
        return len(self.active_touches)
    
    def cleanup(self):
        """Clean up input manager"""
        self.logger.info("Cleaning up InputManager")
        
        self.active_touches.clear()
        self.gesture_callbacks.clear()
        self.keys_pressed.clear()
        
        self.logger.info("InputManager cleanup complete")