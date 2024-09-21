from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio

TOKEN = '7756622464:AAHvMfWP9nuMO2cE0V24zAbikMhhD0bNdgU'

def some_func():
    pass

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    some_func()
    
    @dp.message()
    async def echo(message: Message):
        await message.answer