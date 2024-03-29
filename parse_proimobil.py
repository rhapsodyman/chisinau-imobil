import json
import math
import urllib.parse

import requests
from bs4 import BeautifulSoup
import re

from output_helper import write_results

url = "https://proimobil.md/apartamente-de-vanzare-in-chisinau?filter="
headers = ['Region', 'Street', 'Price', 'Rooms', 'Area', 'Meter Price', 'Link']

if __name__ == '__main__':
    # parse config
    with open("config.json", 'r') as j:
        config = json.loads(j.read())

    filters_part = ""
    filters_part += "category:" + ",".join(config["category"])
    filters_part += ";price:{}..{}".format(config["minPrice"], config["maxPrice"])
    filters_part += ";apartmentType:" + ",".join(config["apartmentType"])
    filters_part += ";apartmentState:" + ",".join(config["apartmentState"])
    filters_part += ";rooms:" + ",".join(config["rooms"])
    filters_part += ";offerType:" + ",".join(config["offerType"])

    url = url + urllib.parse.quote_plus(filters_part)
    print("Url to be used " + url)

    resp = requests.get(url)
    index = BeautifulSoup(resp.content, 'html.parser')

    count = index.find("span", class_="text-secondary").text.replace('oferte', '').strip()
    all_page_items = index.find_all("div", class_=["catCard", "box-shadow"])

    n_pages = math.ceil(int(count) / len(all_page_items))
    apartments = []

    for x in range(1, n_pages + 1):
        print('Processing page # {}'.format(x))

        resp = requests.get(url + '&page=' + str(x))
        index = BeautifulSoup(resp.content, 'html.parser')
        all_page_items = index.find_all("div", class_=["catCard", "box-shadow"])

        for item in all_page_items:
            class_val = item['class']

            if 'sold' in class_val:
                continue  # skipping sold items

            recommended = 0
            new_price = 0

            # if 'recommended' in class_val:
            #     recommended = 1
            #
            # if 'new-price' in class_val:
            #     new_price = 1

            link = 'https://proimobil.md' + item.find('a')['href']
            price = item.find("a", class_='catCard__price').text.replace('€', '').replace(' ', '').replace(',', '').strip()

            if not re.match('\d+', price): # most likely is sold
                continue


            address = item.find("div", class_='catCard__location').text.strip()
            region, street = address.split(",", 1)

            # data = item.find_all('div', class_='catCard__data')
            data = item.select('div.catCard__data > span')
            n_rooms = data[0].text
            area = data[2].text.replace('m2', '').strip()

            meter_price = float(price) / float(area)

            apartment_data = [region, street, price, n_rooms, area, meter_price, link]
            apartments.append(apartment_data)

    # print(headers)
    # for item in apartments:
    #     print(item)

    write_results(headers, apartments, "proimobil", config["outputType"])
