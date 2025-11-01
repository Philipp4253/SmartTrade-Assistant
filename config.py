import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() in ("1","true","yes")
OPENROUTER_URL = "https://openrouter.ai/v1/chat/completions"  # пример endpoint
