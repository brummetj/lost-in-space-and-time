import os
import csv
import time
import docx
import PyPDF2
import thread
import tabula
import docx2txt
import textract
from io import StringIO
from ..utils.logger import Logger
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

        path = os.path.abspath('./lispat/assets')
        self.pyPDFdir = path + "/PyPDF_Data"
        self.pdfminerDir = path + "/pdfminer_Data"
        self.doc2txtDir = path + "/docx2txt_Data"
        self.docxDir = path + "/docx_Data"
        self.csvDir = path + "/csv_Data"

    '''
    Function using PyPDF2 and textract library to extract text from pdfs and
    store them into an array of text files
    '''
    def pypdf_handler(self, data):
        logger = Logger("ArgumentFactory - init")
        logger.getLogger().info("ArgumentFactory - PyPDF")

        self.txt = []
        try:
            for (file, path) in data:
                pdf_file = os.path.join(path, file)
                infile = open(pdf_file, 'rb')

                pdfReader = PyPDF2.PdfFileReader(infile)

                num_pages = pdfReader.numPages
                count = 0
                text = ""

                while count < num_pages:
                    page = pdfReader.getPage(count)
                    count += 1
                    text += page.extractText()

                if text != "":
                    text = text
                else:
                    text = textract.process(pdf_file, method='tesseract',
                                            language='eng')

                file = os.path.splitext(file)[0]
                textFilename = self.pyPDFdir + "/" + file + ".txt"

                textFile = open(textFilename, "w")
                textFile.write(text)
                self.txt.append((textFilename, path))
        except:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using pdfminer to extract text from pdfs and
    store them into an array of text files
    '''
    def pdfminer_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - PDFMiner")

        txt = []
        pagenums = set()
        output = StringIO()
        laparams = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            for (file, path) in data:
                pdf = os.path.join(path, file)

                logger.getLogger().debug("Opening File: {}".format(pdf))
                try:
                    with open(pdf, 'rb') as infile:
                        logger.getLogger().debug("Opening File Successful")

                        for page in PDFPage.get_pages(infile, pagenums):
                                interpreter.process_page(page)

                        text = output.getvalue()
                        file = os.path.splitext(file)[0]
                        textFilename = self.pdfminerDir + "/" + file + ".txt"
                        textFile = open(textFilename, "w")
                        logger.getLogger().debug("File - {} opened for writing"
                                                 .format(textFilename))
                        textFile.write(text)
                        logger.getLogger().debug("File - {} in {}"
                                                 .format(file, path))
                        self.txt.append((textFilename, path))
                        infile.close()

                    converter.close()
                    output.close
                except:
                    logger.getLogger().error("File Failed to Open")
        except:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using pdfminer to extract text from pdfs and
    store them into an array of text files
    '''
    def pdfminer_to_csv(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - PDFMiner")

        txt = []
        pagenums = set()
        output = StringIO()
        laparams = LAParams()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams)
        interpreter = PDFPageInterpreter(manager, converter)

        try:
            for (file, path) in data:
                pdf = os.path.join(path, file)

                logger.getLogger().debug("Opening File: {}".format(pdf))
                try:
                    with open(pdf, 'rb') as infile:
                        logger.getLogger().debug("Opening File Successful")

                        for page in PDFPage.get_pages(infile, pagenums):
                                interpreter.process_page(page)

                        text = output.getvalue()
                        textFilename = file + ".txt"
                        textFile = open(textFilename, "w")
                        logger.getLogger().debug("File - {} opened for writing"
                                                 .format(textFilename))
                        textFile.write(text)
                        logger.getLogger().debug("File - {} in {}"
                                                 .format(file, path))
                        self.txt.append((textFilename, path))
                        infile.close()

                    converter.close()
                    output.close
                except:
                    logger.getLogger().error("File Failed to Open")
        except:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''
    def docx_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - docx")
        doc_text = []
        self.txt = []
        try:
            for (file, path) in data:
                doc_file = os.path.join(path, file)
                doc = docx.Document(doc_file)

                for para in doc.paragraphs:
                    doc_text.append(para.text)

                file = os.path.splitext(file)[0]
                textFilename = self.docxDir + "/" + file + ".txt"

                textFile = open(textFilename, "w")
                textFile.write(doc_text)
                self.txt.append((textFilename, path))
        except:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using docx library to extract text from word docs and
    store them into an array of text files
    '''
    def docx2txt_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - docx2txt")

        self.txt = []
        try:
            for (file, path) in data:
                doc_file = os.path.join(path, file)

                doc_text = docx2txt.process(doc_file)

                file = os.path.splitext(file)[0]
                textFilename = self.doc2txtDir + "/" + file + ".txt"

                textFile = open(textFilename, "w")
                textFile.write(doc_text)
                self.txt.append((textFilename, path))
        except:
            logger.getLogger().error("Error Occured")

        return self.txt

    '''
    Function using tabula library to extract text from word docs and
    store them into an array of csv files
    '''
    def tabula_handler(self, data):
        logger = Logger("ArgumentFactory")
        logger.getLogger().info("ArgumentFactory - tabula")

        txtPath = self.pdfminerDir

        try:
            for (file, txtPath) in data:
                txtFile = os.path.join(txtPath, file)

                file = os.path.splitext(file)[0]
                csvFilename = self.csvDir + "/" + file + ".csv"

                inputFile = open(txtFile, "rb")

                outputFile = csv.writer(open(csvFilename, "wb"))

                outputFile.writerows(inputFile)
        except:
            logger.getLogger().error("Error Occured")

        '''
        try:
            for (file, path) in data:
                pdf = os.path.join(path, file)

                file = os.path.splitext(file)[0]
                csvFilename = self.csvDir + "/" + file + ".csv"

                tabula.convert_into(pdf, csvFilename, output_format='csv')
        except:
            logger.getLogger().error("Error Occured")
        '''
