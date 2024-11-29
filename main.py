import logging
import asyncio
from sched import scheduler

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command, Filter
from aiogram.types import FSInputFile

logging.basicConfig(level=logging.INFO)
TOKEN = '8122833408:AAFdg78LuB8AJFWUFaeU4pB8bMJB_uBM3Lo'

bot = Bot(token=TOKEN)
dp = Dispatcher()

#zet

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply('Hello world!' + message.from_user.username, parse_mode='pre-formatted fixed-width code block')


@dp.message()
async def echo(message: types.Message):
    a = FSInputFile("1.jpg")
    await message.answer_photo(a)

# Илья Маслов
async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


scheduler.add_job(wake_up_members, 'cron', hour=13, minute=39)


async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())
