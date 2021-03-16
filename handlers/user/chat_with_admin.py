import os
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from re import *

from data import config
from keyboards.inline import buttons
from keyboards.inline.callback_datas import confirmation_callback
from loader import dp, bot
from states.user_mes import UserMes
from utils.db_api.models import messagesCouponModel, banListModel, userInformationModel
from utils.notify_admins import notify_admins_message
from utils import function
from utils.telegram_files import TelegramFiles


@dp.message_handler(Text(equals=["Написать администрации", "/ames"]))
async def start_write_administration(message: types.Message, state: FSMContext):
    if banListModel.is_ban_user(message.from_user.id):
        await message.answer("Вы забанены")
        return
    keyboard = None
    lastMessage = messagesCouponModel.get_last_message_day_user(message.from_user.id)
    if lastMessage and len(lastMessage) >= 20:
        mes = config.message["increased_requests"]
    elif lastMessage and lastMessage[len(lastMessage) - 1].date > time.time() - 60 * 30:
        mes = config.message["repeat_requests"].format(
            min=int((lastMessage[len(lastMessage) - 1].date-(time.time() - 60 * 30))/60))
    else:
        await UserMes.email.set()
        await function.set_state_active(state)
        mes = config.message["comment_email"]
        keyboard = await buttons.getCustomKeyboard(cancel="Отменить")
    await message.answer(text=mes, reply_markup=keyboard)


@dp.message_handler(state=UserMes.email)
async def adding_comment(message: types.Message, state: FSMContext):
    message.text = function.string_handler(message.text)
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
    if pattern.match(message.text):
        await state.update_data(email=message.text)
        await UserMes.wait.set()
        await message.answer(config.message["email_confirmation"].format(text=message.text),
                             reply_markup=await buttons.getConfirmationKeyboard(cancel="Отменить"))
    else:
        await message.answer(config.message["comment_email_no_validation"].format(text=message.text),
                             reply_markup=await buttons.getCustomKeyboard(cancel="Отменить"))


@dp.message_handler(state=UserMes.message)
async def adding_comment(message: types.Message, state: FSMContext):
    message.text = function.string_handler(message.text)
    await state.update_data(message=message.text)
    await UserMes.wait.set()
    await message.answer(config.message["comment_confirmation"].format(text=message.text),
                         reply_markup=await buttons.getConfirmationKeyboard(cancel="Отменить"))


@dp.message_handler(state=UserMes.wait)
async def waiting(message: types.Message):
    pass


@dp.message_handler(state=UserMes.document, content_types=types.ContentType.DOCUMENT)
async def message_add_doc(message: types.Message, state: FSMContext):
    if TelegramFiles.document_size(message.document.file_size):
        await state.update_data(document=message.document)
        await UserMes.wait.set()
        await message.answer(config.message["document_confirmation"].format(
            text="{name} {size}мб\n".format(name=message.document.file_name, size=round(message.document.file_size/1024/1024, 3))),
            reply_markup=await buttons.getConfirmationKeyboard(cancel="Отменить"))
    else:
        await message.answer(config.message["document_confirmation_size"].format(
            text="{name} {size}мб\n".format(name=message.document.file_name, size=round(message.document.file_size/1024/1024, 3))),
            reply_markup=await buttons.getCustomKeyboard(cancel="Отменить"))


@dp.message_handler(state=UserMes.document, content_types=types.ContentType.PHOTO)
async def message_add_doc(message: types.Message):
    await message.answer(text=config.errorMessage["not_add_photo"])


@dp.callback_query_handler(confirmation_callback.filter(bool="noElement"), state=UserMes)
async def adding_promoCode_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mes = ""
    state_active = data.get("state_active")
    keyboard = None
    if "UserMes:document" == state_active:
        await create_mes(call, state)
        return
    await call.message.edit_text(text=mes, reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(confirmation_callback.filter(bool="Yes"), state=UserMes)
async def adding_comment_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    state_active = data.get("state_active")
    mes = ""
    keyboard = None
    if "UserMes:document" == state_active:
        await create_mes(call, state)
        return
    elif "UserMes:documentCheck" == state_active:
        await UserMes.document.set()
        mes = config.message["comment_document"]
        keyboard = await buttons.getCustomKeyboard(noElement="Нет файла")
    elif "UserMes:message" == state_active:
        await UserMes.documentCheck.set()
        mes = config.message["comment_documentCheck"]
        keyboard = await buttons.getConfirmationKeyboard(cancel="Отменить")
    elif "UserMes:email" == state_active:
        await UserMes.message.set()
        mes = config.message["report_mes"]
        keyboard = await buttons.getCustomKeyboard(cancel="Отменить")
    await function.set_state_active(state)
    await call.message.edit_text(text=mes, reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(confirmation_callback.filter(bool="No"), state=UserMes)
async def adding_comment_no(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    state_active = data.get("state_active")
    keyboard = await buttons.getCustomKeyboard(cancel="Отменить")
    if "UserMes:document" == state_active:
        await UserMes.document.set()
    elif "UserMes:documentCheck" == state_active:
        await create_mes(call, state)
        return
    elif "UserMes:message" == state_active:
        await UserMes.message.set()
    elif "UserMes:email" == state_active:
        await UserMes.email.set()

    await call.message.edit_text(text=config.message["message_no"], reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(confirmation_callback.filter(bool="cancel"), state=UserMes)
async def adding_comment_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(config.message["message_cancel"])


async def create_mes(call, state):
    data = await state.get_data()
    message = data.get("message") if "message" in data.keys() else ""
    document = [data.get("document").file_id] if "document" in data.keys() else []
    email = data.get("email") if "email" in data.keys() else ""
    if document:
        await save_file(data.get("document"), call.from_user.id)
    messagesCouponModel.create_messages(call.from_user.id, message, document)
    userInformationModel.update_email(call.from_user.id, email)
    await state.finish()
    await notify_admins_message("Новое сообщение")
    await call.message.edit_text(config.message["message_sent"])


async def save_file(document, userID):
    path = f"{os.path.dirname(os.path.abspath(__file__))}/../../documents/{userID}"
    if not os.path.exists(path):
        os.makedirs(path)
    file_info = await bot.get_file(file_id=document.file_id)
    file_extension = os.path.splitext(file_info.file_path)[1]
    file_name = document.file_name.split(".")[0]
    file = await bot.download_file(file_path=file_info.file_path)
    with open(f'{path}/{file_name}{file_extension}', 'wb') as new_file:
        new_file.write(file.read())
