import random
import angar
from aiogram.types import FSInputFile
import logging
from aiogram import Dispatcher, Bot, types
import asyncio
from aiogram.filters import Command
import password

logging.basicConfig(level=logging.INFO)
bot = Bot(password.TOKEN)
dp = Dispatcher()


@dp.message(Command('samoletik'))
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.park[a][0])))
    await message.answer(angar.park[a][1])


async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())