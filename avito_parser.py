import csv
import time
import random
import urllib3
import requests
from bs4 import BeautifulSoup
from IPython.display import clear_output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


HEADERS = {
     'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
}

COLUMNS = ['label', 'model', 'generation', 'modification', 'year', 'mileage', 'condition',
               'doors_num', 'body', 'engine', 'transmission', 'color', 'drive', 'wheel', 'package', 'price']


def parse_avito():
    url = 'https://www.avito.ru/nizhniy_novgorod/avtomobili?cd=1&radius=200'
    request = get_request(url)
    soup = BeautifulSoup(request.text, 'lxml')
    page = soup.find('div', {'class': 'popular-rubricator-links-b0HPS'})
    modelsList = page.find_all('div', {'class': ['popular-rubricator-row-2oc-J']})
    
    for model in modelsList:
        time.sleep(1 + random.random())
        modelLink = 'https://avito.ru' + model.find('a').get('href')
        parse_car_model(modelLink)


def parse_car_model(url):
    lastPage = get_last_page(url)

    for pageNum in range(1, lastPage+1):
        clear_output(wait=True)
        print(f"Страница: {pageNum}/{lastPage}", flush=True)
        time.sleep(1 + random.random())
        pageLink = url + f'&p={pageNum}'
        parse_page_with_ads(pageLink)


def get_last_page(url):

    request = get_request(url)
    soup = BeautifulSoup(request.text, 'lxml')
    pagination = soup.find('div', {'class': 'pagination-root-2oCjZ'})
    page = pagination.find_all('span')
    lastPage = int(page[-2].text)
    return lastPage


def parse_page_with_ads(url):
    request = get_request(url)
    soup = BeautifulSoup(request.text, 'lxml')
    page = soup.find('div', {'class': 'snippet-list js-catalog_serp'})
    carList = page.find_all('div', {'class': ['item__line']})

    for car in carList:
        time.sleep(1 + random.random())
        carLink = 'https://avito.ru' + car.find('div',
                                               {'class': 'snippet-title-row'}).find('a').get('href')
        parse_ad(carLink)


def parse_ad(url):
    carParams = get_car_info(url)
    write_to_csv(carParams)


def get_car_info(url):
    ParamNameToEnglish = {'Марка': 'label', 'Модель': 'model', 'Поколение': 'generation',
                 'Модификация': 'modification', 'Год выпуска': 'year',
                 'Пробег': 'mileage', 'Состояние': 'condition', 'Руль': 'wheel',
                 'Тип кузова': 'body', 'Количество дверей': 'doors_num',
                 'Тип двигателя': 'engine', 'Коробка передач': 'transmission',
                 'Привод': 'drive', 'Цвет': 'color', 'Комплектация': 'package'}

    carParams = {key: '' for key in COLUMNS}
    request = get_request(url)
    soup = BeautifulSoup(request.text, 'lxml')
    params = soup.find_all('li', {'class': 'item-params-list-item'})

    for param in params:
        stringToParse = param.text.replace(u'\xa0', u' ').split(':')
        param = ParamNameToEnglish.get(stringToParse[0].strip())
        paramValue = stringToParse[1].strip()
        carParams[param] = paramValue
            
    price = soup.find('div', {'class': 'item-price'}).text.strip().split()
    carParams['price'] = ''.join(price[:price.index('₽')])
    return carParams


def write_to_csv(carParams):
    with open("data/avito_cars.csv", 'a', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=COLUMNS)
        carDescription = {param:carParams[param] for param in COLUMNS}
        writer.writerow(carDescription)


def get_request(url):
    while True:
        try:
            rs = requests.get(url, headers=HEADERS, verify=False)
            if rs.status_code == 200:
                rs.encoding = 'utf-8'
                return rs
            print("Ошибка, код ответа:", rs.status_code)
            time.sleep(random.random())
            continue

        except:
            print("Ошибка")
            time.sleep(random.random())