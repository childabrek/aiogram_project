import json
import logging
import os
import random
from datetime import datetime, timedelta

import password
import asyncio
import json
import aiogram
import requests
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, inline_query_results_button, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from collections import defaultdict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
# Тут все токены логины и пароли
import password

# инит бота
logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=password.TOKEN)
dp = Dispatcher()

# не очень хорошая глобальная переменная Влада. Нет комментариев как работает, что делает.
# А также в теории от неё можно избавится, но будет висеть как плохой пример
user_message_count = defaultdict(int)

# Шедулер Ильи Маслова
scheduler = AsyncIOScheduler()
scheduler.configure(timezone=utc)


# код Владислава
def load_events_from_json():
    try:
        with open('events.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return None


@dp.message(Command("count_vlad"))
async def count(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    username = message.from_user.full_name
    count = user_message_count[user_id]
    if username == "society":
        username = "Повелитель " + username
    else:
        username = "Ниндзя " + username
    await message.reply(f"{username}, ты отправил(а) {count} сообщений.")


# Функция Ралима
@dp.message(Command("pogoda"))
async def get_weather(message: types.Message):
    query = """{
        weatherByPoint(request: { lat: 53.6246, lon: 55.9501 }) {
            now {
                temperature
                condition
            }
        }
    }"""
    headers = {"X-Yandex-Weather-Key": password.ACCESS_KEY}
    response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query})

    if response.status_code == 200:
        weather_data = response.json()
        if 'data' in weather_data:
            temperature = weather_data['data']['weatherByPoint']['now']['temperature']
            await message.answer(f"Температура в Стерлитамаке: {temperature}°C")
        else:
            await message.answer("Ошибка: данные не получены.")
    else:
        await message.answer("Ошибка API: проверьте свой запрос.")


# Код Ярослава
# Тоже плохие переменные, но от словаря избавится трудно без потери производительности,
# а вот про нижнюю подумать можно
with open('words.json', 'r', encoding='utf-8') as f:
    bad_words_data = json.load(f)
    bad_words = [item['word'] for item in bad_words_data]

user_last_deleted_time = {}


@dp.message(Command('delete'))
async def delete_message(msg: types.Message):
    if msg.reply_to_message:
        message_id_to_delete = msg.reply_to_message.message_id
        chat_id = msg.chat.id

        await bot.delete_message(chat_id, message_id_to_delete)
        await msg.answer("Сообщение удалено.")
        user_last_deleted_time[msg.from_user.id] = datetime.now()
    else:
        await msg.answer("Пожалуйста, ответьте на сообщение, которое хотите удалить.")


# илья маслов
async def wake_up_members():
    await bot.send_message(chat_id='-1002312275639', text="Время вставать!")


scheduled_hour = 7
scheduled_minute = 5
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


# Код Артёма Ч
# floydmacflurry
floydbranch_enabled = True
messages_history = []
MAX_HISTORY_LENGTH = 100


@dp.message(Command("floydbranch_on"))
async def enable_function(message: types.Message):
    global floydbranch_enabled
    floydbranch_enabled = True
    await message.reply("Функция включена.")


@dp.message(Command("floydbranch_off"))
async def disable_function(message: types.Message):
    global floydbranch_enabled
    floydbranch_enabled = False
    await message.reply("Функция отключена.")


# Арслан
async def get_lessons():
    users_url = "https://msapi.top-academy.ru/api/v2/auth/login"
    payload = json.dumps({
        "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "id_city": None,
        "password": password.PASSWORD,
        "username": password.LOGIN
    })
    users_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': 'Bearer null',
        'content-type': 'application/json',
        'origin': 'https://journal.top-academy.ru',
        'priority': 'u=1, i',
        'referer': 'https://journal.top-academy.ru/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': '_csrf=PHrhu1IbcCqAafKD6FydbdEiDt93l5vT'
    }
    user_response = requests.post(users_url, headers=users_headers, data=payload)
    user_data = user_response.json()
    user_token = user_data.get('access_token', '')

    url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru_RU, ru',
        'authorization': 'Bearer ' + user_token,
        'origin': 'https://journal.top-academy.ru',
        'priority': 'u=1, i',
        'referer': 'https://journal.top-academy.ru/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': '_csrf=wGv3YlO5Qpm-pFN4rZrGxc4UsapRA60a'
    }

    response = requests.get(url, headers=headers)
    lessons_data = response.json()

    lessons_full = []
    for lesson in lessons_data:
        lesson_content = lesson.get('subject_name', '')
        lessons_full.append(lesson_content)

    return '\n'.join(lessons_full)


@dp.message(Command('lessons'))
async def send_lessons(message: types.Message):
    ID = -1002249502986
    lessons = await get_lessons()
    title = 'Пары на сегодня:\n'
    await bot.send_message(ID, title + lessons)


# Илья Парфёнов
# Дни рождения
birthdays = {
    'Никиту Владиславовича': '07.02',
    'Регину Маратовну': '17.06',
    'Виктрорию Александровну': '09.03',
    'Владимира Владиславовича': '18.04',
    'Марата': '02.11',
    'Артура': '04.11',
    'Егора': '25.06',
    'Розу': '03.07',
    'Владислава': '30.05',
    'Данила': '24.08',
    'Ралима': '06.09',
    'Карпенко Артема': '03.04',
    'Маслова Илью': '16.08',
    'Ярослава': '22.01',
    'Парфёнова Илью': '08.12',
    'Кирилла': '13.02',
    'Софью': '25.08',
    'Фаезбека': '07.02',
    'Арслана': '16.04',
    'Ченцова Артема': '05.02',
    'Наиля': '08.12',
    'Хаяла': '18.09',
}


# Команда /start
@dp.message(Command('HappyBirthday'))
async def start(message: types.Message):
    await message.reply('Hello Friend!' + message.from_user.username)


# Проверка и отправка поздравлений
async def check_and_send_birthday():
    today = datetime.now().strftime('%d.%m')
    for name, date in birthdays.items():
        if date == today:
            message = f"🎉 Поздравляем {name} с Днем Рождения! 🥳🎂"
            await bot.send_message(chat_id='-1002312275639', text=message)


scheduler.add_job(check_and_send_birthday, 'cron', hour=10, minute=00)


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
async def process_choice(message: types.Message):
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


# Взято из ветки Марата
@dp.message(Command('samoletik'))
async def photo(message: types.Message):
    a = random.choice(os.listdir('bank'))
    print(a)
    if 'a10' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Fairchild Republic A-10 Thunderbolt II Реактивный штурмовик\n\nРазработанный специально для выполнения '
            'задач непосредственной авиационной поддержки (CAS), этот самолет предназначен для поражения наземных целей'
            ' и обеспечения защиты наземных войск. A-10 стал символом мощной поддержки на поле боя благодаря своей'
            ' исключительной живучести, вооруженности и системам наблюдения за полем боя. Сам самолет по сути построен'
            ' вокруг 30-мм авиационной пушки GAU-8 Avenger, разработанной для поражения как пехоты и легкой техники'
            ' так и для уничтожения ОБТ (Основных Боевых Танков) противника. Также вооружался как свободнопадающими так'
            ' и корректируемыми бомбами с лазерной, ТВ, тепловой'
            ' и GPS системами наведения. Ракетами Воздух-Поверхность'
            ' AGM-65 Maverick и ракетами Воздух-Воздух AIM-9 Sidewinder')
    if 'f14' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Grumman F14 Tomcat - палубный истребитель перехватчик\n\nРазработанй в начале 70-х включал в себя все'
            ' достижения авиации того времени и считается первым самолетом 4-о поколения. Он был создан для перехвата'
            ' советских стратегических и тактических бомбардировщиков, однако был способен вести ближний воздушный бой'
            ' против других истребителей. Имел на борту мощный радар с системой TWS (Track While Scan) и был способен'
            ' одновременно сопровождать до 24 целей на расстоянии в 160км. Для перехвата тяжелых бомбардировщиков или'
            ' противокорабельных ракет, специально для программы по его созданию были разработаны ракеты AIM-54'
            ' Phoenix имевших максимальную дальность запуска в 150км. Также истребитель снабжался стандартными'
            ' ракетами AIM-7 Sparrow и AIM-9 Sidewinder')
    if 'e3' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Boeing E-3 Sentry — самолет раннего предупреждения и управления (AWACS)\n\n E-3 Sentry стал основным '
            'элементом системы воздушного командования и контроля ВВС США и других стран НАТО. Оснащенный большим '
            'радаром наклонной антенной, установленным на верхней части фюзеляжа, этот самолет способен обнаруживать'
            ' и отслеживать воздушные цели на дальних расстояниях, обеспечивая таким образом ситуационную '
            'осведомленность для командования. E-3 Sentry активно использовался в различных конфликтах, включая '
            'операции в Персидском заливе, Балканах и Ираке, демонстрируя свою способность предоставлять критически'
            ' важную информацию в реальном времени. Его возможности обеспечивают координацию действий различных типов '
            'авиации и наземных сил, а также способствуют эффективному управлению воздушным пространством.')
    if 'f4' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'McDonnell Douglas F-4 Phantom II — реактивный истребитель-бомбардировщик\n\nИстребитель стал одним из '
            'самых известных многоцелевых военных самолетов своего времени. Введенный в эксплуатацию в 1961 году, F-4'
            ' Phantom II был самый продвинутый боевой самолет в плане электроники и бортовых систем, с двумя'
            ' мощнейшими двигателями на борту он мог развивать скорость свыше 1.6 Маха (~2100км/ч). Также это позволяло'
            ' ему нести на себе большое количество вооружения как ракеты В-В и В-П, а также бомбы, включая управляемые'
            ' и неуправляемые типы. Истребитель активно использовался в войне во Вьетнаме, где продемонстрировал в'
            'ысокую эффективность и не в последнюю очередь в качестве истребителя ПВО применяя первые модели '
            'корректируемых бомб.')
    if 'f15' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'McDonnell Douglas F-15 Eagle — истребитель завоевания господства в воздухе\n\nСтал одним из самых '
            'известных и эффективных истребителей в истории военно-воздушных сил. Созданный как ответ на советский '
            'МиГ-25 ошибочно принятый за многоцелевой истребитель завоевания господства в воздухе, он превосходил '
            'в воздушном бою любой самолет противника. Самолет был спроектирован для достижения превосходства в '
            'воздухе и способен выполнять задачи как в воздушном бою, так и в роли перехватчика. В зависимости от '
            'модификации он может нести разнообразное вооружение, включая управляемые ракеты класса (Воздух-Воздух)'
            ' и бомбы. F-15 стал известен благодаря своим успешным боям и рекордному соотношению побед в воздушных '
            'боях. Истребитель активно использовался в ряде конфликтов, включая операции в Персидском заливе и военные'
            ' действия в Ираке. Запас для модернизации F-15 был настолько велик что его модификации до сих пор стоят'
            ' на вооружении.')
    if 'f16' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'General Dynamics F-16 Fighting Falcon — многоцелевой истребитель\n\nРазработанный в 1970-х годах и ставший'
            ' самым распространенным истребителем в мире. Самолет был спроектирован для ведения ближнего воздушного '
            'боя, но с модификациями получил возможность нести дальнобойное вооружение класса (Воздух-Воздух),'
            ' управляемое вооружение (Воздух-Поверхность), улучшенный радар и улучшенную авионику. F-16 активно и'
            'спользовался в различных конфликтах, таких как войны в Персидском заливе, Боснии и Косово, а также в оп'
            'ерациях на Ближнем Востоке. Его высокая маневренность и возможность ведения боя на больших и малых высота'
            'х сделали его надежным самолетом в руках летчиков. В течение своей службы F-16 прошел множество модификац'
            'ий и обновлений для поддержания актуальности на современном поле боя. F-16 продолжает находиться на в'
            'ооружении более чем 25 стран,')
    if 'f22' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Lockheed Martin F-22 Raptor — стелс-истребитель завоевания господства в воздухе пятого поколения\n\n'
            'Разработанный как ультимативное средство против воздушных сил противника для достижения воздушного пр'
            'евосходства, но также способен выполнять задачи ударной авиации и разведки. F-22 стал первым малозаме'
            'тным истребителем в мире и первым самолетом 5-го поколения. Благодаря развитию Электронно-вычислительн'
            'ых систем конструкторам удалось добиться сильного снижения ЭПР без ухудшения аэродинамики. Т.к. исполь'
            'зование внешних подвесов с вооружением противоречит технологии малозаметности, вооружение размещается '
            'во внутренних отсеках створки которых открываются в момент пуска ракеты или сброса бомбы. Истребитель о'
            'снащен полным комплектом систем предупреждения о пуске и облучении, общей системой связи и передачи дан'
            'ных Link-16 по которой самолету могут передаваться данные о противниках, о местоположении союзников, а т'
            'акже навигационные данные. F-22 имеет свой радар с АФАР (Активной Фазированной Антенной Решеткой) на бо'
            'рту, но в обычных условиях он почти не используется')
    if 'f35' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Lockheed Martin F-35 Lightning II — многоцелевой стелс-истребитель пятого поколения\n\nРазработанный по'
            ' программе JSF (Joint Strike Fighter) он предназначался для всех родов войск использующих авиацию: ВВС('
            'Военно Воздушные Силы), ВМС(Военно Морские силы), КМП(Корпус Морской Пехоты). F-35 включает три основны'
            'е версии: F-35A - для ВВС(обычный взлет и посадка), F-35B - для КМП и для ВМС(сокращенный взлет и верти'
            'кальная посадка). Основным преимуществом F-35 является его малозаметная конструкция которая позволяет с'
            'низить заметность для радаров. Это, наряду с системами сенсоров, камер с ТВ и ИК каналами, обеспечивает'
            ' высокую ситуацию осведомленность. F-35 способен выполнять множество задач, включая воздушные бои, удар'
            'ы по наземным целям, электронную войну и разведку. Он может нести широкий спектр вооружения, включая уп'
            'равляемые ракеты и бомбы, что делает его универсальным решением для современных военных операций. На да'
            'нный момент является самым актуальным истребителем ВВС')
    if 'f111' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'General Dynamics F-111 Aardvark — тактический бомбардировщик и многоцелевой истребитель\n\nF-111 стал п'
            'ервым военным самолетом, который использовал изменяемую геометрию крыла, что позволяло ему эффективно в'
            'ыполнять разнообразные задачи, включая ударные операции, перехват и разведку. Основной задачей F-111 бы'
            'ла тактическая поддержка и нанесение ударов по наземным целям, особенно в условиях противодействия прот'
            'ивовоздушной обороны врага. Он мог выполнять операции через любую погоду благодаря своим современным си'
            'стемам навигации и целеуказания. Самолет также был способен нести широкий диапазон вооружения, включая '
            'ядерные и конвенциональные бомбы, а также управляемые ракеты. F-111 активно использовался во многих кон'
            'фликтах, включая Вьетнамскую войну, где он продемонстрировал свои способности в ночных и низковысотных '
            'налетах. Самолет также принимал участие в операции "Буря в пустыне" в 1991 году, где выполнял успешные у'
            'дары по тактическим целям. На моменте разработки и испытаний рассматривался на роль палубного перехватчи'
            'ка, но был заменен новым F-14 Tomcat')
    if 'sr71' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Lockheed SR-71 Blackbird — стратегический разведывательный самолет\n\nСамолет разработан компанией Lock'
            'heed под руководством конструктора Кейли Джонсона в рамках программы A-12, полученной от Центрального '
            'разведывательного управления (ЦРУ). Одной из главных особенностей SR-71 была его способность летать на'
            ' очень больших высотах (до 25 000 метров) и с огромной скоростью (более 3 Махов), что делало его прак'
            'тически недосягаемым для большинства современных истребителей и ракет в то время. Специальные технолог'
            'ии, такие как стелс-дизайн и использование композитных материалов, позволяли снизить его радарную заме'
            'тность. SR-71 использовался для выполнения разведывательных миссий, включая фотосъемку, электронную ра'
            'зведку и сбор данных о размещении противника. Он значительно превышал скорость и высоту полета своих пр'
            'едшественников, что позволяло завершать задачи быстро и эффективно. Самолет собирал тактическую информа'
            'цию в реальном времени и играл важную роль в Холодной войне, обеспечивая стратегическое преимущество '
            'для США.')
    if 'cesna172' in a:
        await message.answer_photo(FSInputFile('bank\\' + a))
        await message.answer(
            'Cessna 172 Skyhawk — легкий одномоторный самолет\n\nРазработанный компанией Cessna Aircraft Company, Ce'
            'ssna 172 впервые поднялся в воздух в 1955 году и с тех пор стал классическим выбором для обучения пилот'
            'ов, частных владельцев и малых авиаперевозчиков. Основные характеристики Cessna 172 включают просторны'
            'й и комфортный кокпит, высоко расположенные крылья и стабильные летные характеристики. Самолет вмещает '
            'до четырех человек, включая пилота, и имеет максимальную взлетную массу около 1,150 кг. Cessna 172 обы'
            'чно оснащен поршневым двигателем с мощностью около 160-180 л.с., что позволяет ему развивать скорость '
            'до 226 км/ч и выполнять полеты на высоте до 4,000 метров. Cessna 172 известен своей надежностью и прос'
            'тотой в обслуживании, что делает его идеальным для учебных полетов и для владельцев, которые хотят пол'
            'учить опыт в пилотировании.\nА еще один преподаватель по питону в этом чате очень хочет такой')


@dp.message()
async def count_messages(message: types.Message):
    # код Ярослава
    if any(bad_word in message.text.lower() for bad_word in bad_words):
        await bot.delete_message(message.chat.id, message.message_id)
        logging.info(f"Удалено сообщение: {message.text}")

        user_last_deleted_time[message.from_user.id] = datetime.now()

    if message.from_user.id in user_last_deleted_time:
        last_deleted_time = user_last_deleted_time[message.from_user.id]
        if datetime.now() - last_deleted_time <= timedelta(minutes=30):
            await bot.delete_message(message.chat.id, message.message_id)

    # Код Артёма Ч
    global messages_history

    if floydbranch_enabled:
        messages_history.append(message.text)
        if len(messages_history) > MAX_HISTORY_LENGTH:
            messages_history.pop(0)
        if len(messages_history) >= 5:
            selected_messages = random.sample(messages_history, 5)
            words = [word for msg in selected_messages for word in msg.split()]
            combined_message = ' '.join(words[:10])
            if random.randint(0, 1) == 1:
                await bot.send_message(chat_id=message.chat.id, text=combined_message)

    # код Влада

    events = load_events_from_json()
    year = message.text.strip()
    user_id = message.from_user.id
    user_message_count[user_id] += 1
    if year in events:
        funny_event = events[year]['funny']
        scary_event = events[year]['scary']
        response = f"Смешное событие {year} года: {funny_event}\n \nСтрашное событие {year} года: {scary_event}"
        await message.reply(response)
    elif year == "1488":
        await message.reply('Это не смешно, такие "приколы" могут привести к уголовной ответственности.')

    user_id = message.from_user.id
    user_message_count[user_id] += 1


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
