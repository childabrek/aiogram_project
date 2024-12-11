import os
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
    waiting_for_photo = State()
    waiting_for_text = State()

@dp.message(Command('samoletik'))
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.gallery[a])))
    await message.answer(angar.park[a])


@dp.message(Command('add_samoletik'))
async def cmd_add_samoletik(message: types.Message):
    # Переводим пользователя в состояние ожидания текста
    await Form.waiting_for_text.set()
    await message.reply("Введите описание для самолётика:")


@dp.message(state=Form.waiting_for_text)
async def process_text(message: types.Message, state):
    await state.update_data(text=message.text)
    await Form.waiting_for_photo.set()
    await message.reply("Пожалуйста, отправьте изображение самолётика:")

    # Переводим пользователя в состояние ожидания изображения
    await Form.waiting_for_photo.set()
    await message.reply("Пожалуйста, отправьте изображение самолётика:")


@dp.message(state=Form.waiting_for_photo, content_types=['photo'])
async def process_image(message: types.Message, state):
    # Получаем данные из состояния
    user_data = await state.get_data()
    text = user_data.get('text')  # Извлекаем текст

    # Сохраняем текст в файл 'angar.py' в список park
    with open('angar.py', 'a') as f:
        f.write(f"park.append('{text}')\n")  # Добавляем текст в park

    # Получаем файл изображения
    photo = message.photo[-1]  # Получаем наибольшее качество изображения
    file_id = photo.file_id
    file = await bot.get_file(file_id)

    # Загружаем изображение и сохраняем его в папку 'bank'
    await bot.download_file(file.file_path, f'bank/{file.file_path.split("/")[-1]}')

    # Добавляем название изображения в список gallery в 'angar.py'
    with open('angar.py', 'a') as f:
        f.write(f"gallery.append('{file.file_path.split('/')[-1]}')\n")  # Добавляем имя изображения в gallery

    # Уведомляем пользователя об успешном добавлении
    await message.reply("Самолётик добавлен успешно!")

    # Завершаем состояние, чтобы бот мог принимать новые команды
    await state.finish()


@dp.message(state=Form.waiting_for_photo)
async def process_invalid_image(message: types.Message):
    # Если пользователь отправил что-то, кроме изображения, уведомляем его об этом
    await message.reply("Пожалуйста, отправьте изображение самолётика.")

async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())
