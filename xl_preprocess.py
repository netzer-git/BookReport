from openpyxl import Workbook, load_workbook
import pandas as pd

XL_ROOT = 'BookDepository/Fantasy_Bookdepository_Crawler.xlsx'
XL_AUTHORS_OUTPUT = 'Best_Authors.xlsx'
XL_PUBLISHERS_OUTPUT = 'Best_Publishers.xlsx'
AUTHORS_COLUMN_NAME = 'authors'
PUBLISHERS_COLUMN_NAME = "clean-publisher"
CATEGORIES_COLUMN_NAME = "categories"
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
BEST_AUTHOR_RANK = 30_000
BOOK_NUM_IN_CATEGORY = 2_000


def split_category_field(category_str):
    category_lst = category_str.split(',')
    for i in range(len(category_lst)):
        category_lst[i] = category_lst[i].replace('\"', '').replace('\'', '').replace('[', '').replace(']', '')
        category_lst[i] = "".join(category_lst[i].split(' '))

    return category_lst


def analyze_categories(path):
    xls = pd.read_excel(path)
    categories_dict = {}
    for i in range(len(xls[CATEGORIES_COLUMN_NAME])):
        category_lst = split_category_field(xls[CATEGORIES_COLUMN_NAME][i])
        rank = xls[BESTSELLERS_COLUMN_NAME][i]
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


def write_binary_categories_columns(categories_list, path):
    xls = pd.read_excel(path)
    new_columns = {c: [] for c in categories_list}
    for i in range(len(xls['crawl_id'])):
        entry_categories = split_category_field(xls[CATEGORIES_COLUMN_NAME][i])
        for c in categories_list:
            new_columns[c].append(int(c in entry_categories))

    for c in new_columns:
        # xls.insert(c, new_columns[c])
        xls[c] = new_columns[c]

    xls.to_excel(XL_ROOT, index=False)


def get_best_list(path, column_name):
    xls = pd.read_excel(path)
    name_dict = {}
    for i in range(len(xls[column_name])):
        name = xls[column_name][i]
        rank = xls[BESTSELLERS_COLUMN_NAME][i]

        if name is not None and name in name_dict:
            name_dict[name][0] += rank
            name_dict[name][1] += 1
        elif name is not None:
            name_dict[name] = [0.0, 0.0]
            name_dict[name][0] += rank
            name_dict[name][1] += 1

    print(name_dict)
    # best_list = []
    # for key in name_dict:
    #     normalized_author_rank = name_dict[key][0] / name_dict[key][1]
    #
    #     if (normalized_author_rank < BEST_AUTHOR_RANK and name_dict[key][1] > 1) or name_dict[key][1] > 50:
    #         best_list.append(key)
    #
    # return best_list
    for key in name_dict:
        name_dict[key].append(name_dict[key][0] / name_dict[key][1])
    return name_dict


def write_list_to_xl(path, best_dict):
    labels = ['best', 'avg-rank']

    wb = Workbook()
    wb['Sheet'].title = path
    sheet1 = wb.active

    sheet1['A' + str(1)].value = labels[0]
    sheet1['B' + str(1)].value = labels[1]

    i = 1
    for key in best_dict:
        i += 1
        sheet1['A' + str(i)].value = str(key)
        sheet1['B' + str(i)].value = str(best_dict[key][2])

    wb.save(path)


if __name__ == '__main__':
    lst = get_best_list(XL_ROOT, AUTHORS_COLUMN_NAME)
    print(lst)
    write_list_to_xl(XL_AUTHORS_OUTPUT, lst)
    # categories = analyze_categories(XL_ROOT)
    # print(categories)
    # write_binary_categories_columns(categories, XL_ROOT)

