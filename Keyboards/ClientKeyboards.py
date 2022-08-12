from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def HomeKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Искать пару')
    butt2 = KeyboardButton('Моя анкета')
    markup.add(butt1).insert(butt2)
    return markup

def QuestionnaireKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Искать пару')
    butt2 = KeyboardButton('Редактировать анкету')
    markup.add(butt1).insert(butt2)
    return markup

def ChoiceKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('❤️')
    butt2 = KeyboardButton('👎')
    butt3 = KeyboardButton('💤')
    markup.add(butt1).insert(butt2).insert(butt3)
    return markup

def GenderKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Мужской')
    butt2 = KeyboardButton('Женский')
    butt3 = KeyboardButton('Отменить действия с анкетой')
    markup.add(butt1).insert(butt2).add(butt3)
    return markup

def WhoKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Мужчину')
    butt2 = KeyboardButton('Женщину')
    butt3 = KeyboardButton('Отменить действия с анкетой')
    markup.add(butt1).insert(butt2).add(butt3)
    return markup

def ExitQuestionnaireKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Отменить действия с анкетой')
    markup.add(butt1)
    return markup

def SeeKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Посмотреть')
    markup.add(butt1)
    return markup

def CreateQuestionnaireKeyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard= True)
    butt1 = KeyboardButton('Создать анкету')
    markup.add(butt1)
    return markup

def InlineChoiceKeyboard(ID):
    markup = InlineKeyboardMarkup(row_width=2)
    butt1 = InlineKeyboardButton('❤️', callback_data='lik ' + str(ID))
    butt2 = InlineKeyboardButton('👎', callback_data='dis ' + str(ID))
    markup.add(butt1, butt2)
    return markup




