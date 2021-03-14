import json

from utils.db_api.db import DataBase
import time


class MessageCoupon:

    def __init__(self, id, userID, message, document, date, active):
        self.id = id
        self.userID = userID
        self.message = message
        self.document = document
        self.date = date
        self.active = active

    def updateActive_message(self):
        return DataBase.request("UPDATE `messages_coupon` SET `active`=0 WHERE `id`=%(id)s", {"id": self.id})


def create_messages(userID, message, document):
    return DataBase.request(
        "INSERT INTO `messages_coupon`(`userID`, `message`, `document`, `active`, `date`) VALUES (%(userID)s,%(message)s,%(document)s,1,%(date)s)",
        {"userID": userID, "message": message, "document": json.dumps(document), "date": int(time.time())})


def get_messages(page=0, max_size_messages=10):
    response = DataBase.request(
        "SELECT `id`,`userID`, `message`, `date` FROM `messages_coupon` WHERE `active`=1 LIMIT %(page)s,%(max_size_messages)s",
        {"page": page * max_size_messages, "max_size_messages": max_size_messages})
    response["data"] = [response["data"]] if isinstance(response["data"], dict) else response["data"]
    messages = []
    for message in response["data"]:
        messages.append(MessageCoupon(message["id"], message["userID"], message["message"], [], message["date"], True))
    return messages


def get_messages_count():
    response = DataBase.request(
        "SELECT COUNT(`id`) AS 'count' FROM `messages_coupon` WHERE `active`=1")
    return response["data"]["count"] if response["code"] == 200 else 0


def get_message(id):
    response = DataBase.request(
        "SELECT `id`, `userID`, `message`, `document`, `active`, `date` FROM `messages_coupon` WHERE `id`=%(id)s",
        {"id": id})
    message = None
    if response["code"] == 200:
        message = MessageCoupon(response["data"]["id"], response["data"]["userID"], response["data"]["message"], response["data"]["document"], response["data"]["date"], response["data"]["active"])
    return message


def get_last_message_day_user(userID):
    response = DataBase.request(
        "SELECT `id`, `userID`, `message`, `document`, `active`, `date` FROM `messages_coupon` WHERE `userID`=%(userID)s AND `date`>%(date)s",
        {"userID": userID, "date": time.time() - 60 * 60 * 24})
    response["data"] = [response["data"]] if isinstance(response["data"], dict) else response["data"]
    messages = []
    for message in response["data"]:
        messages.append(MessageCoupon(message["id"], message["userID"], message["message"], message["document"], message["date"], message["active"]))
    return messages

