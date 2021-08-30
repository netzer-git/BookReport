import pandas as pd

RATING_AVG_COLUMN_NAME = 'rating-avg'
RATING_COUNT_COLUMN_NAME = 'rating-count'
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
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

    df = normalize_column(df, NUMERIC_AUTHOR_RANK_COLUMN_NAME)
    df = normalize_column(df, NUMERIC_PUBLISHER_RANK_COLUMN_NAME)
    return df


def drop_textual_columns(df, columns_lst):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    return df.drop(columns=columns_lst, inplace=False)


if __name__ == '__main__':
    fantasy = pd.read_excel('BookDepository/Fantasy.xlsx')
    fantasy = normalize_data(fantasy)
    fantasy = drop_textual_columns(fantasy, NON_NUMERIC_COLUMNS)
    print(fantasy)
    print(fantasy.columns)
    fantasy.to_excel('after.xlsx', index=False)

