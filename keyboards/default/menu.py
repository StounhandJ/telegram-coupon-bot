from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Написать администрации")]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сообщения")]],
    resize_keyboard=True
)
