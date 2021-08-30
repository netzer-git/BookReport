from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import df_preprocess


def run_model(df):
    # FIXME: do we need reshape?
    y = df[df_preprocess.BESTSELLERS_COLUMN_NAME].reshape(-1, 1)
    X = df.drop(columns=[df_preprocess.BESTSELLERS_COLUMN_NAME]).reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    regr = RandomForestRegressor(random_state=0)
    regr.fit(X_train, y_train)


if __name__ == '__main__':
    pass
