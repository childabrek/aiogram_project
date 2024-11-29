import json
import logging
import asyncio
from datetime import datetime
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command, Filter
from aiogram.types import FSInputFile

logging.basicConfig(level=logging.INFO)
TOKEN = '7605960349:AAECPUTKkAm_8RR1wvWWMQKYYv8OS8AgQ2Y'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply('Hello world!' + message.from_user.username, parse_mode='pre-formatted fixed-width code block')


@dp.message()
async def echo(message: types.Message):
    a = FSInputFile("1.jpg")
    await message.answer_photo(a)


with open('words.json', 'r', encoding='utf-8') as f:
    bad_words_data = json.load(f)
    bad_words = [item['word'] for item in bad_words_data]

user_last_deleted_time = {}

@dp.message(Command('delete'))
async def delete_message(msg: types.Message):
    if msg.reply_to_message:
        message_id_to_delete = msg.reply_to_message.message_id
        chat_id = msg.chat.id

        await bot.delete_message(chat_id, message_id_to_delete)
        await msg.answer("Сообщение удалено.")

        user_last_deleted_time[msg.from_user.id] = datetime.now()
    else:
        await msg.answer("Пожалуйста, ответьте на сообщение, которое хотите удалить.")

@dp.message()
async def auto_delete_message(msg: types.Message):
    if any(bad_word in msg.text.lower() for bad_word in bad_words):
        await bot.delete_message(msg.chat.id, msg.message_id)
        logging.info(f"Удалено сообщение: {msg.text}")

        user_last_deleted_time[msg.from_user.id] = datetime.now()

    if msg.from_user.id in user_last_deleted_time:
        last_deleted_time = user_last_deleted_time[msg.from_user.id]
        if datetime.now() - last_deleted_time <= timedelta(minutes=30):
            await bot.delete_message(msg.chat.id, msg.message_id)



async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())
