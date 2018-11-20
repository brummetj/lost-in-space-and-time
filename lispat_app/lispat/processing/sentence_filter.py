import os
import nltk
import spacy
from spacy.lang.en.examples import sentences
from lispat.utils.logger import Logger
from lispat.processing.noise_filter import NoiseFilter

logger=Logger("sentence_filter")
nlp = spacy.load('en_core_web_sm')

class SentenceFilter:

    def __init__(self, keywordList):

        self.txt_data = None
        #self.pdf = pdf
        self.pdf_path = "/usr/local/var/lispat/pdf_data/"
        self.keywords = keywordList

    def filter_sentences(self, keywords):
        txt_data = ''
        try:
            for file in os.listdir(self.pdf_path):
                __file = open(self.pdf_path + file, 'rt')
                __text = __file.read()
                txt_data += __text
                self.txt_data = txt_data
                txt_data = txt_data[:50000]
                doc = nlp(txt_data)
                for sent in doc.sents:
                    print(sent.text)
                input("Press enter to continue")
        except RuntimeError as error:
            logger.getLogger().error("Sentence filter - ", error)
        doc = nlp(txt_data)
