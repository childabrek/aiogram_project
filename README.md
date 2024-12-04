Представляю вашему внимаю свою универсальную, гениальную, полностью доработанную, оценённую всем миром, но неоценённую ваней, бота в телеграмме с 2 
УНИВЕРСАЛЬНЫМИ функциями, которые спасут наше человечество от массовой пандемии незнания историй и того, сколько они написали сообщений в чате за все время!

Типичные библиотеки без которых не будет работать код. Добавлялись по мере создания самого кода, в добавлении библиотек мне помог инструмент " интеллект " и немного чат-джипити.
import logging
import password
import asyncio
import json
import aiogram
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from collections import defaultdict

Функция которая загружает данные из файла events.json, в котором находятся даты с 2024 года по 1901. JSON файл делался с помощью чат джипити, так как писать очень долго самому, а нейросеть все сделает за пару секунд.
def load_events_from_json():
    with open('events.json', 'r', encoding='utf-8') as file:
        return json.load(file)
   
events = load_events_from_json()

Здесь мы делаем фундамент для нашего бота, что бы он работал. С помощью файла password.py, я смог спрятать API TOKEN от чужих глаз. А так же здесь стоит переменная на будующие с использованием полезного словаря.
logging.basicConfig(level=logging.INFO)
import password
bot = aiogram.Bot(token=password.TOKEN)
dp = Dispatcher()
user_message_count = defaultdict(int)

Это простая функция, которая считает количество сообщений, которые сделал пользователь в чате с ботом за всё время. по сути user_message_count[user id] и count одинаковы, но я вывожу count, так как в случае чего я могу его спокойно менять, а вот основную нельзя!
@dp.message(Command("count_vlad"))
async def count(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1      ( переменная присвоенная к айди пользователю )
    username = message.from_user.full_name
    count = user_message_count[user_id]
    if username == "society":
        username = "Повелитель " + username               Если пишу команду я, бот обращается ко мне соответственно.
    else:
        username = "Ниндзя " + username                   Если не я, то всё
    await message.reply(f"{username}, ты отправил(а) {count} сообщений.")

И вот дополнительная функция, которая показывает смешные и грустные события того года, который написал пользователь. Вот это было сложно, зато научился пользоваться json файлами.
Например пользователь написал 1941 и ему бот ответил:
Смешное событие 1941 года: Бум на модные поздравительные открытки с абсурдными текстами.
 
Страшное событие 1941 года: Начало Второй мировой войны из-за нападения на Pearl Harbor.

Вот код:
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
        await message.reply('Это не смешно, такие "приколы" могут привести к уголовной ответственности.')         # Что бы не было приколистов с 1488! Нацизм это плохо.

@dp.message()
async def count_messages(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


























