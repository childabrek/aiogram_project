
# Telegram Bot. Содержание:
Для чего нужен: Телеграмм-боты обеспечивают взаимодействие в реальном времени пользователям, позволяя им получать информацию непосредственно через мессенджер. 
Основные функции: Боты могут выполнять повседневные задачи, такие как рассылка напоминаний, обработка запросов пользователей или выполнение действий на основе команд.
Легкость написания программы: Создание бота в Телеграме достаточно просто и не требует сложных знаний программирования, что делает их доступными для широкой аудитории.
# 1 функция
Бот заходит в журнал и выписывает расписание пар на сегодняшний день. Использование библиотеки selenium для авторизации и другими манипуляциями на сайте. Сложнее всего было разобраться с кодом сайта, особено нахождение нужных кнопок.
## Пример использования 1 функции:
Активация проходит через команду '/lessons', после чего наш бот выводит расписание пар на сегодняшний день.
# 2 функция Bobik:

# 3 функция Dzot:
Эта функция по команде вызывает бота и отправляет пользователю случайное фото с небольшой справкой о самолете на этом снимке.
## Пример использования 3 функции:
Ввести в чат команду: /samoletik бот отправит вам фото со справкой
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
# 6 функция branchSophie:

# 7 функция detached:

# 8 функция egor:

# 9 функция floyd_branch:
Функция присылает составленное предложение из несколько слов ранее отправленных в беседу.
## Пример использования 9 функции:
Бот автоматически присылает сообщение, составляя его из несколько слов из разных сообщений присланных пользователями. Бот отправляет сообщение обычно после присланного сообщения пользователя, он делает это рандомно.
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
Это простая функция, которая считает количество сообщений, которые сделал пользователь в чате с ботом за всё время. по сути user_message_count[user id] и count одинаковы, но выводит  count, так как в случае чего можно его спокойно менять, а вот основную нельзя!
