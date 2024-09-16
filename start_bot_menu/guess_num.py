import random

from aiogram import F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from loader import dp

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 10

# Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(F.text == 'Поиграть в игру "отгадай цифру"')
async def process_start_command(message: Message):
    yes_no_bd = [[KeyboardButton(text='Давай'),
                  KeyboardButton(text='Нет')]]
    yes_no_kb = ReplyKeyboardMarkup(
        keyboard=yes_no_bd,
        resize_keyboard=True,
        one_time_keyboard=True)

    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Я загадываю число от 1 до 100, \n'
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} попыток\n'
        'Для завершения игры, напишите /cancel',
        reply_markup=yes_no_kb
    )


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    """
    Выход по команде "/cancel" или оповещение о не игре
    """
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'Так мы же не играем...'
            'Может, сыграем разок?'
        )


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    """
    Срабатывает для начала игры при согласии
    """
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            f'Ну что? Число загадано, попробуй отгадать за {ATTEMPTS} попыток'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


@dp.message(F.text == 'Нет')
async def process_negative_answer(message: Message):
    """
    Срабатывает для завершения игры
    """
    if not user['in_game']:
        await message.answer(
            'Игра не началась по вашей инициативе 😓. \n\n '
            'Если захотите поиграть - просто напишите об этом'
        )


@dp.message(lambda x: x.text and x.text.isdigit())
async def process_numbers_answer(message: Message):
    """
    Срабатывает и отвевает на сообщения,
    которые имеют цифру от 1 до 100
    """
    if user['in_game']:
        if 1 <= int(message.text) <= 100:
            if int(message.text) == user['secret_number']:
                user['in_game'] = False
                await message.answer(
                    ' Вы угадали число! Ура!!!\n\n'
                    'Может, сыграем еще?'
                )
            elif int(message.text) > user['secret_number']:
                user['attempts'] -= 1
                await message.answer(f'Мое число меньше\n\nУ вас осталось:{user["attempts"]} попыток')
            elif int(message.text) < user['secret_number']:
                user['attempts'] -= 1
                await message.answer(f'Мое число больше\n\nУ вас осталось:{user["attempts"]} попыток')

            if user['attempts'] == 0:
                user['in_game'] = False
                await message.answer(
                    f'К сожалению, у вас больше не осталось '
                    f'попыток. Вы проиграли 😰\n\nМое число '
                    f'было {user["secret_number"]}\n\nДавайте '
                    f'сыграем еще?'
                )
        else:
            await message.answer(
                'Это не похоже на нужное число... '
                'Присылай только числа от 1 до 100\n'
                'Для завершения игры, напишите /cancel или любое слово'
            )
    else:
        await message.answer('Это что число? Хотите сыграть?')
