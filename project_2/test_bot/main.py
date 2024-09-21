from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio

TOKEN = '7756622464:AAHvMfWP9nuMO2cE0V24zAbikMhhD0bNdgU'

bot = Bot(token=TOKEN)

dp = Dispatcher()

async def main():
    await dp.start_polling(bot)
    
    
asyncio.run(main())

@dp.message
async def handle_message(message: Message):
    await message.answer(message.text)