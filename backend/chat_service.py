import sqlite3
import asyncio
from datetime import datetime
from typing import List, Optional
import uuid
from pathlib import Path

from backend.models import ChatSession, ChatMessage, TattooImage

class ChatService:
    def __init__(self, db_path: str = "data/chats.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id TEXT PRIMARY KEY,
                chat_session_id TEXT,
                content TEXT,
                image_id TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (chat_session_id) REFERENCES chat_sessions(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tattoo_images (
                id TEXT PRIMARY KEY,
                chat_session_id TEXT,
                prompt TEXT,
                image_path TEXT,
                size TEXT,
                quality TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (chat_session_id) REFERENCES chat_sessions(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def create_session(self, name: str) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            id=str(uuid.uuid4()),
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        await self._execute_query(
            '''INSERT INTO chat_sessions (id, name, created_at, updated_at) 
            VALUES (?, ?, ?, ?)''',
            (session.id, session.name, session.created_at, session.updated_at)
        )
        
        return session
    
    async def get_all_sessions(self) -> List[ChatSession]:
        """Get all chat sessions"""
        rows = await self._fetch_all(
            'SELECT * FROM chat_sessions ORDER BY updated_at DESC'
        )
        
        sessions = []
        for row in rows:
            session = ChatSession(
                id=row[0],
                name=row[1],
                created_at=datetime.fromisoformat(row[2]),
                updated_at=datetime.fromisoformat(row[3])
            )
            sessions.append(session)
        
        return sessions
    
    async def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session"""
        rows = await self._fetch_all(
            '''SELECT * FROM chat_messages 
            WHERE chat_session_id = ? 
            ORDER BY created_at ASC''',
            (session_id,)
        )
        
        messages = []
        for row in rows:
            message = ChatMessage(
                id=row[0],
                chat_session_id=row[1],
                content=row[2],
                image_id=row[3],
                created_at=datetime.fromisoformat(row[4])
            )
            messages.append(message)
        
        return messages
    
    async def add_message(
        self, 
        session_id: str, 
        content: str, 
        image_id: Optional[str] = None
    ) -> ChatMessage:
        """Add a message to a session"""
        message = ChatMessage(
            id=str(uuid.uuid4()),
            chat_session_id=session_id,
            content=content,
            image_id=image_id,
            created_at=datetime.now()
        )
        
        await self._execute_query(
            '''INSERT INTO chat_messages (id, chat_session_id, content, image_id, created_at)
            VALUES (?, ?, ?, ?, ?)''',
            (message.id, message.chat_session_id, message.content, 
            message.image_id, message.created_at)
        )
        
        # Update session timestamp
        await self._execute_query(
            'UPDATE chat_sessions SET updated_at = ? WHERE id = ?',
            (datetime.now(), session_id)
        )
        
        return message
    
    async def save_image_metadata(self, image: TattooImage):
        """Save image metadata to database"""
        await self._execute_query(
            '''INSERT INTO tattoo_images 
            (id, chat_session_id, prompt, image_path, size, quality, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (image.id, image.chat_session_id, image.prompt, image.image_path,
            image.size.value, image.quality.value, image.created_at)
        )
    
    async def get_session_images(self, session_id: str) -> List[TattooImage]:
        """Get all images for a session"""
        rows = await self._fetch_all(
            '''SELECT * FROM tattoo_images 
            WHERE chat_session_id = ? 
            ORDER BY created_at DESC''',
            (session_id,)
        )
        
        images = []
        for row in rows:
            # Convert string values back to enums
            from backend.models import ImageSize, ImageQuality
            
            image = TattooImage(
                id=row[0],
                chat_session_id=row[1],
                prompt=row[2],
                image_path=row[3],
                size=ImageSize(row[4]),
                quality=ImageQuality(row[5]),
                created_at=datetime.fromisoformat(row[6])
            )
            images.append(image)
        
        return images
    
    async def _execute_query(self, query: str, params=None):
        """Execute a database query asynchronously"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._execute_sync, query, params)
    
    def _execute_sync(self, query: str, params=None):
        """Synchronous query execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
    
    async def _fetch_all(self, query: str, params=None):
        """Fetch all results asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._fetch_all_sync, query, params)
    
    def _fetch_all_sync(self, query: str, params=None):
        """Synchronous fetch all"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
