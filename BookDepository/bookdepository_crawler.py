import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

BASE_URL = 'https://www.bookdepository.com'
BESTSELLERS_URL = '/bestsellers'
CATEGORY_URL = [
    '/category/2/Art-Photography',
    '/category/213/Biography',
    '/category/2455/Childrens-Books',
    '/category/2942/Crafts-Hobbies',
    '/category/2616/Crime-Thriller',
    '/category/333/Fiction',
    '/category/2885/Beverages',
    '/category/2633/Graphic-Novels-Anime-Manga',
    '/category/2638/History-Archaeology',
    '/category/2819/Mind-Body-Spirit',
    '/category/2623/Science-Fiction-Fantasy-Horror',
    '/category/928/Business-Finance-Law',
    '/category/2978/Humour',
    '/category/2985/Natural-History',
    '/category/3391/Teen-Young-Adult',
    '/category/3013/Sport'
]
URL_SUFFIX = '/browse/viewmode/all'

GET_NUMBERS = False
BESTSELLERS = False
NUMBER_OF_PAGES = 333
crawl_id = 0
duplicates = 0


def get_title(book):
    try:
        return book.find(itemprop='name').text
    except AttributeError:
        return None


def get_clean_title(title):
    """
    :param title: book's title
    :return: cleaned title
    """
    return None if title is None else title.split(':')[0]


def get_rating_avg(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's rating average
    """
    try:
        return float(book.find(itemprop='ratingValue').text)
    except AttributeError:
        return None


def get_rating_count(book):
    """
    :param book: full book html element as BeautifulSoup
    :return:book's rating count
    """
    try:
        return int(''.join(char for char in book.find(class_='rating-count').text if char.isdigit()))
    except AttributeError:
        return None


def get_price(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's price
    """
    try:
        return float(book.find(class_='sale-price').text[1:])
    except AttributeError:
        try:
            return float(
                ''.join(char for char in book.find(class_='list-price').text if (char.isdigit() or char == '.')))
        except AttributeError:
            return None
    except ValueError:
        return float(''.join(char for char in book.find(class_='sale-price').text if (char.isdigit() or char == '.')))


def get_bestsellers_rank(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's bestsellers rank
    """
    try:
        product_box = book.find(class_='biblio-info')
        li_list = product_box.find_all('li')
        rank_str = li_list[-1].find('span').text.strip('\n').strip(' ')
        return int(''.join(c for c in rank_str if c.isdigit()))
    except AttributeError:
        return None


def get_description(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's description
    """
    try:
        desc = book.find(itemprop="description").text.strip().strip('\n\n')
        desc = ''.join(desc.split('\n\n'))
        return desc
    except AttributeError:
        return None


def get_publisher(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's publisher - cleaned
    """
    try:
        return book.find(itemprop='publisher').text.strip('\n').strip(' ')
    except AttributeError:
        return None


def clean_publisher_name(publisher):
    if publisher is None:
        return None
    country_suffix = ['uk', 'us', 'usa', 'au', 'emea', 'europe', 'australia', 'new zealand', 'singapore']
    company_suffix = ['inc', 'ltd', 'international', 'limited', 'co']
    special_publishers = ['springer']
    # lower case
    publisher = publisher.lower()
    # switch ',' or '-' or '.' to space
    publisher = publisher.replace(",", " ")
    publisher = publisher.replace("-", " ")
    publisher = publisher.replace(".", " ")
    # special publishers check
    publisher_words = publisher.split()
    for s_publisher in special_publishers:
        if s_publisher in publisher_words:
            # special publisher found
            return s_publisher
    # replace '&' with 'and'
    publisher = publisher.replace("&", " and ")
    publisher = ' '.join(publisher.split())
    # get rid of country suffix and company suffix and suffix of (..)
    publisher_without_suffix = []
    publisher_words = publisher.split()
    for word in publisher_words:
        if word in country_suffix + company_suffix:
            continue
        elif word.startswith('(') and word.endswith(')'):
            continue
        else:
            publisher_without_suffix.append(word)
    publisher = ' '.join(publisher_without_suffix)

    # return clean_publisher_name
    return publisher


def get_authors(book):
    try:
        if GET_NUMBERS:
            authors = None
        else:
            authors = book.find(itemprop='author').text.strip('\n').strip(' ')
    except AttributeError:
        return None
    return authors


def get_categories(book):
    try:
        categories = book.find(class_='breadcrumb')
        categories = categories.find_all('a')
        categories = [c.text.strip('\n').strip(' ') for c in categories]
        if GET_NUMBERS:
            categories = [int(categories_dict[c]) for c in categories]
        else:
            pass
    except AttributeError:
        return None
    return categories


def get_isbn13(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: book's isbn13 - the ID of the book
    """
    try:
        return book.find(itemprop='isbn').text
    except AttributeError:
        return None


def get_book_format(book):
    """
    :param book: full book html element as BeautifulSoup
    :return: number of format
    """
    try:
        details_box = book.find(class_='biblio-info')
        sp = details_box.find('span').text.strip('\n').strip(' ')
        book_format = sp.split(' ')[0].strip('\n')
        return format_dict[book_format]
    except AttributeError:
        return None
    except KeyError:
        return None


def get_publication_date(book):
    return None


def get_one_data_from_book(book):
    """
    :param book: BeautifulSoup element of a book page
    :return: TODO
    """
    global crawl_id
    crawl_id += 1

    # gets book title
    title = get_title(book)
    clean_title = get_clean_title(title)
    # gets book rating value
    rating_avg = get_rating_avg(book)
    # gets book rating count
    rating_count = get_rating_count(book)
    # gets book's price
    price = get_price(book)
    # gets book bestsellers rank
    bestsellers_rank = get_bestsellers_rank(book)
    # get the book publisher, and cleaned publisher name
    publisher = get_publisher(book)
    clean_publisher = clean_publisher_name(publisher)
    # get the book authors and find their numbers
    authors = get_authors(book)
    # get the book categories and find their number
    categories = get_categories(book)
    # get the book description
    description = get_description(book)
    # get the book publication date
    publication_date = get_publication_date(book)
    # get book's isbn13 - id number
    isbn13 = get_isbn13(book)
    # get book's format
    book_format = get_book_format(book)

    # return the book data by field
    return {
        'crawl_id': crawl_id,
        'title': title,
        'clean_title': clean_title,
        'rating-avg': rating_avg,
        'rating-count': rating_count,
        'price': price,
        'bestsellers-rank': bestsellers_rank,
        'authors': authors,
        'categories': categories,
        'description': description,
        'publication-date': publication_date,
        'publisher': publisher,
        'clean-publisher': clean_publisher,
        'isbn13': isbn13,
        'format': book_format,
    }


def get_data_from_30_pages(main_bestsellers_url):
    """
    :param main_bestsellers_url: url for a list of TODO
    :return: TODO
    """
    global duplicates
    r = requests.get(main_bestsellers_url)
    data = []
    names = set()

    r_soup = BeautifulSoup(r.text, 'html.parser')
    books = r_soup.find_all(class_="book-item")

    for book in books:
        book_title = book.find(class_="title")
        b_t = book_title.find('a')
        book_url = BASE_URL + b_t['href']

        book_r = requests.get(book_url)
        book_r_soup = BeautifulSoup(book_r.text, 'html.parser')

        book_data = {**get_one_data_from_book(book_r_soup), **{'url': book_url}}
        if book_data['title'] not in full_names:
            data.append(book_data)
            names.add(book_data['title'])
            print(str(crawl_id) + " : " + str(book_data['title']) + " : " + book_url)
        else:
            duplicates += 1

    return data, names


def read_csv_data(filename, header):
    data = {}
    path_prefix = '..DB/'
    entry_id = header + "_id"
    name = header + "_name"
    csv_df = pd.read_csv(path_prefix + filename)
    for i in range(len(csv_df[entry_id])):
        number = csv_df[entry_id][i]
        entry = csv_df[name][i]
        data[entry] = int(number)
    return data


def read_all_csv():
    global authors_dict, categories_dict, format_dict
    if GET_NUMBERS:  # currently bugged fixme
        authors_dict = read_csv_data('bd_authors.csv', 'author')
        categories_dict = read_csv_data('bd_categories.csv', 'category')
        format_dict = read_csv_data('bd_formats.csv', 'format')
    else:
        authors_dict = {}
        categories_dict = {}
        format_dict = {}


def write_data_to_xl(data):
    """
    :param data: [{url: , ... }, ... { ... }]
    """
    labels = ['title', 'clean_title', 'authors', 'bestsellers-rank', 'categories', 'description', 'isbn13', 'format',
              'publication-date', 'rating-avg', 'rating-count', 'url', 'publisher', 'clean-publisher', 'crawl_id']
    ABC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']

    wb = Workbook()
    wb['Sheet'].title = "Bookdepository_Crawler"
    sheet1 = wb.active

    for i in range(len(labels)):
        sheet1[ABC[i] + str(1)].value = labels[i]

    for i in range(len(data)):
        for j in range(len(labels)):
            entry = data[i]
            sheet1[ABC[j] + str(i + 2)].value = str(entry[labels[j]])  # fixme !!!!

    wb.save("Bookdepository_Crawler_fantasy.xlsx")


if __name__ == '__main__':
    full_data = []
    global full_names  # fixme
    full_names = set()
    print("*** Reading xlsx helpers ***")
    read_all_csv()
    if BESTSELLERS:
        print("*** Crawling ***")
        current_url = BASE_URL + BESTSELLERS_URL
        for i in range(1, NUMBER_OF_PAGES + 1):
            # add data from the main page
            page_data, page_names = get_data_from_30_pages(current_url)
            full_data += page_data
            full_names.update(page_names)
            # get the url for the next page
            soup = BeautifulSoup(requests.get(current_url).text, 'html.parser')
            current_url = BASE_URL + BESTSELLERS_URL + '?page=' + str(i + 1)
    else:
        for category in CATEGORY_URL:
            current_url = BASE_URL + category + URL_SUFFIX
            print('*** Crawling ' + category.split('/')[3] + ' ***')
            for i in range(1, NUMBER_OF_PAGES + 1):
                # add data from the main page
                page_data, page_names = get_data_from_30_pages(current_url)
                full_data += page_data
                full_names.update(page_names)
                # get the url for the next page
                soup = BeautifulSoup(requests.get(current_url).text, 'html.parser')
                current_url = BASE_URL + category + URL_SUFFIX + '?page=' + str(i + 1)

    # write data to xlsx
    print("*** Writing data to xlsx ***")
    write_data_to_xl(full_data)

    print(len(full_data))
