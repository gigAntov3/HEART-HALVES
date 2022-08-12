from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

bot = Bot('5534623998:AAELdoUIWjU4vvO7vDGNYjEs3U3U2Y3W-eA')
dp = Dispatcher(bot, storage=MemoryStorage())

connect = sqlite3.connect('AcquaintanceBase.db', check_same_thread=False)
cursor = connect.cursor()