from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
import df_preprocess, Constants


def run_model(df):
    y = df[Constants.BESTSELLERS_COLUMN_NAME]
    X = df.drop(columns=[Constants.BESTSELLERS_COLUMN_NAME])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    rfg = RandomForestRegressor(random_state=0)
    rfg.fit(X_train, y_train)
    y_pred = rfg.predict(X_test)

    # Evaluation and Score
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f'mae_r: {mae}\nmse_r: {mse}')

    test_score = rfg.score(X_test, y_test)
    train_score = rfg.score(X_train, y_train)
    print(f'test_score: {test_score}\ntrain_score: {train_score}')

    print('\nCross-validation:')
    from sklearn.model_selection import cross_val_score, cross_validate
    scores = cross_val_score(rfg, X, y, cv=5)
    print(f'Cross-validation scores:{scores}')
    print(f'Average cross-validation score: {scores.mean()}')
    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))


if __name__ == '__main__':
    main_df = pd.read_excel(Constants.XL_PROCESSED)
    run_model(main_df)
