import requests
import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

import password
bot = Bot(token=password.Token)
dp = Dispatcher()

async def get_lessons():
    url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbXNhcGkuaXRzdGVwLm9yZyIsImlhdCI6MTczMzU0NDI5MywiYXVkIjoxLCJleHAiOjE3MzM1NjU4OTMsImFwaUFwcGxpY2F0aW9uSWQiOjEsImFwaVVzZXJUeXBlSWQiOjEsInVzZXJJZCI6MzIsImlkQ2l0eSI6NDkwfQ.bJa1eSG1fw9vBbYBf2ZqwNlLPFffUjg6b8N2n9zlzGU',
        'origin': 'https://journal.top-academy.ru',
        'priority': 'u=1, i',
        'referer': 'https://journal.top-academy.ru/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': '_csrf=wGv3YlO5Qpm-pFN4rZrGxc4UsapRA60a'
    }

    response = requests.get(url, headers=headers)
    lessons_data = response.json()

    lessons_full = []
    for lesson in lessons_data:
        lesson_content = lesson.get('subject_name', '')
        lessons_full.append(lesson_content)

    return '\n'.join(lessons_full)

@dp.message(Command('lessons'))
async def send_lessons(message: types.Message):
    ID = -1002312275639
    lessons = await get_lessons()
    title = 'Пары на сегодня:\n'
    await bot.send_message(ID, title + lessons)

async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())
