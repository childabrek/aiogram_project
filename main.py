import logging
import asyncio
from sched import scheduler

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Filter
from aiogram import F
from aiogram.types import Message, FSInputFile, inline_query_results_button, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
import yandex_weather_api

logging.basicConfig(level=logging.INFO)

import password

bot = Bot(token=password.TOKEN)
dp = Dispatcher()

# Привет это кар

# keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[])
#
# keyboard.

class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text


@dp.message(Command("start"))
async def start(message: types.Message):
    button = inline_query_results_button.InlineQueryResultsButton(text='test')
    await message.reply('Hello world!' + message.from_user.username, parse_mode='pre-formatted fixed-width code block')


@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    a = FSInputFile('123.txt')
    await message.answer_document(a)

# Илья Маслов
async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


# @dp.message(MyFilter("Хакнуть Илью"))
# async def hack(message: Message):
#     await message.answer(message.text.split()[1])
#
# scheduler.add_job(wake_up_members, 'cron', hour=13, minute=39)


async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())
