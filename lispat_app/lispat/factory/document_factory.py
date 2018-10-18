import os
from lispat.utils.logger import Logger
from lispat.factory.argument_factory import ArgumentFactory


class DocumentFactory:
    """
    This class should break up the dir path by file types
    and return file types that can be aggregated together
    into their own function that handles those certain file types
    """

    def __init__(self, path):
            logger = Logger("DocumentFactory")
            logger.getLogger().info("DocumentFactory Created")
            self.path = path
            self.docs = []
            self.pdf = []
            args_ = ArgumentFactory()
            try:
                for file in os.listdir(path):
                    if file.endswith(".doc"):
                        logger.getLogger().debug("File - {}"
                                                 .format(file))
                        self.docs.append((file, path))

                    elif file.endswith(".docx"):
                        logger.getLogger().debug("File - {}"
                                                 .format(file))
                        self.docs.append((file, path))

                    elif file.endswith(".pdf"):
                        logger.getLogger().debug("File - {}"
                                                 .format(file, path))
                        self.pdf.append((file, path))

                    else:
                        logger.getLogger().error("No elgible files in {}"
                                                 .format(path))
                try:
                    logger.getLogger().debug("Trying to turn files into txt")
                    self.word_data = args_.docx_handler(self.docs)
                    self.pdf_data = args_.pdfminer_handler(self.pdf)
                    self.csv_data = args_.csv_handler()
                except:
                    logger.getLogger().error("Error occured turning documents"
                                             " into .txt files")
            except:
                logger.getLogger().error("Error Occured")
