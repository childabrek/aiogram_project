import json
import logging
from datetime import datetime, timedelta

import password
import asyncio
import json
import aiogram
import requests
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from collections import defaultdict

# Тут все токены логины и пароли
import password


def load_events_from_json():
    try:
        with open('events.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return None


events = load_events_from_json()

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=password.TOKEN)
dp = Dispatcher()
user_message_count = defaultdict(int)


@dp.message(Command("count_vlad"))
async def count(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    username = message.from_user.full_name
    count = user_message_count[user_id]
    if username == "society":
        username = "Повелитель " + username
    else:
        username = "Ниндзя " + username
    await message.reply(f"{username}, ты отправил(а) {count} сообщений.")


@dp.message()
async def handle_message(message: types.Message):
    year = message.text.strip()
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    if year in events:
        funny_event = events[year]['funny']
        scary_event = events[year]['scary']
        response = f"Смешное событие {year} года: {funny_event}\n \nСтрашное событие {year} года: {scary_event}"
        await message.reply(response)
    elif year == "1488":
        await message.reply('Это не смешно, такие "приколы" могут привести к уголовной ответственности.')


URL = 'https://api.weather.yandex.ru/graphql/query'


@dp.message(Command("pogoda"))
async def get_weather(message: types.Message):
    print(123213123)
    query = """{
        weatherByPoint(request: { lat: 53.6246, lon: 55.9501 }) {
            now {
                temperature
                condition
            }
        }
    }"""
    headers = {"X-Yandex-Weather-Key": password.ACCESS_KEY}
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


@dp.message()
async def count_messages(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    await asyncio.sleep(0.1)


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
