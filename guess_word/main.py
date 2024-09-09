import asyncio
import logging
import sys

from handlers import process_stat_command
from loader import bot, dp


async def main() -> None:
    dp.message.register(process_stat_command)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
