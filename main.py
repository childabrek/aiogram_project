import aiogram
import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)
TOKEN = '7252389655:AAEmtpYiwFYGALtHEZC9vpUhB0KJxV9euj0'
bot = Bot(token=TOKEN)
dp = Dispatcher()

bot = Bot(token=TOKEN)

list_student= {"Илья": "ФИО, Дата рождения, номер телефона, серия номер паспорта"}

@dp.message(F.text, Command('test'))
async def start(message: types.Message, my_cakkback=None):
    dox = InlineKeyboardButton
    dox.row(types.InlineKeyboardButton(text="Найти", URL="")
    await message.answer(parse_mode=ParseMode.MARDOWN_V2, replay_markup=builder.as_markup())

if __name__ == '__main__':
    asyncio.run(start_dp())
