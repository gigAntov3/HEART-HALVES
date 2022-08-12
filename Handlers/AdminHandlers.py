import asyncio
from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from Bot_creation import bot, cursor, connect
from Keyboards.ClientKeyboards import HomeKeyboard
from Keyboards.AdminKeyboards import AdminKeyboard, AdminExitMachineKeyboard

class IsAdmin(StatesGroup):
    password = State()

class PhotoPost(StatesGroup):
    text = State()
    photo = State()

class TextPost(StatesGroup):
    text = State()

async def load_password(message: types.Message, state = None):
    await IsAdmin.password.set()
    await bot.send_message(message.chat.id, 'Введите пароль:', reply_markup= AdminExitMachineKeyboard())

async def admin_exit(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы вышли из Admin-панели.', reply_markup= HomeKeyboard())

async def exit_machine(message: types.Message, state = FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    if message.text == 'Отменить вход в Admin-панель':
        await bot.send_message(message.chat.id, 'Операция отменена.', reply_markup= HomeKeyboard())
    else:
        await bot.send_message(message.chat.id, 'Создание поста отменено', reply_markup= AdminKeyboard())

async def create_photopost(message: types.Message, state = None):
    await PhotoPost.text.set()
    await bot.send_message(message.chat.id, 'Введите текст', reply_markup= AdminExitMachineKeyboard())

async def create_textpost(message: types.Message, state = None):
    await TextPost.text.set()
    await bot.send_message(message.chat.id, 'Введите текст', reply_markup= AdminExitMachineKeyboard())

async def panel_entry(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    async with state.proxy() as data:
        if data['password'] == '12121212':
            await bot.send_message(message.chat.id, 'Вы успешно вошли в Admin-панель.', reply_markup= AdminKeyboard())
    await state.finish()

async def textpost_db(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        cursor.execute("INSERT INTO Posts (text) VALUES (?)",[data['text']])
        connect.commit()
    await bot.send_message(message.chat.id, 'Вы успешно создали пост.', reply_markup= AdminKeyboard())
    await state.finish()

async def photopost_text(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await PhotoPost.next()
    await message.answer('Отправь фото...', reply_markup= AdminExitMachineKeyboard())

async def photopost_photo(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        cursor.execute('INSERT INTO Posts (text, photo) VALUES (?, ?)',(data['text'], data['photo']))
        connect.commit()
    await bot.send_message(message.chat.id, 'Вы успешно создали пост.', reply_markup= AdminKeyboard())
    await state.finish()

async def mailing_list(message: types.Message):
    try:
        cursor.execute("Select text, photo FROM Posts")
        select_fetch = cursor.fetchone()
        cursor.execute("Select ID FROM Users")
        select_user_fetch = cursor.fetchall()
        if select_fetch[1] == None:
            for i in range(len(select_user_fetch)):
                await bot.send_message(select_user_fetch[i][0], select_fetch[0])
                await asyncio.sleep(.35)
        if select_fetch[1] != None:
            for i in range(len(select_user_fetch)):
                await bot.send_photo(select_user_fetch[i][0], select_fetch[1], caption = select_fetch[0])
                await asyncio.sleep(.35)
        cursor.execute("DELETE FROM Posts WHERE text = '{}'".format(select_fetch[0]))
        connect.commit()
    except TypeError:
        await bot.send_message(message.chat.id, 'Сначала создайте запись')


   



def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(load_password, commands=['admin'], state= None)
    dp.register_message_handler(exit_machine, lambda message: message.text == 'Отменить вход в Admin-панель' \
        or message.text == 'Отменить создание поста', state= '*')
    dp.register_message_handler(admin_exit, lambda message: message.text == 'Выйти из Admin-панели')
    dp.register_message_handler(create_textpost, lambda message: message.text == 'Создать TextPost', state= None)
    dp.register_message_handler(create_photopost, lambda message: message.text == 'Создать PhotoPost', state= None)
    dp.register_message_handler(panel_entry, state= IsAdmin.password)
    dp.register_message_handler(textpost_db, state= TextPost.text)
    dp.register_message_handler(photopost_text, state= PhotoPost.text)
    dp.register_message_handler(photopost_photo, content_types=['photo'], state= PhotoPost.photo)
    dp.register_message_handler(mailing_list, lambda message: message.text == 'Начать рассылку')
#     dp.register_message_handler(panel_entry, state= Questionnaire.name)