import os
import sys
import csv
import docx
from io import StringIO
from pathlib import Path
from lispat.utils.logger import Logger
from lispat.utils.colors import bcolors
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter


logger = Logger("ArgumentFactory")


class ArgumentFactory:
    """
    This class handles the arguments and converts them to txt files.
    """

    def __init__(self):

        logger.getLogger().info("Argument factory init")

        self.txt = []

        directory_storage = "/usr/local/var/lispat/"

        self.csv_dir = directory_storage + "csv_data/"
        self.docx_dir = directory_storage + "docx_data/"
        self.pdfminer_dir = directory_storage + "pdf_data/"
        self.standard_dir = directory_storage + "standard/"
        self.submitted_dir = directory_storage + "submission/"
        self.visuals_dir = directory_storage + "visuals/"

        self.csv_path = ""

        if not os.path.exists(directory_storage):
            os.makedirs(directory_storage)

        # Simple check to see if we have these dirs in the storage path already
        # best for first time users
        # need a better way to make the local storage system
        if len(os.listdir(directory_storage)) == 0:
            os.makedirs(self.csv_dir)
            os.makedirs(self.docx_dir)
            os.makedirs(self.pdfminer_dir)
            os.makedirs(self.standard_dir)
            os.makedirs(self.submitted_dir)
            os.makedirs(self.visuals_dir)

        if not os.path.exists(self.submitted_dir):
            os.makedirs(self.submitted_dir)

        if not os.path.exists(self.standard_dir):
            os.makedirs(self.standard_dir)

    def pdfminer_handler(self, path, submitted, standard):
        """
        Function using pdfminer to extract text from pdfs and
        store them into an array of text files
        """
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
                logger.getLogger().debug(bcolors.OKBLUE + "Already Exits: "
                                         + bcolors.ENDC + file)
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
                    text_file = self.open_file(submitted, standard, pdf_saved)

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

    def docx_handler(self, path, submitted, standard):
        """
        Function using docx library to extract text from word docs and
        store them into an array of text files
        """
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

            file = os.path.splitext(file)[0]
            text_file = self.open_file(submitted, standard, doc_saved)
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
            csv_filename = self.csv_dir + "data-" + random.randrange(0, 100) + ".csv"
            logger.getLogger().debug("Opening File for csv: " + csv_filename)
            csv__ = open(csv_filename, 'w+')
            self.csv_path = csv_filename
            with open(csv_filename, 'a+', newline='') as outputFile:
                logger.getLogger().debug("csv file opened: " + csv_filename)

                writer = csv.writer(outputFile, dialect='excel')
                logger.getLogger().debug("csv created: " + csv_filename)
                writer.writerows(txt)

                outputFile.close()
                return True, csv_filename
        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    def csv_with_headers(self, std_path, sub_path, std_data, sub_data):

        logger.getLogger().info("Creating a CSV with headers")

        std_path = ''.join(str(item) for sublist in std_path
                           for item in sublist)
        sub_path = ''.join(str(item) for sublist in sub_path
                           for item in sublist)

        std_file = os.path.basename(std_path)
        sub_file = os.path.basename(sub_path)

        std_name = os.path.splitext(std_file)[0]
        sub_name = os.path.splitext(sub_file)[0]
        std_name = "(" + std_name[:10] + ")"
        sub_name = "(" + sub_name[:10] + ")"

        try:
            csv_filename = self.csv_dir + sub_name + "VS" + std_name + ".csv"

            logger.getLogger().debug("Opening File for csv: " + csv_filename)

            with open(csv_filename, 'w') as outputfile:
                myFields = ['Document Type', 'Document', 'Text']
                writer = csv.DictWriter(outputfile, fieldnames=myFields)
                writer.writeheader()
                writer.writerow({'Document Type': 'standard',
                                'Document': std_name, 'Text': std_data})
                writer.writerow({'Document Type': 'submission',
                                'Document': sub_name, 'Text': sub_data})

                return csv_filename

        except RuntimeError as error:
            logger.getLogger().error(error)
            sys.exit(1)

    def open_file(self, submitted, standard, path):
        """
        Creates/Opens text files with input file name.
        """
        file = os.path.basename(path)
        if submitted is True:
            txt_filename = self.submitted_dir + file
            txt_filename = os.path.splitext(txt_filename)[0] + '.txt'
        elif standard is True:
            txt_filename = self.standard_dir + file
            txt_filename = os.path.splitext(txt_filename)[0] + '.txt'
        else:
            txt_filename = path

        logger.getLogger().debug("File opened for writing - {}"
                                 .format(txt_filename))
        self.txt.append(txt_filename)
        return open(txt_filename, "w")

    def file_count(self, files):
        """
        Gets the file count from a list of files
        """
        count = 0
        for file in files:
            count += 1
        return count
