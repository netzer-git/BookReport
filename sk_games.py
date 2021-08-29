from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

le = preprocessing.LabelEncoder()

fantasy = pd.read_excel('Bookdepository/Bookdepository_Crawler_fantasy.xlsx')

print(fantasy)
print(fantasy.categories)
print('*** ****** ****** ****** ***')

publishers_encoded = le.fit_transform(fantasy['clean-publisher'])
print(publishers_encoded[:10])  # its working, now we need to make this part of the df
print('*** ****** ****** ****** ***')
fantasy['clean-publisher'] = publishers_encoded
print(fantasy['clean-publisher'])
print('*** ****** ****** ****** ***')
print(fantasy.title[0])
print('*** ****** ****** ****** ***')
#### START - Word Count
text1 = [fantasy.title[0]]  # we need to put the string in []=array
text2 = [fantasy.title[1]]
vectorizer = CountVectorizer()
vectorizer.fit(text1)
print(vectorizer.vocabulary_)
vector = vectorizer.transform(text1)
print(vector.shape)
print(type(vector))
print(vector.toarray())
#### END
print('*** ****** ****** ****** ***')
