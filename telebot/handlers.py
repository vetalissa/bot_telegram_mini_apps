from contextlib import suppress

from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

from loader import dp


# Декоратор регистрирует этот обработчик для команды /start.
@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Отправила ответное сообщение с приветствием, включая полное имя пользователя в жирном стиле.
    """
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!')
