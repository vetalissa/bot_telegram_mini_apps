import bot_send_media
import rsp_gamebot
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold
from loader import dp


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')


@dp.message()
async def menu(message: Message):
    kb = [[KeyboardButton(text='получить ответ на вопрос, да или нет?')],
          [KeyboardButton(text='посмотреть на котиков?')],
          [KeyboardButton(text='Поиграть в игру "отгадай цифру"')],
          [KeyboardButton(text='Поиграть в игру "камень, ножницы, бумага"')],
          ]
    keyboard2 = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text='Выбери, что ты хочешь:', reply_markup=keyboard2)
