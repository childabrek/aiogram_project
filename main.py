import logging
import asyncio
import os

import aiogram.exceptions

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, KeyboardButton, ReplyKeyboardMarkup

from Config import HELP, TOKEN, MY_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
Songs = os.listdir('Songs/soad')


# Кнопки для бота
def butt():
    kb = [[KeyboardButton(text='/helpFaezbek'), KeyboardButton(text='/list_of_songs alph')],
          [KeyboardButton(text='/list_of_songs pop')],
          [KeyboardButton(text='/list_of_songs fav')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


# Функция, очищающая ненужные символы в треках
def cleaner():
    for file in os.listdir('Songs/soad'):
        q = file.replace('System_of_a_Down_-_', '')
        for letter1 in file:
            try:
                if letter1 == '(':
                    q = q.replace(' (musportal.org)', '')
                if letter1 == "_":
                    q = q.replace(letter1, ' ')
                    continue
                if type(int(letter1)) == int:
                    q = q.replace(letter1, '')
            except ValueError:
                pass
        if q.endswith('p'):
            q += '3'
        if q[len(q) - 5] == ' ':
            q = q[::-1].replace(" ", "", 1)[::-1]
        os.rename(f'Songs/soad/{file}', f'Songs/soad/{q}')


def alph():
    lis = []
    q = 0
    alph1 = ''
    for file in os.listdir('Songs/soad'):
        lis.append(file + '\n')
    with open('Songs/List of songs - alph', 'w') as a:
        for i in lis:
            while True:
                q += 1
                break
            i = i.replace('.mp3', '')
            a.writelines(f'{str(q)}. {i}')
            alph1 += f'{str(q)}. {i}'
    return alph1


def pop():
    with open('Songs/List of songs - pop', 'r') as a:
        lis = []
        q = 0
        pop1 = ''
        for name in a:
            lis.append(name)
        for i in lis:
            while True:
                q += 1
                break
            i = i.replace('.mp3', '')
            pop1 += i
    return pop1


def fav(message):
    q = 0
    user_id = message.from_user.id
    fav1 = ''
    for j in os.listdir(f'Songs/Fav/{user_id}'):
        while True:
            q += 1
            break
        j = j.replace('.mp3', '')
        fav1 += f'{q}. {j}\n'
    return fav1


@dp.message(Command('cleaner'))
async def clean(message):
    if message.from_user.id == MY_ID:
        cleaner()
        await message.answer('BOY\nNEXT DOOR')
    else:
        await message.answer('.')


# Добавить кнопки
@dp.message(Command('startFaezbek'))
async def button(message):
    await message.answer('Кнопки добавлены', reply_markup=butt())


# Добавить директорию для избранных песен
@dp.message(Command('create_fav_dir'))
async def create_fav(message):
    try:
        os.mkdir(f'Songs/Fav/{message.from_user.id}')
        await message.reply('Успешно')
    except FileExistsError:
        await message.reply('Вы уже создавали папку')


# Удалить директорию для избранных песен
@dp.message(Command('delete_fav_dir'))
async def delete_fav(message):
    try:
        os.removedirs(f'Songs/Fav/{message.from_user.id}')
        await message.reply('Успешно')
    except FileNotFoundError:
        await message.reply('Вы еще не создали папку (/create_fav_dir)')


# Добавить песню в избранные
@dp.message(Command('add_fav'))
async def add_to_favorite(message):
    try:
        flag = True
        user_id = message.from_user.id
        for q in os.listdir('Songs/Fav'):
            if str(user_id) == q:
                break
        else:
            flag = False
        if flag is True:
            messag = message.text.replace('/add_fav ', '') + '.mp3'
            for i in os.listdir('Songs/soad'):
                messag1 = messag.replace(' ', '')
                i1 = i.replace(' ', '')
                if messag1.lower() == i1.lower():
                    if len(os.listdir()) > 0:
                        for w in os.listdir(f'Songs/Fav/{user_id}'):
                            if i == w:
                                await message.reply('Песня уже находится в избранных')
                                break
                        else:
                            with open(f'Songs/Fav/{user_id}/{i}', 'a'):
                                pass
                            await message.reply('Успешно')
                            break
                    else:
                        with open(f'Songs/Fav/{user_id}/{i}', 'a'):
                            pass
                        await message.reply('Успешно')
                        break
                    break
            else:
                await message.reply('Песня не найдена')
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        await message.reply('Вы еще не создали папку (/create_fav_dir)')


# Удалить песню из избранных
@dp.message(Command('delete_fav'))
async def delete_favorite(message):
    try:
        w = 0
        messag = message.text.replace('/delete_fav ', '') + '.mp3'
        try:
            messag2 = messag.replace('.mp3', '')
            if type(int(messag2)) == int:
                for i in os.listdir(f'Songs/Fav/{message.from_user.id}'):
                    w += 1
                    if int(messag2) == w:
                        os.remove(f'Songs/Fav/{message.from_user.id}/{i}')
                        await message.reply('Успешно')
                        break
                else:
                    await message.reply('Песня не найдена')
        except ValueError:
            for i in os.listdir(f'Songs/Fav/{message.from_user.id}'):
                messag1 = messag.replace(' ', '')
                i1 = i.replace(' ', '')
                if messag1.lower() == i1.lower():
                    os.remove(f'Songs/Fav/{message.from_user.id}/{i}')
                    await message.reply('Успешно')
                    break
            else:
                await message.reply('Песня не найдена')
    except FileNotFoundError:
        await message.reply('Вы еще не создали папку (/create_fav_dir)')


# Функция для добавления аудиофайлов в папку
@dp.message(F.audio, Command('add'))
async def add_music(message: Message):
    if message.from_user.id == MY_ID:
        await message.answer('BOY')
        audio = message.audio
        file_id = audio.file_id
        file = await message.bot.get_file(file_id)
        path = rf"Songs/soad\{message.audio.file_name}"
        await message.bot.download_file(file.file_path, path)
        await message.answer('NEXT DOOR')
    else:
        await message.answer('Вам нельзя добавлять файлы')
    cleaner()


# Функция для удаления аудиофайлов из папки
@dp.message(Command('del'))
async def del_music(message: Message):
    mess = message.text.replace('/del ', '') + '.mp3'
    if message.from_user.id == MY_ID:
        for i in os.listdir('Songs/soad'):
            mess = mess.replace(' ', '')
            i1 = i.replace(' ', '')
            if mess.lower() == i1.lower():
                os.remove(f'Songs/soad/{i}')
                await message.reply('Успешно')
                break
        else:
            await message.reply('Файл не найден')
    else:
        await message.answer('Вам нельзя удалять файлы')


# Функция комманды help
@dp.message(Command('helpFaezbek'))
async def help1(message):
    await message.answer(HELP)


# Функция вывода списка песен
@dp.message(Command('list_of_songs'))
async def gachi(message):
    messag = message.text
    messag = messag.replace('/list_of_songs ', '')
    if messag == 'alph':
        await message.reply(alph())
    if messag == 'pop':
        await message.reply(pop())
    try:
        if messag == 'fav':
            await message.reply(fav(message))
    except FileNotFoundError:
        await message.answer('Вы еще не создали папку с любимыми песнями (/create_fav_dir)')
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer('Список пуст')


# Функция отправки песен
try:
    @dp.message(Command('send_music'))
    async def music(message):
        mess = message.text.replace('/send_music', '')
        list_cons = []
        f = True
        if mess == '':
            await message.answer('Введите название песни')
            f = False
        else:
            mess = mess + '.mp3'
        mess1 = mess.replace(' ', '')
        for name in os.listdir('Songs/soad'):
            name1 = name.replace(' ', '')
            if mess1.lower() == name1.lower():
                file = FSInputFile(f'Songs/soad/{name}')
                await message.answer_document(file)
                break
        else:
            if f is True:
                for i in os.listdir('Songs/soad'):
                    count_of_coincidence = 0
                    b = -1
                    try:
                        while True:
                            b += 1
                            w = mess1[b]
                            i1 = i[b]
                            if i1.lower() == w.lower():
                                count_of_coincidence += 1
                    except IndexError:
                        list_cons.append(count_of_coincidence)
                index1 = list_cons.index(max(list_cons))
                list_cons[index1] = 0
                index2 = list_cons.index(max(list_cons))
                list_cons[index2] = 0
                index3 = list_cons.index(max(list_cons))
                u = str(Songs[index1].replace('.mp3', ''))
                u1 = str(Songs[index2].replace('.mp3', ''))
                u2 = str(Songs[index3].replace('.mp3', ''))
                await message.answer(f'Возможно вы имели ввиду: {u}, {u1}, {u2}')
except TypeError:
    pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
