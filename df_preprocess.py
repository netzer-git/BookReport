import pandas as pd
import numpy as np
from sklearn import preprocessing
import Constants


def normalize_column(df, feature_name):
    """
    normalize one column with mean-value
    :param df: the full df
    :param feature_name: column name
    :return: the updated df
    """
    # max_value = df[feature_name].max()
    # min_value = df[feature_name].min()
    # df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    df[feature_name] = (df[feature_name] - df[feature_name].mean()) / df[feature_name].std()
    return df


def normalize_data(df):
    """
    normalize all of the df columns, one by one, using preprocessing Scaler
    :param df: the full df
    :return: the updated df
    """
    # df = normalize_column(df, Constants.PRICE_COLUMN_NAME)
    # df = normalize_column(df, Constants.RATING_AVG_COLUMN_NAME)
    # df = normalize_column(df, Constants.RATING_COUNT_COLUMN_NAME)
    #
    # df = normalize_column(df, Constants.NUMERIC_AUTHOR_RANK_COLUMN_NAME)
    # df = normalize_column(df, Constants.NUMERIC_PUBLISHER_RANK_COLUMN_NAME)

    target = df[Constants.BESTSELLERS_COLUMN_NAME]  # save the target column un-normalize
    df.drop(Constants.BESTSELLERS_COLUMN_NAME, axis=1, inplace=True)
    x = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    # scaler = preprocessing.StandardScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    # x_scaled = scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled, columns=df.columns)
    df[Constants.BESTSELLERS_COLUMN_NAME] = target
    return df


def drop_textual_columns(df, columns_lst):
    """
    drops from the df list of columns
    :param df: the full df
    :param columns_lst: list of column names
    :return: the updated df
    """
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    return df.drop(columns=columns_lst, inplace=False)


if __name__ == '__main__':
    main_df = pd.read_excel(Constants.XL_ROOT)
    main_df = drop_textual_columns(main_df, Constants.NON_NUMERIC_COLUMNS)

    main_df.replace(to_replace='None', value=np.nan, inplace=True)
    main_df.dropna(inplace=True)

    main_df = normalize_data(main_df)
    print(main_df)
    print(main_df.columns)
    main_df.to_excel(Constants.XL_PROCESSED, index=False)
