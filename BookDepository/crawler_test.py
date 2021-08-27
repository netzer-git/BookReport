import bookdepository_crawler
import requests
from bs4 import BeautifulSoup

url = 'https://www.bookdepository.com/Circe-Madeline-Miller/9781408890042'

book_r = requests.get(url)
book_r_soup = BeautifulSoup(book_r.text, 'html.parser')
print(bookdepository_crawler.get_description(book_r_soup))
