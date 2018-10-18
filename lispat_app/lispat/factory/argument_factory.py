import os
import csv
import docx
import docx2txt
from io import StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
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

        if not os.path.exists(directory_storage):
            os.makedirs(directory_storage)

        # Simple check to see if we have these dirs in the storage path already
        if len(os.listdir(directory_storage)) == 0:
            os.makedirs(self.pdfminer_dir)
            os.makedirs(self.doc2txt_dir)
            os.makedirs(self.docx_dir)
            os.makedirs(self.csv_dir)

        self.txt = []

    '''
    Function using pdfminer to extract text from pdfs and
    store them into an array of text files
    '''

    def pdfminer_handler(self, data):

        logger.getLogger().info("running PDFMiner")

        page_nums = set()
        output = StringIO()
        la_params = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, la_params)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            for (file, path) in data:
                pdf = os.path.join(path, file)
                pdf_saved = self.pdfminer_dir + file

                pdf_saved = os.path.splitext(pdf_saved)[0] + '.txt'
                if os.path.exists(pdf_saved):
                    logger.getLogger().debug("Already Exits: " + file)
                    continue

                logger.getLogger().debug("Opening File: {}".format(pdf))

                try:
                    with open(pdf, 'rb') as infile:
                        logger.getLogger().debug("Opening File Successful")

                        for page in PDFPage.get_pages(infile, page_nums):
                            interpreter.process_page(page)

                        text = output.getvalue()
                        file = os.path.splitext(file)[0]

                        text_filename = self.pdfminer_dir + "/" + file + ".txt"
                        text_file = open(text_filename, "w")

                        logger.getLogger().debug("File opened for writing - {}"
                                                 .format(text_filename))

                        text_file.write(text)
                        logger.getLogger().debug("File - {} in {}"
                                                 .format(file))

                        self.txt.append((text_filename, self.pdfminer_dir))
                        infile.close()

                    converter.close()
                    # output.close
                    text_file.close()
                except ImportError as error:
                    logger.getLogger().error(error)
        except RuntimeError as error:
            logger.getLogger().error(error)

        #converter.close()
        #output.close()
        #text_file.close()

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''

    def docx_handler(self, data):

        logger.getLogger().info("running docx")
        doc_text = []
        try:
            for (file, path) in data:
                doc_file = os.path.join(path, file)
                doc = docx.Document(doc_file)

                for para in doc.paragraphs:
                    doc_text.append(para.text)

                file = os.path.splitext(file)[0]
                text_filename = self.docx_dir + "/" + file + ".txt"

                text_file = open(text_filename, "w")
                text_file.write(doc_text)
                self.txt.append((text_filename, path))
        except RuntimeError as error:
            logger.getLogger().error(error)

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''

    def docx2txt_handler(self, data):
        logger.getLogger().info("running docx2txt")

        try:
            for (file, path) in data:
                doc_file = os.path.join(path, file)

                doc_text = docx2txt.process(doc_file)

                file = os.path.splitext(file)[0]
                text_filename = self.doc2txt_dir + "/" + file + ".txt"

                text_file = open(text_filename, "w")
                text_file.write(doc_text)
                self.txt.append((text_filename, path))
        except RuntimeError as error:
            logger.getLogger().error(error)

        return self.txt

    '''
    Function using tabula library to extract text from word docs and
    store them into an array of csv files
    '''

    def csv_handler(self):
        logger.getLogger().info("csv_handler")

        try:
            for file in os.listdir(self.pdfminer_dir):

                text_file = self.pdfminer_dir + "/" + file
                print(text_file)

                file = os.path.splitext(file)[0]
                csv_filename = self.csv_dir + "/" + file + ".csv"

                with open(text_file, 'r', newline='') as inputFile:
                    logger.getLogger().debug("Text file opened: " + text_file)

                    reader = csv.reader(inputFile, delimiter=" ")
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
