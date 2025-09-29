#NetworkTables listener that ndles both live NetworkTables connections and placeholder data generation.

import random
from PySide6.QtCore import QObject, Signal
from models.LogMessage import LogMessage
from config import (
    PLACEHOLDER_MODE, 
    ENTRY_TYPES, 
    LOGGING_TABLE_NAME,
    PLACEHOLDER_MESSAGE_PROBABILITY
)

if not PLACEHOLDER_MODE:
    from ntcore import NetworkTableInstance

from placeholder_data import PlaceholderDataGenerator


class NetworkTablesListener(QObject):
    message_received = Signal(LogMessage)
    connection_status_changed = Signal(bool)  # True = connected, False = disconnected
    
    def __init__(self):
        super().__init__()
        
        self.nt_instance = None
        self.log_table = None
        self.subscribers = {}
        self.placeholder_generator = None
        self.last_values = {}  # Tracks the last received values to detect changes
        
        if PLACEHOLDER_MODE:
            self._setup_placeholder_mode()
        else:
            self._setup_networktables()
    
    def _setup_placeholder_mode(self):
        self.placeholder_generator = PlaceholderDataGenerator()
        self.entry_names = ENTRY_TYPES.copy()
        self.connection_status_changed.emit(True)  # ALWAYS "connected" in placeholder mode
    
    def _setup_networktables(self):
        try:
            self.nt_instance = NetworkTableInstance.getDefault()
            self.log_table = self.nt_instance.getTable(LOGGING_TABLE_NAME)
            
            # Subscribe to all logging entries
            for entry_name in ENTRY_TYPES:
                topic = self.log_table.getStringTopic(entry_name)
                subscriber = topic.subscribe("")
                self.subscribers[entry_name] = subscriber
                self.last_values[entry_name] = ""
            
            self.connection_status_changed.emit(True)
            
        except Exception as e:
            print(f"Error initializing NetworkTables: {e}")
            self.connection_status_changed.emit(False)
    
    def check_for_messages(self):
        if PLACEHOLDER_MODE:
            self._check_placeholder_messages()
        else:
            self._check_networktables_messages()
    
    def _check_placeholder_messages(self):
        # Generate message with configured probability
        if random.random() < PLACEHOLDER_MESSAGE_PROBABILITY:
            entry_name = random.choice(self.entry_names)
            message_text = self.placeholder_generator.get_random_message(entry_name)
            
            # Extract timestamp from message if present
            if message_text.startswith("["):
                timestamp_end = message_text.find("]")
                if timestamp_end > 0:
                    message_text = message_text[timestamp_end + 2:]
            
            log_msg = LogMessage(entry_name, message_text)
            self.message_received.emit(log_msg)
    
    def _check_networktables_messages(self):
        try:
            for entry_name, subscriber in self.subscribers.items():
                value = subscriber.get()
                
                if value and value != self.last_values.get(entry_name, ""):
                    self.last_values[entry_name] = value
                    
                    # removes timestamp from message if it was added by robot code
                    message_text = value
                    if message_text.startswith("["):
                        timestamp_end = message_text.find("]")
                        if timestamp_end > 0:
                            message_text = message_text[timestamp_end + 2:]
                    
                    log_msg = LogMessage(entry_name, message_text)
                    self.message_received.emit(log_msg)
                    
        except Exception as e:
            print(f"Error reading NetworkTables: {e}")
            self.connection_status_changed.emit(False)
    
    def add_entry_type(self, entry_name: str):
        if PLACEHOLDER_MODE:
            if entry_name not in self.entry_names:
                self.entry_names.append(entry_name)
        else:
            if entry_name not in self.subscribers:
                topic = self.log_table.getStringTopic(entry_name)
                subscriber = topic.subscribe("")
                self.subscribers[entry_name] = subscriber
                self.last_values[entry_name] = ""
    
    def disconnect(self):
        if not PLACEHOLDER_MODE and self.nt_instance:
            # Unsubscribe from all topics
            for subscriber in self.subscribers.values():
                subscriber.close()
            self.subscribers.clear()
            self.connection_status_changed.emit(False)