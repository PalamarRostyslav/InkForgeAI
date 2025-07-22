"""
MCP (Model Context Protocol) Integration for Tattoo Analysis

This module provides MCP server functionality to analyze tattoo images
using Claude API and return meaningful interpretations.
"""

import asyncio
import base64
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import anthropic
from backend.chat_service import ChatService

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP not installed. Install with: pip install mcp")

class TattooAnalysisMCP:
    def __init__(self, chat_service: ChatService, anthropic_api_key: str):
        self.chat_service = chat_service
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.analysis_queue = asyncio.Queue()
        
        if not MCP_AVAILABLE:
            self.server = None
            return
            
        self.server = Server("tattoo-analysis-mcp")
        
        # Register handlers
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available MCP tools"""
        return [
            {
                "name": "analyze_tattoo",
                "description": "Analyze a tattoo image to understand its meaning, symbolism, and artistic style",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Path to the tattoo image file"
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Chat session ID to add the analysis to"
                        }
                    },
                    "required": ["image_path", "session_id"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Handle tool calls"""
        if name == "analyze_tattoo":
            image_path = arguments.get("image_path")
            session_id = arguments.get("session_id")
            return await self._analyze_tattoo(image_path, session_id)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def _analyze_tattoo(self, image_path: str, session_id: str) -> Dict[str, Any]:
        """Analyze a tattoo image using Claude"""
        try:
            # Read and encode the image
            image_data = await self._encode_image(image_path)
            
            # Create the analysis prompt
            prompt = """Please analyze this tattoo design and provide insights on:

            1. **Symbolism & Meaning**: What symbols, elements, or themes are present? What might they represent?
            2. **Artistic Style**: What tattoo style is this (traditional, neo-traditional, realism, etc.)?
            3. **Cultural Significance**: Are there any cultural or historical references?
            4. **Design Elements**: Describe the composition, use of space, and artistic techniques.
            5. **Personal Interpretation**: What emotions or stories might this tattoo convey?

            Please provide a thoughtful, detailed analysis that would help someone understand the depth and artistry of this tattoo."""

            # Call Claude API
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            analysis_text = response.content[0].text
            
            # Add analysis to chat
            await self.chat_service.add_message(
                session_id,
                f"🔍 Tattoo Analysis:\n\n{analysis_text}"
            )
            
            return {
                "status": "success",
                "analysis": analysis_text,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Failed to analyze tattoo: {str(e)}"
            return {
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    async def run_server(self):
        """Run the MCP server"""
        if not self.server:
            print("MCP not available")
            return
            
        async with stdio_server() as (read, write):
            await self.server.run(read, write)

class MCPClient:
    """Client to communicate with the MCP server"""
    
    def __init__(self, mcp_server: TattooAnalysisMCP):
        self.mcp_server = mcp_server
    
    async def analyze_image(self, image_path: str, session_id: str) -> Dict[str, Any]:
        """Request image analysis from MCP server"""
        if not self.mcp_server.server:
            # Direct call if MCP is not available
            return await self.mcp_server._analyze_tattoo(image_path, session_id)
        
        # Call through MCP protocol
        return await self.mcp_server.call_tool("analyze_tattoo", {
            "image_path": image_path,
            "session_id": session_id
        })

def run_mcp_server_thread(chat_service: ChatService, anthropic_api_key: str):
    """Run MCP server in a separate thread"""
    async def run():
        mcp = TattooAnalysisMCP(chat_service, anthropic_api_key)
        await mcp.run_server()
    
    # Create new event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())