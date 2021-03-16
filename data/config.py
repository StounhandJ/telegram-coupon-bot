from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
dbUSER = env.str("dbUSER")
dbPASSWORD = env.str("dbPASSWORD")
DATABASE = env.str("DATABASE")
DISK_LOGIN = env.str("DISK_LOGIN")
DISK_PASSWORD_APP = env.str("DISK_PASSWORD_APP")

months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декабрь"]

max_size_messages = 10  # Количество репортов в одном сообщение
backup_time = 5  # Время переноса файлов на диск

notFoundImg = "FileNotFound/order_pr_detailed_infoimg.jpg"  # Изображение когда не найдено запрашиваемое
notFoundDocument = "FileNotFound/404.txt"  # Докумень когда не найден запрашиваемый

message = {
    "confirmations_agreement": "<b>Вы подтверждаете согласие с данным соглашением?</b>",
    "confirmations_agreement_no": "❗ <i>При отказе вы не сможете пользоваться услугами бота</i> ❗\n\n<b>Вы подтверждаете согласие с данным соглашением?</b>",

    "Welcome_Menu": "Добрый день. Чего желаете?",
    "About_Us": "Neproblemka.ru - <i>сервис по решению ваших проблем в короткие сроки.</i>\n\n✔ <b>Ваша проблема - наше решение ✔</b>\n\nИспользуйте данную почту для связи: support@neproblemka.ru",
    "Main_Menu": "Главное меню",
    "Help_Menu": "Все ваши вопросы просим направить на почту: <b>support@neproblemka.com</b>",
    "comment_documentCheck": "Есть дополнительный файл?",
    "comment_document": "Прикрепите файл, если у вас несколько файлов добавьте архив:",
    "document_confirmation": "Ваш документ:\n{text}",
    "document_confirmation_size": "Документ:\n{text}\nСлишком большого размера, отправьте другой или свежитесь с администрацией",
    "comment_confirmation": "Ваш текст:\n\n{text}",
    "message_sent": "✔ <b>Сообщение отправлено администрации</b> ✔",
    "message_no": "Напишите свое сообщение ещё раз: ",
    "message_cancel": "❌ Отправка сообщения администрации отменена ❌",
    "increased_requests": "Вы превысили количество обращений в день",
    "repeat_requests": "Вы недавно отправили сообщение.\nПовторное можно будет отправить через\n⏱ <b>{min}</b> минут ⏱",
    "report_mes": "Напишите ваше сообщение:",
    "comment_email": "Напишите свой email для связи: ",
    "email_confirmation": "Ваш email:\n\n{text}",
    "comment_email_no_validation": "Вы ввели неверный email, повторите:",
}

adminMessage = {
    "message_completed": "Данный заказ уже выполнен",
    "message_send": "Напишите сообщение для пользователя",
    "message_yes_send": "Сообщение успешно отправленно пользователю",
    "messages_main": "{start}\n{text}\n/mesinfo - информация о сообщении",
    "messages_missing": "Сообщений нет",
    "message_missing": "Данного сообщения нет",
    "messages_info": "{num}. Номер сообщения <b>{id}</b> от {date}\n",
    "message_detailed_info": "Номер сообщения <b>{id}</b>\nID отправителя <b>{userID}</b>\nТекст: {text}\nДата отправки: {date}\n",
    "messages_main_all": "Список сообщений от обычных пользователей:\n",
}

errorMessage = {
    "not_add_photo": "Если вы хотете прикрепить фото добавьте его,к примеру, в архив и отправьте"
}
