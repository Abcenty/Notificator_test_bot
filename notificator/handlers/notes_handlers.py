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

# Этот хэндлер срабатывает на команду /start
@router.message(F.text == LEXICON_RU['list_notes'], StateFilter(default_state))
async def process_show_notes(message: Message):
    telegram_id = message.from_user.id
    try:
        await message.answer(text=LEXICON_RU['show_notes_answer'], reply_markup=general_buttons)
        user_id = UserGateway.get(telegram_id).id
        notes = [note.text for note in NotesGateway.list(user_id)]
        text = ", ".join(notes).replace(", ", "\n")
        await message.answer(text=text, reply_markup=general_buttons)
    except:
        await message.answer(text=LEXICON_RU['showing_notes_error'])
        logger.info('Error while showing notes')
        
        
# Этот хэндлер срабатывает на отмену создания заметки
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.create_note,
                                                            FSMFillForm.set_timestamp))
async def process_canseling_creating_note(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['canceled_creating_note'],
            reply_markup=general_buttons,
        )
        await state.clear()
    except:
        await message.answer(text=LEXICON_RU['creating_note_error'])
        logger.info('Error while creating note')
        
        
# Этот хэндлер срабатывает на запрос создания заявки
@router.message(F.text == LEXICON_RU['create_note'], StateFilter(default_state))
async def create_note(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON_RU['create_note_answer'], reply_markup=cancel_button)
        await state.set_state(FSMFillForm.create_note)
    except:
        await message.answer(text=LEXICON_RU['create_note_error'])
        logger.info('Error while creating note')
        
        
# Этот хэндлер срабатывает на ввод текста заметки
@router.message(F.text, StateFilter(FSMFillForm.create_note))
async def set_note_text(message: Message, state: FSMContext):
    try:
        await message.answer(text=LEXICON_RU['set_note_text_answer'], reply_markup=cancel_button)
        await state.set_data(data={'text': message.text})
        await state.set_state(FSMFillForm.set_timestamp)
    except:
        await message.answer(text=LEXICON_RU['set_note_text_error'])
        logger.info('Error while setting text of note')
        
     
# Этот хэндлер срабатывает на ввод времени уведомления о заметке
@router.message(F.text, StateFilter(FSMFillForm.set_timestamp))
async def set_note_timestamp(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    try:
        user_id = UserGateway.get(telegram_id).id
        data = await state.get_data()
        text = data['text']
        NotesGateway.create(user_id=user_id, text=text, reminder_time=message.text)
        await message.answer(text=LEXICON_RU['finish_creating_note_answer'], reply_markup=general_buttons)
        await state.clear()
    except:
        await message.answer(text=LEXICON_RU['create_note_error'])
        logger.info('Error while setting timestamp')