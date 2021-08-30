# XL file names
XL_ROOT = 'BookDepository/Fantasy.xlsx'
XL_PROCESSED = 'AfterProcessData.xlsx'
XL_AUTHORS_OUTPUT = 'Best_Authors.xlsx'
XL_PUBLISHERS_OUTPUT = 'Best_Publishers.xlsx'
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
                       # 'format',
                       # 'publication-date',
                       'url',
                       'publisher',
                       'clean-publisher',
                       'crawl_id']
# Analyzing scores
BEST_AUTHOR_RANK = 30_000
BIG_PUBLISHERS_BOOK_NUM = 100
BOOK_NUM_IN_CATEGORY = 1_000
BESTSELLERS_SCORE = 5000
