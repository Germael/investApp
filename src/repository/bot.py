from os import getenv

import httpx


class Bot:
    def __init__(self):
        self.bot_url = f"https://api.telegram.org/bot{getenv('TELEGRAM_BOT_TOKEN')}"
        self.chat_id = getenv('STOCK_CHANNEL_ID')

    async def send_to_telegram(self, message: str):
        url = f"{self.bot_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
        return {"status": response.status_code, "response": response.json()}
