from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Constants


def run_model(df):
    """
    main model run
    :param df: the main analyzed df, with the target column
    """
    df.dropna(inplace=True)

    y = df[Constants.BESTSELLERS_COLUMN_NAME]
    X = df.drop(columns=[Constants.BESTSELLERS_COLUMN_NAME])#.drop(columns=['authors-rank'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    rfg = RandomForestRegressor(random_state=0)
    # rfg = LinearRegression()
    # rfg = MLPRegressor()
    # rfg = AdaBoostRegressor()

    rfg.fit(X_train, y_train)
    y_pred = rfg.predict(X_test)

    # Evaluation and Score
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f'mae_r: {mae}\nmse_r: {mse}\n')

    test_score = rfg.score(X_test, y_test)  # R^2
    train_score = rfg.score(X_train, y_train)
    print(f'test_score: {test_score}\ntrain_score: {train_score}')

    # SECTION 2
    importances = rfg.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rfg.estimators_], axis=0)
    forest_importances = pd.Series(importances, index=[i for i in X.columns])

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.show()

    # SECTION 3
    from sklearn.inspection import permutation_importance
    result = permutation_importance(rfg, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2)
    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()

    # SECTION 4
    # print('\nCross-validation:')
    # from sklearn.model_selection import cross_val_score, cross_validate
    # scores = cross_val_score(rfg, X, y, cv=5)
    # print(f'Cross-validation scores:{scores}')
    # print(f'Average cross-validation score: {scores.mean()}')
    # print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))


if __name__ == '__main__':
    main_df = pd.read_excel(Constants.XL_PROCESSED)
    run_model(main_df)
