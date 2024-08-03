import asyncio
from telethon import TelegramClient
from config_data.config import settings
from bot import get_bot
from services.gateways.notes_gateway import NotesGateway

# Настройки вашего бота
API_ID = settings.tg_app.API_ID
API_HASH = settings.tg_app.API_HASH

bot = get_bot()

# Настройка Telethon
client = TelegramClient("notification_session", API_ID, API_HASH)


async def send_reminder(note_text: str, username: str):
    await client.send_message(username, f"Напоминание: {note_text}")


async def check_reminders(user_id: int, username: str, text: str):
    while True:
        async with client:
            note = NotesGateway.get_for_remind(user_id=user_id, text=text)
            if note is not None:
                await send_reminder(note, username)
                break
        await asyncio.sleep(30)
