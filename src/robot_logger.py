from ntcore import NetworkTableInstance
from datetime import datetime


class RobotLogger:
    
    # Class variables for NetworkTables connection
    _nt_instance = None
    _log_table = None
    _entries = {}
    _initialized = False
    
    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        
        cls._nt_instance = NetworkTableInstance.getDefault()
        cls._log_table = cls._nt_instance.getTable("Logging")
        
        # predefined logging entries for diff subsystems
        cls._entries = {
            "drivetrain": cls._log_table.getStringTopic("drivetrain").publish(),
            "intake": cls._log_table.getStringTopic("intake").publish(),
            "shooter": cls._log_table.getStringTopic("shooter").publish(),
            "elevator": cls._log_table.getStringTopic("elevator").publish(),
            "vision": cls._log_table.getStringTopic("vision").publish(),
            "auto": cls._log_table.getStringTopic("auto").publish(),
            "system": cls._log_table.getStringTopic("system").publish(),
            "error": cls._log_table.getStringTopic("error").publish(),
        }
        
        cls._initialized = True
    
    @classmethod
    def log(cls, entry_name: str, message: str):
        if not cls._initialized:
            cls.initialize()
        
        if entry_name not in cls._entries:
            cls._entries[entry_name] = cls._log_table.getStringTopic(entry_name).publish()

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] {message}"
        
        cls._entries[entry_name].set(formatted_message)
    

    
    @classmethod
    def log_drivetrain(cls, message: str):
        cls.log("drivetrain", message)
    
    @classmethod
    def log_intake(cls, message: str):
        cls.log("intake", message)
    
    @classmethod
    def log_shooter(cls, message: str):
        cls.log("shooter", message)
    
    @classmethod
    def log_elevator(cls, message: str):
        cls.log("elevator", message)
    
    @classmethod
    def log_vision(cls, message: str):
        cls.log("vision", message)
    
    @classmethod
    def log_auto(cls, message: str):
        cls.log("auto", message)
    
    @classmethod
    def log_system(cls, message: str):
        cls.log("system", message)
    
    @classmethod
    def log_error(cls, message: str):
        cls.log("error", message)