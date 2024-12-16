import logging
import requests
import asyncio
import Password
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types


WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Password.API_TOKEN)
dp = Dispatcher()


@dp.message(Command('pogoda'))
async def send_weather(message: types.Message):
    city = "Sterlitamak"  # можно изменить ихменть город ( только на англ!)
    params = {
        'q': city,
        'appid': Password.WEATHER_API_KEY,
        'units': 'metric',
    }
    response = requests.get(WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        message_text = f"Погода в {city}:\nТемпература: {temperature}°C"
        await message.answer(message_text)
    else:
        await message.answer('Ошибка API: проверьте свой запрос.')


async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())
