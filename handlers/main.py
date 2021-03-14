from aiogram import types
from aiogram.dispatcher.filters.builtin import Text, CommandStart
from aiogram.dispatcher.filters.builtin import CommandHelp
from data import config
from keyboards.default.menu import menu
from keyboards.inline import buttons
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=config.message["Welcome_Menu"], reply_markup=menu)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    print(message.from_user.id)
    await message.answer(config.message["Help_Menu"])


@dp.message_handler(commands=["menu"])
async def show_menu(message: types.Message):
    await message.answer(config.message["Main_Menu"], reply_markup=menu)


@dp.message_handler(commands=["about"])
async def show_menu(message: types.Message):
    await message.answer(config.message["About_Us"], reply_markup=menu)


@dp.message_handler(Text(equals=["О нас"]))
async def show_about(message: types.Message):
    await message.answer(config.message["About_Us"], reply_markup=menu)


@dp.message_handler(commands=["Ukeyboard"])
async def show_help(message: types.Message):
    await message.answer(config.adminMessage["help"], reply_markup=menu)