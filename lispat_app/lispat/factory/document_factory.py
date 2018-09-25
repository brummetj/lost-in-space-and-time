import os
from ..utils.logger import Logger
from factory.argument_factory import ArgumentFactory

class DocumentFactory:
    """
    This class should break up the dir path by file types
    and return file types that can be aggregated together
    into their own function that handles those certain file types
    """
    filetype = ['.doc','docx','.pdf','.txt']
    def __init__(self, path):
            self.path = path
            self.txt = []
            self.docx = []
            self.pdf = []
            self.doc = []
            try:
                for file in os.listdir(path):
                    if file.endswith(".txt"):
                        logger.getLogger().info("File - {} in {}".format(file, path))

                    elif file.endswith()
            except:
                print("Error has occured")
