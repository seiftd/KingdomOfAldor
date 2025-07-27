"""
Flask API Routes for PixelLab.ai Asset Generation
Provides REST endpoints for the admin dashboard to generate game assets
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

from pixellab_ai_manager import (
    PixelLabAIManager, 
    AssetGenerationRequest, 
    AssetType, 
    AssetRarity,
    QUICK_GENERATION_TEMPLATES
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global manager instance
pixellab_manager = None

def get_pixellab_manager():
    """Get or create PixelLab.ai manager instance"""
    global pixellab_manager
    if pixellab_manager is None:
        api_key = os.getenv('PIXELLAB_API_KEY')
        if not api_key:
            raise ValueError("PIXELLAB_API_KEY environment variable not set")
        pixellab_manager = PixelLabAIManager(api_key=api_key)
    return pixellab_manager

@app.route('/api/pixellab/status', methods=['GET'])
def api_status():
    """Check API status and PixelLab.ai connection"""
    try:
        manager = get_pixellab_manager()
        return jsonify({
            "status": "online",
            "service": "PixelLab.ai Asset Generation API",
            "version": "1.0.0",
            "supported_assets": [asset.value for asset in AssetType],
            "supported_rarities": [rarity.value for rarity in AssetRarity],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/pixellab/generate', methods=['POST'])
def generate_asset():
    """Generate a single asset using PixelLab.ai"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['asset_type', 'name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create generation request
        asset_request = AssetGenerationRequest(
            asset_type=AssetType(data['asset_type']),
            name=data['name'],
            description=data['description'],
            rarity=AssetRarity(data['rarity']) if data.get('rarity') else None,
            style=data.get('style', 'fantasy'),
            width=data.get('width', 1024),
            height=data.get('height', 1024),
            additional_params=data.get('additional_params', {})
        )
        
        # Run async generation
        async def generate():
            async with get_pixellab_manager() as manager:
                return await manager.generate_asset(asset_request)
        
        asset = asyncio.run(generate())
        
        # Return asset information
        return jsonify({
            "success": True,
            "asset": {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value,
                "url": asset.url,
                "local_path": asset.local_path,
                "metadata": asset.metadata,
                "created_at": asset.created_at.isoformat(),
                "status": asset.status
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Asset generation failed: {str(e)}")
        return jsonify({"error": "Asset generation failed"}), 500

@app.route('/api/pixellab/generate/weapon-set', methods=['POST'])
def generate_weapon_set():
    """Generate a complete weapon set with variations"""
    try:
        data = request.get_json()
        
        required_fields = ['weapon_name', 'rarity']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        weapon_name = data['weapon_name']
        rarity = AssetRarity(data['rarity'])
        
        # Run async generation
        async def generate():
            async with get_pixellab_manager() as manager:
                return await manager.generate_weapon_set(weapon_name, rarity)
        
        assets = asyncio.run(generate())
        
        # Return asset set information
        return jsonify({
            "success": True,
            "weapon_set": {
                "name": weapon_name,
                "rarity": rarity.value,
                "assets": [
                    {
                        "id": asset.id,
                        "name": asset.name,
                        "type": asset.asset_type.value,
                        "url": asset.url,
                        "local_path": asset.local_path,
                        "created_at": asset.created_at.isoformat()
                    }
                    for asset in assets
                ]
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Weapon set generation failed: {str(e)}")
        return jsonify({"error": "Weapon set generation failed"}), 500

@app.route('/api/pixellab/generate/hero-set', methods=['POST'])
def generate_hero_set():
    """Generate a complete hero set with transformations"""
    try:
        data = request.get_json()
        
        required_fields = ['hero_name', 'transformations']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        hero_name = data['hero_name']
        transformations = data['transformations']
        
        # Run async generation
        async def generate():
            async with get_pixellab_manager() as manager:
                return await manager.generate_hero_set(hero_name, transformations)
        
        assets = asyncio.run(generate())
        
        # Return asset set information
        return jsonify({
            "success": True,
            "hero_set": {
                "name": hero_name,
                "transformations": transformations,
                "assets": [
                    {
                        "id": asset.id,
                        "name": asset.name,
                        "type": asset.asset_type.value,
                        "url": asset.url,
                        "local_path": asset.local_path,
                        "created_at": asset.created_at.isoformat()
                    }
                    for asset in assets
                ]
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Hero set generation failed: {str(e)}")
        return jsonify({"error": "Hero set generation failed"}), 500

@app.route('/api/pixellab/generate/map-set', methods=['POST'])
def generate_map_set():
    """Generate a complete map set with different areas"""
    try:
        data = request.get_json()
        
        required_fields = ['map_name', 'areas']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        map_name = data['map_name']
        areas = data['areas']
        
        # Run async generation
        async def generate():
            async with get_pixellab_manager() as manager:
                return await manager.generate_map_set(map_name, areas)
        
        assets = asyncio.run(generate())
        
        # Return asset set information
        return jsonify({
            "success": True,
            "map_set": {
                "name": map_name,
                "areas": areas,
                "assets": [
                    {
                        "id": asset.id,
                        "name": asset.name,
                        "type": asset.asset_type.value,
                        "url": asset.url,
                        "local_path": asset.local_path,
                        "created_at": asset.created_at.isoformat()
                    }
                    for asset in assets
                ]
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Map set generation failed: {str(e)}")
        return jsonify({"error": "Map set generation failed"}), 500

@app.route('/api/pixellab/templates', methods=['GET'])
def get_templates():
    """Get available quick generation templates"""
    return jsonify({
        "success": True,
        "templates": QUICK_GENERATION_TEMPLATES
    })

@app.route('/api/pixellab/generate/template', methods=['POST'])
def generate_from_template():
    """Generate assets from a predefined template"""
    try:
        data = request.get_json()
        
        required_fields = ['template_category', 'template_index']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        category = data['template_category']
        index = data['template_index']
        
        if category not in QUICK_GENERATION_TEMPLATES:
            return jsonify({"error": f"Invalid template category: {category}"}), 400
        
        templates = QUICK_GENERATION_TEMPLATES[category]
        if index >= len(templates):
            return jsonify({"error": f"Invalid template index: {index}"}), 400
        
        template = templates[index]
        
        # Create generation request from template
        asset_request = AssetGenerationRequest(
            asset_type=template['type'],
            name=template['name'],
            description=f"Generated from template: {template['name']}",
            rarity=template.get('rarity'),
            additional_params={
                "prompt_template": template['template'],
                **template.get('params', {})
            }
        )
        
        # Run async generation
        async def generate():
            async with get_pixellab_manager() as manager:
                return await manager.generate_asset(asset_request)
        
        asset = asyncio.run(generate())
        
        return jsonify({
            "success": True,
            "template_used": template['name'],
            "asset": {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value,
                "url": asset.url,
                "local_path": asset.local_path,
                "metadata": asset.metadata,
                "created_at": asset.created_at.isoformat(),
                "status": asset.status
            }
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Template generation failed: {str(e)}")
        return jsonify({"error": "Template generation failed"}), 500

@app.route('/api/pixellab/assets', methods=['GET'])
def list_assets():
    """List all generated assets"""
    try:
        asset_type_filter = request.args.get('type')
        asset_type = AssetType(asset_type_filter) if asset_type_filter else None
        
        # Run async listing
        async def list_assets():
            async with get_pixellab_manager() as manager:
                return await manager.list_generated_assets(asset_type)
        
        assets = asyncio.run(list_assets())
        
        return jsonify({
            "success": True,
            "assets": [
                {
                    "id": asset.id,
                    "name": asset.name,
                    "type": asset.asset_type.value,
                    "url": asset.url,
                    "local_path": asset.local_path,
                    "metadata": asset.metadata,
                    "created_at": asset.created_at.isoformat(),
                    "status": asset.status
                }
                for asset in assets
            ]
        })
        
    except ValueError as e:
        return jsonify({"error": f"Invalid asset type: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Asset listing failed: {str(e)}")
        return jsonify({"error": "Asset listing failed"}), 500

@app.route('/api/pixellab/assets/<asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get specific asset information"""
    try:
        # For now, we'll look for the asset file by ID
        assets_dir = "assets/generated"
        asset_path = os.path.join(assets_dir, f"{asset_id}")
        
        if not os.path.exists(asset_path):
            return jsonify({"error": "Asset not found"}), 404
        
        # Return file info
        stat = os.stat(asset_path)
        return jsonify({
            "success": True,
            "asset": {
                "id": asset_id,
                "path": asset_path,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Asset retrieval failed: {str(e)}")
        return jsonify({"error": "Asset retrieval failed"}), 500

@app.route('/api/pixellab/assets/<asset_id>/download', methods=['GET'])
def download_asset(asset_id):
    """Download a generated asset"""
    try:
        assets_dir = "assets/generated"
        asset_path = os.path.join(assets_dir, asset_id)
        
        if not os.path.exists(asset_path):
            return jsonify({"error": "Asset not found"}), 404
        
        return send_file(asset_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Asset download failed: {str(e)}")
        return jsonify({"error": "Asset download failed"}), 500

@app.route('/api/pixellab/batch-generate', methods=['POST'])
def batch_generate():
    """Generate multiple assets in batch"""
    try:
        data = request.get_json()
        
        if 'requests' not in data:
            return jsonify({"error": "Missing 'requests' field"}), 400
        
        requests = data['requests']
        results = []
        
        async def generate_batch():
            async with get_pixellab_manager() as manager:
                batch_results = []
                for req_data in requests:
                    try:
                        asset_request = AssetGenerationRequest(
                            asset_type=AssetType(req_data['asset_type']),
                            name=req_data['name'],
                            description=req_data['description'],
                            rarity=AssetRarity(req_data['rarity']) if req_data.get('rarity') else None,
                            style=req_data.get('style', 'fantasy'),
                            width=req_data.get('width', 1024),
                            height=req_data.get('height', 1024),
                            additional_params=req_data.get('additional_params', {})
                        )
                        
                        asset = await manager.generate_asset(asset_request)
                        batch_results.append({
                            "success": True,
                            "asset": {
                                "id": asset.id,
                                "name": asset.name,
                                "type": asset.asset_type.value,
                                "url": asset.url,
                                "local_path": asset.local_path,
                                "created_at": asset.created_at.isoformat()
                            }
                        })
                        
                    except Exception as e:
                        batch_results.append({
                            "success": False,
                            "error": str(e),
                            "request": req_data.get('name', 'Unknown')
                        })
                
                return batch_results
        
        results = asyncio.run(generate_batch())
        
        return jsonify({
            "success": True,
            "batch_results": results,
            "total_requests": len(requests),
            "successful": len([r for r in results if r['success']]),
            "failed": len([r for r in results if not r['success']])
        })
        
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        return jsonify({"error": "Batch generation failed"}), 500

@app.route('/api/pixellab/prompts', methods=['GET'])
def get_prompt_templates():
    """Get available prompt templates for different asset types"""
    try:
        manager = get_pixellab_manager()
        return jsonify({
            "success": True,
            "prompt_templates": manager.asset_prompts
        })
    except Exception as e:
        logger.error(f"Failed to get prompt templates: {str(e)}")
        return jsonify({"error": "Failed to get prompt templates"}), 500

@app.route('/api/pixellab/config', methods=['GET'])
def get_config():
    """Get PixelLab.ai configuration and supported options"""
    return jsonify({
        "success": True,
        "config": {
            "asset_types": [
                {"value": asset.value, "label": asset.value.title()} 
                for asset in AssetType
            ],
            "rarities": [
                {"value": rarity.value, "label": rarity.value.title()} 
                for rarity in AssetRarity
            ],
            "styles": [
                "fantasy", "sci-fi", "cartoon", "realistic", "anime", 
                "pixelart", "watercolor", "oil_painting"
            ],
            "dimensions": {
                "weapons": {"width": 1024, "height": 1024},
                "heroes": {"width": 512, "height": 768},
                "maps": {"width": 1920, "height": 1080},
                "icons": {"width": 512, "height": 512},
                "gems": {"width": 256, "height": 256}
            }
        }
    })

if __name__ == '__main__':
    # Ensure assets directory exists
    os.makedirs('assets/generated', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)