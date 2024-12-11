import json
import logging
import asyncio
import requests

from datetime import datetime, timedelta
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from mytoken import TOKEN  # Импортируем токен из файла

logging.basicConfig(level=logging.INFO)


TOKEN = '7539834728:AAGeuBtBetJd9aal7wwdTsoNokWTWukhnHU'
ACCESS_KEY = "в личке в телеграме"
URL = 'https://api.weather.yandex.ru/graphql/query'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("pogoda"))
async def get_weather(message: types.Message):
    query = """{
        weatherByPoint(request: { lat: 53.6246, lon: 55.9501 }) {
            now {
                temperature
                condition
            }
        }
    }"""
    headers = {"X-Yandex-Weather-Key": ACCESS_KEY}
    response = requests.post(URL, headers=headers, json={'query': query})

    if response.status_code == 200:
        weather_data = response.json()
        if 'data' in weather_data:
            temperature = weather_data['data']['weatherByPoint']['now']['temperature']
            await message.answer(f"Температура в Стерлитамаке: {temperature}°C")
        else:
            await message.answer("Ошибка: данные не получены.")
    else:
        await message.answer("Ошибка API: проверьте свой запрос.")



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
