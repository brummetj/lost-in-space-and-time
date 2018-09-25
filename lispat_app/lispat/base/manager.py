import os
from ..utils.logger import Logger

class CommandManager:

    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """
    def __init__(self, path):
        try:
            logging = Logger("CommandManager")
            if os.path.isdir(path):
                logging.getLogger().info("CommandManager created with path={}".format(path))
                self.path = path
            else:
                logging.getLogger().error("Directory does not exist")
        except:
            print("Error occured")
    def run(self):
        print("nothing yet")
