from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import asyncio
from angar import gallery

logging.basicConfig(level=logging.INFO)
bot = Bot("") # <---- Токен
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    waiting_for_photo = State()

@dp.message(Command('add_samoletik'))
async def add(message: types.Message, state: FSMContext):
    await message.reply('Отправьте фото самолетика')
    await state.set_state(Form.waiting_for_photo)

@dp.message(lambda message: message.content_type == types.ContentType.PHOTO)
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

@dp.message(lambda message: message.content_type != types.ContentType.PHOTO)
async def no_photo_received(message: types.Message, state: FSMContext):
    if await state.get_state() == Form.waiting_for_photo:
        await message.reply('Пожалуйста, отправьте фото самолетика.')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())