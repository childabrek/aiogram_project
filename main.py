import logging
import asyncio
from sched import scheduler
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Filter
from aiogram import F
from aiogram.types import Message, FSInputFile, inline_query_results_button, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
import yandex_weather_api

logging.basicConfig(level=logging.INFO)
TOKEN = '8122833408:AAFdg78LuB8AJFWUFaeU4pB8bMJB_uBM3Lo'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher()

# Привет это Никита

# keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[])
#
# keyboard.

class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text



class Form(StatesGroup):
    choice = State()

# Данила Дунаев
@dp.message(Command('list'))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Студенты")],
            [types.KeyboardButton(text="Преподаватели")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите категорию: Студенты или Преподаватели", reply_markup=keyboard)


@dp.message(lambda message: message.text in ["Студенты", "Преподаватели"])
async def process_choice(message: types.Message, state: State):
    students = [
        "Марат Бакаев", "Артур Биккузин", "Егор Брынза", "Роза Валеева", "Владислав Васильев",
        "Данила Дунаев", "Ралим Ибатуллин", "Артем Карпенко", "Илья Маслов", "Ярослав Палехов",
        "Илья Парфенов", "Кирилл Слепнев", "Софья Соколова", "Наиль Шириев", "Артем Ченцов",
        "Фаезбек Хамрабаев", "Арслан Хуснутдинов", "Хаял Эйвазов"
    ]

    teachers = [
        "Никита Владиславович", "Владимир Владимирович",
        "Виктория Александровна", "Венера Баязитовна",
        "Светлана Александровна", "Эльвира Ранифовна",
        "Гузель Ирмаковна", "Альберт Вагизович",
        "Евгения Евгеньевна"
    ]

    if message.text == "Студенты":
        await message.answer("Список студентов:\n" + "\n".join(students), reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Преподаватели":
        await message.answer("Список преподавателей:\n" + "\n".join(teachers), reply_markup=types.ReplyKeyboardRemove())

    @dp.message()
    async def unknown_message(message: types.Message):
        await message.answer("")

    await state.finish()


@dp.message(Command("start"))
async def start(message: types.Message):
    button = inline_query_results_button.InlineQueryResultsButton(text='test')
    await message.reply('Hello world!' + message.from_user.username, parse_mode='pre-formatted fixed-width code block')


@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    a = FSInputFile.read
    await message.answer(
        "Hello, ```world```\!",
        parse_mode=ParseMode.MARKDOWN_V2
    )

# Илья Маслов
async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


@dp.message(MyFilter("Хакнуть Илью"))
async def hack(message: Message):
    await message.answer(message.text.split()[1])

scheduler.add_job(wake_up_members, 'cron', hour=13, minute=39)


async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())
