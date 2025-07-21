from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QInputDialog
)
from PyQt6.QtCore import pyqtSignal, QTimer
import asyncio

from backend.chat_service import ChatService


class ChatSidebar(QWidget):
    session_selected = pyqtSignal(str)
    new_session_created = pyqtSignal(object)
    
    def __init__(self, chat_service: ChatService):
        super().__init__()
        self.chat_service = chat_service
        self.setFixedWidth(280)
        self.init_ui()
        
        # Load sessions on startup
        QTimer.singleShot(100, self.initial_load)
    
    def init_ui(self):
        """Initialize the sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title
        title = QLabel("Chat History")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)
        
        # New chat button
        self.new_chat_btn = QPushButton("+ New Chat")
        self.new_chat_btn.setObjectName("newChatButton")
        self.new_chat_btn.clicked.connect(self.create_new_chat)
        layout.addWidget(self.new_chat_btn)
        
        # Chat list
        self.chat_list = QListWidget()
        self.chat_list.setObjectName("chatList")
        self.chat_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.chat_list)
    
    def initial_load(self):
        """Initial load of sessions"""
        asyncio.create_task(self.refresh_sessions())
    
    async def refresh_sessions(self):
        """Refresh the list of chat sessions"""
        self.chat_list.clear()
        
        sessions = await self.chat_service.get_all_sessions()
        for session in sessions:
            item = QListWidgetItem(session.name)
            item.setData(1, session.id)
            self.chat_list.addItem(item)
    
    def create_new_chat(self):
        """Create a new chat session"""
        name, ok = QInputDialog.getText(
            self, 
            "New Chat", 
            "Enter chat name:",
            text="New Tattoo Session"
        )
        
        if ok and name:
            asyncio.create_task(self._create_session(name))
    
    async def _create_session(self, name: str):
        """Create a new session asynchronously"""
        session = await self.chat_service.create_session(name)
        await self.refresh_sessions()
        
        # Select the new session
        for i in range(self.chat_list.count()):
            item = self.chat_list.item(i)
            if item.data(1) == session.id:
                self.chat_list.setCurrentItem(item)
                break
        
        self.new_session_created.emit(session)
    
    def on_item_clicked(self, item: QListWidgetItem):
        """Handle item click"""
        session_id = item.data(1)
        self.session_selected.emit(session_id)