from bs4 import BeautifulSoup
from openpyxl import Workbook

import Constants
import bookdepository_crawler


def write_category_to_xl(data, category_name):
    """
    write one category data to excel file
    :param data: [{url: , ... }, ... { ... }] - list of scraped-book objects
    :param category_name: the name of the written category
    """
    labels = ['title', 'clean_title', 'authors', 'bestsellers-rank', 'categories', 'description', 'isbn13', 'format',
              'publication-date', 'rating-avg', 'rating-count', 'url', 'publisher', 'clean-publisher', 'price',
              'crawl_id']
    ABC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']

    wb = Workbook()
    wb['Sheet'].title = Constants.OUTPUT_FILE_NAME
    sheet1 = wb.active

    for i in range(len(labels)):
        sheet1[ABC[i] + str(1)].value = labels[i]

    for i in range(len(data)):
        for j in range(len(labels)):
            entry = data[i]
            sheet1[ABC[j] + str(i + 2)].value = str(entry[labels[j]])  # fixme !!!!

    wb.save(Constants.OUTPUT_FILE_NAME + '_' + category_name + ".xlsx")


if __name__ == '__main__':
    for category in Constants.CATEGORY_URL:
        full_data = []
        category_name = category.split('/')[3]
        current_url = Constants.BASE_URL + category + Constants.URL_SUFFIX
        print('*** Crawling ' + category_name + ' ***')
        for i in range(1, Constants.NUMBER_OF_PAGES + 1):
            # add data from the main page
            page_data, page_names = bookdepository_crawler.get_data_from_30_pages(current_url)
            full_data += page_data
            # get the url for the next page
            r = bookdepository_crawler.activate_request(current_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            current_url = Constants.BASE_URL + category + Constants.URL_SUFFIX + '?page=' + str(i + 1)

        print('*** Writing ' + category_name + ' ***')
        write_category_to_xl(full_data, category_name)

    print("*** Finish ***")
