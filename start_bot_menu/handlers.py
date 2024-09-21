import bot_send_media
import rsp_gamebot
import guess_num
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold
from loader import dp


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')


@dp.message()
async def menu(message: Message):
    menu_buttons = [[KeyboardButton(text='получить ответ на вопрос, да или нет?')],
                    [KeyboardButton(text='посмотреть на котиков?')],
                    [KeyboardButton(text='Поиграть в игру "отгадай цифру"')],
                    [KeyboardButton(text='Поиграть в игру "камень, ножницы, бумага"')],
                    ]
    keyboard_menu = ReplyKeyboardMarkup(
        keyboard=menu_buttons,
        resize_keyboard=True,
    )
    await message.answer(text='Выбери, что ты хочешь:', reply_markup=keyboard_menu)
