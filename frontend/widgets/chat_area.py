from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel,
    QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap


class ChatArea(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.loading_label = None
    
    def init_ui(self):
        """Initialize the chat area UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("messageArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Message container
        self.message_container = QWidget()
        self.message_container.setObjectName("messageContainer")
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_layout.setSpacing(8)
        
        self.scroll_area.setWidget(self.message_container)
        layout.addWidget(self.scroll_area)
    
    def add_user_message(self, text: str):
        """Add a user message to the chat"""
        message_widget = QWidget()
        message_layout = QHBoxLayout(message_widget)
        message_layout.setContentsMargins(20, 8, 20, 8)
        
        # Add stretch to align right
        message_layout.addStretch()
        
        # Message label
        label = QLabel(text)
        label.setObjectName("userMessage")
        label.setWordWrap(True)
        label.setMaximumWidth(600)
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        message_layout.addWidget(label)
        
        self.message_layout.addWidget(message_widget)
        self._scroll_to_bottom()
    
    def add_context_indicator(self, message_count: int):
        """Add a context indicator showing conversation history is being used"""
        if message_count > 0:
            context_widget = QWidget()
            context_layout = QHBoxLayout(context_widget)
            context_layout.setContentsMargins(20, 4, 20, 4)
            
            context_label = QLabel(f"🔗 Using context from {message_count} previous {'request' if message_count == 1 else 'requests'}")
            context_label.setStyleSheet("""
                color: #888;
                font-size: 12px;
                padding: 4px 8px;
                background-color: #252525;
                border-radius: 4px;
            """)
            
            context_layout.addWidget(context_label)
            context_layout.addStretch()
            
            self.message_layout.addWidget(context_widget)
    
    def add_image_message(self, prompt: str, image_path: str):
        """Add an image message to the chat"""
        # Add prompt first
        self.add_user_message(prompt)
        
        # Create image widget
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(20, 8, 20, 8)
        
        # Container for image
        container = QWidget()
        container.setObjectName("imageMessage")
        container_layout = QVBoxLayout(container)
        
        # Load and display image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Scale image to reasonable size
            scaled_pixmap = pixmap.scaled(
                400, 400, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            image_label = QLabel()
            image_label.setPixmap(scaled_pixmap)
            container_layout.addWidget(image_label)
        
        image_layout.addWidget(container)
        self.message_layout.addWidget(image_widget)
        self._scroll_to_bottom()
    
    def add_error_message(self, error: str):
        """Add an error message to the chat"""
        error_widget = QWidget()
        error_layout = QHBoxLayout(error_widget)
        error_layout.setContentsMargins(20, 8, 20, 8)
        
        label = QLabel(f"❌ {error}")
        label.setObjectName("errorMessage")
        label.setWordWrap(True)
        label.setStyleSheet("color: #ff6b6b; background-color: #2a1515; padding: 12px; border-radius: 8px;")
        
        error_layout.addWidget(label)
        self.message_layout.addWidget(error_widget)
        self._scroll_to_bottom()
    
    def show_loading(self):
        """Show loading indicator"""
        self.loading_label = QLabel("Generating tattoo design...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_layout.addWidget(self.loading_label)
        self._scroll_to_bottom()
    
    def hide_loading(self):
        """Hide loading indicator"""
        if self.loading_label:
            self.loading_label.deleteLater()
            self.loading_label = None
    
    def clear(self):
        """Clear all messages"""
        while self.message_layout.count():
            child = self.message_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))