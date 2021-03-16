from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Написать администрации")],
        [KeyboardButton(text="Использовать скидку")]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сообщения")]],
    resize_keyboard=True
)
