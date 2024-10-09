from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons 

class FSMStore(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    confirmation = State()

async def start_fsm(message: types.Message):
    await message.answer(text='Введите название товара: ', reply_markup=buttons.start)
    await FSMStore.product_name.set()

async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer('Выберите размер:', reply_markup=buttons.sizes)  
    await FSMStore.size.set()

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Введите категорию товара:')
    await FSMStore.category.set()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Введите стоимость товара:')
    await FSMStore.price.set()

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фото товара:', reply_markup=buttons.cancel) 
    await FSMStore.photo.set()

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

   
    await message.answer('Вот ваши данные:\n'
                         f'Название товара: {data["product_name"]}\n'
                         f'Размер: {data["size"]}\n'
                         f'Категория: {data["category"]}\n'
                         f'Стоимость: {data["price"]}\n')
    await message.answer_photo(photo=data['photo'], caption='Подтвердите данные: "Верные ли данные?"',
                               reply_markup=buttons.confirmation)  "
    await FSMStore.confirmation.set()

async def confirm_data(message: types.Message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            await message.answer("Сохранено в базу.")
        await state.finish()
    elif message.text == "Нет":
        await message.answer("Вы можете начать заново. Введите название товара:")
        await FSMStore.product_name.set()

async def cancel_fsm(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Регистрация отменена.")

def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(start_fsm, commands=['start'])
    dp.register_message_handler(load_product_name, state=FSMStore.product_name)
    dp.register_message_handler(load_size, state=FSMStore.size)
    dp.register_message_handler(load_category, state=FSMStore.category)
    dp.register_message_handler(load_price, state=FSMStore.price)
    dp.register_message_handler(load_photo, state=FSMStore.photo, content_types=['photo'])
    dp.register_message_handler(confirm_data, state=FSMStore.confirmation)
    dp.register_message_handler(cancel_fsm, state='*', commands=['cancel'])
