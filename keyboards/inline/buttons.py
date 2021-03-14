from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import action_callback, confirmation_callback, numbering_callback
from data import config


async def getConfirmationKeyboard(**kwargs):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=confirmation_callback.new(bool="Yes")),
            InlineKeyboardButton(text="Нет", callback_data=confirmation_callback.new(bool="No"))
        ]])
    for arg, text in kwargs.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=confirmation_callback.new(bool=arg)))
    return keyboard


async def getCustomKeyboard(**kwargs):
    keyboard = InlineKeyboardMarkup()
    for arg, text in kwargs.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=confirmation_callback.new(bool=arg)))
    return keyboard


async def getActionKeyboard(id, **kwargs):
    keyboard = InlineKeyboardMarkup()
    for arg, text in kwargs.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=action_callback.new(what_action=arg, id=id)))
    return keyboard


async def getNumbering(count, action):
    if count < 2:
        return None
    buttons = []
    for number in range(0, count):
        if len(buttons) == number // config.row_numbering_keyboard: buttons.append([])
        buttons[number // config.row_numbering_keyboard].append(InlineKeyboardButton(text=str(number+1), callback_data=numbering_callback.new(what_action=action, number=number)))
    keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    return keyboard
