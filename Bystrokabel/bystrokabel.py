from logging import exception
import requests
from bs4 import BeautifulSoup
import csv


URL = "https://bystrokabel.ru/character/search?query="
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
cabel_name = input()
cabel_search = f'{URL}{cabel_name}'

# Получем колличество страниц (итераций)


def count_req(url):
    req = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')
    pre_count = soup.find_all('a', class_="non-selected-right")
    count = pre_count[-1].text
    return int(count)


# Цикл запросов по колличеству страниц (итераций)
for count in range(1, count_req(cabel_search) + 1):
    print(f'{cabel_search}&page={count}')
    req = requests.get(f'{cabel_search}&page={count}', headers=headers)

    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    # Собираем заголовки таблицы
    tabel_head = soup.find(
        'table', class_='result-table').find('thead').find('tr').find_all('th')
    name_cabel = tabel_head[0].text
    mass = tabel_head[3].text
    outside_diameter = tabel_head[4].text
    min_drum = tabel_head[5].text
    max_len_bay = tabel_head[6].text
    with open(f'Bystrokabel\data\Page{count}result.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name_cabel,
                mass,
                outside_diameter,
                min_drum,
                max_len_bay
            )
        )

    # собираем все теги tr в tbody
    cabels_data = soup.find(
        class_='result-table').find_all('tr', class_=False)

    for cabel in cabels_data:
        try:
            cabel_tds = cabel.find_all('td')
            title = cabel_tds[0].text
            mass = cabel_tds[3].text
            outside_diameter = cabel_tds[4].text
            min_drum = f'{cabel_tds[5].text}\n'
            max_len_bay = cabel_tds[6].text
            with open(f'Bystrokabel\data\Page{count}result.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        mass,
                        outside_diameter,
                        min_drum,
                        max_len_bay
                    )
                )
        except:
            next
