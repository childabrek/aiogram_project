from aiogram import F
from aiogram.types import Message, FSInputFile, inline_query_results_button, ReplyKeyboardMarkup, Update
from aiogram.filters import Command
from aiogram.enums import ParseMode
import yandex_weather_api

logging.basicConfig(level=logging.INFO)
TOKEN = '8122833408:AAFdg78LuB8AJFWUFaeU4pB8bMJB_uBM3Lo'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# floydmacflurry
messages_history = []
MAX_HISTORY_LENGTH = 100
@dp.message()
async def generate_combined_message(message: Message):
    global messages_history
    messages_history.append(message.text)
    if len(messages_history) > MAX_HISTORY_LENGTH:
        messages_history.pop(0)
    if len(messages_history) >= 5:
        selected_messages = random.sample(messages_history, 5)
        words = [word for msg in selected_messages for word in msg.split()]
        combined_message = ' '.join(words[:10])
        if random.randint(0, 1) == 1:
            await bot.send_message(chat_id=message.chat.id, text=combined_message)


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text


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
