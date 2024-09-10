import time

import requests
from aiogram import F, types
from aiogram.filters import CommandStart
from aiogram.methods import SendPhoto, SendVideo
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold
from loader import dp

PARAMETER_SENDER = 'CAT'  # Параметр отображения


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')


@dp.message(F.text == 'получить ответ на вопрос, да или нет?')
async def change_yesorno_parameter(message: Message):
    """
     Заменяет параметра на показ гиф мемов
    """
    global PARAMETER_SENDER
    PARAMETER_SENDER = 'YESORNO'
    keybord_yesorno_kb = [[KeyboardButton(text='получить ответ')],
                          [KeyboardButton(text='выйти')]]
    keyboard_yesorno = ReplyKeyboardMarkup(
        keyboard=keybord_yesorno_kb,
        resize_keyboard=True,
    )
    await message.answer(text='Подумай о своем вопросе...', reply_markup=keyboard_yesorno)


@dp.message(F.text == 'посмотреть на котиков?')
async def change_cat_parameter(message: Message):
    """
     Заменяет параметра на показ картинок котиков
    """
    global PARAMETER_SENDER
    PARAMETER_SENDER = 'CAT'
    keybord_cat_kb = [[KeyboardButton(text='Котики?')],
                      [KeyboardButton(text='выйти')]]
    keyboard_cat = ReplyKeyboardMarkup(
        keyboard=keybord_cat_kb,
        resize_keyboard=True,
    )
    await message.answer(text='Котики?', reply_markup=keyboard_cat)


@dp.message(F.text.in_(['Котики?', 'получить ответ']))
async def answer_for_message(message: types.Message) -> None:
    """
     Функция отдает, рандомную картинку или гифку
    """
    if PARAMETER_SENDER == 'YESORNO':
        API_MEM_URL = 'https://yesno.wtf/api?force=no?yes'
        mem_response = requests.get(API_MEM_URL)

        if mem_response.status_code == 200:
            await message.answer('Подумай о своем вопросе...')
            mem_link = mem_response.json()['image']
            time.sleep(2)
            await message.bot(SendVideo(chat_id=message.chat.id, video=mem_link))

    elif PARAMETER_SENDER == 'CAT':
        API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
        cat_response = requests.get(API_CATS_URL)

        if cat_response.status_code == 200:
            cat_link = cat_response.json()[0]['url']
            await message.bot(SendPhoto(chat_id=message.chat.id, photo=cat_link))
            await message.answer('Еще котиков? ответ нет не принимается')


@dp.message()
async def menu(message: Message):
    kb = [[KeyboardButton(text='получить ответ на вопрос, да или нет?')],
          [KeyboardButton(text='посмотреть на котиков?')]]
    keyboard2 = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text='Выбери, что ты хочешь:', reply_markup=keyboard2)
