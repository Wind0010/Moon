import asyncio
from aiogram import Bot, Dispatcher, executor, types
import logging
from decouple import config

token = config('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Hello,{name} i am AI you can ask me anything.")
 @dp.message_handler()
async def echo_handler(message: types.Message):
    text = message.text
    await message.answer(text)
@dp.message_handler()
async def echo_handler(message):
    await message.answer("Ask me here -> https://chatgpt.com/")



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
