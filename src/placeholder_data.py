#Since I don't have access to the actual robot for this, I did research online regarding this 
# & implemented this file to generate REALISTIC test data that copies actual robot logging


import random
from datetime import datetime
from config import PLACEHOLDER_MESSAGES


class PlaceholderDataGenerator:
    
    def __init__(self):
        self.messages = PLACEHOLDER_MESSAGES
    
    def get_random_message(self, entry_name: str) -> str:
        if entry_name not in self.messages:
            return self._generate_generic_message(entry_name)
        
        
        msg_template = random.choice(self.messages[entry_name])
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Fill in template placeholders with realistic values
        message = self._fill_template(msg_template)
        
        return f"[{timestamp}] {message}"
    
    def _fill_template(self, template: str) -> str:
        if "{}" not in template and "{:" not in template:
            return template
        
        if "angle" in template or "degrees" in template:
            return template.format(random.uniform(-180, 180))
        
        elif "position" in template:
            return template.format(random.uniform(0, 10), random.uniform(0, 10))
        
        elif "current" in template:
            return template.format(random.uniform(0, 40))
        
        elif "RPM" in template:
            return template.format(random.randint(4000, 6000))
        
        elif "temperature" in template or "°C" in template:
            return template.format(random.randint(20, 60))
        
        elif "distance" in template:
            return template.format(random.uniform(1, 5))
        
        elif "AprilTag" in template:
            return template.format(random.randint(1, 8))
        
        elif "point" in template:
            return template.format(random.randint(1, 10))
        
        elif "ID" in template or "device" in template:
            return template.format(random.randint(1, 20))
        
        elif "voltage" in template.lower():
            return template.format(random.uniform(11.5, 12.8))
        
        elif "inches" in template:
            return template.format(random.uniform(0, 24))
        
        elif "utilization" in template or "%" in template:
            return template.format(random.randint(20, 80))
        
        elif "memory" in template.lower():
            return template.format(random.randint(100, 500))
        else:
            return template.format(random.randint(1, 100))
    
    def _generate_generic_message(self, entry_name: str) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return f"[{timestamp}] Sample message from {entry_name}"