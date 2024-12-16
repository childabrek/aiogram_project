import aiogram
import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import main

logging.basicConfig(level=logging.INFO)
TOKEN = '7252389655:AAEmtpYiwFYGALtHEZC9vpUhB0KJxV9euj0'
dp = Dispatcher()

bot = Bot(token=TOKEN)

#"БД"
d = ["Дунаев Данила Викторович: ЮЗ:@salhock, ID:931829917"]
i = ["Палехов Ярослав Дмитриевич: ЮЗ:, ID:"]
s = ["Соколова Софья Константиновна:ЮЗ:@soniaai, ID:1006350941"]
r = ["Ибатуллин Ралим Радикович: ЮЗ:@Mestoumenie, ID:5763738414"]
e = ["Брынза Егор Владимирович: ЮЗ:@Revenant_Rgo, ID:2032378519"]
m = ["Бакаев Марат Рашидович: ЮЗ:@dzoooot, ID:1883346287"]
n = ["Шириев Наиль Ильдусович: ЮЗ:@Nafanyadreamsss, ID:5243012628"]
u_p = ["Парфенов Илья Олегович: ЮЗ:@Pare39, ID:759288326"]
a = ["Хуснутдинов Арслан Радикович: ЮЗ:@Orda1982, ID:5898197309"]
ar_k = ["Карпенко Артем Дмитриевич: ЮЗ:@hyi0059, ID:7293642988"]
u_m = ["Маслов Илья Дмитриевич: ЮЗ:@deboshiirr, ID:994753060"]
v = ["Васильев Владислав Владимирович: ЮЗ:@aepaekwwwdge, ID:1895290863"]
ar_ch = ["Ченцов Артем Андреевич: ЮЗ:@inwille, ID:6060657119"]
f = ["Хамрабаев Фаезбек Хикматуллаевич: ЮЗ:@certdz0, ID:5651350400"]
h = ["Эйвазов Хаял Рафиг Оглы: ЮЗ:@H975YM102, ID:1008060956"]
ro = ["Валеева Роза Рамилевна: ЮЗ:@dakarejrf, ID:1975189721"]

@dp.message(Command('help'))
async def HELP(message: types.Message, my_cakkback=None):
    await message.answer("/PRIVATE(отправляет сообщение в ЛС)"
                         " /DOX(выводит данные пользователя по типу данным)"
                         " /NETWORKS(отправляет возможные ссылки на соц сети)")


@dp.message(Command('DOX'))
async def DOX(message: types.Message, my_cakkback=None):
    await message.answer("выберите данные пользователя(ФИО, ДР, ЮЗ, ID, ...")
    a = message.text
    if a == "Данила":
        await message.answer(d)



@dp.message(Command('PRIVATE'))
async def PRIVATE(message: types.Message, my_cakkback=None):
    pass

@dp.message(Command('NETWORKS'))
async def NETWORKS(message: types.Message, my_cakkback=None):
    await message.answer("введите данные пользователя")


async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())


