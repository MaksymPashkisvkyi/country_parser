# Готовый результат :  предоставить  ссылку на GitHub репозиторий
#
# 1.	Используя библиотеку bs4 спарсите список стран со страницы
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81
# %D1%82%D0%B2.
#
# 2.	Подсчитайте количество стран начинающихся на туже букву. Подсчитайте количество слов в полном названии страны.
# Получите url флага.
#
# 3.	Запишите в виде list of dicts:
#
# ПРИМЕР :
#
# [{"country": "Австралия", "full_country_name": "Австралийский Союз", "same_letter_count": 11, "flag_url":
# "upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Flag_of_Australia.svg/50px-Flag_of_Australia.svg.png"},]
#
# 4..  Создайте функцию, которая будет выводить словарь с данными конкретной страны по её короткому имени.

from bs4 import BeautifulSoup
import requests


def country_parser():
    url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0' \
          '%B0%D1%80%D1%81%D1%82%D0%B2 '
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    table = soup.find('table', class_='wikitable')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    countries_data = []

    for row in rows:
        country_data = {}

        try:
            country = row.findAll('td')[2].text
            full_country_name = row.findAll('td')[3].text
        except (UnboundLocalError, IndexError, TypeError):
            country = None
            full_country_name = None

        try:
            flag_url = row.find('img').get('src')
        except AttributeError:
            flag_url = None

        country_data['country'] = country
        country_data['full_country_name'] = full_country_name
        country_data['same_letter_count'] = None
        country_data['flag_url'] = flag_url

        countries_data.append(country_data)

    return countries_data


def get_same_letter_count(countries, country):
    first_str = country[0]
    same_letter = 0

    for country in countries:
        try:
            if country['country'][0] == first_str:
                same_letter = same_letter + 1
        except TypeError:
            same_letter = 0
    return same_letter


def get_country_data(country):
    countries_data = country_parser()
    same_letter_count = get_same_letter_count(countries_data, country)
    search_country = None

    for country_data in countries_data:
        if country_data['country'] == country + '\n':
            country_data['same_letter_count'] = same_letter_count
            search_country = country_data

    return print(search_country)


if __name__ == '__main__':
    get_country_data('Украина')
