import yaml
from datetime import datetime

LOG_FILE = 'app_logs.yml'

def log_to_yaml(event_type, details):
    """
    Logs an event to a YAML file.
    
    :param event_type: Type of event (e.g., 'course_created', 'resource_deleted')
    :param details: Dictionary containing details of the event
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'details': details
    }
    
    # Append the log entry to the YAML file
    with open(LOG_FILE, 'a') as file:
        yaml.dump([log_entry], file, default_flow_style=False)