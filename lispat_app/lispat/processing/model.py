import gensim
from lispat.utils.logger import Logger
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

logger = Logger("Modeling")


class NLPModel:
    def __init__(self, txt):
        txt = " ".join(txt)
        self.nlp = spacy.load('en')
        self.nlp(txt[:100000])
