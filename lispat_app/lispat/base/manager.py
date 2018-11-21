import os
import sys
from lispat.utils.logger import Logger
from lispat.factory.document_factory import DocumentFactory
from lispat.processing.noise_filter import Noise
from lispat.processing.model import NLPModel
import spacy
import pickle
import shutil
logger = Logger("CommandManager")


class CommandManager:
    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """

    def __init__(self):
        self.keys = None
        self.keys_no_count = None
        self.path = None
        self.db = None
        self.noise_filter = None

    def create_path(self, path):
        """
        :param path: path user declared to processing docs
        :return: class variable of the path
        """
        try:
            logger.getLogger().info("Command Manager - Init")
            full_path = os.path.abspath(path)
            if os.path.isdir(full_path):
                logger.getLogger().info("CommandManager created with path={}"
                                        .format(full_path))
                self.path = full_path
            elif os.path.isfile(full_path):
                logger.getLogger().info("CommandManager created with path={}"
                                        .format(full_path))
                self.path = full_path
            else:
                raise RuntimeError

        except RuntimeError as error:
            logger.getLogger().error("Directory does not exist")
            sys.exit(1)

    def run(self, model):
        """
        Main run function to handle learning
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Run")
        try:

            logger.getLogger().debug("Running a " + model)

            if model is 'compare':
                doc_worker = DocumentFactory(self.path, True)
            else:
                doc_worker = DocumentFactory(self.path, False)

            logger.getLogger().info("Converting files")
            __args = doc_worker.convert_file()

            logger.getLogger().info("Applying a filter to the files")
            self.noise_filter = Noise(__args[0], __args[1], model)
            self.noise_filter.get_doc()

            self.noise_filter.word_reduce()

            logger.getLogger().info("Reducing the filter to a word count")
            self.noise_filter.word_map()
            #
            # a dict of most commonly used words, figured it could be smart
            # to have this as a global value in this class
            self.keys = self.noise_filter.get_word_count()

            self.run_args(model)

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)

    def run_args(self, model):

        if model is 'train':
            logger.getLogger().info("Saving object to disk")
            if os.path.isdir("/usr/local/var/lispat/objects"):
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')
            else:
                os.makedirs("/usr/local/var/lispat/objects/")
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')

            obj = self.noise_filter.word_array
            pickle.dump(obj, obj_file)
            logger.getLogger().debug("Object successfully saved")

        if model is 'compare':

            path = "/usr/local/var/lispat/pdf_data/"
            txt_data = ""
            try:
                for file in os.listdir(path):
                    __file = open(path + file, 'rt')
                    __text = __file.read()
                    txt_data += __text
            except RuntimeError as error:
                logger.getLogger().error("Word filter - ", error)
            #
            # logger.getLogger().info("Getting object from disk")
            # obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'rb')

            head, tail = os.path.split(self.path)
            file = os.path.splitext(tail)[0]
            submitted = open("/usr/local/var/lispat/submission/" + file + ".txt" , 'rt')

            # obj = pickle.load(obj_file)
            # txt = " ".join(obj)
            txt2 = submitted.read()

            len(txt_data)
            len(txt2)

            nlp = spacy.load("en")
            doc1 = nlp(txt_data)
            doc2 = nlp(txt2)

            similarity =  doc2.similarity(doc1)
            logger.getLogger().debug("Document Similarity is " + str(similarity))
            shutil.rmtree("/usr/local/var/lispat/submission")
