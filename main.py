from aiogram.filters import Command
import requests
from aiogram import Bot, Dispatcher, types
import asyncio
import random
from bs4 import BeautifulSoup

import password # Замените на токен вашего бота

# Инициализация бота и диспетчера
bot = Bot(token=password.TOKEN)
dp = Dispatcher()

# Функция для получения случайного анекдота с сайта anekdot.ru
def get_white_joke():
    response = requests.get("https://www.anekdot.ru/last/anekdot/")
    soup = BeautifulSoup(response.text, 'html.parser')
    jokes = soup.find_all('div', class_='text')
    if jokes:
        joke = random.choice(jokes).get_text(strip=True)
        return joke
    return "Не удалось найти анекдоты."

# Обработчик команды /white
@dp.message(Command("joke"))
async def send_white_joke(message: types.Message):
    joke = get_white_joke()
    await message.reply(joke)

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())