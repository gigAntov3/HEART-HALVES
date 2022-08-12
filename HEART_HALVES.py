from aiogram import executor
from Bot_creation import dp
from Handlers.ClientHandlers import register_handler_client
from Handlers.AdminHandlers import register_handler_admin

register_handler_admin(dp)
register_handler_client(dp)

executor.start_polling(dp, skip_updates= True)