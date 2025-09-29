from pathlib import Path
from datetime import datetime
from typing import Optional, List
from models.LogMessage import LogMessage
from config import LOG_FILE_DIRECTORY, LOG_FILE_NAME_FORMAT


class LogFileManager:

    def __init__(self):
        #Initialize the log file manager
        self.current_log_file: Optional[Path] = None
        self.file_handle = None
        self.logs_directory = Path(LOG_FILE_DIRECTORY)
        self.logs_directory.mkdir(exist_ok=True)
    
    def create_new_log_file(self) -> Path:
        
        # Close existing file if open
        self.close_current_file()
        
        # Generate filename with timestamp
        timestamp = datetime.now()
        filename = timestamp.strftime(LOG_FILE_NAME_FORMAT)
        self.current_log_file = self.logs_directory / filename
        
        # Open file and write header
        self.file_handle = open(self.current_log_file, "w", encoding="utf-8")
        self._write_header(timestamp)
        
        return self.current_log_file
    
    def _write_header(self, timestamp: datetime):
        if self.file_handle:
            self.file_handle.write(f"FRC Robot Log\n")
            self.file_handle.write(f"Started: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.file_handle.write("=" * 80 + "\n\n")
            self.file_handle.flush()
    
    def write_message(self, log_msg: LogMessage):
        if self.file_handle:
            try:
                self.file_handle.write(str(log_msg) + "\n")
                self.file_handle.flush()
            except Exception as e:
                print(f"Error writing to log file: {e}")
    
    def write_messages(self, messages: List[LogMessage]):
        if self.file_handle:
            try:
                for msg in messages:
                    self.file_handle.write(str(msg) + "\n")
                self.file_handle.flush()
            except Exception as e:
                print(f"Error writing messages to log file: {e}")
    
    def export_to_file(self, filepath: Path, messages: List[LogMessage]) -> bool:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Robot Log Export\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(messages)}\n")
                f.write("=" * 80 + "\n\n")
                
                # write ALL messages
                for msg in messages:
                    f.write(str(msg) + "\n")
            
            return True
            
        except Exception as e:
            print(f"Error exporting log file: {e}")
            return False
    
    def export_filtered(self, filepath: Path, messages: List[LogMessage], 
                       entry_filter: str) -> bool:
        # Filter messages if necessary
        if entry_filter != "All":
            filtered_messages = [msg for msg in messages if msg.entry_name == entry_filter]
        else:
            filtered_messages = messages
        
        return self.export_to_file(filepath, filtered_messages)
    
    def close_current_file(self):
        if self.file_handle:
            try:
                self.file_handle.close()
            except Exception as e:
                print(f"Error closing log file: {e}")
            finally:
                self.file_handle = None
    
    def get_current_filepath(self) -> Optional[Path]:
        return self.current_log_file
    
    def get_log_files(self) -> List[Path]:
        return sorted(self.logs_directory.glob("*.txt"), reverse=True)
    
    def __del__(self):
        self.close_current_file()