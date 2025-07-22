import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter
)
from PyQt6.QtCore import Qt

from frontend.styles import CLAUDE_STYLE
from frontend.widgets.chat_sidebar import ChatSidebar
from frontend.widgets.chat_area import ChatArea
from frontend.widgets.input_widget import InputWidget
from frontend.widgets.image_gallery import ImageGallery
from backend.chat_service import ChatService
from backend.openai_service import OpenAIService


class MainWindow(QMainWindow):
    def __init__(self, openai_api_key: str):
        super().__init__()
        
        # Initialize services
        self.chat_service = ChatService()
        self.openai_service = OpenAIService(openai_api_key)
        
        # Current session
        self.current_session = None
        
        # Setup UI
        self.init_ui()
        self.setStyleSheet(CLAUDE_STYLE)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Tattoo Generator")
        self.setGeometry(100, 50, 1400, 950)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = ChatSidebar(self.chat_service)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.session_selected.connect(self.on_session_selected)
        self.sidebar.new_session_created.connect(self.on_new_session)
        self.sidebar.session_deleted.connect(self.on_session_deleted)
        
        # Add visual separator
        sidebar_container = QWidget()
        sidebar_layout = QHBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar_layout.addWidget(self.sidebar)
        
        # Create main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create splitter for chat and gallery
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Chat area
        chat_container = QWidget()
        chat_container.setObjectName("chatArea")
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        self.chat_area = ChatArea()
        chat_layout.addWidget(self.chat_area)
        
        # Input widget
        self.input_widget = InputWidget()
        self.input_widget.generate_clicked.connect(self.on_generate_tattoo)
        chat_layout.addWidget(self.input_widget)
        
        # Gallery
        self.gallery = ImageGallery()
        
        # Add to splitter
        splitter.addWidget(chat_container)
        splitter.addWidget(self.gallery)
        splitter.setSizes([1000, 400])
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        content_layout.addWidget(splitter)
        
        # Add to main layout
        main_layout.addWidget(sidebar_container)
        main_layout.addWidget(content_widget)
        
        # Set stretch factors
        main_layout.setStretchFactor(self.sidebar, 0)
        main_layout.setStretchFactor(content_widget, 1)
    
    async def on_session_selected(self, session_id: str):
        """Handle session selection"""
        self.current_session = session_id
        
        # Clear current chat
        self.chat_area.clear()
        
        # Load messages
        messages = await self.chat_service.get_session_messages(session_id)
        images = await self.chat_service.get_session_images(session_id)
        
        # Create a map of image IDs to image objects
        image_map = {img.id: img for img in images}
        
        for message in messages:
            if message.image_id and message.image_id in image_map:
                image = image_map[message.image_id]
                if message.content.startswith("Generated tattoo: "):
                    original_prompt = message.content.replace("Generated tattoo: ", "")
                else:
                    original_prompt = message.content
                
                self.chat_area.add_user_message(original_prompt)
                self.chat_area.add_image_message(original_prompt, image.image_path)
            elif not message.content.startswith("Generated tattoo:"):
                self.chat_area.add_user_message(message.content)
        
        # Load gallery images
        self.gallery.clear()
        for image in images:
            self.gallery.add_image(image.image_path, image.prompt)
    
    async def on_new_session(self, session):
        """Handle new session creation"""
        self.current_session = session.id
        self.chat_area.clear()
        self.gallery.clear()
    
    async def on_session_deleted(self, session_id: str):
        """Handle session deletion"""
        # If the deleted session was the current one, clear the UI
        if self.current_session == session_id:
            self.current_session = None
            self.chat_area.clear()
            self.gallery.clear()
    
    async def on_generate_tattoo(self, prompt: str, size, quality):
        """Handle tattoo generation with conversation context"""
        if not self.current_session:
            # Create a new session if none exists
            session = await self.chat_service.create_session(f"Session {prompt[:20]}...")
            self.current_session = session.id
            await self.sidebar.refresh_sessions()
        
        # Add user message
        self.chat_area.add_user_message(prompt)
        await self.chat_service.add_message(self.current_session, prompt)
        
        # Build conversation history
        messages = await self.chat_service.get_session_messages(self.current_session)
        conversation_history = []
        
        for msg in messages[:-1]:
            # Only include user prompts (not system messages)
            if not msg.image_id:
                conversation_history.append({
                    'role': 'user',
                    'content': msg.content
                })
        
        # Show context indicator if there's history
        if conversation_history:
            self.chat_area.add_context_indicator(len(conversation_history))
        
        # Show loading
        self.input_widget.set_loading(True)
        self.chat_area.show_loading()
        
        try:
            # Generate tattoo with conversation context
            image = await self.openai_service.generate_tattoo(
                prompt, size, quality, self.current_session, conversation_history
            )
            
            # Save image metadata
            await self.chat_service.save_image_metadata(image)
            
            # Add to chat
            self.chat_area.hide_loading()
            self.chat_area.add_image_message(prompt, image.image_path)
            
            # Add to gallery
            self.gallery.add_image(image.image_path, prompt)
            
            # Save message with image reference
            await self.chat_service.add_message(
                self.current_session, 
                f"Generated tattoo: {prompt}", 
                image.id
            )
            
        except Exception as e:
            self.chat_area.hide_loading()
            self.chat_area.add_error_message(f"Error generating tattoo: {str(e)}")
        finally:
            self.input_widget.set_loading(False)