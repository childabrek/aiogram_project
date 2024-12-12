import random
from multiprocessing.managers import State
from aiogram.fsm.state import StatesGroup
import angar
from aiogram.types import FSInputFile, Message
import logging
from aiogram import Dispatcher, Bot, types, F
import asyncio
from aiogram.filters import Command
import password
from angar import gallery

logging.basicConfig(level=logging.INFO)
bot = Bot(password.TOKEN)
dp = Dispatcher()


@dp.message(Command('samoletik'))
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.gallery[a])))
    await message.answer(angar.park[a])

@dp.message(Command('add_samoletik'))
async def add(message: Message, bot: Bot):
    print(":")
    await message.reply('Отправьте фото самолетика')
    await bot.download(
        message.photo[-1],
        destination=f"bank/{len(gallery)}.jpg"
    )
    await message.reply('Фото сохранено!\nТеперь отправьте текст')



async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())
