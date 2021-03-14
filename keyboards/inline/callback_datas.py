from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "id", "item_name", "price")

confirmation_callback = CallbackData("confirmation", "bool")

action_callback = CallbackData("edit", "what_action", "id")

numbering_callback = CallbackData("numbering", "what_action", "number")
