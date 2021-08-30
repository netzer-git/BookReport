import pandas as pd
from pip._internal.cli.status_codes import SUCCESS

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


def split_category_field(category_str):
    category_lst = category_str.split(',')
    for i in range(len(category_lst)):
        category_lst[i] = category_lst[i].replace('\"', '').replace('\'', '').replace('[', '').replace(']', '')
        category_lst[i] = "".join(category_lst[i].split(' '))

    return category_lst


def analyze_categories(df):
    categories_dict = {}
    for i in range(len(df[CATEGORIES_COLUMN_NAME])):
        category_lst = split_category_field(df[CATEGORIES_COLUMN_NAME][i])
        rank = df[BESTSELLERS_COLUMN_NAME][i]
        for c in category_lst:
            if c is not None and c in categories_dict:
                categories_dict[c][0] += rank
                categories_dict[c][1] += 1
            elif c is not None:
                categories_dict[c] = [0, 0]
                categories_dict[c][0] += rank
                categories_dict[c][1] += 1

    categories_list = []
    for c in categories_dict:
        if categories_dict[c][1] > BOOK_NUM_IN_CATEGORY:
            categories_list.append(c)
    return categories_list


def get_rank_dict(df, column_name):
    rank_dict = {}
    for i in range(len(df[column_name])):
        name = df[column_name][i]
        rank = df[BESTSELLERS_COLUMN_NAME][i]

        if name is not None and name in rank_dict:
            rank_dict[name][0] += rank
            rank_dict[name][1] += 1
        elif name is not None:
            rank_dict[name] = [0.0, 0.0]
            rank_dict[name][0] += rank
            rank_dict[name][1] += 1

    for key in rank_dict:
        rank_dict[key].append(rank_dict[key][0] / rank_dict[key][1])
    return rank_dict


def write_binary_big_publishers_column(df, rank_dict):
    big_publishers_lst = [key for key in rank_dict if rank_dict[key][1] > BIG_PUBLISHERS_BOOK_NUM]
    new_column = []
    for p in df[PUBLISHERS_COLUMN_NAME]:
        new_column.append(int(p in big_publishers_lst))

    df['big-publisher-rank'] = new_column
    return df


def write_binary_categories_columns(df, categories_list):
    new_columns = {c: [] for c in categories_list}
    for i in range(len(df['crawl_id'])):
        entry_categories = split_category_field(df[CATEGORIES_COLUMN_NAME][i])
        for c in categories_list:
            new_columns[c].append(int(c in entry_categories))

    for c in new_columns:
        df[c] = new_columns[c]

    return df


def write_numeric_rank_column(df, rank_dict, column_name):
    new_column = []
    for a in df[column_name]:
        new_column.append(rank_dict[a][2])

    df[column_name + '-rank'] = new_column
    return df


def preprocess_root_xl(path):
    # reading excel to df
    df = pd.read_excel(path)
    # organize the data
    categories_list = analyze_categories(df)
    publishers_rank_dict = get_rank_dict(df, PUBLISHERS_COLUMN_NAME)
    authors_rank_dict = get_rank_dict(df, AUTHORS_COLUMN_NAME)
    # write binary columns
    df = write_binary_big_publishers_column(df, publishers_rank_dict)
    df = write_binary_categories_columns(df, categories_list)
    # write numeric columns
    df = write_numeric_rank_column(df, publishers_rank_dict, PUBLISHERS_COLUMN_NAME)
    df = write_numeric_rank_column(df, authors_rank_dict, AUTHORS_COLUMN_NAME)
    # writing back to the original file
    df.to_excel(path, index=False)
    return SUCCESS


if __name__ == '__main__':
    preprocess_root_xl(XL_ROOT)
