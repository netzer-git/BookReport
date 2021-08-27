from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

clf = RandomForestClassifier(random_state=0)
X = [[1, 2, 3],  # 2 samples, 3 features
     [11, 12, 13]]
y = [0, 1]  # classes of each sample
md = clf.fit(X, y)
# print(clf.predict([[4, 5, 6], [14, 15, 16]]))

X = [[0, 15], [1, -10]]
s = StandardScaler().fit(X).transform(X)
print(s)
