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


class ArgumentFactory:
    '''
    This class handles the arguments and converts them to txt files.
    '''

    def __init__(self):

        logger = Logger("ArgumentFactory - init")
        logger.getLogger().info("ArgumentFactory Created")

        self.txt = []

        directory_storage = "/usr/local/var/lispat/"
        self.pdfminer_dir = directory_storage + "/pdfminer_Data"
        self.doc2txt_dir = directory_storage + "/docx2txt_Data"
        self.docx_dir = directory_storage + "/docx_Data"
        self.csv_dir = directory_storage + "/csv_Data"

        if not os.path.exists(directory_storage):
            os.makedirs(directory_storage)

        # Simple check to see if we have these dirs in the storage path already
        if len(os.listdir(directory_storage)) == 0:
            os.makedirs(self.pdfminer_dir)
            os.makedirs(self.doc2txt_dir)
            os.makedirs(self.docx_dir)
            os.makedirs(self.csv_dir)

    '''
    Function using PyPDF2 to decrypt a secured pdf file
    '''
    def decrypt_pdf(input_path, output_path, password):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - PyPDF2")
        with open(input_path, 'rb') as input_file, \
             open(output_path, 'wb') as output_file:
                reader = PdfFileReader(input_file)
                reader.decrypt(password)

                writer = PdfFileWriter()

                for i in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(i))

                    writer.write(output_file)

    '''
    Function using pdfminer to extract text from pdfs and
    store them into an array of text files
    '''

    def pdfminer_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - PDFMiner")

        page_nums = set()
        output = StringIO()
        la_params = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, la_params)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            for (file, path) in data:
                pdf = os.path.join(path, file)

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

                        logger.getLogger().debug("File - {} opened for writing"
                                                 .format(text_filename))

                        text_file.write(text)
                        logger.getLogger().debug("File - {} in {}"
                                                 .format(file))

                        self.txt.append((text_filename, self.pdfminer_dir))
                        infile.close()

                except FileNotFoundError:
                    logger.getLogger().error("File Failed to Open")

        except RuntimeError:
            logger.getLogger().error("Error Occured")

        converter.close()
        output.close()
        text_file.close()

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''

    def docx_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - docx")
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
        except RuntimeError:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''

    def docx2txt_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - docx2txt")

        try:
            for (file, path) in data:
                doc_file = os.path.join(path, file)

                doc_text = docx2txt.process(doc_file)

                file = os.path.splitext(file)[0]
                text_filename = self.doc2txt_dir + "/" + file + ".txt"

                text_file = open(text_filename, "w")
                text_file.write(doc_text)
                self.txt.append((text_filename, path))
        except RuntimeError:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using tabula library to extract text from word docs and
    store them into an array of csv files
    '''

    def csv_handler(self):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - csv_handler")

        try:
            for file in os.listdir(self.pdfminer_dir):

                textFile = self.pdfminer_dir + "/" + file
                print(textFile)

                file = os.path.splitext(file)[0]
                csvFilename = self.csv_dir + "/" + file + ".csv"

                with open(textFile, 'r', newline='') as inputFile:
                    print("Text file opened")
                    reader = csv.reader(inputFile, delimiter=" ")
                    print("reader created")
                    with open(csvFilename, 'w', newline='') as outputFile:
                        print("csv file opened")
                        writer = csv.writer(outputFile)
                        print("writer created")
                        for row in reader:
                            print("inside for loop")
                            writer.writerow(row)

                inputFile.close()
                outputFile.close()
        except RuntimeError:
            logger.getLogger().error("Error Occured")
