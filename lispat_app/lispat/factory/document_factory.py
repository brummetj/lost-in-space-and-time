"""
DocumentFactory.

This script recieves user defined path containing files that are to be
converted into text files.
"""

import os
import sys
from pathlib import Path
from joblib import Parallel, delayed
from lispat.utils.logger import Logger
from lispat.factory.argument_factory import ArgumentFactory

logger = Logger("DocumentFactory")


class DocumentFactory:
    """
    Handles file conversion, using the user defined path.

    This class should break up the directory path by file types and
    returns file types that can be aggregated together into their own function
    that handles those certain file types.
    """

    def __init__(self, path, submitted):

        logger.getLogger().info("DocumentFactory Created")

        self.path = path
        self.docs = []
        self.pdfs = []
        self.submitted = False

        self.args_ = ArgumentFactory()

        try:
            if submitted is True:
                self.submitted = True
                logger.getLogger().debug("Submission is True")

            file = Path(path)
            if file.is_file():
                if file.suffix == ".doc":
                    logger.getLogger().debug("File Found - {}".format(file))
                    self.docs.append(path)

                if file.suffix == ".docx":
                    file = os.path.basename(path)
                    logger.getLogger().debug("File Found - {}".format(file))
                    self.docs.append(path)

                if file.suffix == '.pdf':
                    file = os.path.basename(path)
                    logger.getLogger().debug("File Found - {}".format(file))
                    self.pdfs.append(path)

            elif file.is_dir():
                for file in os.listdir(path):
                    if file.endswith(".doc"):
                        logger.getLogger().debug("File Found - {}"
                                                 .format(file))
                        self.docs.append(path + "/" + file)

                    if file.endswith(".docx"):
                        logger.getLogger().debug("File Found - {}"
                                                 .format(file))
                        self.docs.append(path + "/" + file)

                    if file.endswith(".pdf"):
                        print(path)
                        logger.getLogger().debug("File Found - {}"
                                                 .format(file))
                        self.pdfs.append(path + "/" + file)

        except FileNotFoundError as error:
            logger.getLogger().error("No required file types Found - Exiting")
            sys.exit(1)

    def convert_file(self):
        """
        Handles the file conversion.

        Iterate through pdfs and docx files calls ArgumentFactory Class
        functions to extract text.
        """
        try:

            doc_data_txt = []
            pdf_data_txt = []

            n = self.args_.file_count(self.docs)

            if self.docs:
                doc_data_txt = (
                    Parallel
                    (n_jobs=n, backend="multiprocessing", verbose=10)
                    (delayed
                     (self.args_.docx_handler)(path, self.submitted)
                        for path in self.docs))

            n = self.args_.file_count(self.pdfs)

            if self.pdfs:
                pdf_data_txt = (
                    Parallel
                    (n_jobs=n, backend="multiprocessing", verbose=10)
                    (delayed
                     (self.args_.pdfminer_handler)(path, self.submitted)
                        for path in self.pdfs))

            return doc_data_txt, pdf_data_txt

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
