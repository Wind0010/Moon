import asyncio
from aiogram import Bot, Dispatcher, executor, types
import logging
from decouple import config

token = config('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_or_square(message: types.Message):
    try:

        number = float(message.text)

        await message.reply(str(number ** 2))
    except ValueError:

        await message.reply(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

