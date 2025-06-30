import re
import requests
from config import BOT_TOKEN, CHAT_ID

def escape_markdown_v2(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', str(text))

def send_telegram_message(message: dict):
    def esc(t): return escape_markdown_v2(t) if t else ""

    text = (
        f"🏛 *Exchange*: {esc(message.get('exchange', ''))}\n\n"
        f"📅 *Date*: {esc(message['date_time'])}\n\n"
        f"🏢 *Company*: {esc(message['company'])}\n\n"
        f"🔣 *Symbol*: {esc(message.get('symbol', ''))}\n\n"
        f"📰 *Headline*: {esc(message['headline'])}\n\n"
    )

    if message.get("attachment_url"):
        text += f"📎 [View Attachment]({esc(message['attachment_url'])})\n\n"

    if message.get("order_value"):
        text += f"💰 *Order Value*: {esc(message['order_value'])}\n\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.get(url, params=payload, timeout=5)
        if response.status_code != 200:
            print(f"❌ Failed to send Telegram message: {response.text}")
        else:
            print("✅ Telegram message sent successfully.")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")
