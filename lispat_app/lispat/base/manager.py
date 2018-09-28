import os
from ..utils.logger import Logger
from ..factory.document_factory import DocumentFactory
class CommandManager:

    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """
    def __init__(self, path):
        try:
            logger = Logger("CommandManager - init")
            full_path = os.path.abspath(path)
            if os.path.isdir(full_path):
                logger.getLogger().info("CommandManager created with path={}".format(full_path))
                self.path = full_path
            else:
                logger.getLogger().error("Directory does not exist")
        except:
            logger.getLogger().error("Error Occured")
    def run(self):
        # Initialize with our docs.
        logger = Logger("CommandManager - init")
        try:
            DocumentFactory(self.path)
            logger.getLogger().info("Documents converted")
        except:
            logger.getLogger().error("Error Occured")
