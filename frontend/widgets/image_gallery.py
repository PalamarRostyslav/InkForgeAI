from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QLabel, QFrame, QPushButton, QFileDialog, QHBoxLayout, QDialog, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QMouseEvent, QKeyEvent
import shutil
from pathlib import Path

class ImagePreviewDialog(QDialog):
    """Full-size image preview dialog"""
    
    def __init__(self, image_path: str, prompt: str, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.prompt = prompt
        self.init_ui()
    
    def init_ui(self):
        """Initialize preview dialog UI"""
        self.setWindowTitle("Tattoo Design Preview")
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border: 1px solid #3a3a3a;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                color: #e0e0e0;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #3a3a3a;
                background-color: #2a2a2a;
                padding: 8px;
                border-radius: 8px;
            }
        """)
        
        # Load and scale image
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            # Get screen size for reasonable max size
            screen = QApplication.primaryScreen().geometry()
            max_width = min(800, screen.width() - 100)
            max_height = min(600, screen.height() - 200)
            
            scaled_pixmap = pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        
        layout.addWidget(self.image_label)
        
        # Prompt display
        prompt_label = QLabel(f"Prompt: {self.prompt.strip()}")
        prompt_label.setWordWrap(True)
        prompt_label.setStyleSheet("""
            color: #b0b0b0;
            font-size: 13px;
            padding: 12px;
            background-color: #252525;
            border-radius: 4px;
            border: 1px solid #3a3a3a;
            margin: 0px;
        """)
        prompt_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(prompt_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_image)
        button_layout.addWidget(export_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Set reasonable size
        self.resize(max_width + 50, max_height + 150)
        
        # Center on screen
        self.center_on_screen()
    
    def center_on_screen(self):
        """Center dialog on screen"""
        screen = QApplication.primaryScreen().geometry()
        dialog_geometry = self.geometry()
        x = (screen.width() - dialog_geometry.width()) // 2
        y = (screen.height() - dialog_geometry.height()) // 2
        self.move(x, y)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
    
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


class ImageThumbnail(QFrame):
    """Clickable image thumbnail with export and analyze functionality"""
    clicked = pyqtSignal(str)
    analyze_clicked = pyqtSignal(str, str)
    
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
            thumbnail = pixmap.scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.image_label = QLabel()
            self.image_label.setPixmap(thumbnail)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(self.image_label)  # Now this matches
        
        # Add prompt preview with larger font
        prompt_label = QLabel(self.prompt[:50] + "..." if len(self.prompt) > 50 else self.prompt)
        prompt_label.setWordWrap(True)
        prompt_label.setStyleSheet("color: #e0e0e0; font-size: 13px; padding: 4px 0;")
        prompt_label.setMaximumHeight(40)
        layout.addWidget(prompt_label)
        
        # Button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)
        
        # Export button
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
        button_layout.addWidget(export_btn)
        
        # Analyze button
        analyze_btn = QPushButton("Analyze")
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a7bc8;
                border: none;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4a8bd8;
            }
        """)
        analyze_btn.clicked.connect(self.analyze_image)
        button_layout.addWidget(analyze_btn)
        
        layout.addLayout(button_layout)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse click"""
        if event.button() == Qt.MouseButton.LeftButton:
            clicked_widget = self.childAt(event.position().toPoint())
            
            if clicked_widget == self.image_label:
                self.show_preview()
                
    def show_preview(self):
        """Show full-size image preview"""
        preview_dialog = ImagePreviewDialog(self.image_path, self.prompt, self)
        preview_dialog.exec()
    
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
    
    def analyze_image(self):
        """Emit signal to analyze the image"""
        self.analyze_clicked.emit(self.image_path, self.prompt)


class ImageGallery(QWidget):
    image_analyze_requested = pyqtSignal(str, str)
    
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
        thumbnail.analyze_clicked.connect(self.on_analyze_clicked)
        
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
    
    def on_analyze_clicked(self, image_path: str, prompt: str):
        """Handle analyze button click"""
        self.image_analyze_requested.emit(image_path, prompt)