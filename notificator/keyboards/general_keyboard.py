from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

button_list_notes = KeyboardButton(text=LEXICON_RU["list_notes"])
button_create_note = KeyboardButton(text=LEXICON_RU["create_note"])

button_cancel = KeyboardButton(text=LEXICON_RU["cancel"])

cancel_button: ReplyKeyboardMarkup = (
    ReplyKeyboardBuilder()
    .row(
        button_cancel,
        width=6,
    )
    .as_markup(
        one_time_keyboard=True,
        resize_keyboard=True,
    )
)


general_buttons_builder = ReplyKeyboardBuilder()

general_buttons_builder.row(
    button_list_notes,
    button_create_note,
    width=6,
)

general_buttons: ReplyKeyboardMarkup = general_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True,
)
