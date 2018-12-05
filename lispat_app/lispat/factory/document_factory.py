import os
import sys
import traceback
import multiprocessing as mp
from lispat.utils.logger import Logger
from lispat.factory.argument_factory import ArgumentFactory
from lispat.utils.colors import bcolors
from pathlib import Path
logger = Logger("DocumentFactory")


class DocumentFactory:
    """
    This class should break up the dir path by file types
    and return file types that can be aggregated together
    into their own function that handles those certain file types
    """

    def __init__(self, path, submitted, standard):

        logger.getLogger().info("DocumentFactory Created")

        self.path = path
        self.docs = []
        self.pdfs = []
        self.submitted = submitted
        self.standard = standard

        self.args_ = ArgumentFactory()

        try:
            file = Path(path)
            if file.is_file():
                head, tail = os.path.split(file)
                if file.suffix == ".doc":
                    logger.getLogger().debug(bcolors.OKGREEN + "File Found: " + bcolors.ENDC  + " {} in {}"
                                             .format(tail, path))
                    self.docs.append((str(file.absolute()), path))

                if file.suffix == '.pdf':
                    logger.getLogger().debug(bcolors.OKGREEN + "File Found: " + bcolors.ENDC  + " {} in {}"
                                             .format(tail, path))
                    self.pdfs.append((str(file.absolute()), path))

            elif file.is_dir():
                for file in os.listdir(path):
                    if file.endswith(".doc"):
                        logger.getLogger().debug(bcolors.OKGREEN + "File Found: " + bcolors.ENDC  + " {} in {}"
                                                 .format(file, path))
                        self.docs.append((file, path))

                    if file.endswith(".docx"):
                        logger.getLogger().debug(bcolors.OKGREEN + "File Found" + bcolors.ENDC  + " {} in {}"
                                                 .format(file, path))
                        self.docs.append((file, path))

                    if file.endswith(".pdf"):
                        logger.getLogger().debug(bcolors.OKGREEN + "File Found: " + bcolors.ENDC  + " {} in {}"
                                                 .format(file, path))
                        self.pdfs.append((file, path))
                    else:
                        raise FileNotFoundError

        except FileNotFoundError as error:
            logger.getLogger().error("No required file types Found - Exiting")
            sys.exit(1)

    def convert_file(self):
        try:
            self.args_ = ArgumentFactory()

            doc_queue = mp.Queue()
            pdf_queue = mp.Queue()

            doc_jobs = []
            pdf_jobs = []

            doc_data_txt = []
            pdf_data_txt = []

            if self.docs:
                for(file, path) in self.docs:
                    doc_procs = mp.Process(target=self.args_.docx_handler, args=
                                           (file, path, doc_queue, self.submitted, self.standard))
                    doc_procs.start()
                    doc_jobs.append(doc_procs)

                for doc_proc in doc_jobs:
                    doc_data_txt.append(doc_queue.get())
                    doc_proc.join()

            if self.pdfs:
                for (file, path) in self.pdfs:
                    procs = mp.Process(target=self.args_.pdfminer_handler, args=
                                       (file, path, pdf_queue, self.submitted, self.standard))
                    procs.start()
                    pdf_jobs.append(procs)

                for proc in pdf_jobs:
                    pdf_data_txt.append(pdf_queue.get())
                    proc.join()

            return doc_data_txt, pdf_data_txt

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)


