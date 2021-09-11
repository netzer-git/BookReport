import pandas as pd
from pip._internal.cli.status_codes import SUCCESS
import Constants
from openpyxl import Workbook


def split_category_field(category_str):
    """
    scrape the categories field from the crawled format
    :param category_str: category string as in the crawled format
    :return: category list
    """
    category_lst = category_str.split(',')
    for i in range(len(category_lst)):
        category_lst[i] = category_lst[i].replace('\"', '').replace('\'', '').replace('[', '').replace(']', '')
        category_lst[i] = "".join(category_lst[i].split(' '))

    return category_lst


def analyze_categories(path):
    """
    run over the excel file and extract a list of the big categories
    :param path: path to excel file
    :return: a list of the big categories
    """
    df = pd.read_excel(path)
    categories_dict = {}
    for i in range(len(df[Constants.CATEGORIES_COLUMN_NAME])):
        category_lst = split_category_field(df[Constants.CATEGORIES_COLUMN_NAME][i])
        try:
            rank = int(df[Constants.BESTSELLERS_COLUMN_NAME][i])
        except ValueError:
            print(f"ValueError: \'{rank}\'")

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
        if categories_dict[c][1] > Constants.BOOK_NUM_IN_CATEGORY:
            categories_list.append(c)
    return categories_list


def get_rank_dict(df, column_name, target_column):
    """
    analyze the df and get a dict of rank of the entries of column_name
    :param df: the full df
    :param column_name: the name of the analyzed column
    :param target_column: the column to be analyzed as pointes
    :return: dict {entry: [sum_of_rank, num_of_books, rank_avg]
    """
    rank_dict = {}
    for i in range(len(df[column_name])):
        name = df[column_name][i]
        try:
            # rank = float(df[Constants.BESTSELLERS_COLUMN_NAME][i])
            rank = float(df[target_column][i])
        except ValueError:
            print(f"ValueError: \'{df[target_column][i]}\'")

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
    """
    with the rank_dict of the publisher, crate binary column with 1 for the big publisher's books
    :param df: the full df
    :param rank_dict: the rank dict of the publishers
    :return: the df, with the binary columns
    """
    big_publishers_lst = [key for key in rank_dict if rank_dict[key][1] > Constants.BIG_PUBLISHERS_BOOK_NUM]
    new_column = []
    for p in df[Constants.PUBLISHERS_COLUMN_NAME]:
        new_column.append(p in big_publishers_lst)

    df['big-publisher-rank'] = new_column
    return df


def write_binary_categories_columns(df, categories_list):
    """
    with the list of the big categories, crate binary column with 1 for the books in those categories, one column for
    each category
    :param df: the full df
    :param categories_list: the list of the big categories
    :return: the df, with the binary columns
    """
    new_columns = {c: [] for c in categories_list}
    for i in range(len(df['crawl_id'])):
        entry_categories = split_category_field(df[Constants.CATEGORIES_COLUMN_NAME][i])
        for c in categories_list:
            new_columns[c].append(c in entry_categories)

    for c in new_columns:
        df[c] = new_columns[c]

    return df


def write_numeric_rank_column(df, rank_dict, column_name, suffix):
    """
    add the numeric columns from the rank_dict
    :param df: the full df
    :param rank_dict: the rank_dict to fill
    :param column_name: the name of the original column
    :param suffix: the ending of the new column name
    :return: the df with the new column
    """
    new_column = []
    for a in df[column_name]:
        new_column.append(rank_dict[a][2])

    df[column_name + '-rank-' + suffix] = new_column
    return df


def write_ranks_to_xl(rank_dict, path):
    """
    save the rank dict to excel file for further analyzation
    :param rank_dict: the rank_dict
    :param path: the path to the new excel file
    """
    wb = Workbook()
    wb['Sheet'].title = 'sheet1'
    sheet1 = wb.active
    sheet1['A1'] = 'Creator'
    sheet1['B1'] = 'rank'
    sheet1['C1'] = 'rank-sum'
    sheet1['D1'] = 'book-num'
    i = 0

    for entry in rank_dict:
        sheet1['A' + str(i + 2)].value = entry
        sheet1['B' + str(i + 2)].value = rank_dict[entry][2]
        sheet1['C' + str(i + 2)].value = rank_dict[entry][0]
        sheet1['D' + str(i + 2)].value = rank_dict[entry][1]
        i += 1

    wb.save(path + '.xlsx')


def drop_single_book_entries(df, rank_dict):
    """
    dropping each row where the book's author has just 1 book overall
    :param df: the main df
    :param rank_dict: the authors ranks of bestsellers-rank
    :return: the df without the columns
    """
    drop_list = []
    for i in range(len(df[Constants.AUTHORS_COLUMN_NAME])):
        author = df[Constants.AUTHORS_COLUMN_NAME][i]
        if rank_dict[author][1] == 1:
            drop_list.append(i)
    df.drop(drop_list, inplace=True)
    return df


def drop_bestsellers_outliers(df):
    """
    run over the df and drop the outliers target numbers.
    :param df: the main df
    :return: the df without outliers
    """
    drop_list = []
    for i in range(len(df[Constants.BESTSELLERS_COLUMN_NAME])):
        try:
            rank = df[Constants.BESTSELLERS_COLUMN_NAME][i]
            if rank > Constants.WORST_BESTSELLERS:
                drop_list.append(i)
        except KeyError:
            print('KeyError: ' + str(i))
        except TypeError:
            print('TypeError: ' + str(df[Constants.BESTSELLERS_COLUMN_NAME][i]))
    df.drop(drop_list, inplace=True)
    return df


def preprocess_scraped_xl(path_in, path_out):
    """
    take the scraped excel and preprocess as wanted.
    :param path_in: path to input file
    :param path_out: path to output file
    :return: SUCCESS
    """
    # reading excel to df
    df = pd.read_excel(path_in)
    # organize the data
    publishers_rank_avg_dict = get_rank_dict(df, Constants.PUBLISHERS_COLUMN_NAME, Constants.RATING_AVG_COLUMN_NAME)
    publishers_rank_count_dict = get_rank_dict(df, Constants.PUBLISHERS_COLUMN_NAME, Constants.RATING_COUNT_COLUMN_NAME)
    publishers_rank_dict = get_rank_dict(df, Constants.PUBLISHERS_COLUMN_NAME, Constants.BESTSELLERS_COLUMN_NAME)

    authors_rank_avg_dict = get_rank_dict(df, Constants.AUTHORS_COLUMN_NAME, Constants.RATING_AVG_COLUMN_NAME)
    authors_rank_count_dict = get_rank_dict(df, Constants.AUTHORS_COLUMN_NAME, Constants.RATING_COUNT_COLUMN_NAME)
    authors_rank_dict = get_rank_dict(df, Constants.AUTHORS_COLUMN_NAME, Constants.BESTSELLERS_COLUMN_NAME)

    write_ranks_to_xl(authors_rank_count_dict, Constants.XL_AUTHORS_OUTPUT)
    write_ranks_to_xl(publishers_rank_count_dict, Constants.XL_PUBLISHERS_OUTPUT)

    # write binary columns
    df = write_binary_big_publishers_column(df, publishers_rank_avg_dict)
    df = write_binary_categories_columns(df, Constants.CATEGORIES_LIST)
    # write numeric columns
    df = write_numeric_rank_column(df, publishers_rank_avg_dict, Constants.PUBLISHERS_COLUMN_NAME, Constants.AVG)
    df = write_numeric_rank_column(df, publishers_rank_count_dict, Constants.PUBLISHERS_COLUMN_NAME, Constants.COUNT)
    df = write_numeric_rank_column(df, publishers_rank_dict, Constants.PUBLISHERS_COLUMN_NAME, '')

    df = write_numeric_rank_column(df, authors_rank_avg_dict, Constants.AUTHORS_COLUMN_NAME, Constants.AVG)
    df = write_numeric_rank_column(df, authors_rank_count_dict, Constants.AUTHORS_COLUMN_NAME, Constants.COUNT)
    df = write_numeric_rank_column(df, authors_rank_dict, Constants.AUTHORS_COLUMN_NAME, '')

    df = drop_single_book_entries(df, authors_rank_dict)
    # df = drop_bestsellers_outliers(df)
    print("len: " + str(len(df.index)))
    # writing back to the original file
    df.to_excel(path_out, index=False)
    return SUCCESS


if __name__ == '__main__':
    run_process = input("Do you want to run analyze_categories? ")
    if run_process in ['y', 'Y']:
        categories_list = analyze_categories(Constants.XL_SCRAPED)
        print(f"Categories num: {len(categories_list)}\nCategories: {categories_list}")
    run_process = input("Do you want to run preprocess_scraped_xl? ")
    if run_process in ['y', 'Y']:
        preprocess_scraped_xl(Constants.XL_SCRAPED, Constants.XL_ROOT)
    print("Xl Preprocess Complete")
