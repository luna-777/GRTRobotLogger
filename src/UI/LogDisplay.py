# Custom widget for displaying color coded log messages with time stamps AND formats + renders messages in the UI

from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCursor, QTextCharFormat, QFont, QColor
from models.LogMessage import LogMessage
from config import (ENTRY_COLORS, DEFAULT_ENTRY_COLOR, TIMESTAMP_COLOR, LOG_DISPLAY_FONT_FAMILY,LOG_DISPLAY_FONT_SIZE)


class LogDisplay(QTextEdit):
    
    def __init__(self):
        super().__init__()
        
        # Configure widget properties
        self.setReadOnly(True)
        self.setFont(QFont(LOG_DISPLAY_FONT_FAMILY, LOG_DISPLAY_FONT_SIZE))
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        self.document().setMaximumBlockCount(10000)  # Limit for optimal performance
    
    def append_message(self, log_msg: LogMessage, auto_scroll: bool = True): #append the formatted msg to display
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        self._insert_timestamp(cursor, log_msg)
        self._insert_entry_name(cursor, log_msg)
        self._insert_message_content(cursor, log_msg)
        
        cursor.insertText("\n")
        
        if auto_scroll:
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
    
    def _insert_timestamp(self, cursor: QTextCursor, log_msg: LogMessage):
        fmt = QTextCharFormat()
        fmt.setForeground(TIMESTAMP_COLOR)
        
        timestamp_text = f"[{log_msg.formatted_time()}] "
        cursor.insertText(timestamp_text, fmt)
    
    def _insert_entry_name(self, cursor: QTextCursor, log_msg: LogMessage):
        fmt = QTextCharFormat()

        color = ENTRY_COLORS.get(log_msg.entry_name, DEFAULT_ENTRY_COLOR)
        fmt.setForeground(color)
        fmt.setFontWeight(QFont.Bold)
        
        entry_text = f"[{log_msg.entry_name}] "
        cursor.insertText(entry_text, fmt)
    
    def _insert_message_content(self, cursor: QTextCursor, log_msg: LogMessage):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(255, 255, 255))
        
        cursor.insertText(log_msg.message, fmt)
    
    def scroll_to_bottom(self):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def scroll_to_top(self):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.minimum())