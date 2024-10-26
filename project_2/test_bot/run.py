import asyncio
from aiogram import Bot, Dispatcher
from bot.configs.config import BotConfig
from logsettings import create_logger
from bot.handlers.user_handlers import router as user_rounter
from bot.handlers.other_handlers import router as other_rounter
from bot.keyboards.mail_menu import set_main_menu


from books.book_converter import prepare_book

async def mail():
    create_logger(__name__, 'Starting bot')
    
    bot_config= BotConfig()
    
    bot = Bot(token=bot_config.token, parse_mode='HTML')
    dp= Dispatcher()
    
    await set_main_menu(bot)
    
    dp.include_router(user_rounter)
    dp.include_router(other_rounter)

    await bot.delete_webhook(drop_pending_update=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    