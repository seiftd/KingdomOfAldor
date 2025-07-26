"""
Social Media Publishing API
Handles posting articles to Facebook, Instagram, Discord, and Twitter simultaneously
"""

import asyncio
import aiohttp
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import tweepy
import discord
from discord.ext import commands
import facebook
import requests
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Platform(Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    DISCORD = "discord"
    TWITTER = "twitter"

@dataclass
class SocialMediaPost:
    title: str
    content: str
    image_url: Optional[str] = None
    image_data: Optional[bytes] = None
    tags: List[str] = None
    platform_specific: Dict[Platform, Dict] = None
    schedule_time: Optional[datetime] = None

@dataclass
class PlatformConfig:
    platform: Platform
    api_keys: Dict[str, str]
    settings: Dict[str, Any]
    is_enabled: bool = True

class SocialMediaManager:
    def __init__(self):
        self.platforms = {}
        self.load_platform_configs()
        
    def load_platform_configs(self):
        """Load platform configurations from environment variables or config file"""
        # Load from environment variables or config file
        config_file = "config/social_media_config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = {}
        
        # Facebook Configuration
        facebook_config = PlatformConfig(
            platform=Platform.FACEBOOK,
            api_keys={
                "app_id": os.getenv("FACEBOOK_APP_ID", config_data.get("facebook", {}).get("app_id", "")),
                "app_secret": os.getenv("FACEBOOK_APP_SECRET", config_data.get("facebook", {}).get("app_secret", "")),
                "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN", config_data.get("facebook", {}).get("access_token", "")),
                "page_id": os.getenv("FACEBOOK_PAGE_ID", config_data.get("facebook", {}).get("page_id", ""))
            },
            settings={
                "max_length": 63206,
                "supports_images": True,
                "supports_videos": True
            }
        )
        
        # Instagram Configuration (via Facebook Graph API)
        instagram_config = PlatformConfig(
            platform=Platform.INSTAGRAM,
            api_keys={
                "access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN", config_data.get("instagram", {}).get("access_token", "")),
                "business_account_id": os.getenv("INSTAGRAM_BUSINESS_ID", config_data.get("instagram", {}).get("business_account_id", ""))
            },
            settings={
                "max_length": 2200,
                "supports_images": True,
                "supports_videos": True,
                "requires_image": True
            }
        )
        
        # Discord Configuration
        discord_config = PlatformConfig(
            platform=Platform.DISCORD,
            api_keys={
                "bot_token": os.getenv("DISCORD_BOT_TOKEN", config_data.get("discord", {}).get("bot_token", "")),
                "webhook_url": os.getenv("DISCORD_WEBHOOK_URL", config_data.get("discord", {}).get("webhook_url", "")),
                "channel_id": os.getenv("DISCORD_CHANNEL_ID", config_data.get("discord", {}).get("channel_id", ""))
            },
            settings={
                "max_length": 2000,
                "supports_embeds": True,
                "supports_images": True
            }
        )
        
        # Twitter Configuration
        twitter_config = PlatformConfig(
            platform=Platform.TWITTER,
            api_keys={
                "api_key": os.getenv("TWITTER_API_KEY", config_data.get("twitter", {}).get("api_key", "")),
                "api_secret": os.getenv("TWITTER_API_SECRET", config_data.get("twitter", {}).get("api_secret", "")),
                "access_token": os.getenv("TWITTER_ACCESS_TOKEN", config_data.get("twitter", {}).get("access_token", "")),
                "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET", config_data.get("twitter", {}).get("access_token_secret", "")),
                "bearer_token": os.getenv("TWITTER_BEARER_TOKEN", config_data.get("twitter", {}).get("bearer_token", ""))
            },
            settings={
                "max_length": 280,
                "supports_images": True,
                "supports_threads": True
            }
        )
        
        self.platforms = {
            Platform.FACEBOOK: facebook_config,
            Platform.INSTAGRAM: instagram_config,
            Platform.DISCORD: discord_config,
            Platform.TWITTER: twitter_config
        }
    
    async def publish_to_all_platforms(self, post: SocialMediaPost) -> Dict[Platform, Dict]:
        """Publish post to all enabled platforms simultaneously"""
        results = {}
        tasks = []
        
        for platform, config in self.platforms.items():
            if config.is_enabled and self._validate_platform_config(config):
                task = self._publish_to_platform(platform, post, config)
                tasks.append((platform, task))
        
        # Execute all publishing tasks concurrently
        for platform, task in tasks:
            try:
                result = await task
                results[platform] = {
                    "success": True,
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Failed to publish to {platform.value}: {str(e)}")
                results[platform] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
        
        return results
    
    async def _publish_to_platform(self, platform: Platform, post: SocialMediaPost, config: PlatformConfig):
        """Publish to a specific platform"""
        if platform == Platform.FACEBOOK:
            return await self._publish_to_facebook(post, config)
        elif platform == Platform.INSTAGRAM:
            return await self._publish_to_instagram(post, config)
        elif platform == Platform.DISCORD:
            return await self._publish_to_discord(post, config)
        elif platform == Platform.TWITTER:
            return await self._publish_to_twitter(post, config)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
    
    async def _publish_to_facebook(self, post: SocialMediaPost, config: PlatformConfig):
        """Publish to Facebook Page"""
        url = f"https://graph.facebook.com/v18.0/{config.api_keys['page_id']}/posts"
        
        # Prepare content
        content = f"{post.title}\n\n{post.content}"
        if len(content) > config.settings["max_length"]:
            content = content[:config.settings["max_length"]-3] + "..."
        
        # Add hashtags
        if post.tags:
            hashtags = " ".join([f"#{tag.replace(' ', '')}" for tag in post.tags])
            content += f"\n\n{hashtags}"
        
        payload = {
            "message": content,
            "access_token": config.api_keys["access_token"]
        }
        
        # Add image if provided
        if post.image_url:
            payload["link"] = post.image_url
        elif post.image_data:
            # Upload image first
            image_url = await self._upload_image_to_facebook(post.image_data, config)
            if image_url:
                payload["link"] = image_url
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                result = await response.json()
                if response.status == 200:
                    return {
                        "post_id": result.get("id"),
                        "platform": "facebook",
                        "url": f"https://facebook.com/{result.get('id')}"
                    }
                else:
                    raise Exception(f"Facebook API error: {result}")
    
    async def _publish_to_instagram(self, post: SocialMediaPost, config: PlatformConfig):
        """Publish to Instagram Business Account"""
        # Instagram requires an image
        if not post.image_url and not post.image_data:
            raise Exception("Instagram posts require an image")
        
        business_account_id = config.api_keys["business_account_id"]
        access_token = config.api_keys["access_token"]
        
        # Prepare caption
        caption = f"{post.title}\n\n{post.content}"
        if len(caption) > config.settings["max_length"]:
            caption = caption[:config.settings["max_length"]-3] + "..."
        
        # Add hashtags
        if post.tags:
            hashtags = " ".join([f"#{tag.replace(' ', '')}" for tag in post.tags])
            caption += f"\n\n{hashtags}"
        
        # Step 1: Create media object
        media_url = f"https://graph.facebook.com/v18.0/{business_account_id}/media"
        
        media_payload = {
            "image_url": post.image_url if post.image_url else await self._upload_image_for_instagram(post.image_data),
            "caption": caption,
            "access_token": access_token
        }
        
        async with aiohttp.ClientSession() as session:
            # Create media
            async with session.post(media_url, data=media_payload) as response:
                media_result = await response.json()
                if response.status != 200:
                    raise Exception(f"Instagram media creation error: {media_result}")
                
                media_id = media_result["id"]
            
            # Step 2: Publish media
            publish_url = f"https://graph.facebook.com/v18.0/{business_account_id}/media_publish"
            publish_payload = {
                "creation_id": media_id,
                "access_token": access_token
            }
            
            async with session.post(publish_url, data=publish_payload) as response:
                publish_result = await response.json()
                if response.status == 200:
                    return {
                        "post_id": publish_result.get("id"),
                        "platform": "instagram",
                        "url": f"https://instagram.com/p/{publish_result.get('id')}"
                    }
                else:
                    raise Exception(f"Instagram publish error: {publish_result}")
    
    async def _publish_to_discord(self, post: SocialMediaPost, config: PlatformConfig):
        """Publish to Discord via webhook"""
        webhook_url = config.api_keys["webhook_url"]
        
        # Create Discord embed
        embed = {
            "title": post.title,
            "description": post.content[:config.settings["max_length"]],
            "color": 0x3498db,  # Blue color
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Kingdom of Aldoria News",
                "icon_url": "https://your-game-icon-url.com/icon.png"
            }
        }
        
        # Add image if provided
        if post.image_url:
            embed["image"] = {"url": post.image_url}
        
        # Add fields for tags
        if post.tags:
            embed["fields"] = [{
                "name": "Tags",
                "value": ", ".join(post.tags),
                "inline": False
            }]
        
        payload = {
            "embeds": [embed],
            "username": "Kingdom of Aldoria Bot",
            "avatar_url": "https://your-game-icon-url.com/bot-avatar.png"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status in [200, 204]:
                    return {
                        "success": True,
                        "platform": "discord",
                        "webhook_response": response.status
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Discord webhook error: {error_text}")
    
    async def _publish_to_twitter(self, post: SocialMediaPost, config: PlatformConfig):
        """Publish to Twitter"""
        # Initialize Twitter API client
        client = tweepy.Client(
            bearer_token=config.api_keys["bearer_token"],
            consumer_key=config.api_keys["api_key"],
            consumer_secret=config.api_keys["api_secret"],
            access_token=config.api_keys["access_token"],
            access_token_secret=config.api_keys["access_token_secret"],
            wait_on_rate_limit=True
        )
        
        # Prepare tweet content
        content = f"{post.title}\n\n{post.content}"
        
        # Add hashtags
        if post.tags:
            hashtags = " ".join([f"#{tag.replace(' ', '')}" for tag in post.tags])
            content += f"\n\n{hashtags}"
        
        # Handle Twitter's character limit with threading if necessary
        max_length = config.settings["max_length"]
        
        if len(content) <= max_length:
            # Single tweet
            try:
                media_ids = None
                if post.image_data:
                    # Upload image
                    api_v1 = tweepy.API(tweepy.OAuth1UserHandler(
                        config.api_keys["api_key"],
                        config.api_keys["api_secret"],
                        config.api_keys["access_token"],
                        config.api_keys["access_token_secret"]
                    ))
                    
                    media = api_v1.media_upload(filename="post_image.jpg", file=io.BytesIO(post.image_data))
                    media_ids = [media.media_id]
                
                response = client.create_tweet(text=content, media_ids=media_ids)
                return {
                    "tweet_id": response.data["id"],
                    "platform": "twitter",
                    "url": f"https://twitter.com/user/status/{response.data['id']}"
                }
            except Exception as e:
                raise Exception(f"Twitter API error: {str(e)}")
        else:
            # Create thread
            return await self._create_twitter_thread(client, content, post.image_data, config)
    
    async def _create_twitter_thread(self, client, content: str, image_data: bytes, config: PlatformConfig):
        """Create a Twitter thread for long content"""
        max_length = config.settings["max_length"] - 10  # Leave space for thread indicators
        
        # Split content into chunks
        chunks = []
        words = content.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk + " " + word) <= max_length:
                current_chunk += " " + word if current_chunk else word
            else:
                chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Post thread
        thread_tweets = []
        previous_tweet_id = None
        
        for i, chunk in enumerate(chunks):
            tweet_text = f"{chunk} ({i+1}/{len(chunks)})"
            
            media_ids = None
            if i == 0 and image_data:  # Only add image to first tweet
                try:
                    api_v1 = tweepy.API(tweepy.OAuth1UserHandler(
                        config.api_keys["api_key"],
                        config.api_keys["api_secret"],
                        config.api_keys["access_token"],
                        config.api_keys["access_token_secret"]
                    ))
                    
                    media = api_v1.media_upload(filename="post_image.jpg", file=io.BytesIO(image_data))
                    media_ids = [media.media_id]
                except:
                    pass  # Continue without image if upload fails
            
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id,
                media_ids=media_ids
            )
            
            thread_tweets.append(response.data["id"])
            previous_tweet_id = response.data["id"]
        
        return {
            "thread_ids": thread_tweets,
            "platform": "twitter",
            "url": f"https://twitter.com/user/status/{thread_tweets[0]}",
            "thread_length": len(thread_tweets)
        }
    
    async def _upload_image_to_facebook(self, image_data: bytes, config: PlatformConfig) -> Optional[str]:
        """Upload image to Facebook and return URL"""
        try:
            url = f"https://graph.facebook.com/v18.0/{config.api_keys['page_id']}/photos"
            
            files = {
                'source': ('image.jpg', io.BytesIO(image_data), 'image/jpeg')
            }
            
            data = {
                'access_token': config.api_keys['access_token'],
                'published': 'false'  # Upload without publishing
            }
            
            async with aiohttp.ClientSession() as session:
                data_form = aiohttp.FormData()
                for key, value in data.items():
                    data_form.add_field(key, value)
                data_form.add_field('source', io.BytesIO(image_data), filename='image.jpg', content_type='image/jpeg')
                
                async with session.post(url, data=data_form) as response:
                    result = await response.json()
                    if response.status == 200:
                        return result.get('url')
            
            return None
        except Exception as e:
            logger.error(f"Failed to upload image to Facebook: {e}")
            return None
    
    async def _upload_image_for_instagram(self, image_data: bytes) -> str:
        """Upload image for Instagram (placeholder - implement your image hosting)"""
        # This would typically upload to your own image hosting service
        # For now, return a placeholder URL
        return "https://your-image-host.com/uploaded-image.jpg"
    
    def _validate_platform_config(self, config: PlatformConfig) -> bool:
        """Validate that platform configuration has required API keys"""
        required_keys = {
            Platform.FACEBOOK: ["app_id", "app_secret", "access_token", "page_id"],
            Platform.INSTAGRAM: ["access_token", "business_account_id"],
            Platform.DISCORD: ["webhook_url"],
            Platform.TWITTER: ["api_key", "api_secret", "access_token", "access_token_secret", "bearer_token"]
        }
        
        platform_required = required_keys.get(config.platform, [])
        
        for key in platform_required:
            if not config.api_keys.get(key):
                logger.warning(f"Missing required API key '{key}' for {config.platform.value}")
                return False
        
        return True
    
    def get_platform_status(self) -> Dict[str, Dict]:
        """Get status of all platforms"""
        status = {}
        
        for platform, config in self.platforms.items():
            status[platform.value] = {
                "enabled": config.is_enabled,
                "configured": self._validate_platform_config(config),
                "settings": config.settings
            }
        
        return status
    
    def update_platform_config(self, platform: Platform, api_keys: Dict[str, str] = None, enabled: bool = None):
        """Update platform configuration"""
        if platform in self.platforms:
            if api_keys:
                self.platforms[platform].api_keys.update(api_keys)
            if enabled is not None:
                self.platforms[platform].is_enabled = enabled
            
            # Save to config file
            self._save_config_to_file()
    
    def _save_config_to_file(self):
        """Save current configuration to file"""
        config_data = {}
        
        for platform, config in self.platforms.items():
            config_data[platform.value] = {
                "api_keys": config.api_keys,
                "enabled": config.is_enabled
            }
        
        os.makedirs("config", exist_ok=True)
        with open("config/social_media_config.json", 'w') as f:
            json.dump(config_data, f, indent=2)

# Initialize global social media manager
social_media_manager = SocialMediaManager()