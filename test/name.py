import asyncio
import logging
import os
import random
from aiogram import Dispatcher, Bot, types, F
from aiogram.types import FSInputFile
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

bot = Bot("7824388645:AAE6msq5JEgooH4CmGmb6i5lGFViV1uUafo")
dp = Dispatcher()

@dp.message(Command("photo"))
async def photo(message: types.Message):
    if 'хаял' in message.text.lower():
        await message.answer_photo(FSInputFile("photo_5350502582289820453_y.jpg"))
    elif 'егор' in message.text.lower():
        await message.answer_photo(FSInputFile("5352856357512012198.jpg"))
    elif 'софья' in message.text.lower():
        await message.answer_photo(FSInputFile("5352856357512012202.jpg"))
    elif 'данил' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'ярослав' in message.text.lower():
        await message.answer_photo(FSInputFile("5366571021311800345.jpg"))
    elif 'наиль' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'ралим' in message.text.lower():
        await message.answer_photo(FSInputFile("5366571021311800346.jpg"))
    elif 'марат' in message.text.lower():
        await message.answer_photo(FSInputFile("5366571021311800355.jpg"))
    elif 'илья п' in message.text.lower():
        await message.answer_photo(FSInputFile("5368739760752943028.jpg"))
    elif 'роза' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'арслан' in message.text.lower():
        await message.answer_photo(FSInputFile("5263010159985289133.jpg"))
    elif 'кирилл' in message.text.lower():
        await message.answer_photo(FSInputFile("maxresdefault.jpg"))
    elif 'илья м' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'артем ч' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'фаезбек' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'артур' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'влад' in message.text.lower():
        await message.answer_photo(FSInputFile("i.webp"))
    elif 'артем к' in message.text.lower():
        await message.answer_photo(FSInputFile("5368659006777843199.jpg"))
    else:
        await message.reply("\photo + имя человека.")
async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())