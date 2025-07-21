from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QLabel, QFrame, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QMouseEvent
import shutil
from pathlib import Path


class ImageThumbnail(QFrame):
    """Clickable image thumbnail with export functionality"""
    clicked = pyqtSignal(str)
    
    def __init__(self, image_path: str, prompt: str):
        super().__init__()
        self.image_path = image_path
        self.prompt = prompt
        self.init_ui()
    
    def init_ui(self):
        """Initialize thumbnail UI"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid transparent;
                border-radius: 8px;
                background-color: #2a2a2a;
                padding: 8px;
            }
            QFrame:hover {
                border: 2px solid #3a7bc8;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        
        # Load image
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            # Create thumbnail
            thumbnail = pixmap.scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            image_label = QLabel()
            image_label.setPixmap(thumbnail)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)
        
        # Add prompt preview with larger font
        prompt_label = QLabel(self.prompt[:50] + "..." if len(self.prompt) > 50 else self.prompt)
        prompt_label.setWordWrap(True)
        prompt_label.setStyleSheet("color: #e0e0e0; font-size: 13px; padding: 4px 0;")
        prompt_label.setMaximumHeight(40)
        layout.addWidget(prompt_label)
        
        # Add export button
        export_btn = QPushButton("Export")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                color: #e0e0e0;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
            }
        """)
        export_btn.clicked.connect(self.export_image)
        layout.addWidget(export_btn)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse click"""
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < 160:
                self.clicked.emit(self.image_path)
    
    def export_image(self):
        """Export image to user-selected location"""
        file_name = Path(self.image_path).name
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Tattoo Design",
            file_name,
            "PNG Files (*.png);;All Files (*)"
        )
        
        if save_path:
            try:
                shutil.copy2(self.image_path, save_path)
                print(f"Image exported to: {save_path}")
            except Exception as e:
                print(f"Error exporting image: {e}")


class ImageGallery(QWidget):
    def __init__(self):
        super().__init__()
        self.thumbnails = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize gallery UI"""
        self.setObjectName("galleryWidget")
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Title
        title = QLabel("Gallery")
        title.setStyleSheet("font-size: 16px; font-weight: 600; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("galleryScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Grid container
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(8)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area.setWidget(self.grid_widget)
        layout.addWidget(self.scroll_area)
    
    def add_image(self, image_path: str, prompt: str):
        """Add an image to the gallery"""
        thumbnail = ImageThumbnail(image_path, prompt)
        
        # Calculate position in grid - 2 columns layout
        row = len(self.thumbnails) // 2
        col = len(self.thumbnails) % 2
        
        self.grid_layout.addWidget(thumbnail, row, col)
        self.thumbnails.append(thumbnail)
        
        # Update minimum size to ensure scrollability
        self.grid_widget.setMinimumWidth(320)
    
    def clear(self):
        """Clear all images from gallery"""
        for thumbnail in self.thumbnails:
            thumbnail.deleteLater()
        self.thumbnails.clear()