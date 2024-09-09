import time
from contextlib import suppress

import requests
from aiogram import F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.methods import SendPhoto, SendVideo
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from loader import dp

PARAMETER_SENDER = 'CAT' # Параметр отображения


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')


@dp.message(Command('menu'))
async def menu(message: types.Message):
    """
    Навигация для выбора.
    """
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='получить ответ на вопрос, да или нет?',
        callback_data='yes_or_no', ),
        types.InlineKeyboardButton(
            text='посмотреть на котиков?',
            callback_data='cat_img', ))

    with suppress(TelegramBadRequest):
        await message.answer(
            'Выбери, что ты хочешь:',
            reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'yes_or_no')
async def change_yesorno_parameter(callback: types.CallbackQuery):
    """
     Заменяет параметра на показ гиф мемов
    """
    global PARAMETER_SENDER
    PARAMETER_SENDER = 'YESORNO'
    await callback.message.answer('Напиши свой вопрос, ответ да или нет....')
    await callback.answer()


@dp.callback_query(F.data == 'cat_img')
async def change_cat_parameter(callback: types.CallbackQuery):
    """
     Заменяет параметра на показ картинок котиков
    """
    global PARAMETER_SENDER
    PARAMETER_SENDER = 'CAT'
    await callback.message.answer('Ты хочешь посмотреть на котиков?')
    await callback.answer()


@dp.message()
async def answer_for_message(message: types.Message) -> None:
    """
     Функция отдает, рандомную картинку или гифку
    """
    try:
        if PARAMETER_SENDER == 'YESORNO':
            API_MEM_URL = 'https://yesno.wtf/api?force=no?yes'
            mem_response = requests.get(API_MEM_URL)
            if mem_response.status_code == 200:
                mem_link = mem_response.json()['image']
                await message.answer('Подумай о своем вопросе...')
                time.sleep(5)
                await message.bot(SendVideo(chat_id=message.chat.id, video=mem_link))
        elif PARAMETER_SENDER == 'CAT':
            API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                await message.bot(SendPhoto(chat_id=message.chat.id, photo=cat_link))
                await message.answer('Еще котиков? ответ нет не принимается')
    except TypeError:
        await message.answer('Технические шоколадки!')
