import os
import nltk
import spacy
import string
import operator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lispat.utils.logger import Logger
from lispat.factory.filtered_factory import FilteredFactory
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder


nltk.download('punkt')
nltk.download('stopwords')

logger = Logger("Noise Filter")


class Noise:

    def __init__(self, word, pdf, submission):

        """
        :param word: All data coming from word documents
        :param pdf: All data coming from pdf documents
        """
        self.word_array = None
        self.word_count = []
        self.txt_data = None
        self.word = word
        self.pdf = pdf
        self.nlp = spacy.load('en')
        self.max_word_count = 25
        self.gensim_docs = None
        self.keywords = None

        if submission == 'compare':
            self.pdf_path = "/usr/local/var/lispat/submission/"
        else:
            self.pdf_path = "/usr/local/var/lispat/pdf_data/"

        logger.getLogger().debug("Running a noise filter on directory: " +
                                 self.pdf_path)

        self.filtered_words = FilteredFactory()

    def get_doc(self):

        """
        :return: all data in the path to train.
        """
        # Static path to which all doc .txt files will be stored.
        # Could be changed in the future
        txt_data = ""
        try:
            for file in os.listdir(self.pdf_path):
                __file = open(self.pdf_path + file, 'rt')
                __text = __file.read()
                txt_data += __text
                self.txt_data = txt_data
        except RuntimeError as error:
            logger.getLogger().error("Word filter - ", error)

    def word_reduce(self):

        """
        :return: Filtered and none filtered text data
        """

        # split words into tokens.
        try:

            logger.getLogger().info("Mapping")
            tokens = word_tokenize(self.txt_data)

            logger.getLogger().debug("Words tokenized")
            tokens = [self.filtered_words.lower(w) for w in tokens]

            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in tokens]

            logger.getLogger().debug("Removed punctuation")
            words = [word for word in stripped if word.isalnum()]

            stop_words = set(stopwords.words('english'))
            words = [w for w in words if not w in stop_words]

            words = [w for w in words if not "ben" or "pope"]
            logger.getLogger().debug("Removed all stop words")
            logger.getLogger().debug(words[:100])

            logger.getLogger().debug("filtering any words containing integers")
            words = [w for w in words if not any(c.isdigit() for c in w)]
            logger.getLogger().debug(words[:100])

            logger.getLogger().debug("Removing any crazy long words from parsing")
            words = [w for w in words if not len(w) > 50]

            wnl = nltk.WordNetLemmatizer()
            words = [wnl.lemmatize(i) for i in words]

            port = nltk.PorterStemmer()
            words = [port.stem(i) for i in words]

            self.word_array = words
            return words

        except RuntimeError as error:
            logger.getLogger().error("Noise filter", error)

    def word_map(self):

        """
        :return: a word count on most commonly used words in the data set
        """
        logger.getLogger().info("Reducing")
        keywordList = []
        try:
            if len(self.word_array) == 0:
                raise ValueError("No words to reduce", self.word_array)
            word_count = {}
            for word in self.word_array:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

            logger.getLogger().debug("Word Count")
            keys = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
            for i in keys[:self.max_word_count]:
                print(i)
                keywordList.append(i[0])
            self.word_count = keys
            self.keywords = keywordList

        except ValueError as error:
            logger.getLogger().error("Noise filter", error)
        for i in self.keywords[:self.max_word_count]:
            print(i)

    def gensim(self):

        try:
            if self.txt_data is None:
                raise ValueError("No text data to preprocess", self.txt_data)

            for file in os.listdir(self.pdf_path):
                __file = open(self.pdf_path + file, 'rb')
                for i, line in enumerate(__file):
                    if i % 10000 == 0:
                        logger.getLogger().info("read {0} reviews".format(i))
                        # do some pre-processing and return list of words for
                        # each review text
                    yield gensim.utils.simple_preprocess(line)

            logger.getLogger().info("reading txt data...this may take a while")

        except ValueError as error:
            logger.getLogger().error("Noise filter", error)

    def get_keywords(self):
        return self.keywords

    def get_word_count(self):
        return self.word_count

    def get_word_array(self):
        return self.word_array
