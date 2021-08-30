import pandas as pd
from sklearn import preprocessing
import Constants


def normalize_column(df, feature_name):
    # max_value = df[feature_name].max()
    # min_value = df[feature_name].min()
    # df[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    df[feature_name] = (df[feature_name] - df[feature_name].mean()) / df[feature_name].std()
    return df


def normalize_data(df):
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
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled, columns=df.columns)
    df[Constants.BESTSELLERS_COLUMN_NAME] = target
    return df


def drop_textual_columns(df, columns_lst):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    return df.drop(columns=columns_lst, inplace=False)


if __name__ == '__main__':
    main_df = pd.read_excel('BookDepository/Full.xlsx')
    main_df = drop_textual_columns(main_df, Constants.NON_NUMERIC_COLUMNS)
    main_df = normalize_data(main_df)
    print(main_df)
    print(main_df.columns)
    main_df.to_excel(Constants.XL_PROCESSED, index=False)

