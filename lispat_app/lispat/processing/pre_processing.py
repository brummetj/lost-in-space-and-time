import os, sys , operator , spacy , gensim
from lispat.utils.logger import Logger
from lispat.factory.filtered_factory import FilteredFactory

logger = Logger("Noise Filter")

class Preproccessing:

    def __init__(self, word, pdf):

        """
        :param word: All data coming from word documents
        :param pdf: All data coming from pdf documents
        """
        self.word_array = None
        self.word_count_array = None
        self.nlp_filtered = spacy.load('en')
        self.txt_data = ""
        self.word = word
        self.pdf = pdf
        self.nlp = spacy.load('en')
        self.pdf_path = ""
        self.filter = FilteredFactory()

        logger.getLogger().info("Noise filter initialized")

    def get_doc(self, submission):

        """
        :return: all data in the path to train.
        """
        # Static path to which all doc .txt files will be stored. Could be changed in the future
        path = ""
        logger.getLogger().info("Getting files for filter")
        if submission['--compare']:
            path = "/usr/local/var/lispat/submission/"
        else:
            path = "/usr/local/var/lispat/pdf_data/"
            path_csv = "/usr/local/var/lispat/csv_data/" #not used but we need to use all of the data.

        try:
            txt_data = ""
            for file in os.listdir(path):
                __file = open(path + file, 'rt')
                __text = __file.read()
                self.txt_data += __text

            txt_len = len(self.txt_data)
            self.nlp.max_length = txt_len + 1
            self.nlp = self.nlp(self.txt_data)
            self.pdf_path = path
        except RuntimeError as error:
            logger.getLogger().error("Error getting data to filter - ", error)
            sys.exit(1)

    def filter_nlp(self):

        """
        :return: Filtered nlp data spacy object.
        """

        # split words into tokens.
        try:
            logger.getLogger().debug("Running a noise filter on directory: " + self.pdf_path)

            tokens = self.filter.tokenize(self.txt_data)
            stripped = self.filter.translate(tokens)
            words = self.filter.punctuation(stripped)
            words = self.filter.stop_words(words)
            words = self.filter.remove_names(words)
            words = self.filter.integers(words)
            words = self.filter.long_words(words)
            words = self.filter.lemmatize(words)
            words = self.filter.stemmer(words)

            #Lets turn filtered words back to a spacy doc for better data handeling.
            txt =  " ".join(words)
            txt_len = len(txt)
            self.nlp_filtered.max_length = txt_len + 1
            nlp_filtered = self.nlp_filtered(txt)

            self.word_array = words
            self.nlp_filtered = nlp_filtered

        except RuntimeError as error:
            logger.getLogger().error("Noise filter", error)

    def word_count(self):

        """
        :return: a word count on most commonly used words in the data set
        """
        logger.getLogger().info("Getting a word count on filtered words")
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
            for i in keys[:20]:
                print(i)
            self.word_count_array = keys

        except ValueError as error:
            logger.getLogger().error("Noise filter", error)


    def get_word_count(self):
        return self.word_count

    def get_word_array(self):
        return self.word_array



