
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogMessage:
    #single log msg from robot
    entry_name: str
    message: str
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now() #time is set to current time if no timestamp is provided
    
    def __str__(self):
        time_str = self.timestamp.strftime("%H:%M:%S.%f")[:-3] #format msg with timestamp and entry name
        return f"[{time_str}] [{self.entry_name}] {self.message}"
    
    def formatted_time(self):
        return self.timestamp.strftime("%H:%M:%S.%f")[:-3]
    
    def to_dict(self):
        return {
            "entry_name": self.entry_name,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data): #create from dictionary
        return cls(
            entry_name=data["entry_name"],
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )