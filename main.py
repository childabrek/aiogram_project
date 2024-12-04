import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

TOKEN = '7539834728:AAGeuBtBetJd9aal7wwdTsoNokWTWukhnHU'
ACCESS_KEY = "f8a2ea6f-4d3e-472b-9de6-eb6de976e723"
URL = 'https://api.weather.yandex.ru/graphql/query'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("ralim"))
async def salam(message: types.Message):
    await message.answer("Привет! Напиши команду /pogoda, чтобы узнать погоду на сегодня.")

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
            condition = weather_data['data']['weatherByPoint']['now']['condition']
            await message.answer(f"Температура в Стерлитамаке: {temperature}°C")
        else:
            await message.answer("Ошибка: данные не получены.")
    else:
        await message.answer("Ошибка API: проверьте свой запрос.")

async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())