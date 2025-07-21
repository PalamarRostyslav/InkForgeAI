from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ImageSize(Enum):
    SQUARE_1024 = "1024x1024"
    PORTRAIT_1024x1792 = "1024x1792"
    LANDSCAPE_1792x1024 = "1792x1024"
    
class ImageQuality(Enum):
    STANDARD = "standard"
    HD = "hd"

@dataclass
class TattooImage:
    id: str
    prompt: str
    image_path: str
    size: ImageSize
    quality: ImageQuality
    created_at: datetime
    chat_session_id: str

@dataclass
class ChatMessage:
    id: str
    content: str
    image_id: Optional[str]
    created_at: datetime
    chat_session_id: str
    
@dataclass
class ChatSession:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessage] = None
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []