import random

from aiogram import F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from loader import dp

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 10

# кнопки согласия на начало игры
yes_no_bd = [[KeyboardButton(text='Давай'),
              KeyboardButton(text='Выйти')]]
yes_no_kb = ReplyKeyboardMarkup(
    keyboard=yes_no_bd,
    resize_keyboard=True,
    one_time_keyboard=True)

# Клавиатура с цифрами для игры
num_ls = []
num_buttons = []

for i in range(1, 101):
    num_ls.append(KeyboardButton(text=str(i)))
    if not i % 9:
        num_buttons.append(num_ls)
        num_ls = []

num_buttons.append([KeyboardButton(text='100')])
num_buttons.append([KeyboardButton(text='выйти')])
num_keyboard = ReplyKeyboardMarkup(
    keyboard=num_buttons,
    resize_keyboard=True)

# Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'count_game': 0,
        'win': 0,
        'loss': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(F.text == 'Поиграть в игру "отгадай число"')
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Я загадываю число от 1 до 100, \n'
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} попыток\n'
        'Для завершения игры, напишите /cancel\n\n'
        'Для просмотра статистики, напишите /stat\n\n'
        f'Количество побед: {user["win"]}\n'
        f'Количество проигрышей: {user["loss"]}\n'
        f'Всего игры: {user["count_game"]}\n',
        reply_markup=yes_no_kb
    )


@dp.message(Command(commands='stat'))
async def command_static_game(message: Message):
    await message.answer(
        f'Количество побед: {user["win"]}\n'
        f'Количество проигрышей: {user["loss"]}\n'
        f'Всего игры: {user["count_game"]}\n'
        f'Играем?\n',
        reply_markup=num_keyboard if user['in_game'] else yes_no_kb)


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    """
    Выход по команде "/cancel" или оповещение о не игре
    """
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом',
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
            f'Ну что? Число загадано, попробуй отгадать за {ATTEMPTS} попыток',
            reply_markup=num_keyboard
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat',
            reply_markup=num_keyboard
        )


@dp.message(F.text == 'Нет')
async def process_negative_answer(message: Message):
    """
    Срабатывает для завершения игры
    """
    if not user['in_game']:
        await message.answer(
            'Игра не началась по вашей инициативе 😓. \n\n '
            'Если захотите поиграть - просто напишите об этом',
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
                user['win'] += 1
                user['count_game'] += 1
                await message.answer(
                    ' Вы угадали число! Ура!!!\n\n'
                    'Может, сыграем еще?\n\n'
                    f'Количество побед: {user["win"]}\n'
                    f'Количество проигрышей: {user["loss"]}\n'
                    f'Всего игры: {user["count_game"]}\n',
                    reply_markup=yes_no_kb,
                )
            elif int(message.text) > user['secret_number']:
                user['attempts'] -= 1
                await message.answer(f'Мое число меньше\n\nУ вас осталось:{user["attempts"]} попыток',
                                     reply_markup=num_keyboard)
            elif int(message.text) < user['secret_number']:
                user['attempts'] -= 1
                await message.answer(f'Мое число больше\n\nУ вас осталось:{user["attempts"]} попыток',
                                     reply_markup=num_keyboard)

            if user['attempts'] == 0:
                user['in_game'] = False
                user['loss'] += 1
                user['count_game'] += 1
                await message.answer(
                    'К сожалению, у вас больше не осталось попыток\n'
                    'Вы проиграли 😰\n\n'
                    f'Мое число было {user["secret_number"]}\n\n'
                    'Давайте сыграем еще?\n\n'
                    f'Количество побед: {user["win"]}\n'
                    f'Количество проигрышей: {user["loss"]}\n'
                    f'Всего игры: {user["count_game"]}\n',
                    reply_markup=yes_no_kb
                )
        else:
            await message.answer(
                'Это не похоже на нужное число... '
                'Присылай только числа от 1 до 100\n'
                'Для завершения игры, напишите /cancel или любое слово', reply_markup=num_keyboard)
    else:
        await message.answer('Это что число? Хотите сыграть?', reply_markup=yes_no_kb)
