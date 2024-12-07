import requests
import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
import json

logging.basicConfig(level=logging.INFO)

import password
bot = Bot(token=password.Token)
dp = Dispatcher()


async def get_lessons():
    users_url = "https://msapi.top-academy.ru/api/v2/auth/login"
    payload = json.dumps({
        "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "id_city": None,
        "password": "OrdA2020",
        "username": "Husnu_ii62"
    })
    users_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': 'Bearer null',
        'content-type': 'application/json',
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
        'Cookie': '_csrf=PHrhu1IbcCqAafKD6FydbdEiDt93l5vT'
    }
    user_response = requests.post(users_url, headers=users_headers, data=payload)
    user_data = user_response.json()
    user_token = user_data.get('access_token', '')

    url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': 'Bearer ' + user_token,
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
