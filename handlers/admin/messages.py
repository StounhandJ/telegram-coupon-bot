import math
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from data import config
from keyboards.inline import buttons
from keyboards.inline.callback_datas import confirmation_callback, action_callback, numbering_callback
from loader import dp, bot
from states.admin_mes_user import AdminMesUser
from utils.db_api.models import messagesCouponModel
from utils import function
from utils.telegram_files import TelegramFiles


@dp.message_handler(Text(equals=["Сообщения от пользователей", "/mes"]), user_id=config.ADMINS)
async def all_messages(message: types.Message):
    mes, keyboard = await menu_main(0)
    await message.answer(text=mes, reply_markup=keyboard)


@dp.callback_query_handler(numbering_callback.filter(what_action="messagesUserNumbering"), user_id=config.ADMINS)
async def close_order_button(call: types.CallbackQuery, callback_data: dict):
    mes, keyboard = await menu_main(int(callback_data["number"]))
    try:
        await call.message.edit_text(text=mes, reply_markup=keyboard)
    except:
        await call.answer(cache_time=1)


@dp.message_handler(user_id=config.ADMINS, commands=["mesinfo", "infomes"])
async def show_info_mes(message: types.Message):
    await menu_info_mes(function.checkID(message.text), message)


# Отправка сообщения #

@dp.message_handler(user_id=config.ADMINS, commands=["usend", "usersend", "sendu", "usenduser"])
async def start_message_send(message: types.Message, state: FSMContext):
    await menu_send_mes(function.checkID(message.text), message, state)


@dp.callback_query_handler(action_callback.filter(what_action="MessageSend"), user_id=config.ADMINS)
async def close_order_button(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await menu_send_mes(callback_data.get("id"), call.message, state)
    await call.message.delete()


@dp.message_handler(state=AdminMesUser.message)
async def adding_comment(message: types.Message, state: FSMContext):
    message.text = function.string_handler(message.text)
    await state.update_data(message=message.text)
    await AdminMesUser.wait.set()
    await message.answer(config.message["comment_confirmation"].format(text=message.text),
                         reply_markup=await buttons.getConfirmationKeyboard(cancel="Отменить"))


@dp.message_handler(state=AdminMesUser.wait)
async def waiting(message: types.Message):
    pass


@dp.message_handler(state=AdminMesUser.document, content_types=types.ContentType.DOCUMENT)
async def message_add_doc(message: types.Message, state: FSMContext):
    if TelegramFiles.document_size(message.document.file_size):
        await state.update_data(document=message.document)
        await AdminMesUser.wait.set()
        await message.answer(config.message["document_confirmation"].format(
            text="{name} {size}мб\n".format(name=message.document.file_name, size=round(message.document.file_size/1024/1024, 3))),
            reply_markup=await buttons.getConfirmationKeyboard(cancel="Отменить заказ"))
    else:
        await message.answer(config.message["document_confirmation_size"].format(
            text="{name} {size}мб\n".format(name=message.document.file_name, size=round(message.document.file_size/1024/1024, 3))),
            reply_markup=await buttons.getCustomKeyboard(cancel="Отменить заказ"))


@dp.message_handler(state=AdminMesUser.document, content_types=types.ContentType.PHOTO)
async def message_add_doc(message: types.Message):
    await message.answer(text=config.errorMessage["not_add_photo"])


@dp.callback_query_handler(confirmation_callback.filter(bool="noElement"), state=AdminMesUser)
async def adding_promoCode_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mes = ""
    state_active = data.get("state_active")
    keyboard = None
    if "AdminMesUser:document" == state_active:
        await send_mes(call, state)
        return
    await call.message.edit_text(text=mes, reply_markup=keyboard)


@dp.callback_query_handler(confirmation_callback.filter(bool="Yes"), state=AdminMesUser)
async def adding_comment_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    state_active = data.get("state_active")
    mes = ""
    keyboard = None
    if "AdminMesUser:document" == state_active:
        await send_mes(call, state)
        return
    elif "AdminMesUser:documentCheck" == state_active:
        await AdminMesUser.document.set()
        mes = config.message["comment_document"]
        keyboard = await buttons.getCustomKeyboard(noElement="Нет файла")
    elif "AdminMesUser:message" == state_active:
        await AdminMesUser.documentCheck.set()
        mes = config.message["comment_documentCheck"]
        keyboard = await buttons.getConfirmationKeyboard(cancel="Отменить")
    await function.set_state_active(state)
    await call.message.edit_text(text=mes, reply_markup=keyboard)


@dp.callback_query_handler(confirmation_callback.filter(bool="No"), state=AdminMesUser)
async def adding_comment_no(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    state_active = data.get("state_active")
    keyboard = await buttons.getCustomKeyboard(cancel="Отменить")
    if "AdminMesUser:document" == state_active:
        await AdminMesUser.document.set()
    elif "AdminMesUser:documentCheck" == state_active:
        await send_mes(call, state)
        return
    elif "AdminMesUser:message" == state_active:
        await AdminMesUser.message.set()

    await call.message.edit_text(text=config.message["message_no"], reply_markup=keyboard)


@dp.callback_query_handler(confirmation_callback.filter(bool="cancel"), state=AdminMesUser)
async def adding_message_cancel(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.delete()
    await menu_info_mes(data.get("message_sendID"), call.message)
    await state.finish()


async def send_mes(call, state):
    await call.answer(cache_time=2)
    data = await state.get_data()
    messageInfo = messagesCouponModel.get_message(data.get("message_sendID"))
    if not messageInfo or (messageInfo and not messageInfo.active):
        await state.finish()
        await call.message.edit_text(config.adminMessage["message_completed"])
        return
    keys = data.keys()
    chatID = messageInfo.userID
    mes = data.get("message") if "message" in keys else ""
    doc = [data.get("document").file_id] if "document" in keys else []
    await bot.send_message(chat_id=chatID, text="<b>Ответ на вашу заявку</b>:")
    if len(doc) == 0 and mes != "":
        await bot.send_message(chat_id=chatID, text=mes)
    elif len(doc) == 1:
        await bot.send_document(chat_id=chatID, caption=mes, document=doc[0])
    elif len(doc) > 1:
        for document in doc:
            await bot.send_document(chat_id=chatID, document=document)
        if mes\
                != "":
            await bot.send_message(chat_id=chatID, text=mes)
    messageInfo.updateActive_message()
    await state.finish()
    await call.message.edit_text(config.adminMessage["message_yes_send"])


async def menu_send_mes(mesID, message, state):
    mes = config.adminMessage["message_missing"]
    messageInfo = messagesCouponModel.get_message(mesID)
    keyboard = None
    if messageInfo and not messageInfo.active:
        mes = config.adminMessage["message_completed"]
    elif messageInfo:
        await state.update_data(message_sendID=messageInfo.id)
        await AdminMesUser.message.set()
        await function.set_state_active(state)
        mes = config.adminMessage["message_send"]
        keyboard = await buttons.getCustomKeyboard(cancel="Отмена")
    await message.answer(text=mes, reply_markup=keyboard)


async def menu_info_mes(mesID, message):
    mes = "Данное сообщние не найдено"
    messageInfo = messagesCouponModel.get_message(mesID)
    keyboard = None
    if messageInfo:
        mes = config.adminMessage["message_detailed_info"].format(id=messageInfo.id, userID=messageInfo.userID,
                                                                  text=messageInfo.message,
                                                                  date=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                     time.localtime(
                                                                                         messageInfo.date)))
        mes += "Сообщение от пользователя"
        mes += "" if messageInfo.active else "\n<b>На сообщение уже ответили</b>"
        keyboard = await buttons.getActionKeyboard(messageInfo.id, MessageSend="Ответить") if messageInfo.active else None
        if len(messageInfo.document) == 1:
            await message.answer_document(caption=mes, document=messageInfo.document[0], reply_markup=keyboard)
            return
        elif len(messageInfo.document) > 1:
            for document in messageInfo.document:
                await message.answer_document(document=document)
    await message.answer(text=mes, reply_markup=keyboard)


async def menu_main(page):
    messages = messagesCouponModel.get_messages(page=page, max_size_messages=config.max_size_messages)
    messages_count = messagesCouponModel.get_messages_count()
    keyboard = None
    if messages:
        start = config.adminMessage["messages_main_all"]
        text = ""
        num = 1
        for item in messages:
            date = time.localtime(item.date)
            dateMes = "{year} год {day} {month} {min}".format(year=date.tm_year, day=date.tm_mday,
                                                              month=config.months[date.tm_mon - 1],
                                                              hour=date.tm_hour,
                                                              min=time.strftime("%H:%M", date))
            text += config.adminMessage["messages_info"].format(num=num+(page*config.max_size_messages), id=item.id, date=dateMes)
            num += 1
        mes = config.adminMessage["messages_main"].format(start=start, text=text)
        keyboard = await buttons.getNumbering(math.ceil(messages_count/config.max_size_messages), "messagesUserNumbering")
    else:
        mes = config.adminMessage["messages_missing"]
    return [mes, keyboard]
