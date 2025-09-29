from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox, QFileDialog)
from PySide6.QtCore import QTimer, Qt

from models.LogMessage import LogMessage
from NetworkTablesListener import NetworkTablesListener
from LogFileManager import LogFileManager
from UI.LogDisplay import LogDisplay
from config import (PLACEHOLDER_MODE, UPDATE_INTERVAL_MS, DEFAULT_AUTO_SCROLL,DEFAULT_FILTER, ENTRY_TYPES, MAX_MESSAGES_IN_MEMORY)


class LoggingWindow(QMainWindow):
    # Allows viewing, filtering, & exporting robot logs

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("GRT Robot Logger")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize variables & components
        self.paused = False
        self.log_messages = []
        self.current_filter = DEFAULT_FILTER
        self.auto_scroll = DEFAULT_AUTO_SCROLL
     
        self.file_manager = LogFileManager()
        self.nt_listener = NetworkTablesListener()
        self.log_display = None  
    
        self.setup_ui()
        
        # Connect signals
        self.nt_listener.message_received.connect(self.handle_new_message)
        self.nt_listener.connection_status_changed.connect(self.handle_connection_status)
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.nt_listener.check_for_messages)
        self.update_timer.start(UPDATE_INTERVAL_MS)
        
        # Create initial log file
        log_file = self.file_manager.create_new_log_file()
        self.update_status(f"Logging to: {log_file.name}")
    
    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        main_layout.addLayout(self.create_control_bar()) 
        
        self.log_display = LogDisplay() 
        main_layout.addWidget(self.log_display)
        
        main_layout.addLayout(self.create_status_bar())
    
    def create_control_bar(self) -> QHBoxLayout:
        control_layout = QHBoxLayout()
        
        # Mode indicator between passing live data and using placeholder values 
        mode_text = "PLACEHOLDER MODE" if PLACEHOLDER_MODE else "LIVE MODE"
        mode_color = "#ff6b6b" if PLACEHOLDER_MODE else "#51cf66"
        
        self.mode_label = QLabel(mode_text)
        self.mode_label.setStyleSheet(
            f"font-weight: 600; font-size: 32px; padding: 8px; color: {mode_color}; text-align: center;"
        )
        control_layout.addWidget(self.mode_label)
        
        control_layout.addStretch()
        
        # Filter dropdown
        control_layout.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All"] + ENTRY_TYPES)
        self.filter_combo.setCurrentText(DEFAULT_FILTER)
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        control_layout.addWidget(self.filter_combo)
        
        # Auto-scroll checkbox
        self.autoscroll_check = QCheckBox("Auto-scroll")
        self.autoscroll_check.setChecked(DEFAULT_AUTO_SCROLL)
        self.autoscroll_check.stateChanged.connect(self.toggle_autoscroll)
        control_layout.addWidget(self.autoscroll_check)
        
        # Pause button
        self.pause_btn = QPushButton("⏸ PAUSE")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setToolTip("Pause receiving new messages")
        control_layout.addWidget(self.pause_btn)
        
        # Clear button
        clear_btn = QPushButton("CLEAR")
        clear_btn.clicked.connect(self.clear_logs)
        clear_btn.setToolTip("Clear all messages from display!")
        control_layout.addWidget(clear_btn)
        
        # Export button
        export_btn = QPushButton("EXPORT")
        export_btn.clicked.connect(self.export_logs)
        export_btn.setToolTip("Export logs to chosen location")
        control_layout.addWidget(export_btn)
        return control_layout
    
    def create_status_bar(self) -> QHBoxLayout:
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.message_count_label = QLabel("Messages: 0")
        self.connection_label = QLabel("Connecting...")
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.connection_label)
        status_layout.addWidget(self.message_count_label)
        
        return status_layout
    
    def handle_new_message(self, log_msg: LogMessage):
    
        if self.paused:
            return
        
        self.log_messages.append(log_msg) #add to msg list
    
        if MAX_MESSAGES_IN_MEMORY > 0 and len(self.log_messages) > MAX_MESSAGES_IN_MEMORY:
            self.log_messages.pop(0)
        #enforces the memory limit if configured
        
        self.file_manager.write_message(log_msg)
        
        #update display with filter!
        if self.current_filter == "All" or self.current_filter == log_msg.entry_name:
            self.log_display.append_message(log_msg, self.auto_scroll)
        
        self.message_count_label.setText(f"Messages: {len(self.log_messages)}")
    
    def handle_connection_status(self, connected: bool):
    
        if connected:
            self.connection_label.setText("Connected")
        else:
            self.connection_label.setText("Disconnected")
    
    def toggle_pause(self):
        self.paused = not self.paused
        
        if self.paused:
            self.pause_btn.setText("▶ RESUME")
        else:
            self.pause_btn.setText("⏸ PAUSE")
    
    def toggle_autoscroll(self, state):
        self.auto_scroll = (state == Qt.Checked)
    
    def apply_filter(self, filter_text: str):
        self.current_filter = filter_text
        self.refresh_display()
    
    def refresh_display(self):
        self.log_display.clear()
        
        for log_msg in self.log_messages:
            if self.current_filter == "All" or self.current_filter == log_msg.entry_name:
                self.log_display.append_message(log_msg, auto_scroll=False)
        
        # Scroll to bottom after refresh if auto-scroll is enabled
        if self.auto_scroll:
            self.log_display.scroll_to_bottom()
    
    def clear_logs(self):
        self.log_display.clear()
        self.log_messages.clear()
        self.message_count_label.setText("Messages: 0")
        self.update_status("Logs cleared")
    
    def export_logs(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "",
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)"
        )
        
        if filename:
            success = self.file_manager.export_filtered(
                filename,
                self.log_messages,
                self.current_filter
            )
            
            if success:
                self.update_status(f"Exported to: {filename}")
            else:
                self.update_status("Export failed :(")
    
    def update_status(self, message: str):
        self.status_label.setText(message) #update status w message
    
    def closeEvent(self, event):
        # Stop timer
        self.update_timer.stop()
        
        # Disconnect from NetworkTables
        self.nt_listener.disconnect()
        
        # Close log file
        self.file_manager.close_current_file()
        
        event.accept()