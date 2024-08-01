from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from fsm.fsm import FSMFillForm
from keyboards.general_keyboard import general_buttons, cancel_button
from lexicon.lexicon_ru import LEXICON_RU
from services.gateways.users_gateway import UserGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    try:
        # Проверка на известность пользователя
        if UserGateway.get(telegram_id):
            await message.answer(text=LEXICON_RU['start_answer'], reply_markup=general_buttons)
        else:
            await message.answer(text=LEXICON_RU['name_request'], reply_markup=cancel_button)
            await state.set_state(FSMFillForm.set_name)
    except:
        await message.answer(text=LEXICON_RU['start_bot_error'])
        logger.info('Error while starting bot by user')
        
        
# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    try:
        await message.answer(text=LEXICON_RU['help_answer'], reply_markup=general_buttons)
    except:
        await message.answer(text=LEXICON_RU['help_error'])
        logger.info('Error while getting help instruction') 
        

# Этот хэндлер срабатывает на отмену регистрации
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.set_name,
                                                            FSMFillForm.set_email))
async def process_registration_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['canceled_registration'],
        )
        await state.clear()
    except:
        await message.answer(text=LEXICON_RU['registration_cancel_error'])
        logger.info('Error while canceling registration')
        
        
# Этот хэндлер срабатывает на ввод имени пользователя
@router.message(F.text, StateFilter(FSMFillForm.set_name))
async def process_setting_name(message: Message, state: FSMContext):
    try:
        await state.set_data(data={'name': message.text})
        await message.answer(text=LEXICON_RU['setting_name_answer'], reply_markup=cancel_button)
        await state.set_state(FSMFillForm.set_email)
    except:
        await message.answer(text=LEXICON_RU['setting_name_error'])
        logger.info('Error while setting_name by user')
        
        
# Этот хэндлер срабатывает на ввод почты пользователя
@router.message(F.text, StateFilter(FSMFillForm.set_email))
async def process_compliting_registration(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    try:
        email = message.text
        data = await state.get_data()
        name = data['name']
        UserGateway.create(UserGateway, name=name, email=email, telegram_id=telegram_id)
        await message.answer(text=LEXICON_RU['compliting_registration_answer'], reply_markup=general_buttons)
        await state.clear()
    except:
        await message.answer(text=LEXICON_RU['setting_email_error'])
        logger.info('Error while setting email and compliting registration by user')          