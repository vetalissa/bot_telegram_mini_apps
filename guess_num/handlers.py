import random

from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loader import dp

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 10

# Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {user["total_games"]}\n'
        f'Игр выиграно: {user["wins"]}'
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


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    """
    Срабатывает для завершения игры
    """
    if not user['in_game']:
        await message.answer(
            'Игра не началась по вашей инициативе 😓. \n\n '
            'Если захотите поиграть - просто напишите об этом'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    """
    Срабатывает и отвевает на сообщения,
    которые имеют цифру от 1 до 100
    """
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
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
            user['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли 😰\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Это что число? Хотите сыграть?')


@dp.message()
async def process_other_answers(message: Message):
    """ Срабатывает и отвевает на любые другие сообщения,
        которые небыли обработаны выше"""
    if user['in_game']:
        await message.answer(
            'Это не похоже на число... '
            'Присылай только числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я ничего не умею, кроме игры в отгадай цифру...'
            'Давай просто сыграем в игру?'
        )
