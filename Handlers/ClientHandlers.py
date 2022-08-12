from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from Bot_creation import bot, cursor, connect
from Keyboards.ClientKeyboards import HomeKeyboard, ExitQuestionnaireKeyboard, CreateQuestionnaireKeyboard,\
     ChoiceKeyboard, SeeKeyboard, InlineChoiceKeyboard, GenderKeyboard, WhoKeyboard, QuestionnaireKeyboard
from Handlers.ClientMessage import QuestionnaireMessage, MyQuestionnaireMessage
from random import randint

select_list = {}

class Questionnaire(StatesGroup):
    name = State()
    age = State()
    gender = State()
    who_find = State()
    city = State()
    photo = State()
    description = State()

async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Давай найдем тебе пару?', reply_markup= HomeKeyboard())

async def send_questionnaire(message: types.Message):
    try:
        cursor.execute("SELECT name, age, city, photo, description FROM Users WHERE ID = {}".format(message.chat.id))
        select_fetch = cursor.fetchone()
        await bot.send_photo(message.chat.id, select_fetch[3],caption= MyQuestionnaireMessage(select_fetch), reply_markup= QuestionnaireKeyboard())
    except:
       await bot.send_message(message.chat.id, 'У вас пока нет анкеты', reply_markup= CreateQuestionnaireKeyboard()) 

async def look_for_people(message: types.Message):
    
        cursor.execute("SELECT age, city, who_find FROM Users WHERE ID = {}".format(message.chat.id))
        select_fetch = cursor.fetchone()
        cursor.execute("SELECT name, age, city, photo, description FROM Users WHERE ID != {} AND age>={} AND age<={} AND city = '{}'\
             AND gender = '{}'".format(message.chat.id, select_fetch[0] - 2, select_fetch[0] + 2, select_fetch[1], select_fetch[2] ))
        select_fetch = cursor.fetchall()
        i = randint(0, len(select_fetch) - 1)
        await bot.send_photo(message.chat.id, select_fetch[i][3],caption= QuestionnaireMessage(select_fetch, i), reply_markup= ChoiceKeyboard())
        select_list['message.chat.id'] = select_fetch[i][3]
    # except:
    #     await bot.send_message(message.chat.id, 'Нет подходящих людей для вас, попробуйте изменить параметры анкеты.', reply_markup= QuestionnaireKeyboard())

async def like_choice(message: types.Message):
    try:
        cursor.execute("SELECT ID FROM Users WHERE photo = '{}'".format(select_list['message.chat.id']))
        select_fetch = cursor.fetchone()
        cursor.execute('INSERT INTO People_search (sender_ID, recipient_ID, status) VALUES (?, ?, ?)', \
            (message.chat.id, select_fetch[0], 'Отправлено'))
        connect.commit()
        await bot.send_message(select_fetch[0], 'Вы кому-то понравились', reply_markup= SeeKeyboard())
        cursor.execute("SELECT name, age, city, photo, description FROM Users WHERE ID != {}".format(message.chat.id))
        select_fetch = cursor.fetchall()
        i = randint(0, len(select_fetch) - 1)
        await bot.send_photo(message.chat.id, select_fetch[i][3],caption= QuestionnaireMessage(select_fetch, i), reply_markup= ChoiceKeyboard())
        select_list['message.chat.id'] = select_fetch[i][3]
    except:
        await bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз.', reply_markup= HomeKeyboard())

async def like_questionnaire(message: types.Message):
    cursor.execute("SELECT sender_ID FROM People_search WHERE recipient_ID = {} AND status = 'Отправлено'".format(message.chat.id))
    select_fetch = cursor.fetchall()
    for i in range(len(select_fetch)):
        cursor.execute("SELECT name, age, city, photo, description FROM Users WHERE ID = {}".format(select_fetch[i][0]))
        select_fetch_2 = cursor.fetchone()
        await bot.send_photo(message.chat.id, select_fetch_2[3],caption= MyQuestionnaireMessage(select_fetch_2), reply_markup= InlineChoiceKeyboard(select_fetch[i][0]))

async def inline_handler(callback: types.CallbackQuery):
    try:
        data = callback.data.split(' ')
        cursor.execute("UPDATE People_search SET status = 'Просмотрено' WHERE sender_ID = ? AND recipient_ID = ?", \
            (data[1], callback.message.chat.id))
        cursor.execute("DELETE FROM People_search WHERE sender_ID = ? AND recipient_ID = ? AND status = 'Просмотрено'", \
            (data[1], callback.message.chat.id))
        connect.commit()
        if 'lik' in callback.data:
            cursor.execute("SELECT username FROM Users WHERE ID = {}".format(callback.message.chat.id))
            username_fetch = cursor.fetchone()
            cursor.execute("SELECT name, age, city, photo, description, gender, username FROM Users WHERE ID = {}".format(data[1]))
            select_fetch = cursor.fetchone()
            await bot.send_message(callback.message.chat.id,'Вот ссылка на профиль:    @' + str(select_fetch[6]), reply_markup= HomeKeyboard())
            cursor.execute("SELECT name, age, city, photo, description, gender, username FROM Users WHERE ID = {}".format(data[1]))
            select_fetch = cursor.fetchone()
            if select_fetch[5] == 'Мужской':
                await bot.send_photo(data[1], select_fetch[3],caption= 'Вам ответил ' + MyQuestionnaireMessage(select_fetch) + \
                    '\nВот ссылка на профиль:    @' + str(username_fetch[0]), reply_markup= HomeKeyboard())
            else:
                await bot.send_photo(data[1], select_fetch[3],caption= 'Вам ответила ' + MyQuestionnaireMessage(select_fetch) + \
                    '\nВот ссылка на профиль:    @' + str(username_fetch[0]), reply_markup= HomeKeyboard())    
    except:
        await bot.send_message(callback.message.chat.id, 'Вы уже ответили этому человеку.', reply_markup= HomeKeyboard())

async def start_load(message: types.Message, state = None):
    await Questionnaire.name.set()
    await bot.send_message(message.chat.id, 'Напиши свое имя...', reply_markup= ExitQuestionnaireKeyboard())

async def exit_machine(message: types.Message, state = FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, 'Создание или редактирование анкеты прекращено.', reply_markup= HomeKeyboard())

async def load_name(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Questionnaire.next()
    await message.answer('Напиши свой возраст...', reply_markup= ExitQuestionnaireKeyboard())

async def load_age(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await Questionnaire.next()
    await message.answer('Напиши свой пол...', reply_markup= GenderKeyboard())

async def load_gender(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await Questionnaire.next()
    await message.answer('Напиши кого хочешь найти...', reply_markup= WhoKeyboard())

async def load_who(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['who_find'] = message.text
    await Questionnaire.next()
    await message.answer('Напиши откуда ты...', reply_markup= ExitQuestionnaireKeyboard())

async def load_city(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await Questionnaire.next()
    await message.answer('Отправь фото...', reply_markup= ExitQuestionnaireKeyboard())

async def load_photo(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await Questionnaire.next()
    await message.answer('Напиши о себе...', reply_markup= ExitQuestionnaireKeyboard())

async def load_description(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    async with state.proxy() as data:
        cursor.execute("SELECT ID FROM Users WHERE ID ={}".format(message.chat.id))
        select_fetch = cursor.fetchone()
        try:
            if data['who_find'] == 'Мужчину':
                data['who_find'] = 'Мужской'
            elif data['who_find'] == 'Женщину':
                data['who_find'] = 'Женский'
            if message.chat.id == select_fetch[0]:
                cursor.execute("UPDATE Users SET name = '{}', age = {}, city = '{}', photo = '{}', description = '{}', gender = '{}',\
                     who_find = '{}', username = '{}' WHERE ID = '{}'".format(data['name'], int(data['age']), data['city'], data['photo'],\
                         data['description'], data['gender'], data['who_find'], message.chat.username, message.chat.id))
                await bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup= HomeKeyboard())
            elif not TypeError:
                cursor.execute('INSERT INTO Users (ID, name, age, city, photo, description, gender, who_find, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',\
                     (message.chat.id, data['name'], data['age'], data['city'], data['photo'], data['description'], data['gender'], \
                        data['who_find'], message.chat.username))
                await bot.send_message(message.chat.id, 'Анкета создана', reply_markup= HomeKeyboard())
                
        except TypeError:
            cursor.execute('INSERT INTO Users (ID, name, age, city, photo, description, gender, who_find, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',\
                 (message.chat.id, data['name'], data['age'], data['city'], data['photo'], data['description'], data['gender'],\
                     data['who_find'], message.chat.username))
            await bot.send_message(message.chat.id, 'Анкета создана', reply_markup= HomeKeyboard())
    connect.commit()
    await state.finish()

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(start, lambda message: message.text == '💤')
    dp.register_message_handler(look_for_people, lambda message: message.text == 'Искать пару')
    dp.register_message_handler(like_questionnaire, lambda message: message.text == 'Посмотреть')
    dp.register_callback_query_handler(inline_handler)
    dp.register_message_handler(like_choice, lambda message: message.text == '❤️')
    dp.register_message_handler(look_for_people, lambda message: message.text == '👎')
    dp.register_message_handler(send_questionnaire, lambda message: message.text == 'Моя анкета')
    dp.register_message_handler(start_load,lambda message: message.text == 'Создать анкету' or message.text == 'Редактировать анкету', state= None)
    dp.register_message_handler(exit_machine, lambda message: message.text == 'Отменить действия с анкетой', state= '*')
    dp.register_message_handler(load_name, state= Questionnaire.name)
    dp.register_message_handler(load_age, state= Questionnaire.age)
    dp.register_message_handler(load_gender, state= Questionnaire.gender)
    dp.register_message_handler(load_who, state= Questionnaire.who_find)
    dp.register_message_handler(load_city, state= Questionnaire.city)
    dp.register_message_handler(load_photo, content_types=['photo'], state= Questionnaire.photo)
    dp.register_message_handler(load_description, state= Questionnaire.description)