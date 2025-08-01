import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # AI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Application Settings
        self.app_name = "AI Tattoo Generator"
        self.version = "1.0.0"
        
        # Storage Configuration
        self.data_dir = Path("data")
        self.db_path = self.data_dir / "chats.db"
        self.images_dir = self.data_dir / "images"
        
        # UI Configuration
        self.window_width = 1400
        self.window_height = 900
        self.sidebar_width = 280
        
        # Image Generation Defaults
        self.default_image_size = "1024x1024"
        self.default_image_quality = "standard"
        
        # MCP Configuration
        self.enable_mcp = self.anthropic_api_key != ""
        self.mcp_port = int(os.getenv("MCP_PORT", "5000"))
        
    def validate(self):
        """Validate configuration"""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
        return True