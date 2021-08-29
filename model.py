from sklearn.ensemble import RandomForestClassifier
import pandas as pd

if __name__ == '__main__':
    from sklearn.datasets import make_classification

    X, y = make_classification(n_samples=1000, n_features=4,
                               n_informative=2, n_redundant=0,
                               random_state=0, shuffle=False)

    clf = RandomForestClassifier(max_depth=100, random_state=0)
    clf.fit(X, y)
    print(clf.predict([[2, 1, 1, 115]]))