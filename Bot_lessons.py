import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

logging.basicConfig(level=logging.INFO)
a = '7879535551:AAHIBTSqKL_F63fHMhhy9--xW5hNuNTmUb4'

bot = Bot(token=a)
dp = Dispatcher()
# Привет это Арслан


@dp.message(Command('lessons'))
async def start(message: types.Message):
    driver = webdriver.Chrome()
    driver.get("https://journal.top-academy.ru/ru/main/schedule/page/index")

    time.sleep(2)

    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys('Husnu_ii62')

    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys('OrdA2020')

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()

    time.sleep(2)

    today = driver.find_element(By.XPATH, '//div[@class="active-day"]')
    today.click()

    time.sleep(2)

    ID = -1002312275639
    await bot.send_message(ID, 'Пары на сегодня:')
    lessons = driver.find_elements(By.CLASS_NAME, 'less-name')
    for lesson in lessons:
        lesson_content = lesson.get_attribute('innerHTML')
        await bot.send_message(ID, lesson_content)

    driver.quit()


async def start_dp():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_dp())