
from aiogram.types import FSInputFile
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
logging.basicConfig(level=logging.INFO)
TOKEN = '8122833408:AAFdg78LuB8AJFWUFaeU4pB8bMJB_uBM3Lo'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply('Hello world!' + message.from_user.username, parse_mode='pre-formatted fixed-width code block')


@dp.message()
async def echo(message: types.Message):
    a = FSInputFile("1.jpg")
    await message.answer_photo(a)


# илья маслов
scheduler = AsyncIOScheduler()

scheduled_hour = 7
scheduled_minute = 5

async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


scheduler.add_job(wake_up_members, 'cron', hour=scheduled_hour, minute=scheduled_minute, id='wake_up_job')

@dp.message(Command('set_time'))
async def set_time(message: types.Message):
    global scheduled_hour, scheduled_minute

    time_data = message.text.split(' ')[1:]
    if len(time_data) != 2:
        await message.reply("Укажите время в формате: /set_time ЧЧ ММ")
        return

    try:
        hour, minute = int(time_data[0]), int(time_data[1])
        if 0 <= hour < 24 and 0 <= minute < 60:
            scheduled_hour = hour
            scheduled_minute = minute

            scheduler.remove_job('wake_up_job')
            scheduler.add_job(wake_up_members, 'cron', hour=scheduled_hour, minute=scheduled_minute, id='wake_up_job')

            await message.reply(f"Время было обновлено на: {scheduled_hour}:{scheduled_minute:02d}")
        else:
            await message.reply("Некорректное время. Часы должны быть от 0 до 23, минуты от 0 до 59.")
    except ValueError:
        await message.reply("Пожалуйста, используйте целые числа для часового и минутного значений.")

@dp.message(Command('chatid'))
async def chat_id(message: types.Message):
    await message.reply(f'ID чата: {message.chat.id}')

async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())
