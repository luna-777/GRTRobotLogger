#configuration settings for the UI

from PySide6.QtGui import QColor


# Placeholder mode (for testing) and live NetworkTables connection toggle
PLACEHOLDER_MODE = True

# NetworkTables server address (note: since I did not actually have access to the robot for this project, I did some 
# research and saw that it would be in the format of 10.TE.AM.2 where TEAM is the team number so I just plugged that value in)
NETWORKTABLES_SERVER = "10.19.2.2" 


LOGGING_TABLE_NAME = "Logging" #networks table name for loggin

LOG_FILE_DIRECTORY = "robot_logs"

# Log file name strftime format
LOG_FILE_NAME_FORMAT = "robot_log_%Y%m%d_%H%M%S.txt"

AUTO_SAVE_INTERVAL = 5

# Max messages to keep in memory
MAX_MESSAGES_IN_MEMORY = 10000

UPDATE_INTERVAL_MS = 100

DEFAULT_AUTO_SCROLL = True

DEFAULT_FILTER = "All"

LOG_DISPLAY_FONT_FAMILY = "Courier New"
LOG_DISPLAY_FONT_SIZE = 10

# Define logging entry types 
ENTRY_TYPES = [
    "drivetrain",
    "intake", 
    "shooter",
    "elevator",
    "vision",
    "auto",
    "system",
    "error"
]

# RGB colors for diff entry types
ENTRY_COLORS = {
    "drivetrain": QColor(100, 150, 255),  # Light blue
    "intake": QColor(100, 255, 150),      # Light green
    "shooter": QColor(255, 150, 100),     # Light orange
    "elevator": QColor(255, 200, 100),     # Yellow-orange
    "vision": QColor(200, 100, 255),      # Purple
    "auto": QColor(150, 255, 255),        # Cyan
    "system": QColor(200, 200, 200),      # Light gray
    "error": QColor(255, 100, 100),       # Light red
}

# Default color for unknown entry types
DEFAULT_ENTRY_COLOR = QColor(255, 255, 255)

TIMESTAMP_COLOR = QColor(150, 150, 150)

PLACEHOLDER_MESSAGE_PROBABILITY = 0.3

# Constant placehodler message templates for each entry type (FOR TESTING)
PLACEHOLDER_MESSAGES = {
    "drivetrain": [
        "Motor speeds normalized",
        "Gyro angle: {:.1f} degrees",
        "Odometry position updated: ({:.2f}, {:.2f})",
        "Turning to target angle",
        "Brake mode engaged"
    ],
    "intake": [
        "Note detected in intake",
        "Intake motor current: {:.1f}A",
        "Deploying intake mechanism",
        "Intake stalled - possible jam",
        "Retracting intake"
    ],
    "shooter": [
        "Shooter spinning up",
        "Target velocity reached: {} RPM",
        "Shot executed",
        "Shooter temperature: {}°C",
        "Cooling down shooter"
    ],
    "vision": [
        "AprilTag {} detected",
        "Target locked - distance: {:.2f}m",
        "Lost tracking of target",
        "Camera exposure adjusted",
        "Processing pipeline switched"
    ],
    "auto": [
        "Starting autonomous routine",
        "Path point {} reached",
        "Executing action: shoot",
        "Autonomous completed successfully",
        "Trajectory following active"
    ],
    "elevator": [
    "Elevator moving to setpoint: {:.1f} inches",
    "Elevator current position: {:.1f} inches",
    "Elevator soft limit reached at {:.1f} inches",
    "Elevator power: {:.1f}V",
    "Elevator limit switch triggered"
    ],
    "system": [
        "Battery voltage: {:.1f}V",
        "CAN utilization: {}%",
        "CPU temperature: {}°C",
        "Free memory: {}MB",
        "Robot enabled"
    ],
    "error": [
        "CAN timeout on device ID {}",
        "Motor controller fault detected",
        "Pressure sensor disconnected",
        "Communication lost with coprocessor",
        "Brownout detected"
    ]
}