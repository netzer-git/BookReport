import Constants
import pandas as pd

if __name__ == '__main__':
    df_array = []
    # take all of the scraping slices to one array
    for category in Constants.CATEGORY_URL:
        file_name = Constants.OUTPUT_FILE_NAME + '_' + category.split('/')[3] + ".xlsx"
        df_array.append(pd.read_excel(file_name))

    # merge the slices to one df
    result = pd.concat(df_array)
    # write the df to excel
    result.to_excel(Constants.OUTPUT_FILE_NAME + '.xlsx')
