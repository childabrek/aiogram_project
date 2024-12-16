import random
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import asyncio
from aiogram.types import FSInputFile
import angar
from angar import gallery
from password import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)      ### ------- TOOOOOOOOOOOOOOOKEEEEEEEEEEEEEEEEN
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    waiting_for_photo = State()

@dp.message(Command('samoletik'))     ### ------- команда по которой вызывается рандомный самолетик
async def samoletik(message: types.Message):
    a = random.randint(0, len(angar.park))
    await message.answer_photo(FSInputFile('bank\\' + (angar.gallery[a])))
    await message.answer(angar.park[a])

@dp.message(Command('add_samoletik'))     ### ------- команда по которой переключается состояние и бот начинает ожидать фото самолетика
async def add(message: types.Message, state: FSMContext):
    await message.reply('Отправьте фото самолетика')
    await state.set_state(Form.waiting_for_photo)

@dp.message(lambda message: message.content_type == types.ContentType.PHOTO)     ### ------- бот получает фото и выключает состояние
async def waiting_for_photo(message: types.Message, state: FSMContext):
    if await state.get_state() == Form.waiting_for_photo:
        try:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_path = f"bank/{len(gallery)}.jpg"

            await bot.download_file(file.file_path, file_path)
            await message.reply('Фото сохранено!')
            await state.clear()
        except Exception as e:
            await message.reply('Ошибка при сохранении фото.')
            await message.answer(str(e))

@dp.message(lambda message: message.content_type != types.ContentType.PHOTO)     ### ------- если бот получил НЕ фотку
async def no_photo_received(message: types.Message, state: FSMContext):
    if await state.get_state() == Form.waiting_for_photo:
        await message.reply('Пожалуйста, отправьте фото самолетика.')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
