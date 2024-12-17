import logging
import asyncio
from datetime import date, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
TOKEN = "7694855874:AAGptMKWQ1OsSN_sncjbtPKrPHZs-Byczio"

bot = Bot(token=TOKEN)
dp = Dispatcher()

duty = ["Хаял", "Влад", "Данила", "Кирилл", "Арслан", "Ярослав", "Артем Карпенко",
        "Наиль", "Илья Парфенов", "Роза", "Егор", "Ралим", "Соня", "Марат",
        "Илья Маслов", "Артем Ченцов", "Фаезбек", "Артур Биккузин"]

current_date = date.today()
counter = 0

scheduler = AsyncIOScheduler()
scheduler.configure(timezone='Asia/Yekaterinburg')


async def check_and_send_duty(message: types.Message):
    global counter
    today = date.today()

    if today.weekday() in [5, 6]:  # Если выходные
        return

    name = duty[counter]
    counter = (counter + 1) % len(duty)  # Сброс на 0 после последнего

    await message.answer(f'Сегодня дежурный: {name}')


@dp.message(Command("startSophie"))
async def start_command_handler(message: types.Message):
    await message.reply('Напоминание о дежурных включено')
    scheduler.add_job(check_and_send_duty, 'cron', hour=13, minute=00, args=[message])


async def start_db():
    scheduler.start()  # Запускаем планировщик
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_db())
