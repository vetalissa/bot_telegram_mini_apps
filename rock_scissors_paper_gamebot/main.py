import asyncio
import logging
import sys

from handlers import game_process, process_start_command
from loader import bot, dp


async def main() -> None:
    dp.message.register(game_process)
    dp.message.register(process_start_command)

    await dp.start_polling(bot)


if __name__ == '__main__':
    """
    Настройка журналирования на уровне INFO.
    Запуск основной функции main с использованием asyncio.run().
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
