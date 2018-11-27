import nltk
import string
from lispat.utils.logger import Logger
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from lispat.base.constants import DESIRED_TERMS, DESIRED_PHRASE

logger = Logger("Filter Factory")


class FilteredFactory:

    def __init__(self):
        self.tokens = []
        self.stripped = None
        self.stop_word_var = None
        self.int_var = None
        self.punct_var = None
        self.long_words_var = None
        self.lemm_var = None
        self.stem_var = None

    def lower(self, w):
        self.tokens.append(w)
        return w.lower()

    def tokenize(self, val):
        tokens = [w.lower() for w in word_tokenize(val)]
        self.tokens = tokens
        return tokens

    def translate(self, val):
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in val]
        return stripped

    def punctuation(self, val):
        punct = [w for w in val if w.isalnum()]
        return punct

    def remove_names(self, val):
        remove_list = ['pope', 'benjamin', 'ben']
        words = [w for w in val if w not in remove_list]
        return words

    def stop_words(self, val):
        logger.getLogger().debug("Removing stop words")
        stop_words = set(stopwords.words('english'))
        words = [w for w in val if w not in stop_words]
        return words

    def integers(self, val):
        words = [w for w in val if not any(c.isdigit() for c in w)]
        return words

    def long_words(self, val):
        words = [w for w in val if not len(w) > 50]
        return words

    def lemmatize(self, val):
        wnl = nltk.WordNetLemmatizer()
        lemmed = [wnl.lemmatize(i) for i in val]
        return lemmed

    def stemmer(self, val):
        port = nltk.PorterStemmer()
        words = [port.stem(i) for i in val]
        return words

    def get_desired_terms(self, val):
        for w in val:
            if w in DESIRED_TERMS:
                return val
        return []

    def get_desired_phrase(self, val):
        for w in val:
            if w in DESIRED_PHRASE:
                return val
        return []