import os
from google.cloud import secretmanager_v1 as secretmanager 

def load_config():
    """Loads environment variables and sets up configuration."""
    gemini_key = os.environ.get("GEMINI_KEY")
    model = os.environ.get("MODEL", "gemini-1.5-flash")
    sp_control = os.environ.get("SP_CONTROL")
    project_id = os.environ.get("PROJECT_ID")

    if project_id != "local":
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/GEMINI_KEY/versions/latest"
            response = client.access_secret_version(request={"name": name})
            gemini_key = response.payload.data.decode("UTF-8")
        except Exception as e:
            return e

    if not all([gemini_key, model, sp_control, project_id]):
        return Exception("Missing required configuration values")
    
    return {
        "GEMINI_KEY": gemini_key,
        "MODEL": model,
        "SP_CONTROL": sp_control,
        "PROJECT_ID": project_id
    }
