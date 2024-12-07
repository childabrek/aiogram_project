import asyncio
import logging
import password
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler



# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger


CHAT_ID = '-1002312275639'


bot = Bot(token=password.TOKEN)
dp = Dispatcher()

# Дни рождения
birthdays = {
    'Никиту Владиславовича': '07.02',
    'Регину Маратовну': '17.06',
    'Виктрорию Александровну': '09.03',
    'Владимира Владиславовича': '18.04',
    'Марата': '02.11',
    'Артура': '04.11',
    'Егора': '25.06',
    'Розу': '03.07',
    'Владислава': '30.05',
    'Данила': '24.08',
    'Ралима': '06.09',
    'Карпенко Артема': '03.04',
    'Маслова Илью': '16.08',
    'Ярослава': '22.01',
    'Парфёнова Илью': '08.12',
    'Кирилла': '13.02',
    'Софью': '25.08',
    'Фаезбека': '07.02',
    'Арслана': '16.04',
    'Ченцова Артема': '05.02',
    'Наиля': '08.12',
    'Хаяла': '18.09',
}


# Команда /start
@dp.message(Command('HappyBirthday'))
async def start(message: types.Message):
    await message.reply('Hello Friend!' + message.from_user.username)


# Планировщик задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_birthday, 'cron', hour=10, minute=00)
    scheduler.start()


# Проверка и отправка поздравлений
async def check_and_send_birthday():
    today = datetime.now().strftime('%d.%m')
    for name, date in birthdays.items():
        if date == today:
            message = f"🎉 Поздравляем {name} с Днем Рождения! 🥳🎂"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            logger(f"Поздравление отправлено: {name}")


# Запуск диспетчера
async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())