from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from bot import get_bot
from logger import logger

router = Router()

bot = get_bot()


# Хэндлер для обработки некорректных сообщений
@router.message()
async def process_incorrect_message(message: Message):
    try:
        await message.answer(text=LEXICON_RU["other_answer"])
    except:
        await message.answer(text=LEXICON_RU["processing_incorrect_message_error"])
        logger.info("Error while processing incorrect message")
