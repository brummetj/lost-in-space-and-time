import os
import nltk
from lispat.utils.logger import Logger
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
logger = Logger("Noise Filter")


class NoiseFilter:

    def __init__(self, word, pdf):
        self.word = word
        self.pdf = pdf
        self.pdf_path = "/usr/local/var/lispat/pdf_data/"

    def word_filter(self):

        # Static path to which all doc .txt files will be stored.
        # Could be changed in the future
        txt_data = ''
        try:
            for file in os.listdir(self.pdf_path):
                __file = open(self.pdf_path + file, 'rt')
                __text = __file.read()
                txt_data += __text
        except RuntimeError as error:
            logger.getLogger().error("Word filter - ", error)

        # split words into tokens.
        try:
            tokens = word_tokenize(txt_data)
            logger.getLogger().debug("Words tokenized")

            tokens = [w.lower() for w in tokens]
            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in tokens]

            logger.getLogger().debug("Removed punctuation")

            words = [word for word in stripped if word.isalnum()]

            stop_words = set(stopwords.words('english'))
            words = [w for w in words if not w in stop_words]

            logger.getLogger().debug("Removed all stop words")
            logger.getLogger().debug(words[:100])
        except RuntimeError as error:
            logger.getLogger().error("Noise filter", error)
