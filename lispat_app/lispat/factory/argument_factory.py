import os
from ..utils.logger import Logger
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import PyPDF2
import textract


class ArgumentFactory:

    '''
    This class handles the arguments and converts them to txt files.
    '''
    def __init__(self):
        logger = Logger("ArgumentFactory - init")
        logger.getLogger().info("ArgumentFactory Created")

        path = os.path.abspath('./lispat/assets')
        self.dirName = path + "/textFiles"

        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            logger.getLogger().info("Text Files Directory created with path={}"
                                    .format(self.dirName))

    '''
    Function using PyPDF2 and textract library to extract text from pdfs and
    store them into an array of text files
    '''
    def pypdf_handler(self, data):
        logger = Logger("ArgumentFactory - init")
        logger.getLogger().info("ArgumentFactory - PDF to Text")
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
                textFilename = self.dirName + "/" + file + ".txt"

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
        logger.getLogger().info("ArgumentFactory - PDF to Text")

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
                except:
                    logger.getLogger().error("File Failed to Open")

                for page in PDFPage.get_pages(infile, pagenums):
                        logger.getLogger().debug("Iterating through pages")
                        interpreter.process_page(page)

                logger.getLogger().info("PDF file {} processed".format(infile))

                infile.close()
                text = output.getvalue()
                textFilename = file + ".txt"
                textFile = open(textFilename, "w")
                logger.getLogger().debug("File - {} opened for writing"
                                         .format(textFilename))
                textFile.write(text)
                logger.getLogger().debug("File - {} in {}".format(file, path))
                self.txt.append((textFilename, path))

            converter.close()
            output.close
        except:
            logger.getLogger().error("Error Occured")

        return self.txt
