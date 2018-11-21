import os
import csv
import docx
import sys
from io import StringIO
from lispat.utils.logger import Logger
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


logger = Logger("ArgumentFactory")


class ArgumentFactory:
    '''
    This class handles the arguments and converts them to txt files.
    '''

    def __init__(self):

        logger.getLogger().info("Argument factory init")

        self.txt = []
        directory_storage = "/usr/local/var/lispat/"
        self.pdfminer_dir = directory_storage + "pdf_data/"
        self.doc2txt_dir = directory_storage + "doc_data/"
        self.docx_dir = directory_storage + "docx_data/"
        self.csv_dir = directory_storage + "csv_data/"
        self.submitted_dir = directory_storage + "submission/"

        if not os.path.exists(directory_storage):
            os.makedirs(directory_storage)

        # Simple check to see if we have these dirs in the storage path already
        # best for first time users
        # need a better way to make the local storage system
        if len(os.listdir(directory_storage)) == 0:
            os.makedirs(self.pdfminer_dir)
            os.makedirs(self.doc2txt_dir)
            os.makedirs(self.docx_dir)
            os.makedirs(self.csv_dir)
            os.makedirs(self.submitted_dir)

        if not os.path.exists(self.submitted_dir):
            os.makedirs(self.submitted_dir)

    '''
    Function using pdfminer to extract text from pdfs and
    store them into an array of text files
    '''
    def pdfminer_handler(self, file, path, queue, submitted):

        logger.getLogger().info("Running PDFMiner")

        page_nums = set()
        output = StringIO()
        la_params = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, la_params)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            pdf = os.path.join(path, file)
            pdf_saved = self.pdfminer_dir + file

            pdf_saved = os.path.splitext(pdf_saved)[0] + '.txt'

            if os.path.exists(pdf_saved):
                logger.getLogger().debug("Already Exits: " + file)
                self.txt.append((pdf_saved, self.pdfminer_dir))
                queue.put(self.txt)
                return None

            logger.getLogger().debug("Opening File: {}".format(pdf))

            try:
                with open(pdf, 'rb') as infile:
                    logger.getLogger().debug("Opening File Successful")

                    for page in PDFPage.get_pages(infile, page_nums):
                        interpreter.process_page(page)

                    text = output.getvalue()
                    head, tail = os.path.split(path)
                    file = os.path.splitext(tail)[0]

                    logger.getLogger().debug("Writing " + file)
                    # open file is a static function.
                    text_file = self.open_file(submitted, file,
                                               self.pdfminer_dir)

                    text_file.write(text)

                    infile.close()

                    converter.close()
                    output.close
                    text_file.close()
                    queue.put(self.txt)
            except ImportError as error:
                logger.getLogger().error(error)
                sys.exit(1)
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''
    def docx_handler(self, file, path, queue, submitted):
        logger.getLogger().info("running docx")
        doc_text = []
        try:

            doc_file = os.path.join(path, file)
            doc_saved = self.docx_dir + file
            doc_saved = os.path.splitext(doc_saved)[0] + '.txt'

            if os.path.exists(doc_saved):
                logger.getLogger().debug("Already Exits: " + file)
                self.txt.append((doc_saved, self.docx_dir))
                queue.put(self.txt)
                return None

            doc = docx.Document(doc_file)

            for para in doc.paragraphs:
                doc_text.append(para.text)

            doc_text = '\n'.join(doc_text)

            file = os.path.splitext(file)[0]
            text_file = self.open_file(submitted, file, self.docx_dir)
            text_file.write(doc_text)

            queue.put(self.txt)
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    '''
    Function using tabula library to extract text from word docs and
    store them into an array of csv files
    '''
    def csv_handler(self):
        logger.getLogger().info("csv_handler")

        try:
            for file in os.listdir(self.pdfminer_dir):

                text_file = self.pdfminer_dir + "/" + file

                file = os.path.splitext(file)[0]
                csv_filename = self.csv_dir + "/" + file + ".csv"

                with open(text_file, 'r', newline='') as inputFile:
                    logger.getLogger().debug("Text file opened: " + text_file)

                    reader = csv.reader(inputFile, delimiter=".")
                    logger.getLogger().debug("render created")

                    with open(csv_filename, 'w', newline='') as outputFile:
                        logger.getLogger().debug("csv file opened")

                        writer = csv.writer(outputFile)
                        logger.getLogger().debug("writer created")
                        for row in reader:
                            writer.writerow(row)

                inputFile.close()
                outputFile.close()
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    def open_file(self, submitted, file, dir):
        if submitted is True:
            txt_filename = self.submitted_dir + file + ".txt"
        else:
            txt_filename = dir + file + ".txt"

        logger.getLogger().debug("File opened for writing - {}"
                                 .format(txt_filename))
        self.txt.append((txt_filename, dir))
        return open(txt_filename, "w")
