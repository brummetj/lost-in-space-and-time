import os
<<<<<<< HEAD
import time
=======
>>>>>>> 5c8ae1de1f08be9826005d6177a6299ef5eddb1e
import multiprocessing as mp
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
        self.pdfs = []
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
                    self.pdfs.append((file, path))

        except FileNotFoundError as error:
            logger.getLogger().error(error)

    def convert_file(self):
        try:
            args_ = ArgumentFactory()

<<<<<<< HEAD
            #word_data_txt = args_.docx_handler(self.docs)

            doc_output = mp.Queue()
            doc_jobs = []
            for(file, path) in self.docs:
                doc_procs = mp.Process(target=args_.docx_handler, args=(file,
                                       path, doc_output))
                doc_jobs.append(doc_procs)
                doc_procs.start()

            for doc_proc in doc_procs:
                doc_proc.join()

            word_data_txt = [doc_output.get() for doc_proc in doc_procs]

            pdf_output = mp.Queue()
            pdf_jobs = []

            for (file, path) in self.pdf:
                procs = mp.Process(target=args_.pdfminer_handler, args=(file,
                                   path, pdf_output))
                pdf_jobs.append(procs)
                procs.start()

            for proc in procs:
                proc.join()

            logger.getLogger().debug("DONE WITH PROCESSES")

            pdf_data_txt = [pdf_output.get() for proc in procs]

            return word_data_txt, pdf_data_txt

=======
            doc_queue = mp.Queue()
            pdf_queue = mp.Queue()

            doc_jobs = []
            pdf_jobs = []

            doc_data_txt = []
            pdf_data_txt = []

            if self.docs:
                for(file, path) in self.docs:
                    doc_procs = mp.Process(target=args_.docx_handler, args=
                                           (file, path, doc_queue))
                    doc_procs.start()
                    doc_jobs.append(doc_procs)

                for doc_proc in doc_jobs:
                    doc_data_txt.append(doc_queue.get())
                    doc_proc.join()

            if self.pdfs:
                for (file, path) in self.pdfs:
                    procs = mp.Process(target=args_.pdfminer_handler, args=
                                       (file, path, pdf_queue))
                    procs.start()
                    pdf_jobs.append(procs)

                for proc in pdf_jobs:
                    pdf_data_txt.append(pdf_queue.get())
                    proc.join()

            return doc_data_txt, pdf_data_txt
>>>>>>> 5c8ae1de1f08be9826005d6177a6299ef5eddb1e
        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)
