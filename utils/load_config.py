import os
from google.cloud import secretmanager_v1 as secretmanager 

def load_config():
    """Loads environment variables and sets up configuration."""
    gemini_key = os.environ.get("GEMINI_KEY")
    model = os.environ.get("MODEL", "gemini-1.5-flash")
    sp_control = os.environ.get("SP_CONTROL")
    project_env = os.environ.get("PROJECT_ENV")

    if not all([gemini_key, model, sp_control, project_env]):
        return Exception("Missing required configuration values")
    
    return {
        "GEMINI_KEY": gemini_key,
        "MODEL": model,
        "SP_CONTROL": sp_control,
        "PROJECT_ENV": project_env
    }
