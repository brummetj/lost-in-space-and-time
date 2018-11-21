import os
from lispat.utils.logger import Logger
from lispat.factory.document_factory import DocumentFactory
from lispat.processing.noise_filter import NoiseFilter
from lispat.processing.model import GensimModel

import spacy
nlp = spacy.load('en_core_web_lg')

logger = Logger("CommandManager")


class CommandManager:
    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """

    def __init__(self):
        self.keys = None
        self.path = None

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
            else:
                logger.getLogger().error("Directory does not exist")
        except RuntimeError as error:
            logger.getLogger().error(error)

    def convert(self):
        """
        Convert function to handle converting pdfs/docs to txt
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Convert")
        try:
            doc_worker = DocumentFactory(self.path)

            logger.getLogger().info("Converting files")
            __args = doc_worker.convert_file()

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)

    def train(self, model):
        """
        Main run function to handle learning
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Run")
        try:
            doc_worker = DocumentFactory(self.path)

            logger.getLogger().info("Converting files")
            __args = doc_worker.convert_file()

            logger.getLogger().info("Applying a filter to the files")
            noise_filter = NoiseFilter(__args[0], __args[1])
            words = noise_filter.mapper()

            logger.getLogger().info("Applying a reduce to the files")
            noise_filter.reduce()

            # a dict of most commonly used words, figured it could be smart
            # to have this as a global value in this class
            self.keys = noise_filter.get_word_count()

            if model is 'ss':
                logger.getLogger().info("Using spacy symantic similarity")
                #words = words[:100000]
                #strings = ' '.join(self.keys)
                strings = [i[0] for i in self.keys]
                strings = ' '.join(strings)
                tokens = nlp(strings)

                for token1 in tokens:
                    for token2 in tokens:
                        print(token1.text, token2.text, token1.similarity(token2))

                for token in tokens:
                    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                          token.shape_, token.is_alpha, token.is_stop)


        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
