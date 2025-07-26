"""
2D Visual Effects (VFX) System for Kingdom of Aldoria
Handles weapon trails, skill effects, particle systems, and environmental effects
"""

import pygame
import math
import random
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import os

class EffectType(Enum):
    WEAPON_TRAIL = "weapon_trail"
    SKILL_ACTIVATION = "skill_activation"
    PARTICLE_BURST = "particle_burst"
    ENVIRONMENTAL = "environmental"
    UI_EFFECT = "ui_effect"

class BlendMode(Enum):
    NORMAL = pygame.BLEND_ALPHA_SDL2
    ADDITIVE = pygame.BLEND_ADD
    MULTIPLY = pygame.BLEND_MULT
    OVERLAY = pygame.BLEND_OVERLAY

@dataclass
class Particle:
    x: float
    y: float
    vel_x: float
    vel_y: float
    size: float
    color: Tuple[int, int, int, int]
    life: float
    max_life: float
    rotation: float = 0.0
    rotation_speed: float = 0.0
    scale: float = 1.0
    gravity: float = 0.0
    fade_rate: float = 1.0

@dataclass
class Effect:
    effect_type: EffectType
    x: float
    y: float
    particles: List[Particle]
    duration: float
    max_duration: float
    active: bool = True
    properties: Dict[str, Any] = None

class WeaponTrailEffect:
    def __init__(self, weapon_rank: str):
        self.weapon_rank = weapon_rank
        self.trail_points = []
        self.max_points = 15
        self.alpha_decay = 0.85
        
    def add_point(self, x: float, y: float):
        """Add a new point to the weapon trail"""
        self.trail_points.append({
            'x': x, 'y': y, 
            'alpha': 255, 
            'time': time.time()
        })
        
        if len(self.trail_points) > self.max_points:
            self.trail_points.pop(0)
    
    def update(self):
        """Update trail points and fade them"""
        current_time = time.time()
        self.trail_points = [
            point for point in self.trail_points 
            if current_time - point['time'] < 0.5
        ]
        
        for point in self.trail_points:
            age = current_time - point['time']
            point['alpha'] = max(0, 255 * (1 - age / 0.5))
    
    def draw(self, screen: pygame.Surface):
        """Draw the weapon trail"""
        if len(self.trail_points) < 2:
            return
            
        # Different effects based on weapon rank
        if self.weapon_rank in ['silver']:
            self._draw_silver_trail(screen)
        elif self.weapon_rank in ['gold', 'golden']:
            self._draw_gold_trail(screen)
        elif self.weapon_rank in ['platinum']:
            self._draw_platinum_trail(screen)
        elif self.weapon_rank in ['diamond']:
            self._draw_diamond_trail(screen)
        elif self.weapon_rank in ['legendary']:
            self._draw_legendary_trail(screen)
        else:
            self._draw_basic_trail(screen)
    
    def _draw_silver_trail(self, screen: pygame.Surface):
        """Silver weapons: Shimmering light particles"""
        for i, point in enumerate(self.trail_points):
            if i == 0:
                continue
                
            prev_point = self.trail_points[i-1]
            
            # Create shimmering effect with white/silver particles
            for j in range(3):
                shimmer_x = point['x'] + random.randint(-5, 5)
                shimmer_y = point['y'] + random.randint(-5, 5)
                
                color = (200 + random.randint(-50, 50), 
                        200 + random.randint(-50, 50), 
                        255, 
                        int(point['alpha'] * 0.7))
                
                if color[3] > 0:
                    size = random.randint(2, 4)
                    pygame.draw.circle(screen, color[:3], 
                                     (int(shimmer_x), int(shimmer_y)), size)
    
    def _draw_gold_trail(self, screen: pygame.Surface):
        """Gold weapons: Golden afterimages + spark bursts"""
        # Draw golden afterimage trail
        for i in range(1, len(self.trail_points)):
            point = self.trail_points[i]
            prev_point = self.trail_points[i-1]
            
            # Golden trail line
            alpha = int(point['alpha'] * 0.8)
            if alpha > 0:
                color = (255, 215, 0, alpha)  # Gold color
                
                # Draw thick golden line
                start_pos = (int(prev_point['x']), int(prev_point['y']))
                end_pos = (int(point['x']), int(point['y']))
                
                # Create gradient effect
                for thickness in range(5, 0, -1):
                    line_alpha = alpha // thickness
                    if line_alpha > 0:
                        pygame.draw.line(screen, (*color[:3], line_alpha), 
                                       start_pos, end_pos, thickness)
                
                # Add spark bursts
                if random.random() < 0.3:
                    self._create_spark_burst(screen, point['x'], point['y'], alpha)
    
    def _create_spark_burst(self, screen: pygame.Surface, x: float, y: float, alpha: int):
        """Create spark burst effect for gold weapons"""
        num_sparks = random.randint(3, 6)
        for _ in range(num_sparks):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(5, 15)
            
            spark_x = x + math.cos(angle) * distance
            spark_y = y + math.sin(angle) * distance
            
            spark_color = (255, 255, 100, alpha // 2)
            pygame.draw.circle(screen, spark_color[:3], 
                             (int(spark_x), int(spark_y)), 2)
    
    def _draw_platinum_trail(self, screen: pygame.Surface):
        """Platinum weapons: Electric energy trails"""
        for i in range(1, len(self.trail_points)):
            point = self.trail_points[i]
            prev_point = self.trail_points[i-1]
            
            # Electric blue-white trail
            alpha = int(point['alpha'])
            if alpha > 0:
                # Main trail
                color = (150, 200, 255, alpha)
                start_pos = (int(prev_point['x']), int(prev_point['y']))
                end_pos = (int(point['x']), int(point['y']))
                
                pygame.draw.line(screen, color[:3], start_pos, end_pos, 3)
                
                # Electric crackle effects
                if random.random() < 0.4:
                    for _ in range(2):
                        offset_x = random.randint(-8, 8)
                        offset_y = random.randint(-8, 8)
                        
                        crackle_pos = (int(point['x'] + offset_x), 
                                     int(point['y'] + offset_y))
                        pygame.draw.circle(screen, (255, 255, 255), 
                                         crackle_pos, 1)
    
    def _draw_diamond_trail(self, screen: pygame.Surface):
        """Diamond weapons: Crystal prismatic effects"""
        for i in range(1, len(self.trail_points)):
            point = self.trail_points[i]
            
            alpha = int(point['alpha'])
            if alpha > 0:
                # Prismatic rainbow effect
                colors = [
                    (255, 0, 0, alpha),    # Red
                    (255, 127, 0, alpha),  # Orange
                    (255, 255, 0, alpha),  # Yellow
                    (0, 255, 0, alpha),    # Green
                    (0, 0, 255, alpha),    # Blue
                    (75, 0, 130, alpha),   # Indigo
                    (148, 0, 211, alpha)   # Violet
                ]
                
                for j, color in enumerate(colors):
                    offset_angle = (j * math.pi * 2) / len(colors)
                    offset_x = math.cos(offset_angle + time.time() * 2) * 3
                    offset_y = math.sin(offset_angle + time.time() * 2) * 3
                    
                    pos = (int(point['x'] + offset_x), int(point['y'] + offset_y))
                    pygame.draw.circle(screen, color[:3], pos, 2)
    
    def _draw_legendary_trail(self, screen: pygame.Surface):
        """Legendary weapons: Divine aura effects"""
        for i in range(1, len(self.trail_points)):
            point = self.trail_points[i]
            
            alpha = int(point['alpha'])
            if alpha > 0:
                # Divine golden-white aura
                center = (int(point['x']), int(point['y']))
                
                # Multiple layers for divine effect
                for radius in range(8, 0, -2):
                    layer_alpha = alpha // (9 - radius)
                    if layer_alpha > 0:
                        color = (255, 250, 205, layer_alpha)  # Divine gold-white
                        pygame.draw.circle(screen, color[:3], center, radius)
                
                # Add floating light orbs
                if random.random() < 0.2:
                    for _ in range(2):
                        orb_x = point['x'] + random.randint(-15, 15)
                        orb_y = point['y'] + random.randint(-15, 15)
                        orb_pos = (int(orb_x), int(orb_y))
                        pygame.draw.circle(screen, (255, 255, 200), orb_pos, 3)
    
    def _draw_basic_trail(self, screen: pygame.Surface):
        """Basic weapon trail for lower tier weapons"""
        for i in range(1, len(self.trail_points)):
            point = self.trail_points[i]
            prev_point = self.trail_points[i-1]
            
            alpha = int(point['alpha'] * 0.5)
            if alpha > 0:
                color = (128, 128, 128, alpha)  # Gray trail
                start_pos = (int(prev_point['x']), int(prev_point['y']))
                end_pos = (int(point['x']), int(point['y']))
                
                pygame.draw.line(screen, color[:3], start_pos, end_pos, 2)

class SkillEffect:
    def __init__(self, skill_name: str, x: float, y: float):
        self.skill_name = skill_name
        self.x = x
        self.y = y
        self.start_time = time.time()
        self.duration = self.get_skill_duration()
        self.active = True
        
    def get_skill_duration(self) -> float:
        """Get duration based on skill type"""
        durations = {
            'time_rewind': 2.5,
            'damage_doubler': 3.0,
            'elemental_burst': 1.5,
            'shield_barrier': 4.0,
            'healing_aura': 3.5
        }
        return durations.get(self.skill_name, 2.0)
    
    def update(self) -> bool:
        """Update skill effect and return if still active"""
        elapsed = time.time() - self.start_time
        self.active = elapsed < self.duration
        return self.active
    
    def draw(self, screen: pygame.Surface):
        """Draw skill effect based on type"""
        if not self.active:
            return
            
        elapsed = time.time() - self.start_time
        progress = elapsed / self.duration
        
        if self.skill_name == 'time_rewind':
            self._draw_time_rewind_effect(screen, progress)
        elif self.skill_name == 'damage_doubler':
            self._draw_damage_doubler_effect(screen, progress)
        elif self.skill_name == 'elemental_burst':
            self._draw_elemental_burst_effect(screen, progress)
        elif self.skill_name == 'shield_barrier':
            self._draw_shield_barrier_effect(screen, progress)
        elif self.skill_name == 'healing_aura':
            self._draw_healing_aura_effect(screen, progress)
    
    def _draw_time_rewind_effect(self, screen: pygame.Surface, progress: float):
        """Time Rewind: Reverse-motion ghosting + clock gears"""
        center = (int(self.x), int(self.y))
        
        # Clock gears rotating
        gear_radius = 30 + int(progress * 20)
        gear_rotation = time.time() * -2  # Reverse rotation for time rewind
        
        # Draw gear teeth
        teeth_count = 12
        for i in range(teeth_count):
            angle = (i * 2 * math.pi / teeth_count) + gear_rotation
            
            # Outer tooth
            outer_x = center[0] + math.cos(angle) * gear_radius
            outer_y = center[1] + math.sin(angle) * gear_radius
            
            # Inner tooth
            inner_x = center[0] + math.cos(angle) * (gear_radius - 8)
            inner_y = center[1] + math.sin(angle) * (gear_radius - 8)
            
            alpha = int(255 * (1 - progress))
            if alpha > 0:
                color = (100, 150, 255, alpha)  # Time blue
                pygame.draw.line(screen, color[:3], 
                               (int(inner_x), int(inner_y)), 
                               (int(outer_x), int(outer_y)), 3)
        
        # Central gear hub
        hub_alpha = int(200 * (1 - progress))
        if hub_alpha > 0:
            pygame.draw.circle(screen, (150, 200, 255), center, 10, 2)
        
        # Ghosting effect (multiple faded copies)
        for i in range(5):
            ghost_alpha = int((50 - i * 10) * (1 - progress))
            if ghost_alpha > 0:
                ghost_offset = i * 3
                ghost_center = (center[0] - ghost_offset, center[1])
                pygame.draw.circle(screen, (200, 200, 255), ghost_center, 15, 1)
    
    def _draw_damage_doubler_effect(self, screen: pygame.Surface, progress: float):
        """Damage Doubler: Red energy crackling on character"""
        center = (int(self.x), int(self.y))
        
        # Crackling energy bolts
        num_bolts = 8
        for i in range(num_bolts):
            angle = (i * 2 * math.pi / num_bolts) + time.time() * 3
            
            # Create jagged lightning bolt
            bolt_points = []
            bolt_length = 40
            segments = 5
            
            for j in range(segments + 1):
                segment_progress = j / segments
                
                # Base position along the bolt
                base_x = center[0] + math.cos(angle) * bolt_length * segment_progress
                base_y = center[1] + math.sin(angle) * bolt_length * segment_progress
                
                # Add random jaggedness
                if j > 0 and j < segments:
                    perpendicular_angle = angle + math.pi / 2
                    jag_distance = random.randint(-8, 8)
                    base_x += math.cos(perpendicular_angle) * jag_distance
                    base_y += math.sin(perpendicular_angle) * jag_distance
                
                bolt_points.append((int(base_x), int(base_y)))
            
            # Draw the bolt
            alpha = int(255 * (1 - progress) * random.uniform(0.5, 1.0))
            if alpha > 20 and len(bolt_points) > 1:
                color = (255, 0, 0)  # Red energy
                for j in range(len(bolt_points) - 1):
                    pygame.draw.line(screen, color, bolt_points[j], bolt_points[j + 1], 2)
        
        # Pulsing red aura around character
        pulse_intensity = math.sin(time.time() * 5) * 0.5 + 0.5
        aura_alpha = int(100 * (1 - progress) * pulse_intensity)
        if aura_alpha > 0:
            aura_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (255, 50, 50, aura_alpha), (50, 50), 45)
            screen.blit(aura_surface, (center[0] - 50, center[1] - 50), 
                       special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_elemental_burst_effect(self, screen: pygame.Surface, progress: float):
        """Elemental Burst: Expanding ring of elemental particles"""
        center = (int(self.x), int(self.y))
        
        # Expanding ring
        ring_radius = int(progress * 80)
        
        # Create particles around the ring
        particle_count = 20
        for i in range(particle_count):
            angle = (i * 2 * math.pi / particle_count) + time.time()
            
            particle_x = center[0] + math.cos(angle) * ring_radius
            particle_y = center[1] + math.sin(angle) * ring_radius
            
            # Elemental colors (cycling)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            color = colors[i % len(colors)]
            
            alpha = int(255 * (1 - progress))
            if alpha > 0:
                particle_size = max(1, int(5 * (1 - progress)))
                pygame.draw.circle(screen, color, 
                                 (int(particle_x), int(particle_y)), particle_size)
    
    def _draw_shield_barrier_effect(self, screen: pygame.Surface, progress: float):
        """Shield Barrier: Protective dome with hexagonal pattern"""
        center = (int(self.x), int(self.y))
        shield_radius = 40
        
        # Hexagonal shield pattern
        hex_count = 3
        for ring in range(hex_count):
            ring_radius = shield_radius - (ring * 10)
            hex_points = []
            
            for i in range(6):
                angle = i * math.pi / 3 + time.time() * 0.5
                hex_x = center[0] + math.cos(angle) * ring_radius
                hex_y = center[1] + math.sin(angle) * ring_radius
                hex_points.append((int(hex_x), int(hex_y)))
            
            # Draw hexagon
            alpha = int(150 * (1 - progress * 0.3))
            if alpha > 0 and len(hex_points) > 2:
                color = (0, 150, 255)  # Shield blue
                pygame.draw.polygon(screen, color, hex_points, 2)
        
        # Shimmering effect
        for _ in range(8):
            shimmer_angle = random.uniform(0, 2 * math.pi)
            shimmer_radius = random.uniform(20, shield_radius)
            
            shimmer_x = center[0] + math.cos(shimmer_angle) * shimmer_radius
            shimmer_y = center[1] + math.sin(shimmer_angle) * shimmer_radius
            
            shimmer_alpha = int(100 * (1 - progress) * random.uniform(0.3, 1.0))
            if shimmer_alpha > 0:
                pygame.draw.circle(screen, (200, 200, 255), 
                                 (int(shimmer_x), int(shimmer_y)), 2)
    
    def _draw_healing_aura_effect(self, screen: pygame.Surface, progress: float):
        """Healing Aura: Green spiraling energy with plus symbols"""
        center = (int(self.x), int(self.y))
        
        # Spiraling green energy
        spiral_points = []
        spiral_rotations = 3
        spiral_radius = 50
        
        for i in range(50):
            spiral_progress = i / 49
            angle = spiral_progress * spiral_rotations * 2 * math.pi + time.time()
            radius = spiral_radius * (1 - spiral_progress)
            
            spiral_x = center[0] + math.cos(angle) * radius
            spiral_y = center[1] + math.sin(angle) * radius
            spiral_points.append((int(spiral_x), int(spiral_y)))
        
        # Draw spiral
        alpha = int(200 * (1 - progress * 0.5))
        if alpha > 0:
            for i, point in enumerate(spiral_points):
                point_alpha = alpha * (1 - i / len(spiral_points))
                if point_alpha > 20:
                    color = (0, 255, 0)  # Healing green
                    pygame.draw.circle(screen, color, point, 2)
        
        # Floating plus symbols
        plus_count = 6
        for i in range(plus_count):
            plus_angle = (i * 2 * math.pi / plus_count) + time.time() * 0.8
            plus_radius = 30 + math.sin(time.time() * 2 + i) * 10
            
            plus_x = center[0] + math.cos(plus_angle) * plus_radius
            plus_y = center[1] + math.sin(plus_angle) * plus_radius
            
            plus_alpha = int(180 * (1 - progress * 0.3))
            if plus_alpha > 0:
                # Draw plus symbol
                plus_size = 6
                color = (100, 255, 100)
                
                # Horizontal line
                pygame.draw.line(screen, color, 
                               (int(plus_x - plus_size), int(plus_y)), 
                               (int(plus_x + plus_size), int(plus_y)), 2)
                # Vertical line
                pygame.draw.line(screen, color, 
                               (int(plus_x), int(plus_y - plus_size)), 
                               (int(plus_x), int(plus_y + plus_size)), 2)

class EnvironmentalEffect:
    def __init__(self, effect_type: str, screen_width: int, screen_height: int):
        self.effect_type = effect_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.initialize_effect()
    
    def initialize_effect(self):
        """Initialize particles based on effect type"""
        if self.effect_type == 'sandstorm':
            self._init_sandstorm()
        elif self.effect_type == 'aurora_borealis':
            self._init_aurora()
        elif self.effect_type == 'rain':
            self._init_rain()
        elif self.effect_type == 'snow':
            self._init_snow()
    
    def _init_sandstorm(self):
        """Initialize sandstorm particles"""
        for _ in range(100):
            particle = Particle(
                x=random.uniform(-50, self.screen_width + 50),
                y=random.uniform(0, self.screen_height),
                vel_x=random.uniform(2, 8),
                vel_y=random.uniform(-1, 1),
                size=random.uniform(1, 3),
                color=(194, 154, 108, random.randint(50, 150)),  # Sandy color
                life=1.0,
                max_life=1.0
            )
            self.particles.append(particle)
    
    def _init_aurora(self):
        """Initialize aurora borealis effect"""
        # Aurora uses fewer, larger "particles" that represent aurora bands
        for _ in range(8):
            particle = Particle(
                x=random.uniform(0, self.screen_width),
                y=random.uniform(0, self.screen_height // 3),
                vel_x=random.uniform(-0.5, 0.5),
                vel_y=0,
                size=random.uniform(50, 150),
                color=(random.randint(0, 100), random.randint(150, 255), 
                      random.randint(100, 200), random.randint(30, 80)),
                life=1.0,
                max_life=1.0
            )
            self.particles.append(particle)
    
    def _init_rain(self):
        """Initialize rain particles"""
        for _ in range(150):
            particle = Particle(
                x=random.uniform(-100, self.screen_width + 100),
                y=random.uniform(-100, self.screen_height),
                vel_x=random.uniform(-1, 1),
                vel_y=random.uniform(5, 12),
                size=random.uniform(1, 2),
                color=(100, 150, 255, random.randint(100, 200)),
                life=1.0,
                max_life=1.0
            )
            self.particles.append(particle)
    
    def _init_snow(self):
        """Initialize snow particles"""
        for _ in range(80):
            particle = Particle(
                x=random.uniform(-50, self.screen_width + 50),
                y=random.uniform(-50, self.screen_height),
                vel_x=random.uniform(-1, 1),
                vel_y=random.uniform(1, 3),
                size=random.uniform(2, 5),
                color=(255, 255, 255, random.randint(150, 255)),
                life=1.0,
                max_life=1.0
            )
            self.particles.append(particle)
    
    def update(self):
        """Update environmental effect"""
        if self.effect_type == 'sandstorm':
            self._update_sandstorm()
        elif self.effect_type == 'aurora_borealis':
            self._update_aurora()
        elif self.effect_type == 'rain':
            self._update_rain()
        elif self.effect_type == 'snow':
            self._update_snow()
    
    def _update_sandstorm(self):
        """Update sandstorm effect"""
        for particle in self.particles:
            particle.x += particle.vel_x
            particle.y += particle.vel_y
            
            # Reset particles that move off screen
            if particle.x > self.screen_width + 50:
                particle.x = -50
                particle.y = random.uniform(0, self.screen_height)
            
            # Add some wind variation
            particle.vel_x += random.uniform(-0.1, 0.1)
            particle.vel_x = max(2, min(8, particle.vel_x))  # Clamp velocity
    
    def _update_aurora(self):
        """Update aurora borealis effect"""
        for particle in self.particles:
            particle.x += particle.vel_x
            
            # Pulsing effect
            pulse = math.sin(time.time() * 2 + particle.x * 0.01) * 0.3 + 0.7
            original_alpha = particle.color[3]
            particle.color = (*particle.color[:3], int(original_alpha * pulse))
            
            # Wrap around screen
            if particle.x > self.screen_width:
                particle.x = -particle.size
            elif particle.x < -particle.size:
                particle.x = self.screen_width
    
    def _update_rain(self):
        """Update rain effect"""
        for particle in self.particles:
            particle.x += particle.vel_x
            particle.y += particle.vel_y
            
            # Reset particles that fall off screen
            if particle.y > self.screen_height:
                particle.y = -10
                particle.x = random.uniform(-100, self.screen_width + 100)
    
    def _update_snow(self):
        """Update snow effect"""
        for particle in self.particles:
            particle.x += particle.vel_x
            particle.y += particle.vel_y
            
            # Add gentle swaying
            particle.vel_x += math.sin(time.time() + particle.y * 0.01) * 0.05
            
            # Reset particles that fall off screen
            if particle.y > self.screen_height:
                particle.y = -10
                particle.x = random.uniform(-50, self.screen_width + 50)
    
    def draw(self, screen: pygame.Surface):
        """Draw environmental effect"""
        if self.effect_type == 'sandstorm':
            self._draw_sandstorm(screen)
        elif self.effect_type == 'aurora_borealis':
            self._draw_aurora(screen)
        elif self.effect_type == 'rain':
            self._draw_rain(screen)
        elif self.effect_type == 'snow':
            self._draw_snow(screen)
    
    def _draw_sandstorm(self, screen: pygame.Surface):
        """Draw sandstorm with particle-blurred visibility"""
        # Create sand particles
        for particle in self.particles:
            if particle.color[3] > 0:
                pygame.draw.circle(screen, particle.color[:3], 
                                 (int(particle.x), int(particle.y)), 
                                 int(particle.size))
        
        # Add overall sandy tint overlay
        sand_overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        sand_overlay.fill((194, 154, 108, 30))  # Sandy tint
        screen.blit(sand_overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_aurora(self, screen: pygame.Surface):
        """Draw aurora borealis with pulsing light shaders"""
        # Create aurora bands
        for particle in self.particles:
            if particle.color[3] > 0:
                # Create aurora band as an elongated ellipse
                aurora_surface = pygame.Surface((int(particle.size * 3), int(particle.size)), pygame.SRCALPHA)
                
                # Create gradient effect
                for i in range(int(particle.size)):
                    alpha = particle.color[3] * (1 - i / particle.size)
                    if alpha > 0:
                        color = (*particle.color[:3], int(alpha))
                        pygame.draw.ellipse(aurora_surface, color[:3], 
                                          (0, i, int(particle.size * 3), 2))
                
                screen.blit(aurora_surface, (int(particle.x - particle.size * 1.5), int(particle.y)), 
                           special_flags=pygame.BLEND_ADD)
    
    def _draw_rain(self, screen: pygame.Surface):
        """Draw rain effect"""
        for particle in self.particles:
            if particle.color[3] > 0:
                # Draw rain as small lines
                start_pos = (int(particle.x), int(particle.y))
                end_pos = (int(particle.x + particle.vel_x), 
                          int(particle.y + particle.vel_y * 2))
                pygame.draw.line(screen, particle.color[:3], start_pos, end_pos, 1)
    
    def _draw_snow(self, screen: pygame.Surface):
        """Draw snow effect"""
        for particle in self.particles:
            if particle.color[3] > 0:
                pygame.draw.circle(screen, particle.color[:3], 
                                 (int(particle.x), int(particle.y)), 
                                 int(particle.size))

class VFXManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.weapon_trails = {}
        self.skill_effects = []
        self.environmental_effects = {}
        self.active_effects = []
        
    def create_weapon_trail(self, weapon_id: str, weapon_rank: str) -> WeaponTrailEffect:
        """Create and track a weapon trail effect"""
        trail = WeaponTrailEffect(weapon_rank)
        self.weapon_trails[weapon_id] = trail
        return trail
    
    def update_weapon_trail(self, weapon_id: str, x: float, y: float):
        """Update weapon trail position"""
        if weapon_id in self.weapon_trails:
            self.weapon_trails[weapon_id].add_point(x, y)
    
    def create_skill_effect(self, skill_name: str, x: float, y: float) -> SkillEffect:
        """Create a skill activation effect"""
        effect = SkillEffect(skill_name, x, y)
        self.skill_effects.append(effect)
        return effect
    
    def create_environmental_effect(self, effect_type: str) -> EnvironmentalEffect:
        """Create an environmental effect"""
        effect = EnvironmentalEffect(effect_type, self.screen_width, self.screen_height)
        self.environmental_effects[effect_type] = effect
        return effect
    
    def remove_environmental_effect(self, effect_type: str):
        """Remove an environmental effect"""
        if effect_type in self.environmental_effects:
            del self.environmental_effects[effect_type]
    
    def update(self):
        """Update all VFX systems"""
        # Update weapon trails
        for trail in self.weapon_trails.values():
            trail.update()
        
        # Update skill effects and remove inactive ones
        self.skill_effects = [effect for effect in self.skill_effects if effect.update()]
        
        # Update environmental effects
        for effect in self.environmental_effects.values():
            effect.update()
    
    def draw(self, screen: pygame.Surface):
        """Draw all VFX effects"""
        # Draw environmental effects first (background)
        for effect in self.environmental_effects.values():
            effect.draw(screen)
        
        # Draw weapon trails
        for trail in self.weapon_trails.values():
            trail.draw(screen)
        
        # Draw skill effects
        for effect in self.skill_effects:
            effect.draw(screen)
    
    def clear_weapon_trail(self, weapon_id: str):
        """Clear a specific weapon trail"""
        if weapon_id in self.weapon_trails:
            del self.weapon_trails[weapon_id]
    
    def clear_all_effects(self):
        """Clear all VFX effects"""
        self.weapon_trails.clear()
        self.skill_effects.clear()
        self.environmental_effects.clear()
        self.active_effects.clear()
    
    def get_effect_count(self) -> Dict[str, int]:
        """Get count of active effects for performance monitoring"""
        return {
            'weapon_trails': len(self.weapon_trails),
            'skill_effects': len(self.skill_effects),
            'environmental_effects': len(self.environmental_effects),
            'total_particles': sum(len(effect.particles) 
                                 for effect in self.environmental_effects.values())
        }