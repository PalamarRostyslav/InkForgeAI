from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTextEdit,
    QPushButton, QComboBox, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from backend.models import ImageSize, ImageQuality

class InputWidget(QWidget):
    generate_clicked = pyqtSignal(str, ImageSize, ImageQuality) 
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the input widget UI"""
        self.setObjectName("inputArea")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(16, 8, 16, 12)
        
        # Options row
        options_layout = QHBoxLayout()
        options_layout.setSpacing(12)
        
        # Size dropdown
        size_label = QLabel("Size:")
        options_layout.addWidget(size_label)
        
        self.size_combo = QComboBox()
        for size in ImageSize:
            self.size_combo.addItem(size.value.replace("x", " × "), size)
        self.size_combo.setCurrentIndex(0)
        self.size_combo.setFixedWidth(140)
        options_layout.addWidget(self.size_combo)
        
        # Quality dropdown
        quality_label = QLabel("Quality:")
        options_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        for quality in ImageQuality:
            self.quality_combo.addItem(quality.value.upper(), quality)
        self.quality_combo.setCurrentIndex(0)
        self.quality_combo.setFixedWidth(100)
        options_layout.addWidget(self.quality_combo)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        # Text input
        self.prompt_input = QTextEdit()
        self.prompt_input.setObjectName("promptInput")
        self.prompt_input.setPlaceholderText("Describe your tattoo design...")
        self.prompt_input.setFixedHeight(50)
        
        # Install event filter for Enter key
        self.prompt_input.installEventFilter(self)
        
        input_layout.addWidget(self.prompt_input)
        
        # Generate button
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.on_generate)
        self.generate_btn.setFixedHeight(50)
        self.generate_btn.setFixedWidth(120)
        input_layout.addWidget(self.generate_btn)
        
        layout.addLayout(input_layout)
    
    def eventFilter(self, obj, event):
        """Handle Enter key in text input"""
        if obj == self.prompt_input and event.type() == event.Type.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key.Key_Return and not key_event.modifiers():
                self.on_generate()
                return True
            elif key_event.key() == Qt.Key.Key_Return and key_event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                return False
            
        return super().eventFilter(obj, event)
    
    def on_generate(self):
        """Handle generate button click"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            return
        
        size = self.size_combo.currentData()
        quality = self.quality_combo.currentData()
        
        # Clear input
        self.prompt_input.clear()
        
        # Emit signal
        self.generate_clicked.emit(prompt, size, quality)
    
    def set_loading(self, loading: bool):
        """Set loading state"""
        self.generate_btn.setEnabled(not loading)
        self.prompt_input.setEnabled(not loading)
        self.size_combo.setEnabled(not loading)
        self.quality_combo.setEnabled(not loading)
        
        if loading:
            self.generate_btn.setText("Generating...")
        else:
            self.generate_btn.setText("Generate")