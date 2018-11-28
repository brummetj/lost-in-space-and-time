import os
import sys
import spacy
import pickle
import shutil
import numpy as np
import pandas as pd
import scattertext as st
from textblob import TextBlob
from lispat.utils.logger import Logger
from lispat.factory.filtered_factory import FilteredFactory

logger = Logger("Modeling")


class NLPModel:
    def __init__(self):
        self.sent_list = None
        self.nlp = spacy.load('en_core_web_sm')
        self.filter = FilteredFactory()

    def data_frame(self, path):
        '''
        This function takes the test.csv file and turns it into a
        usable dataframe.
        :return:
        '''
        try:
            print(path)
            logger.getLogger().info("Running information on text dataframe.")
            # A word count on each sentence. not sure if helpful...

            train = pd.read_csv(path, names=["ID", "sentence"])
            train['word_count'] = (train['sentence'].apply
                                   (lambda x: len(str(x).split(" "))))
            train['filtered'] = (train['sentence'].apply
                                 (lambda x: self.filter.tokenize(x)))

            train['desired_phrase'] = (train['filtered'].apply(lambda x:
                                       self.filter.get_desired_phrase(x)))
            train['desired_phrase'] = (train['desired_phrase'].apply(lambda x:
                                       self.filter.punctuation(x)))
            train['desired_phrase'] = (train['desired_phrase'].apply(lambda x:
                                       self.filter.stemmer(x)))
            train_pe = train[train['desired_phrase'].map(lambda x: len(x)) > 0]

            train['desired_term'] = (train['filtered'].apply(lambda x:
                                     self.filter.get_desired_terms(x)))
            train_te = train[train['desired_term'].map(lambda x: len(x)) > 0]

            # train.drop(columns=['ID'])
            # train.reset_index(drop=True)
            # train.set_index(np.arange(len(train.index)))
            # train.reindex()

            frames = [train_pe, train_te]
            df = pd.concat(frames)
            df.drop('ID', axis=1, inplace=True)

            # df = df.apply(lambda x: " ".join([str(i) for i in x]))
            df.reset_index(drop=True)
            df.reindex()
            print(df)

            headers = ["desired_term", "Desired_phrase",
                       "sentences", "word_count"]

            df.to_csv('/usr/local/var/lispat/csv_data/output.csv',
                      encoding='utf-8', columns=headers)

            # Getting a ngram of size 6... just with the second row...
            logger.getLogger().debug("Showing the ngram for the 30th"
                                     "row in the DF")
            for w in TextBlob(train['sentence'][30]).ngrams(6):
                print(w)

            # For spelling
            # train['sentence'][2].apply(lambda x: str(TextBlob(x).correct()))
            # tf1 = (train['sentence'][1:3]).apply(lambda x: pd.value_counts
            #       (x.split(" "))).sum(axis=0).reset_index()
            # tf1.columns = ['words', 'tf']

        except RuntimeError:
            logger.getLogger().debug("Error with Dataframe calculation")
            sys.exit(1)

    def save_trained(self, word_array):
        '''
        :param word_array: an array of words that will be saved
         as a object for now..
        :return: None
        '''
        try:

            logger.getLogger().info("Saving the trained model")
            if os.path.isdir("/usr/local/var/lispat/objects"):
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')
            else:
                os.makedirs("/usr/local/var/lispat/objects/")
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')

            obj = word_array

            pickle.dump(obj, obj_file)
            logger.getLogger().debug("Object successfully saved")
        except RuntimeError as e:
            logger.getLogger().debug("Run time error saving the object")
            sys.exit(1)

    def compare_doc_similarity(self, path):
        '''
        :param path: path to submission file.
        :return: None

        TODO: Clean this up and make the comparison give better feedback.
        Use Gensim instead of spaCy..
        '''
        try:
            logger.getLogger().info("Comparing document similarity")
            data_path = "/usr/local/var/lispat/pdf_data/"
            txt1 = ""
            try:
                for file in os.listdir(data_path):
                    __file = open(data_path + file, 'rt')
                    __text = __file.read()
                    txt1 += __text
            except RuntimeError as error:
                logger.getLogger().error("Word filter - ", error)

            # This is for using the saved object...
            # logger.getLogger().info("Getting object from disk")
            # obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'rb')

            head, tail = os.path.split(path)
            file = os.path.splitext(tail)[0]
            submitted = open("/usr/local/var/lispat/submission/" + file +
                             ".txt", 'rt')

            # obj = pickle.load(obj_file)
            # txt = " ".join(obj)
            txt2 = submitted.read()

            txt1_len = len(txt1)

            self.nlp.max_length = txt1_len + 1
            doc1 = self.nlp(txt1)
            doc2 = self.nlp(txt2)

            similarity = doc2.similarity(doc1)
            logger.getLogger().debug("Document Similarity is " +
                                     str(similarity))
            shutil.rmtree("/usr/local/var/lispat/submission")

        except RuntimeError as error:
            logger.getLogger().error("Error with comparing the two"
                                     "documents with spaCy")
            shutil.rmtree("/usr/local/var/lispat/submission")
            sys.exit(1)

    def build_sents(self, sentences):
        nlp_array = []
        logger.getLogger().info("Building sentence Array")
        for i, sent in enumerate(sentences):
            nlp_array.append((i, sent))
        return nlp_array

    def print_full(self, x):
        pd.set_option('display.max_rows', len(x))
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 2000)
        pd.set_option('display.float_format', '{:20,.2f}'.format)
        pd.set_option('display.max_colwidth', -1)
        print(x)
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
        pd.reset_option('display.float_format')
        pd.reset_option('display.max_colwidth')
