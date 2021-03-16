import time

from YaDiskClient.YaDiskClient import YaDisk
from data import config


class YandexDiskClass:

    def __init__(self):
        self.path_main = "TelegramCouponBOT"
        self.disk = YaDisk(config.DISK_LOGIN, config.DISK_PASSWORD_APP)
        elements = self.disk.ls("/")
        for element in elements:
            if element['isDir'] and element['displayname'] == self.path_main:
                return
        self.disk.mkdir(self.path_main)

    def get_user(self, userID):
        try:
            return self.disk.ls(f"{self.path_main}/{userID}")
        except:
            return None

    def mkdir_user(self, userID):
        try:
            self.disk.mkdir(f"{self.path_main}/{userID}")
        except:
            print(f"YandexDisk Error: <{userID}> Данный пользователь уже создан")

    def add_file(self, userID, file):
        if not self.get_user(userID):
            self.mkdir_user(userID)
        elements_path = file.split('/')
        file_name = elements_path[len(elements_path)-1]
        self.disk.upload(file, f"/{self.path_main}/{userID}/{file_name}")


YandexDisk = YandexDiskClass()
