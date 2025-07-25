"""
Kingdom of Aldoria - State Manager
Manages game state transitions and state lifecycle
"""

import logging
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod

class GameState(ABC):
    """Abstract base class for all game states"""
    
    def __init__(self, game):
        """Initialize the game state
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def enter(self, **kwargs):
        """Called when entering this state"""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update state logic
        
        Args:
            dt: Delta time since last frame in seconds
        """
        pass
    
    @abstractmethod
    def render(self, screen):
        """Render the state
        
        Args:
            screen: Pygame surface to render to
        """
        pass
    
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame events
        
        Args:
            event: Pygame event object
        """
        pass

class StateManager:
    """Manages game state transitions and lifecycle"""
    
    def __init__(self):
        """Initialize the state manager"""
        self.logger = logging.getLogger(__name__)
        
        # State storage
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None
        self.current_state_name: Optional[str] = None
        
        # State transition queue
        self.pending_state_change: Optional[str] = None
        self.pending_state_kwargs: Dict[str, Any] = {}
        
        # State history for back navigation
        self.state_history = []
        self.max_history = 10
        
        self.logger.info("StateManager initialized")
    
    def add_state(self, name: str, state: GameState):
        """Add a new state to the manager
        
        Args:
            name: Unique identifier for the state
            state: GameState instance
        """
        if name in self.states:
            self.logger.warning(f"State '{name}' already exists, overwriting")
        
        self.states[name] = state
        self.logger.debug(f"Added state: {name}")
    
    def remove_state(self, name: str):
        """Remove a state from the manager
        
        Args:
            name: Name of state to remove
        """
        if name in self.states:
            if self.current_state_name == name:
                self.logger.warning(f"Cannot remove current state: {name}")
                return False
            
            del self.states[name]
            self.logger.debug(f"Removed state: {name}")
            return True
        
        self.logger.warning(f"State '{name}' not found for removal")
        return False
    
    def change_state(self, new_state_name: str, **kwargs):
        """Request a state change
        
        Args:
            new_state_name: Name of the state to change to
            **kwargs: Additional arguments to pass to the new state
        """
        if new_state_name not in self.states:
            self.logger.error(f"State '{new_state_name}' not found")
            return False
        
        # Queue the state change to be processed at a safe time
        self.pending_state_change = new_state_name
        self.pending_state_kwargs = kwargs
        
        self.logger.debug(f"Queued state change to: {new_state_name}")
        return True
    
    def _execute_state_change(self):
        """Execute a pending state change"""
        if not self.pending_state_change:
            return
        
        new_state_name = self.pending_state_change
        kwargs = self.pending_state_kwargs.copy()
        
        # Clear pending change
        self.pending_state_change = None
        self.pending_state_kwargs.clear()
        
        # Exit current state
        if self.current_state:
            try:
                self.current_state.exit()
                self.logger.debug(f"Exited state: {self.current_state_name}")
            except Exception as e:
                self.logger.error(f"Error exiting state {self.current_state_name}: {e}")
        
        # Update state history
        if self.current_state_name:
            self.state_history.append(self.current_state_name)
            if len(self.state_history) > self.max_history:
                self.state_history.pop(0)
        
        # Change to new state
        old_state_name = self.current_state_name
        self.current_state_name = new_state_name
        self.current_state = self.states[new_state_name]
        
        # Enter new state
        try:
            self.current_state.enter(**kwargs)
            self.logger.info(f"State changed: {old_state_name} -> {new_state_name}")
        except Exception as e:
            self.logger.error(f"Error entering state {new_state_name}: {e}")
            # Revert to previous state if possible
            if old_state_name and old_state_name in self.states:
                self.current_state_name = old_state_name
                self.current_state = self.states[old_state_name]
    
    def go_back(self):
        """Go back to the previous state"""
        if not self.state_history:
            self.logger.debug("No previous state to go back to")
            return False
        
        previous_state = self.state_history.pop()
        self.change_state(previous_state)
        return True
    
    def update(self, dt: float):
        """Update the current state
        
        Args:
            dt: Delta time since last frame in seconds
        """
        # Execute any pending state changes first
        self._execute_state_change()
        
        # Update current state
        if self.current_state:
            try:
                self.current_state.update(dt)
            except Exception as e:
                self.logger.error(f"Error updating state {self.current_state_name}: {e}")
    
    def render(self, screen):
        """Render the current state
        
        Args:
            screen: Pygame surface to render to
        """
        if self.current_state:
            try:
                self.current_state.render(screen)
            except Exception as e:
                self.logger.error(f"Error rendering state {self.current_state_name}: {e}")
    
    def handle_event(self, event):
        """Handle pygame events for the current state
        
        Args:
            event: Pygame event object
        """
        if self.current_state:
            try:
                self.current_state.handle_event(event)
            except Exception as e:
                self.logger.error(f"Error handling event in state {self.current_state_name}: {e}")
    
    def get_current_state_name(self) -> Optional[str]:
        """Get the name of the current state"""
        return self.current_state_name
    
    def get_current_state(self) -> Optional[GameState]:
        """Get the current state instance"""
        return self.current_state
    
    def is_state_active(self, state_name: str) -> bool:
        """Check if a specific state is currently active
        
        Args:
            state_name: Name of state to check
            
        Returns:
            True if the state is currently active
        """
        return self.current_state_name == state_name
    
    def get_state_history(self) -> list:
        """Get a copy of the state history"""
        return self.state_history.copy()
    
    def clear_history(self):
        """Clear the state history"""
        self.state_history.clear()
        self.logger.debug("State history cleared")
    
    def cleanup(self):
        """Cleanup the state manager"""
        self.logger.info("Cleaning up StateManager")
        
        # Exit current state
        if self.current_state:
            try:
                self.current_state.exit()
            except Exception as e:
                self.logger.error(f"Error during cleanup exit of state {self.current_state_name}: {e}")
        
        # Clear all states
        self.states.clear()
        self.current_state = None
        self.current_state_name = None
        self.state_history.clear()
        
        self.logger.info("StateManager cleanup complete")