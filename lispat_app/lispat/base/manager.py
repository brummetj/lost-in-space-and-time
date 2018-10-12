import os

# from ..utils.logger import Logger
# from ..factory.document_factory import DocumentFactory
from lispat.utils.logger import Logger
from lispat.factory.document_factory import DocumentFactory
from lispat.utils.noise_filter import NoiseFilter

logger = Logger("CommandManager")


class CommandManager:
    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """

    def __init__(self, path):
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

    def run(self):
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Run")
        try:
            doc_worker = DocumentFactory(self.path)

            logger.getLogger().info("Converting files")
            __args = doc_worker.convert_file()

            logger.getLogger().info("Applying a filter to the files")
            noise_filter = NoiseFilter(__args[0], __args[1])

            noise_filter.word_filter()

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
