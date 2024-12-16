import logging
import password
import asyncio
import json
import aiogram
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from collections import defaultdict
# готово
def load_events_from_json():
    with open('events.json', 'r', encoding='utf-8') as file:
        return json.load(file)

events = load_events_from_json()

logging.basicConfig(level=logging.INFO)



bot = aiogram.Bot(password.TOKEN)
dp = Dispatcher()
user_message_count = defaultdict(int)

peoples = list()
ludi = set()
@dp.message(Command("count_vlad"))
async def count(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    username = message.from_user.full_name
    ludi.add(username[0])
    count = user_message_count[user_id]
    dad = str(username) + " отправил " + str(count) + " сообщений"
    if username == "society" or username == "Никита":
        username = "Повелитель " + username
    else:
        username = "Ниндзя " + username
    peoples.append(dad)
    print(*peoples)
    with open("ludi.json", "a", encoding="utf-8") as a:
        a.write(username + " " + str(count))

    await message.reply(f"{username}, ты отправил(а) {count} сообщений.")

@dp.message(Command("vlad"))
async def tab(message: types.Message):
    await message.reply(f"{peoples}")


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
        await message.reply('В тюрьму хочешь?')
        await message.delete()








@dp.message()
async def count_messages(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())