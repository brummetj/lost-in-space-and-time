import os
from ..utils.logger import Logger
from .argument_factory import ArgumentFactory

class DocumentFactory:
    """
    This class should break up the dir path by file types
    and return file types that can be aggregated together
    into their own function that handles those certain file types
    """
    filetype = ['.doc','docx','.pdf','.txt']

    def __init__(self, path):
            logger = Logger("DocumentFactory")
            logger.getLogger().info("DocumentFactory Created")
            self.path = path
            self.docs = []
            self.docx = []
            self.pdf = []
            try:
                for file in os.listdir(path):
                    if file.endswith(".doc"):
                        logger.getLogger().debug("File - {} in {}".format(file, path))
                        self.docs.append((file, path))

                    elif file.endswith(".pdf"):
                        logger.getLogger().debug("File - {} in {}".format(file, path))
                        self.pdf.append((file, path))

                    elif file.endswith(".docx"):
                        logger.getLogger().debug("File - {} in {}".format(file, path))
                        self.docx.append((file, path))

                    else:
                        logger.getLogger().error("No elgible files in {}".format(path))
                try:
                    logger.getLogger().debug("Attemping to turn files into texts")
                    self.word_data = word_documents(self.docx)
                    self.pdf_data = pdf_documents(self.pdf)
                except:
                    logger.getLogger().error("Error occured turning documents into .txt files")
            except:
                logger.getLogger().error("Error Occured")
