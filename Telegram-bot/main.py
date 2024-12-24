from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

frame_buttons_1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Регистрация')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Купить')

frame_buttons_1.row(button1, button2)
frame_buttons_1.add(button3, button4)

frame_buttons_2 = InlineKeyboardMarkup(resize_keyboard=True)
button5 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button6 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
frame_buttons_2.row(button5, button6)

frame_prod_buttons = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
prod_button1 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
prod_button2 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
prod_button3 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
prod_button4 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
frame_prod_buttons.add(prod_button1, prod_button2, prod_button3, prod_button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно!')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=frame_buttons_1)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=frame_buttons_2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = [
        r'D:\Python\ProjectPythonUrbanUni\module_14\images_product\1.jpeg',
        r'D:\Python\ProjectPythonUrbanUni\module_14\images_product\2.jpeg',
        r'D:\Python\ProjectPythonUrbanUni\module_14\images_product\3.jpeg',
        r'D:\Python\ProjectPythonUrbanUni\module_14\images_product\4.jpeg',
    ]

    base = get_all_products()

    for i, v in enumerate(images):
        with open(v, 'rb') as img:
            await message.answer_photo(img)
            await message.answer(f'Название: {base[i][1]}|' f' Описание: {base[i][2]}| Цена: {base[i][3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=frame_prod_buttons)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=float(message.text))
    await message.answer('Введите свой рост (см.):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите свой вес (кг.):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    norm_cal = (10.0 * data['weight']) + (6.25 * data['growth']) - (5.0 * data['age']) - 161.0
    await message.answer(f'Ваша норма калорий, необходимая для '
                         f'функцйонирования организма - {norm_cal} калорий.')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
