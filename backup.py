import os
import shutil
import time

from utils.yandex_disk import YandexDisk
from data import config


def log(text):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] Backup: {text}")


def backup():
    log(f"Скрипт для бэкапа запущен. Бэкап будет происходить в {config.backup_time}")
    start_day = time.localtime(time.time()).tm_yday - 1
    while True:
        if time.localtime(time.time()).tm_hour == config.backup_time and start_day!=time.localtime(time.time()).tm_yday:
            start_day = time.localtime(time.time()).tm_yday
            date = time.time()
            log(f"Начался перенос файлов")
            users = os.listdir("documents")
            for user in users:
                if len(user.split(".")) == 1:
                    files = os.listdir(f"{os.getcwd()}/documents/{user}")
                    for file in files:
                        if len(file.split(".")) != 1:
                            YandexDisk.add_file(user, f"{os.getcwd()}/documents/{user}/{file}")
                    shutil.rmtree(f'{os.getcwd()}/documents/{user}')
            log(f"Перенос фалов закончился за {int(time.time() - date)} секунд")
        time.sleep(60*20)
