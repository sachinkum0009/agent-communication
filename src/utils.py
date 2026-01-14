"""
Utils scripts
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")

missing_vars = []
if not BASE_URL:
    missing_vars.append("BASE_URL")
if not EMBED_MODEL:
    missing_vars.append("EMBED_MODEL")
if not LLM_MODEL:
    missing_vars.append("LLM_MODEL")

if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )
