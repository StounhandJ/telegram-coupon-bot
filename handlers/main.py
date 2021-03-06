from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, CommandStart
from aiogram.dispatcher.filters.builtin import CommandHelp
from data import config
from keyboards.default.menu import menu
from keyboards.inline import buttons
from keyboards.inline.callback_datas import confirmation_callback
from loader import dp
from states.start import StartState
from utils.telegram_files import TelegramFiles


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await StartState.Confirmation.set()
    await message.answer_document(caption=config.message["confirmations_agreement"], document=await TelegramFiles.get_telegram_key_files("documents/Пользовательское соглашение.pdf", message.chat.id), reply_markup=await buttons.getConfirmationKeyboard())


@dp.callback_query_handler(confirmation_callback.filter(bool="Yes"), state=StartState)
async def adding_comment_or_promoCode_yes(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=config.message["Welcome_Menu"], reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(confirmation_callback.filter(bool="No"), state=StartState)
async def adding_comment_or_promoCode_yes(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.edit_caption(caption=config.message["confirmations_agreement_no"], reply_markup=await buttons.getConfirmationKeyboard())
    except:
        pass


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


@dp.message_handler(Text(equals=["Использовать скидку"]))
async def show_product(message: types.Message):
    await message.answer(config.message["use_discount"])
