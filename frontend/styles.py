CLAUDE_STYLE = """
/* Main Application Styles */
QMainWindow {
    background-color: #1a1a1a;
}

/* Sidebar Styles */
QWidget#sidebar {
    background-color: #202020;
    border-right: 3px solid #3a3a3a;
}

QListWidget#chatList {
    background-color: transparent;
    border: none;
    outline: none;
    padding: 8px;
}

QListWidget#chatList::item {
    background-color: transparent;
    border: none;
    padding: 0;
    margin: 4px 8px;
}

QListWidget#chatList::item:selected {
    background-color: transparent;
}

/* Chat List Item Widget Styles */
ChatListItem {
    background-color: transparent;
    border-radius: 8px;
}

ChatListItem:hover {
    background-color: #2a2a2a;
}

QListWidget#chatList::item:selected ChatListItem {
    background-color: #3a3a3a;
}

/* Main Chat Area */
QWidget#chatArea {
    background-color: #1a1a1a;
}

QScrollArea#messageArea {
    background-color: transparent;
    border: none;
}

QWidget#messageContainer {
    background-color: transparent;
}

/* Message Bubbles */
QLabel#userMessage {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px;
}

QLabel#imageMessage {
    background-color: #252525;
    border-radius: 12px;
    padding: 8px;
    margin: 8px;
}

/* Input Area */
QWidget#inputArea {
    background-color: #202020;
    border-top: 1px solid #333;
    padding: 8px 16px 12px 16px;
}

QTextEdit#promptInput {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    color: #e0e0e0;
    padding: 8px 12px;
    font-size: 14px;
    max-height: 60px;
    min-height: 40px;
}

QTextEdit#promptInput:focus {
    border: 1px solid #4a4a4a;
    outline: none;
}

/* Buttons */
QPushButton {
    background-color: #3a7bc8;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #4a8bd8;
}

QPushButton:pressed {
    background-color: #2a6bb8;
}

QPushButton#newChatButton {
    background-color: transparent;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    margin: 8px;
}

QPushButton#newChatButton:hover {
    background-color: #2a2a2a;
    border: 1px solid #4a4a4a;
}

/* Dropdown Styles */
QComboBox {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 6px 12px;
    color: #e0e0e0;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #4a4a4a;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e0e0e0;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    selection-background-color: #3a3a3a;
    color: #e0e0e0;
}

/* Labels */
QLabel {
    color: #e0e0e0;
}

QLabel#sidebarTitle {
    font-size: 18px;
    font-weight: 600;
    padding: 16px;
    color: #f0f0f0;
}

/* Gallery Styles */
QWidget#galleryWidget {
    background-color: #252525;
    border-radius: 12px;
    padding: 12px;
    margin: 8px;
}

QScrollArea#galleryScroll {
    background-color: transparent;
    border: none;
}

/* Scrollbar Styles */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3a3a3a;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    height: 0;
    width: 0;
    border: none;
}

/* Loading Indicator */
QLabel#loadingLabel {
    color: #888;
    font-style: italic;
    padding: 20px;
}
"""