XL_ROOT = 'BookDepository/Fantasy.xlsx'
XL_AUTHORS_OUTPUT = 'Best_Authors.xlsx'
XL_PUBLISHERS_OUTPUT = 'Best_Publishers.xlsx'
AUTHORS_COLUMN_NAME = 'authors'
PUBLISHERS_COLUMN_NAME = "clean-publisher"
CATEGORIES_COLUMN_NAME = "categories"
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
BEST_AUTHOR_RANK = 30_000
BIG_PUBLISHERS_BOOK_NUM = 30
BOOK_NUM_IN_CATEGORY = 150

RATING_AVG_COLUMN_NAME = 'rating-avg'
RATING_COUNT_COLUMN_NAME = 'rating-count'
NUMERIC_AUTHOR_RANK_COLUMN_NAME = 'authors-rank'
NUMERIC_PUBLISHER_RANK_COLUMN_NAME = 'clean-publisher-rank'

NON_NUMERIC_COLUMNS = ['title',
                       'clean_title',
                       'authors',
                       'categories',
                       'description',
                       'isbn13',
                       # 'format',
                       # 'publication-date',
                       'url',
                       'publisher',
                       'clean-publisher',
                       'crawl_id']

PRICE_COLUMN_NAME = 'price'
BESTSELLERS_SCORE = 5000
