import asyncio
import logging
import sys

from handlers import answer_for_message, cmd_start, menu
from loader import bot, dp


async def main() -> None:
    """
    Регистрация обработчиков команды /start и эха.
    Запуск процесса опроса для получения обновлений.
    """
    dp.message.register(cmd_start)
    dp.message.register(menu)
    dp.message.register(answer_for_message)

    await dp.start_polling(bot)


if __name__ == '__main__':
    """
    Настройка журналирования на уровне INFO.
    Запуск основной функции main с использованием asyncio.run().
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
