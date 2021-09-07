import Constants
import pandas as pd

if __name__ == '__main__':
    df_array = []
    for category in Constants.CATEGORY_URL:
        file_name = Constants.OUTPUT_FILE_NAME + '_' + category.split('/')[3] + ".xlsx"
        df_array.append(pd.read_excel(file_name))

    result = pd.concat(df_array)
    result.to_excel(Constants.OUTPUT_FILE_NAME + '.xlsx')
