from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def AdminKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Создать TextPost')
    butt2 = KeyboardButton('Создать PhotoPost')
    butt3 = KeyboardButton('Начать рассылку')
    butt4 = KeyboardButton('Выйти из Admin-панели')
    markup.add(butt1).insert(butt2).add(butt3).insert(butt4)
    return markup

def AdminExitMachineKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Отменить вход в Admin-панель')
    markup.add(butt1)
    return markup

def AdminExitMachineKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Отменить создание поста')
    markup.add(butt1)
    return markup