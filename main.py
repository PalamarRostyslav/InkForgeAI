import sys
import asyncio
import signal
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from qasync import QEventLoop, asyncSlot

from frontend.main_window import MainWindow
from config import Config


class TattooAIApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("AI Tattoo Generator")
        
        # Set up async event loop
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        
        # Load configuration
        self.config = Config()
        
        # Validate API key
        if not self.config.openai_api_key:
            self.show_api_key_error()
            sys.exit(1)
        
        # Create main window
        self.window = MainWindow(self.config.openai_api_key)
        
        # Make async slots work
        self._setup_async_handlers()
    
    def _setup_async_handlers(self):
        """Setup async signal handlers"""
        # Convert sync signals to async
        original_on_generate = self.window.on_generate_tattoo
        original_on_session = self.window.on_session_selected
        original_on_new = self.window.on_new_session
        original_on_delete = self.window.on_session_deleted
        
        @asyncSlot(str, object, object)
        async def async_generate(prompt, size, quality):
            await original_on_generate(prompt, size, quality)
        
        @asyncSlot(str)
        async def async_session(session_id):
            await original_on_session(session_id)
        
        @asyncSlot(object)
        async def async_new(session):
            await original_on_new(session)
        
        @asyncSlot(str)
        async def async_delete(session_id):
            await original_on_delete(session_id)
        
        # Replace with async versions
        self.window.input_widget.generate_clicked.disconnect()
        self.window.input_widget.generate_clicked.connect(async_generate)
        
        self.window.sidebar.session_selected.disconnect()
        self.window.sidebar.session_selected.connect(async_session)
        
        self.window.sidebar.new_session_created.disconnect()
        self.window.sidebar.new_session_created.connect(async_new)
        
        self.window.sidebar.session_deleted.disconnect()
        self.window.sidebar.session_deleted.connect(async_delete)
    
    def show_api_key_error(self):
        """Show error dialog for missing API key"""
        QMessageBox.critical(
            None,
            "Configuration Error",
            "OpenAI API key not found!\n\n"
            "Please set your API key in one of the following ways:\n"
            "1. Set OPENAI_API_KEY environment variable\n"
            "2. Create a .env file with OPENAI_API_KEY=your-key\n"
            "3. Update config.py with your API key"
        )
    
    def run(self):
        """Run the application"""
        self.window.show()
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        with self.loop:
            self.loop.run_forever()


if __name__ == "__main__":
    app = TattooAIApp()
    app.run()