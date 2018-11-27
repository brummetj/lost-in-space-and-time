import os
import sys
from lispat.utils.logger import Logger
from lispat.factory.document_factory import DocumentFactory
from lispat.processing.predictive_model import Predict
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
        self.doc_worker = None
        self.model = NLPModel()

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

    def convert(self):
        """
        Convert function to handle file conversion
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Convert")
        try:

            doc_worker = DocumentFactory(self.path, False)

            logger.getLogger().info("Converting files")

            __args = doc_worker.convert_file()

            logger.getLogger().info("Files stored in /usr/local/var/lispat/")

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)

    def run(self, args):
        """
        Main run function to handle learning
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Run")
        try:

            if args['--compare']:
                self.doc_worker = DocumentFactory(self.path, True)
            if args['--train']:
                self.doc_worker = DocumentFactory(self.path, False)

            docs = self.doc_worker.convert_file()
            self.filter = Preproccessing(docs[0], docs[1])
            self.filter.get_doc(args)

            if args['--array']:
                self.filter.filter_nlp()
                self.filter.word_count()
                self.keys = self.filter.get_word_count()

            if args['--df']:
                nlp_array_unfiltered = (self.model.
                                        build_sents(self.filter.nlp.sents))
                print(nlp_array_unfiltered[:5])
                csv_success = (self.doc_worker.args_.
                               csv_handler(nlp_array_unfiltered))
                if csv_success:
                    self.model.data_frame(self.doc_worker.args_.csv_path)

            # TODO: figure out how we can make it so we don't need to
            # check this again...
            if args['--compare']:
                self.model.compare_doc_similarity(self.path)
            if args['--train']:
                self.model.save_trained(self.filter.word_array)

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)

    def predict(self):
        line = input("Enter a sentence: ")
        predictor = Predict()
        predictor.output(line)
