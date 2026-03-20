# Copy this file to `local_settings.py` and fill in your Cohere API key.
#
# `local_settings.py` is git-ignored, so your secret stays local.

COHERE_API_KEY = "YOUR_COHERE_API_KEY_HERE"

# Flask uses this to protect forms. Change it before you deploy or share the app.
SECRET_KEY = "CHANGE_ME"

# Optional model settings.
COHERE_MODEL = "command-a-03-2025"
COHERE_MAX_TOKENS = 160
COHERE_TEMPERATURE = 0.9
COHERE_TIMEOUT_SECONDS = 20.0
