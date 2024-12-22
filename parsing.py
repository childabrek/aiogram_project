import requests
from datetime import datetime
import json

import password

url = "https://msapi.top-academy.ru/api/v2/auth/login"

payload = json.dumps({
    "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
    "id_city": None,
    "password": password.pass_1,
    "username": password.user_1
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

base_url = "https://msapi.top-academy.ru/api/v2/homework/operations/list?page=1&type=0&group_id=12"

headers.update({'Authorization': f'Bearer {token_dz_function}'})

responses = {}
for status in range(1, 4):
    response_url = f"{base_url}&status={status}"
    response = requests.get(response_url, headers=headers)
    responses[f'response{status}'] = response


def process_response(response):
    s = []

    try:
        data = response.json()

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    s.append(item.get('name_spec', ''))
                    s.append(item.get('completion_time', ''))
                    s.append(item.get('theme', ''))
                else:
                    print("Ошибка: элемент не является словарем:", item)
        elif isinstance(data, dict):
            s.append(data.get('name_spec', ''))
            s.append(data.get('completion_time', ''))
            s.append(data.get('theme', ''))
        else:
            print("Ошибка: ожидался список или словарь, получен:", type(data))

    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON:", response.text)
    except Exception as e:
        print("Произошла ошибка:", e)

    todays = datetime.today().strftime('%Y-%m-%d')
    indices = [index for index, element in enumerate(s) if todays in element]

    result = []
    for index in indices:
        if index > 0:
            result.append(s[index - 1])
        if index < len(s) - 1:
            result.append(s[index + 1])

    combined_strings = []
    for i in range(0, len(result), 2):
        if i + 1 < len(result):
            combined_strings.append(result[i] + " - " + result[i + 1])
        else:
            combined_strings.append(result[i])

    return '\n'.join(combined_strings)


all_processed_outputs = []
for i in range(1, 4):
    processed_output = process_response(responses[f'response{i}'])
    if processed_output:
        all_processed_outputs.append(processed_output)

final_output = '\n'.join(all_processed_outputs)
print(final_output)
