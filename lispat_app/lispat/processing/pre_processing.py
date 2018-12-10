import os
import re
import sys
import nltk
import spacy
import gensim
import operator
from lispat.utils.logger import Logger
from lispat.factory.filtered_factory import FilteredFactory
from lispat.utils.colors import bcolors
import matplotlib.pyplot as plt
import numpy as np
logger = Logger("Noise Filter")


class Preproccessing:

    def __init__(self, word=None, pdf=None):

        """
        :param word: All data coming from word documents
        :param pdf: All data coming from pdf documents
        """
        self.pdf = pdf
        self.word = word
        self.pdf_path = ""
        self.txt_data = ""

        self.word_array = None
        self.word_count_array = None
        self.pre_processed_string = None

        self.nlp = spacy.load('en')
        self.nlp_filtered = spacy.load('en')

        self.filter = FilteredFactory()

        logger.getLogger().info("Noise filter initialized")

    def get_docs_dir(self, submission):

        """
        :return: all data in the path to train.
        """
        # Static path to which all doc .txt files will be stored.
        # Could be changed in the future
        logger.getLogger().info("Getting files for filter")
        if submission['--compare']:
            path = "/usr/local/var/lispat/submission/"
            path_array = [path]
        else:
            path = "/usr/local/var/lispat/pdf_data/"
            path_docx = "/usr/local/var/lispat/docx_data/"
            # not used but we need to use all of the data.
            path_csv = "/usr/local/var/lispat/csv_data/"
            # Only docx and pdf are used right now.
            path_array = [path, path_docx]

        try:
            txt_data = ""
            for path in path_array:
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

    def get_doc(self):
        """
        Gets the parsed text data, from either a pdf or docx
        :return: a doc of text data.
        """

        if self.word:
            text = open(self.word[0][0], 'rt')
            self.txt_data = text.read()

        if self.pdf:
            text = open(self.pdf[0][0], 'rt')
            self.txt_data = text.read()

    def ret_doc(self):
        """
        Gets the parsed text data, from either a pdf or docx
        :return: a doc of text data.
        """

        if self.word:
            text = open(self.word[0][0], 'rt')
            self.txt_data = text.read()

        if self.pdf:
            text = open(self.pdf[0][0], 'rt')
            self.txt_data = text.read()

        return self.txt_data

    def filter_nlp(self):

        """
        :return: Filtered nlp data spacy object.
        """

        # split words into tokens.
        try:
            if self.pdf_path:
                logger.getLogger().debug("Running pre-processing on directory:"
                                         " " + self.pdf_path)

            if self.pdf:
                logger.getLogger().debug("Running pre-processing on file: "
                                         + self.pdf[0][0])

            if self.word:
                logger.getLogger().debug("Running pre-processing on file: "
                                         + self.word[0][0])

            tokens = self.filter.tokenize(self.txt_data)
            stripped = self.filter.translate(tokens)
            words = self.filter.punctuation(stripped)
            words = self.filter.stop_words(words)
            words = self.filter.remove_names(words)
            words = self.filter.integers(words)
            words = self.filter.long_words(words)
            words = self.filter.lemmatize(words)
            words = self.filter.stemmer(words)

            # Lets turn filtered words back to a spacy doc
            # for better data handling.
            txt = " ".join(words)
            txt_len = len(txt)
            self.nlp_filtered.max_length = txt_len + 1
            nlp_filtered = self.nlp_filtered(txt)

            self.word_array = words
            self.pre_processed_string = txt
            self.nlp_filtered = nlp_filtered

        except RuntimeError as error:
            logger.getLogger().error("Noise filter", error)

    def get_sentences(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        raw_sentences = tokenizer.tokenize(self.txt_data)
        return raw_sentences

    def get_sent_tokens(self, raw):
            clean = re.sub("[^a-zA-Z]", " ", raw).lower()
            words = clean.split()
            return words

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

            keys = sorted(word_count.items(), key=operator.itemgetter(1),
                          reverse=True)
            print(bcolors.BOLD + "Word Count" + bcolors.ENDC)
            for i in keys[:20]:
                print(bcolors.HEADER + str(i) + bcolors.ENDC)
            self.word_count_array = keys

            n, bins, patches = plt.hist(x=keys, bins='auto', color='#0504aa',
                                        alpha=0.7, rwidth=0.85)
            # plt.grid(axis='y', alpha=0.75)
            # plt.xlabel('Value')
            # plt.ylabel('Frequency')
            # plt.title('Top Word Frequency')
            # max_freq = n.max()
            # plt.ylim(ymax=np.ceil(max_freq / 10) * 10 if max_freq %
            # 10 else max_freq + 10)
            # plt.show()

        except ValueError as error:
            logger.getLogger().error(bcolors.FAIL + "Pylot error, please check"
                                     " stack trace" + bcolors.ENDC)
            sys.exit(1)

    def get_word_count(self):
        return self.word_count

    def get_word_array(self):
        return self.word_array
