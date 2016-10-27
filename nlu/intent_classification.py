import os
import sys
import inspect
import ujson
import glob
import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from utilities import function_timer, exception


def preprocess(text):
    """
    Convert text into unicoded text
    """
    return text.strip("\n").decode("utf-8")


def get_intent_map(imap_fpath):
    """
    Loads intent map from disk
     as a json file
    """
    with open(imap_fpath, 'r') as infile:
        intent_map = ujson.load(infile)
    return intent_map


def get_data(intent_path, intent_name):
    """
    Reads training data from the disk
    for intent classification, retuns
    as a set of tuples, one file at a
    time
    """
    x = map(preprocess, open(intent_path, "r").readlines())
    y = [intent_name]*len(x)
    return zip(x, y)


def get_labeled_data(basepath):
    """
    Iterates over all intent training
    files and retrieves the data as
    (x,y) tuples
    """
    all_samples = []
    intent_data_path = os.path.join(basepath, u"training", u"*.txt")
    for intent_path in glob.glob(intent_data_path):
        intent_name = intent_path.split("/")[-1].split(".")[0]
        all_samples.extend(get_data(intent_path, intent_name))
    return all_samples


def vectorization_x(texts):
    """
    Takes some text and converts
    it into numpy arrays using
    n-gram count vectorizer
    """
    vectorizer1 = CountVectorizer(min_df=1)
    vectorizer2 = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    vectorizer3 = CountVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', min_df=1)
    vectorizer4 = CountVectorizer(analyzer='char_wb', ngram_range=(2, 2), min_df=1)
    vectorizer5 = CountVectorizer(analyzer='char_wb', ngram_range=(2, 3), min_df=1)
    vectorizer6 = CountVectorizer(analyzer='char_wb', ngram_range=(2, 4), min_df=1)
    vectorizer7 = CountVectorizer(analyzer='char_wb', ngram_range=(2, 5), min_df=1)
    vectorizer8 = TfidfVectorizer(min_df=1)
    vectorizer9 = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    vectorizer10 = TfidfVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', min_df=1)


    vectorizer = vectorizer5.fit(texts)
    _ = joblib.dump(vectorizer, u"data/intent/vectorizer", compress=9)
    vectors = vectorizer.transform(texts)
    return vectors.toarray()


def vectorization_y(labels, intent_map):
    """
    Vectorizes y labels using the
    intent map
    """
    vectors = np.zeros(len(labels))
    for i, lab in enumerate(labels):
        vectors[i] = intent_map[lab]
    return vectors


def train(model_name, basepath):
    """
    Trains a linear model using
    LogReg and saves to the disk
    """
    clf_fpath = os.path.join(basepath, model_name, model_name+u".clf")
    imap_fpath = os.path.join(basepath, model_name, u"intent_map.json")

    intent_map = get_intent_map(imap_fpath)
    data = get_labeled_data(basepath)
    targets = map(str, sorted(intent_map.values()))

    all_x = map(lambda t: t[0], data)
    all_y = map(lambda t: t[1], data)

    x_vectors = vectorization_x(all_x)
    y_vectors = vectorization_y(all_y, intent_map)

    clf = LogisticRegression(class_weight=u"balanced", C=0.5)

    x_train, x_test, y_train, y_test = train_test_split(x_vectors, y_vectors, test_size=0.0, random_state=42)
    clf_model = clf.fit(x_train, y_train)
    predictions = clf_model.predict(x_train)
    cr = classification_report(y_train, predictions, target_names=targets)
    _ = joblib.dump(clf_model, clf_fpath, compress=9)
    return cr


def model_predict(text, clf_fpath, imap_path, vec_path, prob=False):
    """
    A functions that takes some takes and
    a trained intent classifier with its intent
    map and returns predicted intent
    """
    vectorizer = joblib.load(vec_path)
    text_vector = vectorizer.transform([text])

    clf_model = joblib.load(clf_fpath)
    text_pred = clf_model.predict(text_vector)
    text_prob_dist = None
    im = get_intent_map(imap_path)
    if prob:
        text_prob_dist = clf_model.predict_proba(text_vector).tolist()[0]
    return im.keys()[im.values().index(int(text_pred[0]))], text_prob_dist


def main():

    print train(u"intent_classifier", u"data/intent")

    print model_predict(u"how do you work?",
                        u"data/intent/intent_classifier/intent_classifier.clf",
                        u"data/intent/intent_classifier/intent_map.json", u"data/intent/vectorizer")

if __name__ == u"__main__":
    main()





