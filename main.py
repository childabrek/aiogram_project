import os
import json
import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
from password import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)            #----- ТОКЕН
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):            #----- Статусы
    waiting_for_name = State()
    waiting_for_text = State()
    waiting_for_photo = State()
    waiting_for_delete_name = State()

@dp.message(Command("help_samoletik"))            #----- Все доступные команды
async def help_samoletik(message: types.Message):
    await message.answer("/samoletik - Отправить рандомный самолетик\n"
                         "/help_samoletik - Отправить список всех команд\n"
                         "/list_samoletik - Вывести лист всех самолетиков\n"
                         "/delete_samoletik - Удалить самолетик по названию\n"
                         "/add_samoletik - Добавить самолетик")

@dp.message(Command('samoletik'))            #----- Рандомный самолетик
async def get_random_samoletik(message: types.Message):
    try:
        with open('angarinfo.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            if not json_data:
                await message.reply('Нет сохраненных самолетиков.')
                return
            random_data = random.choice(json_data)
            await message.answer_photo(FSInputFile(random_data['photo_path']))
            await message.answer(random_data['text'])
    except FileNotFoundError:
        await message.reply('Нет сохраненных самолетиков.')
    except Exception as e:
        await message.reply('Ошибка при получении случайного самолетика.')
        await message.answer(str(e))

@dp.message(Command('list_samoletik'))            #----- общий список доступных самолетиков
async def listsamoletik(message: types.Message):
    try:
        with open('angarinfo.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            if not json_data:
                await message.reply('Нет сохраненных самолетиков.')
                return
            names = [item['name'] for item in json_data]
            names_list = "\n".join(names)
            await message.answer(f'Сохраненные самолетики:\n{names_list}')
    except FileNotFoundError:
        await message.answer('Нет сохраненных самолетиков.')
    except Exception as e:
        await message.reply('Ошибка при получении списка самолетиков.')
        await message.answer(str(e))

@dp.message(Command('delete_samoletik'))            #----- удалить самолетик
async def delete_samoletik(message: types.Message):
    name_to_delete = message.text.replace('/delete_samoletik', '').strip()

    if not name_to_delete:
        await message.answer('Пожалуйста, укажите название самолетика после команды.')
        return

    try:
        if not os.path.exists('angarinfo.json'):
            await message.reply('Нет сохраненных самолетиков.')
            return

        with open('angarinfo.json', 'r+', encoding='utf-8') as f:
            json_data = json.load(f)

            if not json_data:
                await message.reply('Нет сохраненных самолетиков.')
                return

            item_to_delete = next((item for item in json_data if item['name'] == name_to_delete), None)

            if item_to_delete:
                photo_path = item_to_delete['photo_path']
                if os.path.exists(photo_path):
                    os.remove(photo_path)

                json_data.remove(item_to_delete)
                f.seek(0)
                json.dump(json_data, f, ensure_ascii=False, indent=4)
                f.truncate()

                await message.reply(f'Самолетик "{name_to_delete}" успешно удален.')
            else:
                await message.reply(f'Самолетик с названием "{name_to_delete}" не найден.')
    except Exception as e:
        await message.reply('Ошибка при удалении самолетика.')
        await message.answer(str(e))


@dp.message(Command('add_samoletik'))            #----- добавить самолетик
async def add(message: types.Message, state: FSMContext):
    await message.answer('Введите название самолетика')
    await state.set_state(Form.waiting_for_name)

@dp.message(lambda message: message.content_type == types.ContentType.TEXT)            #----- название нового самолетика
async def text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Form.waiting_for_name:
        name = message.text
        await state.update_data(name=name)
        await message.answer('Введите текст о самолетике')
        await state.set_state(Form.waiting_for_text)
    elif current_state == Form.waiting_for_text:            #----- текст нового самолетика
        text = message.text
        await state.update_data(text=text)
        await message.answer('Отправьте фото самолетика')
        await state.set_state(Form.waiting_for_photo)

@dp.message(lambda message: message.content_type == types.ContentType.PHOTO)            #----- фото нового самолетика
async def waiting_for_photo(message: types.Message, state: FSMContext):
    if await state.get_state() == Form.waiting_for_photo:
        try:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            data = await state.get_data()
            file_path = f"angar/{data['name']}.jpg"

            if not os.path.exists("angar"):
                os.makedirs("angar")

            await bot.download_file(file.file_path, file_path)
            data['photo_path'] = file_path

            if not os.path.exists('angarinfo.json'):
                with open('angarinfo.json', 'w', encoding='utf-8') as f:
                    json.dump([], f)

            with open('angarinfo.json', 'r+', encoding='utf-8') as f:
                json_data = json.load(f)
                json_data.append(data)
                f.seek(0)
                json.dump(json_data, f, ensure_ascii=False, indent=4)
                f.truncate()

            await message.reply('Фото сохранено!')
            await state.clear()
        except Exception as e:
            await message.reply('Ошибка при сохранении фото.')
            await message.answer(str(e))

@dp.message(lambda message: message.content_type != types.ContentType.PHOTO)            #----- если не фотка
async def no_photo_received(message: types.Message, state: FSMContext):
    if await state.get_state() == Form.waiting_for_photo:
        await message.reply('Пожалуйста, отправьте фото самолетика.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())