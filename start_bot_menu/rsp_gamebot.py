from random import choice

from aiogram import F
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from loader import dp

DATA_ANSWER = ['Камень 🗿', 'Ножницы ✂', 'Бумага 📜']
BOT_ANSWER = choice(DATA_ANSWER)


@dp.message(F.text == 'Поиграть в игру "камень, ножницы, бумага"')
async def process_start_command(message: Message):
    yes_no_bd = [[KeyboardButton(text='Давай играть'),
                  KeyboardButton(text='Не хочу')]]
    yes_no_kb = ReplyKeyboardMarkup(
        keyboard=yes_no_bd,
        resize_keyboard=True,
        one_time_keyboard=True)
    await message.answer('Привет!\nДавайте сыграем в игру "Камень, ножницы, бумага"?\n\n',
                         reply_markup=yes_no_kb)


@dp.message(F.text == 'Давай играть')
async def game_start(message: Message):
    game_bd = [[KeyboardButton(text='Камень 🗿')],
               [KeyboardButton(text='Ножницы ✂')],
               [KeyboardButton(text='Бумага 📜')],
               [KeyboardButton(text='Stop')]]

    game_kb = ReplyKeyboardMarkup(
        keyboard=game_bd,
        resize_keyboard=True)
    await message.answer('Выбирай', reply_markup=game_kb)


@dp.message(lambda message: message.text in DATA_ANSWER)
async def game_process(message: Message):
    print(message.text)
    try:
        global BOT_ANSWER
        tp_answer = (message.text, BOT_ANSWER)
        otvet = {
            ('Камень 🗿', 'Бумага 📜'): 'Камень 🗿 укрывается Бумагой 📜\nВы проиграли...',
            ('Камень 🗿', 'Ножницы ✂'): 'Камень 🗿 ломает Ножницы ✂\nВы выиграли!!!!',
            ('Камень 🗿', 'Камень 🗿'): 'Камень 🗿 равен Камню 🗿\nНичья...',

            ('Бумага 📜', 'Ножницы ✂'): 'Бумага 📜 режется об Ножницы ✂\nВы проиграли...',
            ('Бумага 📜', 'Камень 🗿'): 'Бумага 📜 укрывает камень 🗿\nВы выиграли!!!!',
            ('Бумага 📜', 'Бумага 📜'): 'Бумага 📜 равна Бумаге 📜\nНичья...',

            ('Ножницы ✂', 'Камень 🗿'): 'Ножницы ✂ ломаются об камень 🗿\nВы проиграли...',
            ('Ножницы ✂', 'Бумага 📜'): 'Ножницы ✂ режут Бумагу 📜\nВы выиграли!!!!',
            ('Ножницы ✂', 'Ножницы ✂'): 'Ножницы ✂ равны Ножницам ✂\nНичья...'
        }

        await message.answer(otvet[tp_answer])
        BOT_ANSWER = choice(DATA_ANSWER)
    except KeyError:
        await message.answer("ошибка")
