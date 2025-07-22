from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QInputDialog, QHBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal, QTimer, Qt
import asyncio

from backend.chat_service import ChatService

class ChatListItem(QWidget):
    """Custom widget for chat list items with delete button"""
    delete_clicked = pyqtSignal(str)
    
    def __init__(self, session_id: str, session_name: str):
        super().__init__()
        self.session_id = session_id
        self.session_name = session_name
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        # Session name label
        self.name_label = QLabel(self.session_name)
        self.name_label.setStyleSheet("color: #e0e0e0;")
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        layout.addStretch()
        
        # Delete button (hidden by default)
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888;
                font-size: 16px;
                padding: 0;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """)
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.session_id))
        self.delete_btn.hide()
        layout.addWidget(self.delete_btn)
    
    def enterEvent(self, event):
        """Show delete button on hover"""
        self.delete_btn.show()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Hide delete button when not hovering"""
        self.delete_btn.hide()
        super().leaveEvent(event)

class ChatSidebar(QWidget):
    session_selected = pyqtSignal(str)
    new_session_created = pyqtSignal(object)
    session_deleted = pyqtSignal(str)
    
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
            # Create custom widget
            item_widget = ChatListItem(session.id, session.name)
            item_widget.delete_clicked.connect(lambda sid: asyncio.create_task(self.delete_session(sid)))
            
            # Create list item
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, session.id)
            
            # Set proper size hint with padding
            size_hint = item_widget.sizeHint()
            size_hint.setHeight(max(50, size_hint.height()))
            item.setSizeHint(size_hint)
            
            # Add to list
            self.chat_list.addItem(item)
            self.chat_list.setItemWidget(item, item_widget)
    
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
            if item.data(Qt.ItemDataRole.UserRole) == session.id:
                self.chat_list.setCurrentItem(item)
                break
        
        self.new_session_created.emit(session)
    
    async def delete_session(self, session_id: str):
        """Delete a chat session"""
        sessions = await self.chat_service.get_all_sessions()
        session = next((s for s in sessions if s.id == session_id), None)
        
        if not session:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Delete Chat",
            f"Are you sure you want to delete '{session.name}'?\n\nThis will permanently delete all messages and images in this chat.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            await self.chat_service.delete_session(session_id)
            await self.refresh_sessions()
            
            self.session_deleted.emit(session_id)
    
    def on_item_clicked(self, item: QListWidgetItem):
        """Handle item click"""
        session_id = item.data(Qt.ItemDataRole.UserRole)
        self.session_selected.emit(session_id)