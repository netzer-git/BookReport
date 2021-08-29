from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('Bookdepository/Fantasy.xlsx')
    X = [df['rating-avg'], df['rating-count'], df['price']]
    # X = [df['rating-count']]
    y = [df['bestsellers-rank']]
    X = pd.concat(X, axis=1, keys=['rating-avg', 'rating-count', 'price'])
    # X = pd.concat(X, axis=1, keys=['rating-count'])
    y = pd.concat(y, axis=1, keys=['bestsellers-rank'])

    print(X)
    print(y)

    # imp = SimpleImputer(missing_values=None, strategy='mean')
    # imp.fit_transform(X)
    # imp.fit_transform(y)

    model = LinearRegression().fit(X, y)
    r_sq = model.score(X, y)
    print('coefficient of determination:', r_sq)
    print('intercept:', model.intercept_)
    print('slope:', model.coef_)

    d = pd.DataFrame({'rating_count': [123],
                      'rating-avg': [4.4],
                      'price': [50]})
    print("prediction: " + str(model.predict(d)))