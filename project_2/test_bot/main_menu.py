from aiogram import Bot
from aiogram.types import BotCommand

from bot.lexicon.lexicon_ru import get_menu_args

async def set_main_menu(bot: BOT) -> None:
    main_menu_command = [BotCommand(
        **kwargs
    ) for kwargs in get_menu_args()]
    await bot.set_my_command(main_menu_commands)