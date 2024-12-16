#----------------------TGbot------------------------------------->
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import asyncio
#---------------------Parser------------------------------------->
import requests
import json
from datetime import datetime
import time
#-----------Не забудьте добавить----------------------------->
from password import TOKEN_ROBOT, ALLOWED_USERNAME, FORBIDDEN_CHAT_ID, PASSWORD_DZ_FUNCTION, USERNAME_DZ_FUNCTION

bot = Bot(TOKEN_ROBOT)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
#Help
@dp.message(Command("adminhelp"))
async def admin(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            await message.answer("Добавить id заблокированного чата | админа\n"
                                 "/addDZid | /addDZadmin\n"
                                 "Убрать id заблокированного чата | админа\n"
                                 "/removeDZid | /removeDZadmin\n"
                                 "Вывести лист всех id | админов\n"
                                 "/listDZid | /listDZadmin")

#Изменение ID -------------------------------------------------------------------------------------->
@dp.message(Command("addDZid"))
async def addDZid(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            newid = message.text.replace("/addDZid", "").replace(" ", "")
            if newid:
                if newid not in FORBIDDEN_CHAT_ID:
                    FORBIDDEN_CHAT_ID.append(newid)
                    await message.answer(f"Вы добавили id {newid}")
                else:
                    await message.answer("Такой id уже есть в списке")
            else:
                await message.answer("Введите команду + id")


@dp.message(Command("removeDZid"))
async def removeDZid(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            deleteid = message.text.replace("/removeDZid", "").replace(" ", "")
            try:
                if deleteid:
                    if deleteid in FORBIDDEN_CHAT_ID:
                        FORBIDDEN_CHAT_ID.remove(deleteid)
                        await message.answer(f"Вы успешно удалили id {deleteid}")
                    else:
                        await message.answer(f"id {deleteid} не найден")
                else:
                    await message.answer("Введите команду + id")
            except Exception as errorbotdzid:
                await message.answer(f"Произошла ошибка:\n{errorbotdzid}")


@dp.message(Command("listDZid"))
async def listDZid(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            list_bucket_id = []
            for i in FORBIDDEN_CHAT_ID:
                list_bucket_id.append(i)
            await message.answer(str(' '.join(list_bucket_id).replace(" ",", ")))

#Изменение username ----------------------------------------------------------------------------------->
@dp.message(Command("addDZadmin"))
async def addDZadmin(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            newadmin = message.text.replace("/addDZadmin", "").replace(" ", "").replace("@", "")
            if newadmin:
                if newadmin not in ALLOWED_USERNAME:
                    ALLOWED_USERNAME.append(newadmin)
                    await message.answer(f"Вы добавили нового админа {newadmin}")
                else:
                    await message.answer("Такой админ уже есть в списке")
            else:
                await message.answer("Введите команду + username")


@dp.message(Command("removeDZadmin"))
async def removeDZadmin(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            deleteadmin = message.text.replace("/removeDZadmin", "").replace(" ", "").replace("@", "")
            try:
                if deleteadmin:
                    if deleteadmin in ALLOWED_USERNAME:
                        ALLOWED_USERNAME.remove(deleteadmin)
                        await message.answer(f"Вы успешно удалили username {deleteadmin}")
                    else:
                        await message.answer(f"Username {deleteadmin} не найден")
                else:
                    await message.answer("Введите команду + username")
            except Exception as errorbotdzid:
                await message.answer(f"Произошла ошибка:\n{errorbotdzid}")


@dp.message(Command("listDZadmin"))
async def listDZadmin(message: types.Message):
    if message.chat.id not in FORBIDDEN_CHAT_ID:
        if message.from_user.username in ALLOWED_USERNAME:
            list_bucket_admin = []
            for i in ALLOWED_USERNAME:
                list_bucket_admin.append(i)
            await message.answer(str(' '.join(list_bucket_admin).replace(" ",", ")))

#----------------------------My name is Parser--------------------------------->
def fetch_homework_data(statuses_dz_function=[1, 2, 3]):

    list_s_status_code = []
    url = "https://msapi.top-academy.ru/api/v2/auth/login"
    payload = json.dumps({
        "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "id_city": None,
        "password": PASSWORD_DZ_FUNCTION,
        "username": USERNAME_DZ_FUNCTION
    })
    headers = {
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
    user_response = requests.post(url, headers=headers, data=payload)
    user_data = user_response.json()
    token_dz_function = user_data.get('refresh_token', '')

    try:
        list_s_dz_function = []
        for status_dz_function in statuses_dz_function:
            for random_variable_dz_function in range(1, 4):

                url = f"https://msapi.top-academy.ru/api/v2/homework/operations/list?page={random_variable_dz_function}&status={status_dz_function}&type=0&group_id=12"

                payload = {}
                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'ru_RU, ru',
                    'authorization': f'Bearer {token_dz_function}',
                    'origin': 'https://journal.top-academy.ru',
                    'priority': 'u=1, i',
                    'referer': 'https://journal.top-academy.ru/',
                    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                if response.status_code != 200:
                    list_s_status_code.append(f"Ошибка при запросе данных: {response.status_code}")
                    return list_s_status_code
                    break
                data_dz_function = json.loads(response.text)

                for item in data_dz_function:
                    completion_time = item.get('completion_time', '')
                    if not completion_time:
                        continue

                    completion_date_dz_function = datetime.strptime(completion_time, "%Y-%m-%d").date()
                    today = datetime.today().date()

                    if completion_date_dz_function > today:
                        file_path_dz_function = item.get('file_path', '')
                        if file_path_dz_function:
                            list_s_dz_function.append(
                                f"{item.get('name_spec', '')}\n"
                                f"Комментарий: {item.get('comment', '')}\n"
                                f"Файл: {file_path_dz_function}\n"
                                f"Дата выдачи: {item.get('creation_time', '')}\n"
                                f"Дата конца: {completion_time}\n"
                            )
        return list_s_dz_function
    except Exception as error_dz_function:
        return (f"The DZ function caused an error: {error_dz_function}")


#Отправка ДЗ ----------------------------------------------------------------------------------------->
@dp.message(Command("DZ"))
async def send_welcome(message: types.Message):
    if message.chat.id in FORBIDDEN_CHAT_ID:
        delete_message_dz_function = await message.answer(
            "В общем чате данная функция не работает, напишите в личное сообщение боту команду /DZ\n"
            "@test_rpo1kurs_bot")
        time.sleep(600)
        await delete_message_dz_function.delete()
        await message.delete()
    else:
        delete_message_Dz_id = await message.answer("Загрузка данных...")
        for entry in fetch_homework_data():
            await message.answer(entry)
        await delete_message_Dz_id.delete()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
