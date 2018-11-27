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
        self.docx_dir = directory_storage + "docx_data/"
        self.csv_dir = directory_storage + "csv_data/"
        self.submitted_dir = directory_storage + "submission/"

        self.csv_path = ""

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
    def pdfminer_handler(self, path, submitted):

        logger.getLogger().info("Running PDFMiner")

        page_nums = set()
        output = StringIO()
        la_params = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, la_params)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            file = os.path.basename(path)
            pdf_saved = self.pdfminer_dir + file
            pdf_saved = os.path.splitext(pdf_saved)[0] + '.txt'

            if os.path.exists(pdf_saved):
                logger.getLogger().debug("Already Exits: " + file)
                self.txt.append(pdf_saved)
                return self.txt

            logger.getLogger().debug("Opening File: {}".format(file))

            try:
                with open(path, 'rb') as infile:
                    logger.getLogger().debug("Opening File Successful")

                    for page in PDFPage.get_pages(infile, page_nums):
                        interpreter.process_page(page)

                    text = output.getvalue()

                    logger.getLogger().debug("Writing " + pdf_saved)
                    # open file is a static function.
                    text_file = self.open_file(submitted, pdf_saved)

                    text_file.write(text)

                    infile.close()
                    converter.close()
                    output.close
                    text_file.close()

                    return self.txt
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
    def docx_handler(self, path, submitted):
        logger.getLogger().info("running docx")
        doc_text = []
        try:
            file = os.path.basename(path)
            doc_saved = self.docx_dir + file
            doc_saved = os.path.splitext(doc_saved)[0] + '.txt'

            if os.path.exists(doc_saved):
                logger.getLogger().debug("Already Exits: " + file)
                self.txt.append(doc_saved)
                return self.txt

            doc = docx.Document(path)

            for para in doc.paragraphs:
                doc_text.append(para.text)

            doc_text = '\n'.join(doc_text)

            text_file = self.open_file(submitted, doc_saved)
            text_file.write(doc_text)

            return self.txt
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    def csv_handler(self, txt):
        """
        Function using tabula library to extract text from word docs and
        store them into an array of csv files

        TODO: This class needs to be more modular for different arrays
        and csv files.
        """
        logger.getLogger().info("Creating a CSV")

        try:
            csv_filename = self.csv_dir + "test.csv"
            logger.getLogger().debug("Opening File for csv: " + csv_filename)
            csv__ = open(csv_filename, 'w+')
            self.csv_path = csv_filename
            with open(csv_filename, 'a+', newline='') as outputFile:
                logger.getLogger().debug("csv file opened: " + csv_filename)

                writer = csv.writer(outputFile, dialect='excel')
                logger.getLogger().debug("csv created: " + csv_filename)
                writer.writerows(txt)

                outputFile.close()
                return True
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    """
    Creates/Opens text files with input file name
    """
    def open_file(self, submitted, file):
        if submitted is True:
            file = os.path.basename(path)
            txt_filename = self.submitted_dir + file
            txt_filename = os.path.splitext(txt_filename)[0] + '.txt'
        else:
            txt_filename = file

        logger.getLogger().debug("File opened for writing - {}"
                                 .format(txt_filename))
        self.txt.append(txt_filename)
        return open(txt_filename, "w")

    """
    Gets the file count from a list of files
    """
    def file_count(self, files):
        count = 0
        for file in files:
            count += 1
        return count
