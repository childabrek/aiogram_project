import logging
import asyncio
import time
import datetime
from aiogram.types import UNSET_PARSE_MODE
from datetime import date, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Filter
from aiogram.types import FSInputFile
from apscheduler.schedulers.blocking import BlockingScheduler
from pyexpat.errors import messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc


logging.basicConfig(level=logging.INFO)
TOKEN = "7694855874:AAGptMKWQ1OsSN_sncjbtPKrPHZs-Byczio"


bot = Bot(token=TOKEN)
dp = Dispatcher()

duty = ["Хаял", "Влад", "Данила", "Кирилл", "Арслан", "Ярослав", "Артем Карпенко", "Наиль", "Илья Парфенов", "Роза",
        "Егор", "Ралим", "Соня", "Марат", "Илья Маслов", "Артем Ченцов", "Фаезбек", "Артур Биккузин"]

current_date = date.today()
counter = 0


@dp.message(Command("startSophie")) #начальная команда
async def check_and_send_duty(message: types.Message): #наша функция
    global counter
    today = datetime.date.today()
    if today.weekday() in [5,6]: #если выходные то пропускаем
        pass
    else:
        if today.weekday() in [0,1,2,3,4]: #если рабочие дни
            if counter >= len(duty): #как список с дежурными заканчивается,сбрасываем его до нуля
                counter = 0
            name = duty[counter]
            counter = (counter + 1)  # счетчик дежурного
            await message.answer(f'Сегодня дежурный: {name}')


        scheduler = AsyncIOScheduler()
        scheduler.configure(timezone=utc)
        scheduler.add_job(check_and_send_duty, 'cron', hour=13, minute=00,args=[message])



async def start_db():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_db())
