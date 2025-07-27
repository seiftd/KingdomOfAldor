"""
PixelLab.ai Asset Generation Manager
Integrates with PixelLab.ai API to generate game assets from admin dashboard
"""

import asyncio
import aiohttp
import json
import os
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetType(Enum):
    """Types of assets that can be generated"""
    WEAPON = "weapon"
    HERO = "hero"
    MAP = "map"
    GEM = "gem"
    ICON = "icon"
    SKIN = "skin"
    BOSS = "boss"
    ENVIRONMENT = "environment"
    UI_ELEMENT = "ui_element"
    PROMOTIONAL = "promotional"

class AssetRarity(Enum):
    """Asset rarity levels"""
    WOOD = "wood"
    IRON = "iron"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    EMERALD = "emerald"
    DIAMOND = "diamond"
    ELITE = "elite"
    HYPER = "hyper"
    LEGENDARY = "legendary"

@dataclass
class AssetGenerationRequest:
    """Request structure for asset generation"""
    asset_type: AssetType
    name: str
    description: str
    rarity: Optional[AssetRarity] = None
    style: str = "fantasy"
    width: int = 1024
    height: int = 1024
    additional_params: Dict[str, Any] = None

@dataclass
class GeneratedAsset:
    """Generated asset information"""
    id: str
    asset_type: AssetType
    name: str
    url: str
    local_path: str
    metadata: Dict[str, Any]
    created_at: datetime
    status: str

class PixelLabAIManager:
    """Main manager for PixelLab.ai integration"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.pixellab.ai"):
        self.api_key = api_key or os.getenv('PIXELLAB_API_KEY')
        self.base_url = base_url
        self.session = None
        self.asset_prompts = self._load_asset_prompts()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _load_asset_prompts(self) -> Dict[str, Dict[str, str]]:
        """Load pre-defined prompts for different asset types"""
        return {
            "weapon": {
                "legendary_sword": "Epic fantasy sword, glowing {color} blade with {effect} emanating from edges, ornate crossguard, detailed metalwork, mystical atmosphere, 4K resolution",
                "legendary_bow": "Legendary bow, {material} frame with {energy} veins, crystalline string, {projectile} arrows, cosmic effects, ethereal glow",
                "legendary_staff": "Ancient wizard staff, {wood_type} shaft with {metal} inlay, {crystal} orb containing {magic_effect}, floating fragments, mystical energy",
                "elite_blade": "Elite tier sword, {style} design, {material} blade with {pattern} patterns, {handle_material} grip, {special_effect} energy",
                "void_weapon": "Void-touched {weapon_type}, matte black frame with purple energy, ethereal effects, shadow particles, dark energy aura"
            },
            "hero": {
                "dragon_lord": "Epic fantasy hero transformation, Dragon Lord {name}, dragon scale armor glowing with inner fire, dragon wings, flame aura, heroic pose",
                "cosmic_emperor": "Ascended hero form, Cosmic Emperor {name}, starlight armor, cosmic crown, galaxy patterns, reality distortion effects",
                "void_knight": "Dark knight transformation, Void Knight {name}, black armor with purple void energy, mysterious helmet, ethereal cape",
                "base_knight": "Fantasy knight hero, {name} base form, polished steel armor with {color} accents, noble bearing, royal crest"
            },
            "map": {
                "forest": "Dark fantasy forest environment, twisted ancient trees, moonlight filtering through canopy, mysterious fog, glowing elements, atmospheric lighting",
                "ice_peaks": "Frozen mountain environment, ice-covered peaks, aurora borealis, crystalline formations, magical winter landscape",
                "volcanic": "Volcanic hellscape, active lava flows, smoking peaks, cracked ground, ash-filled sky, apocalyptic atmosphere",
                "desert": "Mystical desert environment, sand dunes, ancient ruins, ghostly spirits, oasis, starry night sky, ethereal atmosphere",
                "underwater": "Underwater dungeon, deep ocean, bioluminescent creatures, coral formations, ancient ruins, mysterious aquatic atmosphere",
                "floating_islands": "Floating islands environment, ancient ruins suspended in sky, stone bridges, flowing clouds, ethereal atmosphere"
            },
            "gem": {
                "currency": "Game currency gem, multifaceted crystal, {color} glow, transparent with light reflections, sparkle effects, UI suitable",
                "magic_gem": "Magical gem, {type} crystal, {color} energy emanating, mystical properties, floating with {effect} aura",
                "rare_crystal": "Rare crystal formation, {material} structure, {color} internal glow, geometric patterns, precious stone"
            },
            "boss": {
                "dragon": "Massive {color} dragon boss, {scale_type} scales with glowing {accent_color} cracks, enormous wingspan, {breath_type} breath, fierce eyes",
                "corrupted_champion": "Fallen hero boss, corrupted champion, twisted armor leaking dark energy, glowing red eyes, menacing presence"
            }
        }
    
    async def generate_asset(self, request: AssetGenerationRequest) -> GeneratedAsset:
        """Generate a single asset using PixelLab.ai"""
        try:
            # Build the prompt based on asset type and parameters
            prompt = self._build_prompt(request)
            
            # Prepare API request
            payload = {
                "prompt": prompt,
                "width": request.width,
                "height": request.height,
                "style": request.style,
                "quality": "high",
                "steps": 50,
                "guidance_scale": 7.5
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            async with self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return await self._process_generation_result(request, result)
                else:
                    error_text = await response.text()
                    raise Exception(f"PixelLab.ai API error: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Asset generation failed: {str(e)}")
            raise
    
    def _build_prompt(self, request: AssetGenerationRequest) -> str:
        """Build appropriate prompt based on asset type and parameters"""
        asset_type = request.asset_type.value
        base_prompts = self.asset_prompts.get(asset_type, {})
        
        # Get base prompt or use description
        if request.additional_params and "prompt_template" in request.additional_params:
            template = request.additional_params["prompt_template"]
            prompt = base_prompts.get(template, request.description)
        else:
            prompt = request.description
        
        # Add rarity-specific enhancements
        if request.rarity:
            prompt = self._enhance_prompt_with_rarity(prompt, request.rarity)
        
        # Add Kingdom of Aldoria style elements
        prompt += ", Kingdom of Aldoria game art style, high quality fantasy art, detailed, vibrant colors"
        
        # Format with additional parameters
        if request.additional_params:
            try:
                prompt = prompt.format(**request.additional_params)
            except KeyError:
                # If formatting fails, use original prompt
                pass
        
        return prompt
    
    def _enhance_prompt_with_rarity(self, prompt: str, rarity: AssetRarity) -> str:
        """Enhance prompt based on rarity level"""
        rarity_enhancements = {
            AssetRarity.LEGENDARY: ", legendary quality, glowing aura, mystical effects, golden accents",
            AssetRarity.HYPER: ", hyper-advanced design, energy effects, futuristic elements",
            AssetRarity.ELITE: ", elite craftsmanship, superior materials, enhanced details",
            AssetRarity.DIAMOND: ", diamond-like brilliance, crystalline effects, prismatic colors",
            AssetRarity.EMERALD: ", emerald green glow, nature-inspired elements, precious stone quality",
            AssetRarity.PLATINUM: ", platinum finish, metallic sheen, refined elegance",
            AssetRarity.GOLD: ", golden glow, warm lighting, rich textures",
            AssetRarity.SILVER: ", silver highlights, cool metallic tones, polished finish",
            AssetRarity.IRON: ", sturdy iron construction, weathered but reliable",
            AssetRarity.WOOD: ", natural wood grain, earthy tones, organic textures"
        }
        
        return prompt + rarity_enhancements.get(rarity, "")
    
    async def _process_generation_result(self, request: AssetGenerationRequest, result: Dict) -> GeneratedAsset:
        """Process the generation result and save the asset"""
        try:
            # Extract image data
            image_url = result.get("url")
            image_data = result.get("image_data")  # base64 encoded
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{request.asset_type.value}_{request.name.lower().replace(' ', '_')}_{timestamp}.png"
            local_path = f"assets/generated/{filename}"
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Save image locally
            if image_data:
                # If base64 data is provided
                image_bytes = base64.b64decode(image_data)
                with open(local_path, "wb") as f:
                    f.write(image_bytes)
            elif image_url:
                # If URL is provided, download the image
                async with self.session.get(image_url) as img_response:
                    if img_response.status == 200:
                        image_bytes = await img_response.read()
                        with open(local_path, "wb") as f:
                            f.write(image_bytes)
            
            # Create asset record
            asset = GeneratedAsset(
                id=result.get("id", f"asset_{timestamp}"),
                asset_type=request.asset_type,
                name=request.name,
                url=image_url or f"/assets/generated/{filename}",
                local_path=local_path,
                metadata={
                    "rarity": request.rarity.value if request.rarity else None,
                    "style": request.style,
                    "dimensions": f"{request.width}x{request.height}",
                    "prompt_used": self._build_prompt(request),
                    "additional_params": request.additional_params or {}
                },
                created_at=datetime.now(),
                status="completed"
            )
            
            logger.info(f"Successfully generated asset: {asset.name}")
            return asset
            
        except Exception as e:
            logger.error(f"Failed to process generation result: {str(e)}")
            raise
    
    async def generate_weapon_set(self, weapon_name: str, rarity: AssetRarity) -> List[GeneratedAsset]:
        """Generate a complete weapon set (different angles/variations)"""
        variations = ["main", "icon", "inventory"]
        assets = []
        
        for variation in variations:
            request = AssetGenerationRequest(
                asset_type=AssetType.WEAPON,
                name=f"{weapon_name}_{variation}",
                description=f"{weapon_name} weapon, {variation} view",
                rarity=rarity,
                additional_params={
                    "prompt_template": "legendary_sword" if "sword" in weapon_name.lower() else "legendary_bow",
                    "color": self._get_rarity_color(rarity),
                    "effect": self._get_rarity_effect(rarity)
                }
            )
            
            asset = await self.generate_asset(request)
            assets.append(asset)
        
        return assets
    
    async def generate_hero_set(self, hero_name: str, transformations: List[str]) -> List[GeneratedAsset]:
        """Generate a complete hero set with different transformations"""
        assets = []
        
        for transformation in transformations:
            request = AssetGenerationRequest(
                asset_type=AssetType.HERO,
                name=f"{hero_name}_{transformation}",
                description=f"{hero_name} in {transformation} form",
                rarity=AssetRarity.LEGENDARY,
                width=512,
                height=768,  # Portrait ratio for characters
                additional_params={
                    "prompt_template": transformation.lower().replace(" ", "_"),
                    "name": hero_name
                }
            )
            
            asset = await self.generate_asset(request)
            assets.append(asset)
        
        return assets
    
    async def generate_map_set(self, map_name: str, areas: List[str]) -> List[GeneratedAsset]:
        """Generate a complete map set with different areas"""
        assets = []
        
        for area in areas:
            request = AssetGenerationRequest(
                asset_type=AssetType.MAP,
                name=f"{map_name}_{area}",
                description=f"{map_name} - {area} area",
                width=1920,
                height=1080,  # Landscape ratio for environments
                additional_params={
                    "prompt_template": area.lower().replace(" ", "_")
                }
            )
            
            asset = await self.generate_asset(request)
            assets.append(asset)
        
        return assets
    
    def _get_rarity_color(self, rarity: AssetRarity) -> str:
        """Get color associated with rarity"""
        color_map = {
            AssetRarity.LEGENDARY: "golden",
            AssetRarity.HYPER: "cosmic purple",
            AssetRarity.ELITE: "brilliant white",
            AssetRarity.DIAMOND: "crystal clear",
            AssetRarity.EMERALD: "emerald green",
            AssetRarity.PLATINUM: "platinum silver",
            AssetRarity.GOLD: "golden yellow",
            AssetRarity.SILVER: "silver white",
            AssetRarity.IRON: "steel gray",
            AssetRarity.WOOD: "natural brown"
        }
        return color_map.get(rarity, "golden")
    
    def _get_rarity_effect(self, rarity: AssetRarity) -> str:
        """Get visual effect associated with rarity"""
        effect_map = {
            AssetRarity.LEGENDARY: "divine light",
            AssetRarity.HYPER: "cosmic energy",
            AssetRarity.ELITE: "brilliant aura",
            AssetRarity.DIAMOND: "prismatic reflections",
            AssetRarity.EMERALD: "nature magic",
            AssetRarity.PLATINUM: "metallic shine",
            AssetRarity.GOLD: "warm glow",
            AssetRarity.SILVER: "cool gleam",
            AssetRarity.IRON: "sturdy presence",
            AssetRarity.WOOD: "natural grain"
        }
        return effect_map.get(rarity, "magical aura")
    
    async def get_generation_status(self, generation_id: str) -> Dict:
        """Check the status of an ongoing generation"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with self.session.get(
            f"{self.base_url}/status/{generation_id}",
            headers=headers
        ) as response:
            return await response.json()
    
    async def list_generated_assets(self, asset_type: AssetType = None) -> List[GeneratedAsset]:
        """List all generated assets, optionally filtered by type"""
        # This would typically query your database
        # For now, we'll scan the generated assets directory
        assets = []
        assets_dir = "assets/generated"
        
        if os.path.exists(assets_dir):
            for filename in os.listdir(assets_dir):
                if filename.endswith('.png'):
                    # Parse filename to extract asset info
                    parts = filename.replace('.png', '').split('_')
                    if len(parts) >= 3:
                        asset_type_str = parts[0]
                        asset_name = '_'.join(parts[1:-1])
                        timestamp = parts[-1]
                        
                        if not asset_type or asset_type.value == asset_type_str:
                            assets.append(GeneratedAsset(
                                id=filename,
                                asset_type=AssetType(asset_type_str),
                                name=asset_name,
                                url=f"/assets/generated/{filename}",
                                local_path=f"{assets_dir}/{filename}",
                                metadata={},
                                created_at=datetime.strptime(timestamp, "%Y%m%d_%H%M%S"),
                                status="completed"
                            ))
        
        return sorted(assets, key=lambda x: x.created_at, reverse=True)

# Predefined asset generation templates for quick access
QUICK_GENERATION_TEMPLATES = {
    "legendary_weapons": [
        {
            "name": "Godslayer Excalibur",
            "type": AssetType.WEAPON,
            "rarity": AssetRarity.LEGENDARY,
            "template": "legendary_sword",
            "params": {"color": "golden", "effect": "holy fire", "material": "divine steel"}
        },
        {
            "name": "Worldender Bow",
            "type": AssetType.WEAPON,
            "rarity": AssetRarity.LEGENDARY,
            "template": "legendary_bow",
            "params": {"material": "void crystal", "energy": "cosmic purple", "projectile": "starlight"}
        },
        {
            "name": "Staff of Omniscience",
            "type": AssetType.WEAPON,
            "rarity": AssetRarity.LEGENDARY,
            "template": "legendary_staff",
            "params": {"wood_type": "ancient oak", "metal": "silver", "crystal": "galaxy", "magic_effect": "swirling cosmos"}
        }
    ],
    "hero_transformations": [
        {
            "name": "Dragon Lord Arin",
            "type": AssetType.HERO,
            "template": "dragon_lord",
            "params": {"name": "Arin"}
        },
        {
            "name": "Cosmic Emperor Arin",
            "type": AssetType.HERO,
            "template": "cosmic_emperor",
            "params": {"name": "Arin"}
        },
        {
            "name": "Void Knight Arin",
            "type": AssetType.HERO,
            "template": "void_knight",
            "params": {"name": "Arin"}
        }
    ],
    "game_environments": [
        {
            "name": "Forest of Shadows",
            "type": AssetType.MAP,
            "template": "forest"
        },
        {
            "name": "Ice Peaks",
            "type": AssetType.MAP,
            "template": "ice_peaks"
        },
        {
            "name": "Volcanic Wasteland",
            "type": AssetType.MAP,
            "template": "volcanic"
        },
        {
            "name": "Desert of Souls",
            "type": AssetType.MAP,
            "template": "desert"
        }
    ]
}

# Usage example
async def main():
    """Example usage of PixelLabAIManager"""
    async with PixelLabAIManager() as manager:
        # Generate a legendary weapon
        weapon_request = AssetGenerationRequest(
            asset_type=AssetType.WEAPON,
            name="Godslayer Excalibur",
            description="Epic legendary sword with divine properties",
            rarity=AssetRarity.LEGENDARY,
            additional_params={
                "prompt_template": "legendary_sword",
                "color": "golden",
                "effect": "holy fire"
            }
        )
        
        weapon_asset = await manager.generate_asset(weapon_request)
        print(f"Generated weapon: {weapon_asset.name} at {weapon_asset.local_path}")

if __name__ == "__main__":
    asyncio.run(main())