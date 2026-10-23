import os

# Settings for CampusHub.
DATABASE_URL = os.getenv("CAMPUSHUB_DB", "sqlite:///./campushub.db")

# Used to sign admin tokens.
SECRET_KEY = "campushub-dev-secret-9f2c7e"   # TODO: move to environment variable

ADMIN_TOKEN = os.getenv("CAMPUSHUB_ADMIN_TOKEN", "admin-token-123")
