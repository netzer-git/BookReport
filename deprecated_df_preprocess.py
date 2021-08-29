import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

PUBLISHERS_COLUMN_NAME = 'clean-publisher'
AUTHORS_COLUMN_NAME = 'authors'
TITLE_COLUMN_NAME = 'title'
DESCRIPTION_COLUMN_NAME = 'description'
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


def preprocess_description(df):
    # FIXME
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    tfidf_wm = tfidfvectorizer.fit_transform(df[DESCRIPTION_COLUMN_NAME])
    # print(df[DESCRIPTION_COLUMN_NAME])
    print(tfidf_wm[0])
    tfidf_tokens = tfidfvectorizer.get_feature_names()
    df_tfidfvect = pd.DataFrame(data=tfidf_wm.toarray(), index=df.title, columns=tfidf_tokens)
    print(df_tfidfvect)
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
    # fantasy = preprocess_data(fantasy)

    fantasy = preprocess_description(fantasy)
    # print(fantasy)
