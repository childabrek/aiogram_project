import random
from multiprocessing.managers import State
from aiogram.fsm.state import StatesGroup
import angar
from aiogram.types import FSInputFile
import logging
from aiogram import Dispatcher, Bot, types
import asyncio
from aiogram.filters import Command
from aiogram.dispatcher import FSMContext
import password


logging.basicConfig(level=logging.INFO)
bot = Bot(password.TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()

@dp.message(Command('samoletik'))
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.gallery[a])))
    await message.answer(angar.park[a])

@dp.message(Command=['add_samoletik'])
async def add_samoletik(message: types.Message):
    await message.answer("Для добавления текстового сообщения отправьте его. Для добавления фото отправьте фотографию!")

# Обработка текстовых сообщений
@dp.message(content_types=['text'])
async def handle_text(message: types.Message):
    angar.park.append(message.text)  # Сохраняем текст в список park
    await message.answer("Текст сохранён!")

# Обработка фотографий
@dp.message(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo = await bot.download_file_by_id(message.photo)  # Скачиваем фото
    file_path = os.path.join('gallery', f'{photo_file_id}.jpg')  # Указываем путь для сохранения
    with open(file_path, 'wb') as new_file:
        new_file.write(photo.getvalue())  # Сохраняем фото
    gallery.append(file_path)  # Добавляем путь к фото в список gallery
    await message.answer("Фото сохранено!")

async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())