import asyncio
from typing import List, Dict
from pathlib import Path
import base64
from datetime import datetime
import uuid
from openai import AsyncOpenAI

from backend.models import ImageSize, ImageQuality, TattooImage


class OpenAIService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_tattoo(
        self, 
        prompt: str, 
        size: ImageSize = ImageSize.SQUARE_1024,
        quality: ImageQuality = ImageQuality.STANDARD,
        chat_session_id: str = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> TattooImage:
        """Generate a tattoo image using DALL-E 3 with conversation context"""
        
        # Build context-aware prompt
        enhanced_prompt = await self._build_contextual_prompt(prompt, conversation_history)
        
        try:
            # Generate image using OpenAI client
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                n=1,
                size=size.value,
                quality=quality.value,
                response_format="b64_json"
            )
            
            image_b64 = response.data[0].b64_json
            
            # Save image
            image_id = str(uuid.uuid4())
            image_path = await self._save_image(
                image_b64, 
                image_id, 
                chat_session_id
            )
            
            return TattooImage(
                id=image_id,
                prompt=prompt,
                image_path=image_path,
                size=size,
                quality=quality,
                created_at=datetime.now(),
                chat_session_id=chat_session_id
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
    
    async def _build_contextual_prompt(self, current_prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Build a prompt that includes conversation context"""
        
        if not conversation_history:
            # First request - standard tattoo prompt
            return f"Professional tattoo design: {current_prompt}. Black ink style by default if style is not provided by user, high contrast, clean lines suitable for skin application."
        
        # For subsequent requests, use GPT to understand context and refine the prompt
        try:
            system_prompt = """You are a tattoo design assistant. Based on the conversation history, 
            create a detailed prompt for DALL-E 3 that incorporates all previous design requests while 
            emphasizing the latest request. The design should evolve and build upon previous iterations, 
            maintaining consistency while adding new elements."""
            
            # Build conversation context
            context = "Previous tattoo design requests in this session:\n"
            for i, msg in enumerate(conversation_history):
                context += f"{i+1}. {msg['content']}\n"
            
            context += f"\nCurrent request: {current_prompt}\n\n"
            context += """Create a single, comprehensive prompt for DALL-E 3 that:
            1. Incorporates all design elements from previous requests
            2. Emphasizes the new elements from the current request
            3. Maintains stylistic consistency
            4. Is suitable for a professional tattoo design"""
            
            # Use GPT to create an optimized prompt
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content
            
            # Add tattoo-specific requirements
            return f"{enhanced_prompt}\n\nProfessional tattoo design, black ink style, high contrast, clean lines suitable for skin application."
            
        except Exception as e:
            # Fallback to simple context building if GPT fails
            print(f"GPT context building failed: {e}")
            return self._build_simple_contextual_prompt(current_prompt, conversation_history)
    
    def _build_simple_contextual_prompt(self, current_prompt: str, conversation_history: List[Dict[str, str]]) -> str:
        """Fallback simple context builder"""
        context_parts = ["Professional tattoo design with the following evolution:"]
        
        for i, msg in enumerate(conversation_history):
            if msg['role'] == 'user':
                context_parts.append(f"Request {i//2 + 1}: {msg['content']}")
        
        context_parts.append(f"Current request: {current_prompt}")
        context_parts.append(
            "Create a tattoo design that builds upon the previous requests, "
            "maintaining stylistic consistency while incorporating the new elements from the current request. "
            "Black ink style, high contrast, clean lines suitable for skin application."
        )
        
        return "\n".join(context_parts)
    
    async def _save_image(
        self, 
        image_b64: str, 
        image_id: str, 
        chat_session_id: str
    ) -> str:
        """Save base64 image to file system"""
        
        # Create directory structure
        base_path = Path("data/images")
        if chat_session_id:
            session_path = base_path / chat_session_id
        else:
            session_path = base_path / "unsorted"
        
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Save image
        image_path = session_path / f"{image_id}.png"
        image_data = base64.b64decode(image_b64)
        
        # Use asyncio for file operations
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: image_path.write_bytes(image_data)
        )
        
        return str(image_path)