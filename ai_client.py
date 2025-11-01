import os
import httpx
import json
import logging
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

logging.basicConfig(level=logging.INFO)

async def ask_openrouter(prompt: str, system_prompt: str = "You are a helpful AI trading assistant."):
    if MOCK_MODE or not OPENROUTER_API_KEY:
        return "MOCK: пример ответа от ИИ (заполните OPENROUTER_API_KEY и установите MOCK_MODE=false, чтобы получить реальный ответ)."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://github.com/filippvysotzky/smarttrade-assistant",
        "X-Title": "SmartTrade Assistant"
    }
    data = {
        "model": "gpt-4o-mini",  # или gpt-4o, если доступен
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=data)
            logging.info(f"Status: {r.status_code}")
            logging.info(f"Response: {r.text[:300]}")  # первые 300 символов для проверки

            if r.status_code != 200:
                return f"❌ Ошибка API ({r.status_code}): {r.text}"

            resp = r.json()
            return resp["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logging.error(f"Ошибка при подключении к OpenRouter: {e}")
        return f"⚠️ Ошибка при обращении к OpenRouter: {e}"
