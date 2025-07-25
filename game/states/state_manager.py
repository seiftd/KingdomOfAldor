"""
Kingdom of Aldoria - State Manager
Manages different game states and transitions
"""

import pygame
from typing import List, Optional
from abc import ABC, abstractmethod

class GameState(ABC):
    """Abstract base class for all game states"""
    
    def __init__(self):
        """Initialize the game state"""
        self.name = self.__class__.__name__
        self.active = False
        self.next_state = None
        self.state_manager = None
    
    @abstractmethod
    def enter(self):
        """Called when entering this state"""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update game logic"""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render the state"""
        pass
    
    def set_next_state(self, state_class, *args, **kwargs):
        """Set the next state to transition to"""
        self.next_state = (state_class, args, kwargs)

class StateManager:
    """Manages game states and transitions"""
    
    def __init__(self):
        """Initialize the state manager"""
        self.states: List[GameState] = []
        self.pending_transition = None
        self.should_quit_flag = False
        
        # Import core states
        self._import_states()
    
    def _import_states(self):
        """Import all state classes for later use"""
        # This will be populated as we create more states
        self.state_classes = {}
    
    def push_state(self, state: GameState):
        """Push a new state onto the stack"""
        if self.states:
            self.states[-1].active = False
        
        state.state_manager = self
        self.states.append(state)
        state.active = True
        state.enter()
        
        print(f"Pushed state: {state.name}")
    
    def pop_state(self):
        """Pop the current state from the stack"""
        if not self.states:
            return
        
        current_state = self.states.pop()
        current_state.active = False
        current_state.exit()
        
        print(f"Popped state: {current_state.name}")
        
        # Activate previous state if exists
        if self.states:
            self.states[-1].active = True
        else:
            # No more states, quit the game
            self.should_quit_flag = True
    
    def change_state(self, new_state: GameState):
        """Change to a new state (replaces current state)"""
        if self.states:
            current_state = self.states.pop()
            current_state.active = False
            current_state.exit()
        
        self.push_state(new_state)
    
    def get_current_state(self) -> Optional[GameState]:
        """Get the current active state"""
        return self.states[-1] if self.states else None
    
    def handle_event(self, event: pygame.event.Event):
        """Handle events for the current state"""
        current_state = self.get_current_state()
        if current_state and current_state.active:
            current_state.handle_event(event)
    
    def update(self, dt: float):
        """Update the current state"""
        current_state = self.get_current_state()
        if current_state and current_state.active:
            current_state.update(dt)
            
            # Check for state transition
            if current_state.next_state:
                state_class, args, kwargs = current_state.next_state
                new_state = state_class(*args, **kwargs)
                current_state.next_state = None
                self.change_state(new_state)
    
    def render(self, screen: pygame.Surface):
        """Render the current state"""
        current_state = self.get_current_state()
        if current_state and current_state.active:
            current_state.render(screen)
    
    def handle_back_button(self):
        """Handle Android back button"""
        current_state = self.get_current_state()
        if current_state:
            # Let the state handle back button, or pop by default
            if hasattr(current_state, 'handle_back_button'):
                current_state.handle_back_button()
            else:
                self.pop_state()
    
    def should_quit(self) -> bool:
        """Check if the game should quit"""
        return self.should_quit_flag or len(self.states) == 0
    
    def quit_game(self):
        """Quit the game"""
        self.should_quit_flag = True
    
    def clear_states(self):
        """Clear all states"""
        while self.states:
            self.pop_state()
    
    def get_state_count(self) -> int:
        """Get number of states in the stack"""
        return len(self.states)