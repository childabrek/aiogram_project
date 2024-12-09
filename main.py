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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
# Тут все токены логины и пароли
import password

# инит бота
logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=password.TOKEN)
dp = Dispatcher()

# не очень хорошая глобальная переменная Влада. Нет комментариев как работает, что делает.
# А также в теории от неё можно избавится, но будет висеть как плохой пример
user_message_count = defaultdict(int)

# Шедулер Ильи Маслова
scheduler = AsyncIOScheduler()
scheduler.configure(timezone=utc)


# код Владислава
def load_events_from_json():
    try:
        with open('events.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return None


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
    events = load_events_from_json()
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


@dp.message()
async def count_messages(message: types.Message):
    # код Ярослава
    if any(bad_word in message.text.lower() for bad_word in bad_words):
        await bot.delete_message(message.chat.id, message.message_id)
        logging.info(f"Удалено сообщение: {message.text}")

        user_last_deleted_time[message.from_user.id] = datetime.now()

    if message.from_user.id in user_last_deleted_time:
        last_deleted_time = user_last_deleted_time[message.from_user.id]
        if datetime.now() - last_deleted_time <= timedelta(minutes=30):
            await bot.delete_message(message.chat.id, message.message_id)

    # код Влада

    user_id = message.from_user.id
    user_message_count[user_id] += 1
    await asyncio.sleep(0.1)


# Функция Ралима
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
    headers = {"X-Yandex-Weather-Key": password.ACCESS_KEY}
    response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query})

    if response.status_code == 200:
        weather_data = response.json()
        if 'data' in weather_data:
            temperature = weather_data['data']['weatherByPoint']['now']['temperature']
            await message.answer(f"Температура в Стерлитамаке: {temperature}°C")
        else:
            await message.answer("Ошибка: данные не получены.")
    else:
        await message.answer("Ошибка API: проверьте свой запрос.")


# Код Ярослава
# Тоже плохие переменные, но от словаря избавится трудно без потери производительности,
# а вот про нижнюю подумать можно
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


# илья маслов
async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


scheduled_hour = 7
scheduled_minute = 5
scheduler.add_job(wake_up_members, 'cron', hour=scheduled_hour, minute=scheduled_minute, id='wake_up_job')


@dp.message(Command('set_time'))
async def set_time(message: types.Message):
    global scheduled_hour, scheduled_minute

    time_data = message.text.split(' ')[1:]
    if len(time_data) != 2:
        await message.reply("Укажите время в формате: /set_time ЧЧ ММ")
        return

    try:
        hour, minute = int(time_data[0]), int(time_data[1])
        if 0 <= hour < 24 and 0 <= minute < 60:
            scheduled_hour = hour
            scheduled_minute = minute

            scheduler.remove_job('wake_up_job')
            scheduler.add_job(wake_up_members, 'cron', hour=scheduled_hour, minute=scheduled_minute, id='wake_up_job')

            await message.reply(f"Время было обновлено на: {scheduled_hour}:{scheduled_minute:02d}")
        else:
            await message.reply("Некорректное время. Часы должны быть от 0 до 23, минуты от 0 до 59.")
    except ValueError:
        await message.reply("Пожалуйста, используйте целые числа для часового и минутного значений.")


@dp.message(Command('chatid'))
async def chat_id(message: types.Message):
    await message.reply(f'ID чата: {message.chat.id}')


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
