"""
Kingdom of Aldoria - Thumbnail and Game Icon Generator
Creates promotional images, thumbnails, and game icons based on specifications
"""

import pygame
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import json
import math
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import io

class ImageFormat(Enum):
    WEBP = "webp"
    PNG = "png"
    JPG = "jpg"

@dataclass
class ColorPalette:
    dark_red: str = "#8B0000"
    void_black: str = "#000000"
    gold: str = "#FFD700"
    void_purple: str = "#9400D3"
    crimson: str = "#DC143C"
    fire_orange: str = "#FF4500"
    shadow_gray: str = "#2F2F2F"

@dataclass
class ThumbnailSpec:
    width: int = 1280
    height: int = 720
    aspect_ratio: str = "16:9"
    format: ImageFormat = ImageFormat.WEBP
    quality: int = 90
    max_size_kb: int = 150

class ThumbnailGenerator:
    def __init__(self, assets_path: str = "assets/images"):
        self.assets_path = assets_path
        self.colors = ColorPalette()
        self.spec = ThumbnailSpec()
        
        # Ensure assets directory exists
        os.makedirs(assets_path, exist_ok=True)
        os.makedirs(f"{assets_path}/thumbnails", exist_ok=True)
        os.makedirs(f"{assets_path}/icons", exist_ok=True)
        
        # Initialize fonts (will use default if custom fonts not available)
        self.gothic_font_large = self._load_font("assets/fonts/gothic.ttf", 72)
        self.gothic_font_medium = self._load_font("assets/fonts/gothic.ttf", 48)
        self.gothic_font_small = self._load_font("assets/fonts/gothic.ttf", 32)
        
    def _load_font(self, font_path: str, size: int) -> ImageFont.ImageFont:
        """Load font or return default if not available"""
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
            else:
                # Try to use a system gothic-style font
                system_fonts = [
                    "C:/Windows/Fonts/oldengl.ttf",  # Windows
                    "/System/Library/Fonts/Papyrus.ttc",  # macOS
                    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"  # Linux
                ]
                
                for font in system_fonts:
                    if os.path.exists(font):
                        return ImageFont.truetype(font, size)
                
                # Fall back to default
                return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _create_gradient(self, width: int, height: int, 
                        start_color: str, end_color: str, 
                        direction: str = "vertical") -> Image.Image:
        """Create a gradient background"""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        start_rgb = self._hex_to_rgb(start_color)
        end_rgb = self._hex_to_rgb(end_color)
        
        if direction == "vertical":
            for y in range(height):
                ratio = y / height
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:  # horizontal
            for x in range(width):
                ratio = x / width
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        
        return gradient
    
    def _draw_dragon_silhouette(self, draw: ImageDraw.Draw, 
                               center_x: int, center_y: int, 
                               scale: float = 1.0) -> None:
        """Draw a stylized dragon silhouette"""
        # Dragon body (serpentine curve)
        body_points = []
        for i in range(20):
            angle = i * 0.3
            x = center_x + int(math.cos(angle) * 200 * scale)
            y = center_y + int(math.sin(angle) * 100 * scale) + int(i * 15 * scale)
            body_points.append((x, y))
        
        # Draw body
        if len(body_points) > 2:
            draw.polygon(body_points, fill=self._hex_to_rgb(self.colors.void_black))
        
        # Dragon head
        head_size = int(80 * scale)
        head_x = center_x - int(100 * scale)
        head_y = center_y - int(50 * scale)
        
        # Head outline
        draw.ellipse([head_x - head_size, head_y - head_size//2, 
                     head_x + head_size, head_y + head_size//2], 
                    fill=self._hex_to_rgb(self.colors.void_black))
        
        # Eyes (glowing red)
        eye_size = int(15 * scale)
        draw.ellipse([head_x - 30, head_y - 10, head_x - 30 + eye_size, head_y - 10 + eye_size], 
                    fill=self._hex_to_rgb(self.colors.crimson))
        draw.ellipse([head_x - 10, head_y - 10, head_x - 10 + eye_size, head_y - 10 + eye_size], 
                    fill=self._hex_to_rgb(self.colors.crimson))
        
        # Wings (spread wide)
        wing_span = int(400 * scale)
        wing_height = int(200 * scale)
        
        # Left wing
        left_wing = [
            (center_x - wing_span//2, center_y),
            (center_x - wing_span//3, center_y - wing_height),
            (center_x - wing_span//6, center_y - wing_height//2),
            (center_x, center_y - wing_height//4)
        ]
        draw.polygon(left_wing, fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Right wing
        right_wing = [
            (center_x + wing_span//2, center_y),
            (center_x + wing_span//3, center_y - wing_height),
            (center_x + wing_span//6, center_y - wing_height//2),
            (center_x, center_y - wing_height//4)
        ]
        draw.polygon(right_wing, fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Add crimson cracks on dragon body
        crack_points = [
            (center_x - 50, center_y - 20),
            (center_x + 30, center_y + 10),
            (center_x - 20, center_y + 40)
        ]
        
        for point in crack_points:
            draw.line([point, (point[0] + 20, point[1] + 5)], 
                     fill=self._hex_to_rgb(self.colors.crimson), width=3)
    
    def _draw_hero_silhouette(self, draw: ImageDraw.Draw, 
                             center_x: int, center_y: int, 
                             scale: float = 1.0) -> None:
        """Draw hero (Arin) in combat pose"""
        # Hero body (simplified figure)
        body_width = int(40 * scale)
        body_height = int(100 * scale)
        
        # Torso
        draw.rectangle([center_x - body_width//2, center_y - body_height//2,
                       center_x + body_width//2, center_y + body_height//2],
                      fill=self._hex_to_rgb(self.colors.void_purple))
        
        # Head
        head_size = int(25 * scale)
        draw.ellipse([center_x - head_size//2, center_y - body_height//2 - head_size,
                     center_x + head_size//2, center_y - body_height//2],
                    fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Glowing red eyes
        eye_size = int(3 * scale)
        draw.ellipse([center_x - 8, center_y - body_height//2 - 15,
                     center_x - 8 + eye_size, center_y - body_height//2 - 15 + eye_size],
                    fill=self._hex_to_rgb(self.colors.crimson))
        draw.ellipse([center_x + 5, center_y - body_height//2 - 15,
                     center_x + 5 + eye_size, center_y - body_height//2 - 15 + eye_size],
                    fill=self._hex_to_rgb(self.colors.crimson))
        
        # Sword (Solar Flare Sword - raised)
        sword_length = int(120 * scale)
        sword_x = center_x + int(60 * scale)
        sword_y = center_y - int(80 * scale)
        
        # Sword blade (golden)
        draw.line([sword_x, sword_y, sword_x + 20, sword_y - sword_length],
                 fill=self._hex_to_rgb(self.colors.gold), width=6)
        
        # Sword glow effect
        draw.line([sword_x - 2, sword_y, sword_x + 22, sword_y - sword_length],
                 fill=self._hex_to_rgb(self.colors.fire_orange), width=10)
        
        # Arm holding sword
        draw.line([center_x + 20, center_y - 20, sword_x, sword_y],
                 fill=self._hex_to_rgb(self.colors.void_purple), width=8)
        
        # Void energy aura around hero
        aura_radius = int(60 * scale)
        for i in range(3):
            radius = aura_radius + i * 10
            # Create semi-transparent circles for aura effect
            # Note: PIL doesn't have great transparency support, so we'll use multiple thin lines
            for angle in range(0, 360, 20):
                x1 = center_x + int(math.cos(math.radians(angle)) * radius)
                y1 = center_y + int(math.sin(math.radians(angle)) * radius)
                x2 = center_x + int(math.cos(math.radians(angle + 10)) * radius)
                y2 = center_y + int(math.sin(math.radians(angle + 10)) * radius)
                draw.line([x1, y1, x2, y2], fill=self._hex_to_rgb(self.colors.void_purple), width=2)
    
    def _draw_castle_silhouette(self, draw: ImageDraw.Draw, 
                               center_x: int, center_y: int, 
                               scale: float = 1.0) -> None:
        """Draw burning castle silhouette"""
        # Main tower
        tower_width = int(80 * scale)
        tower_height = int(200 * scale)
        
        draw.rectangle([center_x - tower_width//2, center_y,
                       center_x + tower_width//2, center_y + tower_height],
                      fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Castle battlements
        battlement_height = int(20 * scale)
        for i in range(5):
            x = center_x - tower_width//2 + i * (tower_width // 5)
            if i % 2 == 0:  # Create crenelations
                draw.rectangle([x, center_y, x + (tower_width // 5), center_y + battlement_height],
                              fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Side towers
        side_tower_width = int(50 * scale)
        side_tower_height = int(150 * scale)
        
        # Left tower
        draw.rectangle([center_x - tower_width//2 - side_tower_width, center_y + 30,
                       center_x - tower_width//2, center_y + 30 + side_tower_height],
                      fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Right tower
        draw.rectangle([center_x + tower_width//2, center_y + 30,
                       center_x + tower_width//2 + side_tower_width, center_y + 30 + side_tower_height],
                      fill=self._hex_to_rgb(self.colors.shadow_gray))
        
        # Fire effects on castle
        fire_points = [
            (center_x - 20, center_y + 50),
            (center_x + 30, center_y + 80),
            (center_x - 40, center_y + 120)
        ]
        
        for point in fire_points:
            # Draw flame shapes
            flame_height = int(40 * scale)
            flame_points = [
                point,
                (point[0] - 10, point[1] + flame_height//2),
                (point[0], point[1] + flame_height),
                (point[0] + 10, point[1] + flame_height//2)
            ]
            draw.polygon(flame_points, fill=self._hex_to_rgb(self.colors.fire_orange))
    
    def _add_text_with_effects(self, image: Image.Image, text: str, 
                              x: int, y: int, font: ImageFont.ImageFont,
                              fill_color: str, border_color: str = "#000000",
                              glow_color: str = None, border_width: int = 2) -> Image.Image:
        """Add text with border and glow effects"""
        # Create a larger canvas for effects
        margin = 20
        text_img = Image.new('RGBA', (image.width + margin*2, image.height + margin*2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        # Adjust position for margin
        text_x = x + margin
        text_y = y + margin
        
        # Draw border (outline effect)
        for dx in range(-border_width, border_width + 1):
            for dy in range(-border_width, border_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((text_x + dx, text_y + dy), text, font=font, 
                             fill=self._hex_to_rgb(border_color))
        
        # Draw glow effect if specified
        if glow_color:
            glow_radius = 5
            for dx in range(-glow_radius, glow_radius + 1):
                for dy in range(-glow_radius, glow_radius + 1):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= glow_radius and distance > border_width:
                        alpha = int(100 * (1 - distance / glow_radius))
                        glow_rgb = self._hex_to_rgb(glow_color)
                        draw.text((text_x + dx, text_y + dy), text, font=font, 
                                 fill=(*glow_rgb, alpha))
        
        # Draw main text
        draw.text((text_x, text_y), text, font=font, fill=self._hex_to_rgb(fill_color))
        
        # Composite with original image
        result = Image.new('RGBA', image.size)
        result.paste(image, (0, 0))
        
        # Crop the text image back to original size
        text_img = text_img.crop((margin, margin, text_img.width - margin, text_img.height - margin))
        result = Image.alpha_composite(result.convert('RGBA'), text_img)
        
        return result.convert('RGB')
    
    def generate_main_thumbnail(self, save_path: str = None) -> str:
        """Generate the main game thumbnail based on specifications"""
        # Create base image with gradient background
        image = self._create_gradient(self.spec.width, self.spec.height, 
                                    self.colors.void_black, self.colors.dark_red)
        
        # Convert to RGBA for effects
        image = image.convert('RGBA')
        draw = ImageDraw.Draw(image)
        
        # Background: Burning kingdom with aurora effects
        # Add aurora-like energy waves
        for i in range(5):
            wave_y = 100 + i * 50
            wave_points = []
            for x in range(0, self.spec.width, 20):
                y_offset = int(30 * math.sin(x * 0.01 + i))
                wave_points.append((x, wave_y + y_offset))
            
            if len(wave_points) > 1:
                for j in range(len(wave_points) - 1):
                    draw.line([wave_points[j], wave_points[j+1]], 
                             fill=self._hex_to_rgb(self.colors.void_purple), width=3)
        
        # Midground: Castle with dragon
        castle_x = self.spec.width // 2
        castle_y = self.spec.height // 2 + 50
        self._draw_castle_silhouette(draw, castle_x, castle_y, 0.8)
        
        # Dragon coiled around castle
        dragon_x = castle_x + 100
        dragon_y = castle_y - 50
        self._draw_dragon_silhouette(draw, dragon_x, dragon_y, 1.2)
        
        # Foreground: Hero Arin
        hero_x = self.spec.width // 4
        hero_y = self.spec.height // 2 + 100
        self._draw_hero_silhouette(draw, hero_x, hero_y, 1.5)
        
        # Convert back to RGB for text
        image = image.convert('RGB')
        
        # Add main title text
        title_text = "KINGDOM OF ALDORIA"
        title_x = self.spec.width // 2 - 300  # Approximate centering
        title_y = 50
        
        image = self._add_text_with_effects(
            image, title_text, title_x, title_y, self.gothic_font_large,
            self.colors.gold, self.colors.void_black, self.colors.fire_orange, 3
        )
        
        # Add subtitle
        subtitle_text = "Dragon's Wrath Edition"
        subtitle_x = self.spec.width // 2 - 150
        subtitle_y = 140
        
        image = self._add_text_with_effects(
            image, subtitle_text, subtitle_x, subtitle_y, self.gothic_font_medium,
            self.colors.crimson, self.colors.void_black, None, 2
        )
        
        # Save the image
        if not save_path:
            save_path = f"{self.assets_path}/thumbnails/kingdom_of_aldoria_main.{self.spec.format.value}"
        
        # Optimize file size
        image = self._optimize_image_size(image, self.spec.max_size_kb)
        image.save(save_path, format=self.spec.format.value.upper(), 
                  quality=self.spec.quality, optimize=True)
        
        return save_path
    
    def generate_game_icon(self, size: int = 512, save_path: str = None) -> str:
        """Generate game icon in specified size"""
        # Create square icon
        icon = Image.new('RGB', (size, size), self._hex_to_rgb(self.colors.void_black))
        draw = ImageDraw.Draw(icon)
        
        # Background gradient (circular)
        for radius in range(size//2, 0, -5):
            intensity = 1 - (radius / (size//2))
            r = int(self._hex_to_rgb(self.colors.dark_red)[0] * intensity)
            g = int(self._hex_to_rgb(self.colors.dark_red)[1] * intensity)
            b = int(self._hex_to_rgb(self.colors.dark_red)[2] * intensity)
            
            draw.ellipse([size//2 - radius, size//2 - radius, 
                         size//2 + radius, size//2 + radius], 
                        fill=(r, g, b))
        
        # Central dragon head
        dragon_scale = size / 512  # Scale based on icon size
        dragon_x = size // 2
        dragon_y = size // 2 - int(30 * dragon_scale)
        
        # Simplified dragon head for icon
        head_size = int(60 * dragon_scale)
        draw.ellipse([dragon_x - head_size, dragon_y - head_size//2,
                     dragon_x + head_size, dragon_y + head_size//2],
                    fill=self._hex_to_rgb(self.colors.void_black))
        
        # Dragon eyes
        eye_size = int(12 * dragon_scale)
        draw.ellipse([dragon_x - 25, dragon_y - 8, dragon_x - 25 + eye_size, dragon_y - 8 + eye_size],
                    fill=self._hex_to_rgb(self.colors.crimson))
        draw.ellipse([dragon_x + 13, dragon_y - 8, dragon_x + 13 + eye_size, dragon_y - 8 + eye_size],
                    fill=self._hex_to_rgb(self.colors.crimson))
        
        # Crown/jewel above dragon (representing the shattered jewel)
        jewel_points = [
            (dragon_x, dragon_y - int(80 * dragon_scale)),
            (dragon_x - int(15 * dragon_scale), dragon_y - int(60 * dragon_scale)),
            (dragon_x + int(15 * dragon_scale), dragon_y - int(60 * dragon_scale))
        ]
        draw.polygon(jewel_points, fill=self._hex_to_rgb(self.colors.gold))
        
        # Add glow effect around jewel
        for i in range(3):
            glow_radius = int((20 + i * 5) * dragon_scale)
            angles = range(0, 360, 30)
            for angle in angles:
                x = dragon_x + int(math.cos(math.radians(angle)) * glow_radius)
                y = dragon_y - int(80 * dragon_scale) + int(math.sin(math.radians(angle)) * glow_radius)
                draw.ellipse([x-2, y-2, x+2, y+2], fill=self._hex_to_rgb(self.colors.void_purple))
        
        # Save icon
        if not save_path:
            save_path = f"{self.assets_path}/icons/kingdom_of_aldoria_icon_{size}x{size}.png"
        
        icon.save(save_path, format='PNG', optimize=True)
        
        return save_path
    
    def generate_icon_set(self) -> Dict[str, str]:
        """Generate complete icon set for different platforms"""
        icon_sizes = {
            'android_ldpi': 36,
            'android_mdpi': 48,
            'android_hdpi': 72,
            'android_xhdpi': 96,
            'android_xxhdpi': 144,
            'android_xxxhdpi': 192,
            'ios_small': 29,
            'ios_medium': 40,
            'ios_large': 60,
            'ios_iphone': 120,
            'ios_ipad': 152,
            'ios_app_store': 1024,
            'windows': 256,
            'web_favicon': 32,
            'web_large': 512
        }
        
        generated_icons = {}
        
        for platform, size in icon_sizes.items():
            icon_path = self.generate_game_icon(size, 
                f"{self.assets_path}/icons/icon_{platform}_{size}x{size}.png")
            generated_icons[platform] = icon_path
        
        return generated_icons
    
    def _optimize_image_size(self, image: Image.Image, max_size_kb: int) -> Image.Image:
        """Optimize image to meet size requirements"""
        quality = 90
        
        while quality > 10:
            buffer = io.BytesIO()
            image.save(buffer, format=self.spec.format.value.upper(), 
                      quality=quality, optimize=True)
            
            size_kb = len(buffer.getvalue()) / 1024
            
            if size_kb <= max_size_kb:
                break
                
            quality -= 10
        
        return image
    
    def generate_promotional_set(self) -> Dict[str, str]:
        """Generate complete set of promotional images"""
        generated_assets = {}
        
        # Main thumbnail
        main_thumb = self.generate_main_thumbnail()
        generated_assets['main_thumbnail'] = main_thumb
        
        # Icon set
        icon_set = self.generate_icon_set()
        generated_assets['icons'] = icon_set
        
        # Additional promotional images
        # Social media variants
        social_sizes = {
            'facebook_cover': (820, 312),
            'twitter_header': (1500, 500),
            'instagram_post': (1080, 1080),
            'youtube_thumbnail': (1280, 720)
        }
        
        for social_type, (width, height) in social_sizes.items():
            # Create variant based on main thumbnail
            original = Image.open(main_thumb)
            
            if width != height:  # Rectangular formats
                resized = original.resize((width, height), Image.Resampling.LANCZOS)
            else:  # Square format (Instagram)
                # Create square version with focused composition
                size = min(original.size)
                left = (original.width - size) // 2
                top = (original.height - size) // 2
                cropped = original.crop((left, top, left + size, top + size))
                resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
            
            social_path = f"{self.assets_path}/thumbnails/{social_type}.{self.spec.format.value}"
            resized.save(social_path, format=self.spec.format.value.upper(), 
                        quality=self.spec.quality, optimize=True)
            
            generated_assets[social_type] = social_path
        
        return generated_assets
    
    def create_asset_manifest(self, generated_assets: Dict[str, str]) -> str:
        """Create a manifest file listing all generated assets"""
        manifest = {
            'generated_at': str(datetime.now()),
            'spec': {
                'thumbnail': {
                    'width': self.spec.width,
                    'height': self.spec.height,
                    'format': self.spec.format.value,
                    'quality': self.spec.quality,
                    'max_size_kb': self.spec.max_size_kb
                },
                'color_palette': {
                    'dark_red': self.colors.dark_red,
                    'void_black': self.colors.void_black,
                    'gold': self.colors.gold,
                    'void_purple': self.colors.void_purple,
                    'crimson': self.colors.crimson,
                    'fire_orange': self.colors.fire_orange
                }
            },
            'assets': generated_assets
        }
        
        manifest_path = f"{self.assets_path}/asset_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return manifest_path

# Example usage and CLI interface
if __name__ == "__main__":
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='Generate Kingdom of Aldoria promotional assets')
    parser.add_argument('--type', choices=['thumbnail', 'icon', 'icon-set', 'all'], 
                       default='all', help='Type of asset to generate')
    parser.add_argument('--size', type=int, default=512, help='Icon size (for single icon)')
    parser.add_argument('--output', type=str, default='assets/images', help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = ThumbnailGenerator(args.output)
    
    print("🎨 Kingdom of Aldoria Asset Generator")
    print("=" * 50)
    
    generated_assets = {}
    
    if args.type in ['thumbnail', 'all']:
        print("📸 Generating main thumbnail...")
        thumbnail_path = generator.generate_main_thumbnail()
        generated_assets['main_thumbnail'] = thumbnail_path
        print(f"✅ Thumbnail saved: {thumbnail_path}")
    
    if args.type in ['icon', 'all']:
        print(f"🎯 Generating game icon ({args.size}x{args.size})...")
        icon_path = generator.generate_game_icon(args.size)
        generated_assets['game_icon'] = icon_path
        print(f"✅ Icon saved: {icon_path}")
    
    if args.type in ['icon-set', 'all']:
        print("📱 Generating complete icon set...")
        icon_set = generator.generate_icon_set()
        generated_assets.update(icon_set)
        print(f"✅ Generated {len(icon_set)} platform icons")
    
    if args.type == 'all':
        print("🌟 Generating promotional set...")
        promo_assets = generator.generate_promotional_set()
        generated_assets.update(promo_assets)
        print(f"✅ Generated {len(promo_assets)} promotional assets")
        
        # Create manifest
        manifest_path = generator.create_asset_manifest(generated_assets)
        print(f"📋 Asset manifest saved: {manifest_path}")
    
    print("\n🎉 Asset generation complete!")
    print(f"📁 Assets saved to: {args.output}")
    print(f"📊 Total assets generated: {len(generated_assets)}")