import pandas as pd
from sklearn import preprocessing

PUBLISHERS_COLUMN_NAME = 'clean-publisher'
AUTHORS_COLUMN_NAME = 'authors'
TITLE_COLUMN_NAME = 'title'
DESCRIPTION_COLUMN_NAME = 'description'
RATING_AVG_COLUMN_NAME = 'rating-avg'
RATING_COUNT_COLUMN_NAME = 'rating-count'
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
PRICE_COLUMN_NAME = 'price'
BESTSELLERS_SCORE = 5000


def normalize_column(df, feature_name):
    # max_value = df[feature_name].max()
    # min_value = df[feature_name].min()
    # df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    df[feature_name] = (df[feature_name] - df[feature_name].mean()) / df[feature_name].std()
    return df


def normalize_data(df):
    df = normalize_column(df, PRICE_COLUMN_NAME)
    df = normalize_column(df, RATING_AVG_COLUMN_NAME)
    df = normalize_column(df, RATING_COUNT_COLUMN_NAME)
    # TODO: normalize publisher and author rank
    return df


if __name__ == '__main__':
    fantasy = pd.read_excel('BookDepository/Fantasy.xlsx')
    # print(fantasy.columns)
    print(fantasy["price"])
    fantasy = normalize_column(fantasy, PRICE_COLUMN_NAME)
    print(fantasy["price"])