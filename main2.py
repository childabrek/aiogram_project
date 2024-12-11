import random
from multiprocessing.managers import State
from aiogram.fsm.state import StatesGroup
import angar
from aiogram.types import FSInputFile
import logging
from aiogram import Dispatcher, Bot, types
import asyncio
from aiogram.filters import Command
import password
from angar import gallery

logging.basicConfig(level=logging.INFO)
bot = Bot(password.TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_image = State()

@dp.message(Command('samoletik'))
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.gallery[a])))
    await message.answer(angar.park[a])

@dp.message(Command('add_samoletik'))
async def cmd_add_samoletik(message: types.Message):
    await message.reply("Пожалуйста, отправьте изображение самолётика:")

@dp.message(lambda message: message.photo is not None)
async def process_image(message: types.Message):
    name = len(angar.park)
    # Обработка полученного изображения
    file_id = message.photo[-1].file_id  # Получаем ID изображения самого высокого разрешения
    file = await bot.get_file(file_id)  # Получаем информацию о файле по его ID

    file_path = file.file_path  # Получаем путь к файлу на сервере
    downloaded_file = await bot.download_file(file_path)  # Загружаем файл

    # Формируем имя файла для сохранения
    file_name = f"{'bank'}/{name}.jpg"  # Уникальное имя файла: ID пользователя + ID изображения

    # Сохраняем загруженный файл в папку bank
    with open(file_name, 'wb') as new_file:  # Открываем файл для записи в бинарном режиме
        new_file.write(downloaded_file.getvalue())  # Записываем содержимое загруженного файла

    image_title = f"{name}.jpg"  # Формируем название изображения
    angar.gallery.append(image_title)
    with open('angar.py', 'w') as f:
        f.write('gallery = ' + repr(angar.gallery))

    # Отправляем ответ пользователю о том, что изображение успешно добавлено
    await message.reply("Самолётик добавлен! Спасибо за изображение.")

@dp.message(lambda message: message.text is not None)
async def process_text(message: types.Message):
    await message.reply("Пожалуйста, отправьте изображение самолётика, а не текст.")



async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())
