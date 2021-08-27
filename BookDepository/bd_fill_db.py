import pandas as pd
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
import bookdepository_crawler

BASE_URL = 'https://www.bookdepository.com'
MAX_DATA = 1111


def get_data_from_url(url):
    r = requests.get(BASE_URL + url)
    book_soup = BeautifulSoup(r.text, 'html.parser')
    price = bookdepository_crawler.get_price(book_soup)
    publisher = bookdepository_crawler.get_publisher(book_soup)
    clean_publisher = bookdepository_crawler.clean_publisher_name(publisher)
    return {
        'url': url,
        'price': price,
        'publisher': publisher,
        'clean_publisher': clean_publisher
    }


def write_data_to_xl(data):
    """
    :param data: [{url: , price: , publisher: }, ... { ... }]
    """
    wb = Workbook()
    wb['Sheet'].title = "DB missing labels"
    sheet1 = wb.active
    sheet1['A1'].value = 'url'
    sheet1['B1'].value = 'Price'
    sheet1['C1'].value = 'Publisher'
    sheet1['D1'].value = 'Clean Publisher'

    for line_num in range(len(data)):
        sheet1['A' + str(line_num + 2)].value = data[line_num]['url']
        sheet1['B' + str(line_num + 2)].value = data[line_num]['price']
        sheet1['C' + str(line_num + 2)].value = data[line_num]['publisher']
        sheet1['D' + str(line_num + 2)].value = data[line_num]['clean_publisher']

    wb.save("publishers_and_price.xlsx")


def get_data(df):
    data = []
    counter = 0

    for url in df['url']:
        counter += 1  # Debug
        try:
            entry = get_data_from_url(url)
            data.append(entry)

            # Debug
            # print(str(counter) + "/" + str(MAX_DATA) + " : " + str(entry))
            print("{:.2f}".format((counter*100)/MAX_DATA) + "% : " + str(entry))
            if counter == MAX_DATA:
                break

        except ValueError or AttributeError:
            pass

    return data


if __name__ == '__main__':
    df = pd.read_csv('../../DB/bd_dataset.csv')
    print('*** all set ***')
    data = get_data(df)
    print('Got: ' + str(len(data)) + ' items')
    write_data_to_xl(data)
    print('*** all in ***')
