import os

# from ..utils.logger import Logger
# from ..factory.document_factory import DocumentFactory
from lispat.utils.logger import Logger
from lispat.factory.document_factory import DocumentFactory
from lispat.processing.noise_filter import NoiseFilter
from lispat.processing.model import GensimModel
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
            noise_filter.mapper()

            logger.getLogger().info("Applying a reduce to the files")
            noise_filter.reduce()

            # a dict of most commonly used words, figured it could be smart to have this as a global value in this class
            self.keys = noise_filter.get_word_count()

            if model is 'nn':
                logger.getLogger().info("Using gensim pre-processing")
                documents = noise_filter.gensim()
                print(documents)
                logger.getLogger().info("Training Data with gensim, may take some time.... ")
                # nn_model = GensimModel()
                # nn_model.train(noise_filter.get_word_array())
                # logger.getLogger().info("Training finished")
                #
                # w1 = "shall"
                # nn_model = nn_model.get_model()
                # logger.getLogger().debug("Nearest Neighbor to :", w1)
                # logger.getLogger().debug(nn_model.wv.most_similar(positive=w1))

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
