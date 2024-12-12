
# Telegram Bot. Содержание:
Для чего нужен: Телеграмм-боты обеспечивают взаимодействие в реальном времени пользователям, позволяя им получать информацию непосредственно через мессенджер. 
Основные функции: Боты могут выполнять повседневные задачи, такие как рассылка напоминаний, обработка запросов пользователей или выполнение действий на основе команд.
Легкость написания программы: Создание бота в Телеграме достаточно просто и не требует сложных знаний программирования, что делает их доступными для широкой аудитории.
## Функции бота:
### Ветка Arslan: /lessons
### Ветка Dzot: /samoletik
### Ветка Ilia-P: /HappyBirthday
### Ветка artem-karpenko: /photo + имя человека
### Ветка ilya-M: /settime + ЧЧ ММ
### Ветка jarvis-branch: /list
### Ветка ralim: /ralim, /pogoda
### Ветка test: /delete
### Ветка floyd_branch: /floydbranch_on, /floydbranch_off
### Ветка vlados: /count_vlad
### Ветка branchSophie: /startSophie
# 1 функция
Бот заходит в журнал и выписывает расписание пар на сегодняшний день. Использование библиотеки selenium для авторизации и другими манипуляциями на сайте. Сложнее всего было разобраться с кодом сайта, особено нахождение нужных кнопок.
## Пример использования 1 функции:
Активация проходит через команду '/lessons', после чего наш бот выводит расписание пар на сегодняшний день.
# 2 функция Bobik:

# 3 функция Dzot:
Эта функция по команде вызывает бота и отправляет пользователю случайное фото с небольшой справкой о самолете на этом снимке.
## Пример использования 3 функции:
Ввести в чат команду: /samoletik бот отправит вам фото со справкой
## Трудности при изготовлении:
Одним из главных факторов оказался один питоновый задрот в адрес кого еще говорят «Ноулайфер». Этот самый задрот на данный момент среди обучающихся понимает питон, если не лучше всех то на 5 уровней выше других студентов, однако это не помогает ему в общении. Стоит у него либо спросить, и тогда можно узнать много нового не только о питоне, но, в первую очередь, о себе и своих когнетивных способах дыхания, которые иногда могут сильно задеть.
# 4 функция Ilia-P:
Этот код представляет собой Telegram-бота, который автоматически отправляет поздравления с днем рождения и реагирует на команду /HappyBirthday. Следуйте этой инструкции для его настройки и использования.
Установите зависимости Для работы кода необходимо установить Python-библиотеки: pip install aiogram apscheduler
Подготовьте токен для бота Код использует модуль Password, в котором должен быть указан токен бота.
TOCEN = 'ваш_токен_бота'
## Пример использования 4 функции:
Укажите ID чата для отправки поздравлений Параметр CHAT_ID указывает, куда будут отправляться поздравления. Чтобы получить ID: Если бот будет поздравлять в группе или канале: Добавьте бота в группу/канал. Используйте инструмент, например, UserInfoBot, чтобы узнать ID. Обычно он начинается с -100.
Измените значение переменной CHAT_ID в коде:

CHAT_ID = '-1002312275639' # Замените на ваш ID

Настройте список дней рождения Список именинников хранится в словаре birthdays. Добавьте имена и даты в формате дд.мм:
birthdays = { 'Имя Фамилия': 'дд.мм', ... }

Пример: birthdays = { 'Иван Иванов': '01.01', 'Мария Петрова': '15.06', }

Проверьте время отправки поздравлений Код настроен на отправку поздравлений ежедневно в 10:00. Чтобы изменить время:
Найдите строку: scheduler.add_job(check_and_send_birthday, 'cron', hour=10, minute=00)
Измените параметры hour (часы) и minute (минуты) на желаемое время.
Как использовать бота
Запустите бота: Запустить бота можно по горячим клавишам Ctrl + Shift + F10
Отправка приветствия: В чате с ботом введите команду /HappyBirthday. Бот ответит вам приветственным сообщением.
Автоматическое поздравление: Бот ежедневно проверяет текущую дату и отправляет поздравления в определенное время всем, кто указан в списке birthdays.
Отладка и тестирование Если бот не работает как ожидается: Проверьте корректность токена (Password.TOCEN) и ID чата (CHAT_ID). Убедитесь, что даты в списке birthdays совпадают с форматом дд.мм. Проверьте логи: настройки логгера выводят отладочную информацию в консоль.
Завершение работы Для остановки бота нажмите Ctrl+C в терминале. Теперь ваш бот готов к использованию и отправке поздравлений!
# 5 функция artem-karpenko:
Задача этой функции выводить фото какого-либо студента.
## Пример использования 5 функции:
Пользователи должны ввести команду /photo + имя человека, для того чтобы вывести фото
# 6 функция branchSophie:
Представляю вашему вниманию - бот напоминание о дежурствах.
Этот бот был создан и предназначен для автоматического уведомления о том,кто сегодня дежурит. Список дежурных у нас находится в массиве duty,и мы используем планировщик задач apscheduler для отправки нашего сообщения о том - кто сегодня дежурит в определенное нами время,при этом пропуская выходные дни,отправляя сообщение только в рабочие будние дни.
Для того чтобы бот работал нужно обязательно установить - aiogram,apscheduler,pytz.
## Пример использования 6 функции:
Чтобы запустить нашего бота, мы используем команду /startSophie. После, бот начинает автоматическую отправку сообщения в заданное нами время в рабочие дни(с пн по пт).Current_day отвечает за текущую дату. Когда наш список дежурных подходит к концу, то благодаря counter наш список обновляется и начинается заново,продолжая выводить текущего дежурного в текущий день не переставая работать.
Приходилось столкнуться с проблемой того,что когда список заканчивался,перестовало выводиться сообщение о том кто сегодня дежурит.Поэтому пришлось создать counter - счетчик,который следит за тем, когда список дежурных лиц закончится,он снова обновится до нуля,продолжая функционировать дальше. Была проблема с тем,что в определнное время не выводилось сообщение о сегодняшнем дежурном.Поэтому, здесь решило проблему timezone из планировщика задач apscheduler,с помощью которой мы определяем временную зону и без проблем выводим сообщение в заданное нами время.
В будущем планируется добавить функционал,который будет пропускать не только выходные выводя сообщение о сегодняшнем дежурном в рабочие будние дни,но и пропускать каникулы,праздничные нерабочие дни.
Приятного вам пользования ботом!
# 7 функция detached:

# 8 функция egor:

# 9 функция floyd_branch:
Функция присылает составленное предложение из несколько слов ранее отправленных в беседу.
## Пример использования 9 функции:
Бот автоматически присылает сообщение, составляя его из несколько слов из разных сообщений присланных пользователями. Бот отправляет сообщение обычно после присланного сообщения пользователя, он делает это рандомно. Для того чтобы включить бота, нужно написать команду /floydbranch_on, дял того чтобы выключить /floydbranch_off.
# 10 функция ilya-M:
Этот проект представляет собой бот для Telegram, который функционирует как будильник. Он позволяет пользователям устанавливать время для напоминания, отправляя простые команды в чат с ботом. Когда приходит время будильника, бот отправляет сообщение в указанный чат.
## Пример использования 10 функции:
Пользователи могут установить время для будильника, отправляя команду /set_time в формате ЧЧ ММ.
# 11 функция jarvis-branch:
Функция будет давать на выбор либо студентов, либо преподавателей. При выборе выводится та категория, которую мы выбрали до этого.
## Пример использования 11 функции:
Необходимо прописать в чат с ботом команду "/list", после чего выходит клавиатура с двумя кнопками "Преподаватели" и "Студенты". После нажатия на кнопку "Студенты", бот присылает в чат список студентов.
# 12 функция ralim:
## Telegram Weather
Данный проект представляет собой бота для Telegram, который показывает погоду. 
Он позволяет быстро и удобно получать актуальные данные о погоде.
## Пример использования 
Пользователь может прописать команду /ralim для получения привественного сообщения, а также есть команда /pogoda, она выдаст вам +- точные данные о текущей погоде.
## Сложные моментики
Самое сложное было выбрать тему.
В основом были трудности с тем, как соединить код с погодой и код с ботом.
изначально пытался запарсить сам сайт с погодой, но нечего не вышло, после чего решил взять API с яндекс погоды и работать с ним в дальнейшем. В итоге с ним заработало.
карочеееее?!:"№?!:" страдал,плакал,арал,рвал,пинал, не понимал, но все-таки сделал :3
## Пример использования 12 функции:
Пользователь может прописать команду /ralim для получения привественного сообщения, а если пользователь пропишет команду /pogoda, то он получить +- точные данные о погоде на данный момент.
# 13 функция test:
Данная функция блокирует людей на 30 минут в чате, за сквернословие. Эта функция поможет создать более дружелюбную и безопасную атмосферу для всех участников.

# 14 функция vlados:
Представляю вам свою универсальную, гениальную, полностью доработанную, оценённую всему миру, но неоценённую ваней, боту в телеграмме с 2 УНИВЕРСАЛЬНЫМИ явлениями, которые спасут наше человечество от пандемии пандемии незнания истории и того, сколько они писали сообщений в чате за все время!

Типичные библиотеки, код которых не будет работать. Добавлены при создании самого кода, в добавлении библиотек мне помог инструмент "интеллект" и немного чат-джипити. Айограмма, Asyncio и т.д.

Эта функция загружает данные из файла event.json, в котором отображаются даты с 2024 года по 1901 год. Файл JSON делался с помощью чата, так как писать очень долго самому, нейросеть все делает за пару секунд. события load_events_from_json() = load_events_from_json()

Это простая функция, которая считает количество сообщений, которые сделал пользователь в чате за всё время. по сути user_message_count[идентификатор пользователя] и count совпадают, но я вывожу count, так как в случае чего я могу его спокойно поменять, а вот в принципе нельзя!

А вот дополнительная функция, которая показывает смешные и грустные события того года, которые написал пользователь. Вот это было сложно, зато научился пользоваться json-файлами. Например, пользователь написал 1941 год, и ему бот ответил: Смешное событие 1941 года: Бум на модные поздравительные открытки с абсурдными текстами.

Страшное событие 1941 года: Начало Второй мировой войны из-за вспышки в Перл-Харборе.
# 15 функция Faezbek:
