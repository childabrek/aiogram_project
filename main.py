import requests
from bs4 import BeautifulSoup



url = 'https://journal.top-academy.ru/en/main/schedule/page/index'
response = requests.get(url)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'html.parser')
TEXT = soup.findAll('div', class_='time-content__item')
print(TEXT)