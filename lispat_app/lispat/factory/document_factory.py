import os
from lispat.utils.logger import Logger
from lispat.factory.argument_factory import ArgumentFactory

logger = Logger("DocumentFactory")


class DocumentFactory:
    """
    This class should break up the dir path by file types
    and return file types that can be aggregated together
    into their own function that handles those certain file types
    """

    def __init__(self, path):

        logger.getLogger().info("DocumentFactory Created")

        self.path = path
        self.docs = []
        self.pdf = []
        try:
            for file in os.listdir(path):
                if file.endswith(".doc"):
                    logger.getLogger().debug("File Found - {} in {}"
                                             .format(file, path))
                    self.docs.append((file, path))

                if file.endswith(".docx"):
                    logger.getLogger().debug("File Found - {} in {}"
                                             .format(file, path))
                    self.docs.append((file, path))

                if file.endswith(".pdf"):
                    logger.getLogger().debug("File Found - {} in {}"
                                             .format(file, path))
                    self.pdf.append((file, path))

        except FileNotFoundError as error:
            logger.getLogger().error(error)

    def convert_file(self):
        try:
            args_ = ArgumentFactory()
            word_data_txt = args_.docx_handler(self.docs)
            pdf_data_txt = args_.pdfminer_handler(self.pdf)
            return word_data_txt, pdf_data_txt
        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
