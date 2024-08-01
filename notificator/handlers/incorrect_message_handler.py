from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from fsm.fsm import FSMFillForm
from keyboards.general_keyboard import general_buttons, cancel_button
from lexicon.lexicon_ru import LEXICON_RU
from services.gateways.notes_gateway import NotesGateway
from services.gateways.users_gateway import UserGateway
from bot import get_bot
from logger import logger

router = Router()

bot = get_bot()


# Хэндлер для обработки некорректных сообщений
@router.message()
async def process_incorrect_message(message: Message):
    try:
        await message.answer(text=LEXICON_RU['other_answer'])
    except:
        await message.answer(text=LEXICON_RU['processing_incorrect_message_error'])
        logger.info('Error while processing incorrect message')