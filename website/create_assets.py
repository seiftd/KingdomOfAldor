#!/usr/bin/env python3
"""
Create placeholder assets for Kingdom of Aldoria Payment Website
Generates logos, images and icons needed for the website
"""

import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_directories():
    """Create asset directories"""
    directories = [
        "assets",
        "assets/images",
        "assets/icons"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_logo():
    """Create Kingdom of Aldoria logo"""
    # Create a 200x200 logo
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a castle-like logo
    # Main castle body
    draw.rectangle([60, 120, 140, 180], fill=(75, 0, 130), outline=(255, 215, 0), width=3)
    
    # Castle towers
    draw.rectangle([40, 100, 70, 180], fill=(75, 0, 130), outline=(255, 215, 0), width=2)
    draw.rectangle([130, 100, 160, 180], fill=(75, 0, 130), outline=(255, 215, 0), width=2)
    
    # Tower tops
    draw.polygon([(25, 100), (55, 80), (85, 100)], fill=(255, 215, 0))
    draw.polygon([(115, 100), (145, 80), (175, 100)], fill=(255, 215, 0))
    
    # Main castle roof
    draw.polygon([(50, 120), (100, 90), (150, 120)], fill=(255, 215, 0))
    
    # Castle gate
    draw.rectangle([85, 150, 115, 180], fill=(0, 0, 0))
    
    # Windows
    draw.rectangle([50, 130, 60, 145], fill=(255, 255, 100))
    draw.rectangle([140, 130, 150, 145], fill=(255, 255, 100))
    
    # Save logo
    img.save('assets/logo.png')
    print("Created logo.png")

def create_knight_hero():
    """Create knight hero image"""
    img = Image.new('RGBA', (400, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Knight silhouette
    # Body
    draw.ellipse([150, 200, 250, 300], fill=(100, 149, 237), outline=(255, 215, 0), width=3)
    
    # Head
    draw.ellipse([175, 150, 225, 200], fill=(255, 220, 177), outline=(255, 215, 0), width=2)
    
    # Helmet
    draw.arc([170, 140, 230, 180], 0, 180, fill=(192, 192, 192), width=8)
    
    # Sword
    draw.rectangle([260, 180, 270, 280], fill=(192, 192, 192))
    draw.rectangle([255, 170, 275, 185], fill=(255, 215, 0))
    
    # Shield
    draw.ellipse([130, 220, 160, 280], fill=(75, 0, 130), outline=(255, 215, 0), width=3)
    
    # Cape
    draw.polygon([(180, 250), (120, 300), (120, 400), (200, 380), (220, 250)], fill=(148, 0, 211))
    
    img.save('assets/knight-hero.png')
    print("Created knight-hero.png")

def create_item_images():
    """Create placeholder item images"""
    items = [
        ('void-scythe', (138, 43, 226)),     # Purple scythe
        ('solar-sword', (255, 140, 0)),      # Orange sword  
        ('void-knight', (75, 0, 130))        # Purple armor
    ]
    
    for item_name, color in items:
        img = Image.new('RGBA', (150, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if 'scythe' in item_name:
            # Draw scythe
            draw.line([(75, 20), (75, 130)], fill=color, width=8)
            draw.arc([60, 20, 100, 60], 0, 180, fill=color, width=6)
            draw.rectangle([70, 120, 80, 140], fill=(139, 69, 19))
            
        elif 'sword' in item_name:
            # Draw sword
            draw.rectangle([70, 20, 80, 110], fill=color)
            draw.polygon([(65, 20), (75, 10), (85, 20)], fill=color)
            draw.rectangle([65, 110, 85, 125], fill=(255, 215, 0))
            draw.rectangle([70, 125, 80, 140], fill=(139, 69, 19))
            
        elif 'knight' in item_name:
            # Draw armor
            draw.rectangle([60, 40, 90, 120], fill=color, outline=(255, 215, 0), width=2)
            draw.ellipse([65, 30, 85, 50], fill=color, outline=(255, 215, 0), width=2)
            draw.rectangle([50, 80, 70, 130], fill=color)
            draw.rectangle([80, 80, 100, 130], fill=color)
        
        img.save(f'assets/{item_name}.png')
        print(f"Created {item_name}.png")

def create_payment_logos():
    """Create payment method logos"""
    
    # RedotPay logo
    img = Image.new('RGB', (120, 60), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # RedotPay - red circle with "R"
    draw.ellipse([10, 10, 50, 50], fill=(220, 20, 60))
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((25, 22), "R", fill=(255, 255, 255), font=font, anchor="mm")
    draw.text((60, 30), "RedotPay", fill=(220, 20, 60), font=font, anchor="lm")
    
    img.save('assets/redotpay-logo.png')
    print("Created redotpay-logo.png")
    
    # Binance logo
    img = Image.new('RGB', (120, 60), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Binance - yellow diamond with "B"
    draw.polygon([(30, 10), (50, 20), (30, 30), (10, 20)], fill=(243, 186, 47))
    draw.text((30, 20), "B", fill=(0, 0, 0), font=font, anchor="mm")
    draw.text((60, 30), "Binance", fill=(243, 186, 47), font=font, anchor="lm")
    
    img.save('assets/binance-logo.png')
    print("Created binance-logo.png")

def create_favicon():
    """Create favicon"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Mini castle
    draw.rectangle([8, 16, 24, 28], fill=(255, 215, 0))
    draw.polygon([(6, 16), (16, 8), (26, 16)], fill=(75, 0, 130))
    draw.rectangle([14, 20, 18, 28], fill=(0, 0, 0))
    
    img.save('assets/favicon.ico')
    print("Created favicon.ico")

def create_background_pattern():
    """Create background pattern"""
    img = Image.new('RGBA', (200, 200), (30, 30, 62, 100))
    draw = ImageDraw.Draw(img)
    
    # Create mystical pattern
    for i in range(0, 200, 40):
        for j in range(0, 200, 40):
            # Small stars
            draw.polygon([
                (i+20, j+10), (i+22, j+18), (i+30, j+18), 
                (i+24, j+24), (i+26, j+32), (i+20, j+28),
                (i+14, j+32), (i+16, j+24), (i+10, j+18), (i+18, j+18)
            ], fill=(255, 215, 0, 50))
    
    img.save('assets/bg-pattern.png')
    print("Created bg-pattern.png")

def main():
    """Generate all website assets"""
    print("🎨 Creating Kingdom of Aldoria Website Assets 🎨")
    print("=" * 50)
    
    try:
        create_directories()
        print("\n🏰 Creating logos and branding...")
        create_logo()
        create_favicon()
        
        print("\n⚔️ Creating character assets...")
        create_knight_hero()
        create_item_images()
        
        print("\n💳 Creating payment logos...")
        create_payment_logos()
        
        print("\n🎭 Creating backgrounds...")
        create_background_pattern()
        
        print("\n✅ Asset creation complete!")
        print("All placeholder assets generated successfully")
        print("\nGenerated files:")
        print("- assets/logo.png")
        print("- assets/favicon.ico") 
        print("- assets/knight-hero.png")
        print("- assets/void-scythe.png")
        print("- assets/solar-sword.png")
        print("- assets/void-knight.png")
        print("- assets/redotpay-logo.png")
        print("- assets/binance-logo.png")
        print("- assets/bg-pattern.png")
        
    except Exception as e:
        print(f"❌ Error creating assets: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎨 Website assets ready! Your payment portal looks amazing.")
    else:
        print("\n❌ Asset creation failed.")