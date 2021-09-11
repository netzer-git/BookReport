"""
Constants file
"""
# XL file names
XL_SCRAPED = 'dbSlices/BD_Crawler.xlsx'
XL_ROOT = 'xl_process/BD_Crawler_Full.xlsx'
XL_PROCESSED = 'xl_process/AfterProcessData.xlsx'
XL_AUTHORS_OUTPUT = 'xl_process/Best_Authors'
XL_PUBLISHERS_OUTPUT = 'xl_process/Best_Publishers'
# Column names
AUTHORS_COLUMN_NAME = 'authors'
PUBLISHERS_COLUMN_NAME = "clean-publisher"
CATEGORIES_COLUMN_NAME = "categories"
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
RATING_AVG_COLUMN_NAME = 'rating-avg'
RATING_COUNT_COLUMN_NAME = 'rating-count'
NUMERIC_AUTHOR_RANK_COLUMN_NAME = 'authors-rank'
NUMERIC_PUBLISHER_RANK_COLUMN_NAME = 'clean-publisher-rank'
PRICE_COLUMN_NAME = 'price'
NON_NUMERIC_COLUMNS = ['title',
                       'clean_title',
                       'authors',
                       'categories',
                       'description',
                       'isbn13',
                       'format',
                       'publication-date',
                       'url',
                       'publisher',
                       'clean-publisher',
                       'crawl_id']
LOG_COLUMNS = ['rating-count',
               'clean-publisher-rank',
               'authors-rank']
COUNT = 'count'
AVG = 'AVG'
# Analyzing scores
WORST_BESTSELLERS = 1_000_000  #_000_000
BEST_AUTHOR_RANK = 30_000
BIG_PUBLISHERS_BOOK_NUM = 1_000
BOOK_NUM_IN_CATEGORY = 3_500
BESTSELLERS_SCORE = 5000
CATEGORIES_LIST = ['ContemporaryFiction', 'Fantasy', 'Mind', 'Memoirs', 'FunnyBooks&Stories', 'GraphicNovels',
                   'Anime&Manga', 'ScienceFiction', 'Crime', 'CrimeFiction']

# Crawling Constants
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
OUTPUT_FILE_NAME = 'BD_Crawler'
GET_NUMBERS = False
BESTSELLERS = False
NUMBER_OF_PAGES = 100
crawl_id = 0
duplicates = 0
