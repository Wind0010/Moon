import random

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from config import bot, dp


async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Далее', callback_data='quiz_2')

    keyboard.add(button)

    question = 'BMW or Mersedes or Audi'

    answer = ['BMW', "Mersedes", "Audi"]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='Ауди лучше!',
        open_period=20,
        reply_markup=keyboard
    )

async def quiz_2(call: types.CallbackQuery):
    question = 'Сколько хромосом у человека'
    answer = ['54', '67', '46', '15']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='Ну ну)',
        open_period=20
    )


def register_handlers_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='quiz_2')


games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']

@dp.message_handler(commands=['game'])
async def game_dice(message: types.Message):
    dice = random.choice(games)
    await message.answer(f'Вот ваша игра: {dice}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

