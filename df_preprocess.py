import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

PUBLISHERS_COLUMN_NAME = 'clean-publisher'
AUTHORS_COLUMN_NAME = 'authors'
TITLE_COLUMN_NAME = 'title'
BESTSELLERS_COLUMN_NAME = 'bestsellers-rank'
STOP_WORDS = set(stopwords.words('english'))
BESTSELLERS_SCORE = 5000


def preprocess_publishers(df):
    le = preprocessing.LabelEncoder()
    publishers_encoded = le.fit_transform(df[PUBLISHERS_COLUMN_NAME])
    df[PUBLISHERS_COLUMN_NAME] = publishers_encoded
    return df


def preprocess_authors(df):
    le = preprocessing.LabelEncoder()
    publishers_encoded = le.fit_transform(df[AUTHORS_COLUMN_NAME])
    df[AUTHORS_COLUMN_NAME] = publishers_encoded
    return df


def preprocess_single_description(description):
    tokens = word_tokenize(description)
    tokens = [w for w in tokens if w not in STOP_WORDS]
    # FIXME vectorize the description - do we need the same vector shape?
    return " ".join(tokens)


def preprocess_description(df):
    # FIXME
    text = [preprocess_single_description(d) for d in df.description]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(text)
    vector = vectorizer.transform([text[0]])
    df.description = [vectorizer.transform([t]) for t in df.description]
    return df


def preprocess_sindle_title(title, bestsellers_title_words):
    bestsellers_similarity = 0
    for word in title.split():
        if word in bestsellers_title_words:
            # bestsellers_similarity += 1
            bestsellers_similarity = bestsellers_title_words[word]
    return bestsellers_similarity  # / len(title.split())


def preprocess_title(df):
    bestsellers_title_words = []
    for i in range(len(df[TITLE_COLUMN_NAME])):
        if df[BESTSELLERS_COLUMN_NAME][i] < BESTSELLERS_SCORE:
            bestsellers_title_words += [w for w in df[TITLE_COLUMN_NAME][i].split() if w not in STOP_WORDS]
    bestsellers_title_words = set(bestsellers_title_words)
    new_title_column = []
    for i in range(len(df[TITLE_COLUMN_NAME])):
        title = df[TITLE_COLUMN_NAME][i]
        new_title_column.append(preprocess_sindle_title(title, bestsellers_title_words))

    print(bestsellers_title_words)
    df[TITLE_COLUMN_NAME] = new_title_column
    return df


def preprocess_title_word_score(df):
    bestsellers_title_words = dict()
    for i in range(len(df[TITLE_COLUMN_NAME])):
        if df[BESTSELLERS_COLUMN_NAME][i] < BESTSELLERS_SCORE:
            for w in df[TITLE_COLUMN_NAME][i].split():
                if w not in STOP_WORDS and w in bestsellers_title_words:
                    bestsellers_title_words[w] += 1
                elif w not in STOP_WORDS:
                    bestsellers_title_words[w] = 1
    bestsellers_title_words_sum = sum(bestsellers_title_words.values())
    for key in bestsellers_title_words:
        bestsellers_title_words[key] = bestsellers_title_words[key] / bestsellers_title_words_sum
    new_title_column = []
    for i in range(len(df[TITLE_COLUMN_NAME])):
        title = df[TITLE_COLUMN_NAME][i]
        new_title_column.append(preprocess_sindle_title(title, bestsellers_title_words))

    print(bestsellers_title_words)
    df[TITLE_COLUMN_NAME] = new_title_column
    return df


def preprocess_data(df):
    # TODO
    df = preprocess_title_word_score(df)
    df = preprocess_authors(df)
    df = preprocess_publishers(df)
    return df


if __name__ == '__main__':
    # TEST section
    fantasy = pd.read_excel('Bookdepository/Bookdepository_Crawler_fantasy.xlsx')
    fantasy = preprocess_data(fantasy)
    print(fantasy)
