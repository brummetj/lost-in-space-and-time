import os
import sys
import spacy
import pickle
import shutil
import pandas as pd
from lispat.utils.logger import Logger
from lispat.utils.colors import bcolors
from lispat.processing.model_processing import NLPModel
from lispat.factory.document_factory import DocumentFactory
from lispat.factory.argument_factory import ArgumentFactory
from lispat.processing.pre_processing import Preproccessing
from lispat.processing.visual_processing import Visualization

nlp = spacy.load('en')

logger = Logger("CommandManager")


class CommandManager:
    """
    CommandManager will be used to handle multiple tasks.
    Such as spin off threads, handle command line inputs,
    and create the necessary communication between sources.
    """

    def __init__(self):
        self.keys = None
        self.path = None
        self.sub_path = None
        self.db = None
        self.noise_filter = None
        self.doc_worker = None
        self.model = NLPModel()

    def create_path(self, path, sub_path=None):
        """
        :param path: path user declared to processing docs
        :return: class variable of the path
        """
        try:
            logger.getLogger().info("Command Manager - Init")
            full_path = os.path.abspath(path)

            if sub_path is not None:
                sub_full_path = os.path.abspath(sub_path)
                if os.path.isfile(sub_full_path):
                    logger.getLogger().info("CommandManager created "
                                            "submission path: {}"
                                            .format(sub_full_path))
                    self.sub_path = sub_full_path

            if os.path.isdir(full_path):
                logger.getLogger().info("CommandManager created with path={}"
                                        .format(full_path))
                self.path = full_path
            elif os.path.isfile(full_path):
                logger.getLogger().info("CommandManager created with path={}"
                                        .format(full_path))
                self.path = full_path
            else:
                raise RuntimeError

        except RuntimeError as error:
            logger.getLogger().error("Directory does not exist")
            sys.exit(1)

    def run_analytics(self, args):
        """
        Main run function to handle learning
        :return: Exit code
        """
        # Initialize with our docs.
        logger.getLogger().info("Command Manager - Run")
        try:
            doc_worker = None
            if args['--compare']:
                doc_worker = DocumentFactory(self.path, True, False)
            elif args['--train']:
                doc_worker = DocumentFactory(self.path, False, False)
            else:
                raise RuntimeError("No arguments found, please try using "
                                   "--compare or --train")

            docs = doc_worker.convert_file()
            filter = Preproccessing(docs[0], docs[1])

            if args['-A']:
                filter.get_docs_dir(args)
            else:
                filter.get_doc()

            if args['--array']:
                filter.filter_nlp()
                filter.word_count()
                self.keys = filter.get_word_count()

            if args['--df']:
                nlp_array_unfiltered = self.model.build_sents(filter.nlp.sents)
                print(nlp_array_unfiltered[:5])
                csv_success = self.doc_worker.args_.csv_handler(nlp_array_unfiltered)
                if csv_success:
                    self.model.data_frame(self.doc_worker.args_.csv_path)

            if args['--sp']:
                vis = Visualization()
                sentences = []
                raw_sentences = filter.get_sentences()
                for raw_sentence in raw_sentences:
                    if len(raw_sentence) > 0:
                        sentences.append(filter.get_sent_tokens(raw_sentence))

                file = os.path.basename(self.path)
                points = self.model.semantic_properties_model(sentences)
                vis.nearest(points1=points, file1=file)


            # TODO: figure out how we can make it so we don't need to check this again...

            if args['--compare']:
                self.model.compare_doc_similarity(self.path)
            if args['--train']:
                self.model.save_trained(filter.word_array)

        except RuntimeError as error:
            logger.getLogger().error(error)
            exit(1)

    def run_sub_vs_std(self, args):
        """
        This function is to handle the comparison of two submissions with the
        command line.
        :param args: command line arguments
        :return: N/A
        """

        logger.getLogger().info("Command Manager - Run Submission vs Standard")

        try:
            args_ = ArgumentFactory()

            doc_std = DocumentFactory(self.path, False, True)
            doc_sub = DocumentFactory(self.sub_path, True, False)

            doc_std_converted = doc_std.convert_file()
            doc_sub_converted = doc_sub.convert_file()

            filter_std = Preproccessing(doc_std_converted[0],
                                        doc_std_converted[1])
            filter_sub = Preproccessing(doc_sub_converted[0],
                                        doc_sub_converted[1])

            if args['--clean']:
                filter_std.filter_nlp()
                filter_sub.filter_nlp()

            std_data = filter_std.ret_doc()
            sub_data = filter_sub.ret_doc()

            std_size = len(std_data)
            sub_size = len(sub_data)

            if(std_size > sub_size):
                nlp.max_length = std_size + 1
            else:
                nlp.max_length = sub_size + 1

            std_path = ""
            sub_path = ""
            if doc_std_converted[0]:
                std_path = doc_std_converted[0]
            elif doc_std_converted[1]:
                std_path = doc_std_converted[1]

            if doc_sub_converted[0]:
                sub_path = doc_sub_converted[0]

            elif doc_sub_converted[1]:
                sub_path = doc_sub_converted[1]

            csv = args_.csv_with_headers(std_path, sub_path,
                                         std_data, sub_data)

            dataframe = pd.read_csv(csv, names=["Document Type",
                                    "Document", "Text"])

            vis = Visualization(nlp)

            if args['--empath']:
                vis.empath(dataframe)
            elif args['--gitc']:
                vis.gitc(dataframe)
            elif args['--character']:
                vis.chrctrstc(dataframe)
            elif args['--nn']:

                sentences_sub = []
                raw_sentences_sub = filter_sub.get_sentences()
                for raw_sentence in raw_sentences_sub:
                    if len(raw_sentence) > 0:
                        sentences_sub.append(filter_sub.get_sent_tokens(raw_sentence))

                sentences_std = []
                raw_sentences_std = filter_std.get_sentences()
                for raw_sentence in raw_sentences_std:
                    if len(raw_sentence) > 0:
                        sentences_std.append(filter_std.get_sent_tokens(raw_sentence))

                file1 = os.path.basename(self.path)
                file2 = os.path.basename(self.sub_path)
                points_sub = self.model.semantic_properties_model(sentences_sub)
                points_std = self.model.semantic_properties_model(sentences_std)
                vis.nearest(points1=points_std, points2=points_sub, file1=file1, file2=file2)

            #if not args['--empath'] and not args['--gitc'] and not args['--character'] and not args['--nn']:
            else:
                vis.standard(dataframe)

        except RuntimeError as error:
            logger.getLogger().error("Error with run_sub_vs_std please "
                                     "check stack trace")
            exit(1)

    def run_sub_vs_txt(self, args):
        args_ = ArgumentFactory()
        vis = Visualization(nlp)
        doc_std = DocumentFactory(self.path, False, True)
        doc_std_converted = doc_std.convert_file()
        filter_std = Preproccessing(doc_std_converted[0],
                                    doc_std_converted[1])
        std_data = filter_std.ret_doc()
        if args['--clean']:
            filter_std.filter_nlp()

        std_path = ""
        if doc_std_converted[0]:
            std_path = doc_std_converted[0]
        elif doc_std_converted[1]:
            std_path = doc_std_converted[1]

        sentences_sub = []
        raw_sentences_sub = filter_std.get_sentences()
        for raw_sentence in raw_sentences_sub:
            if len(raw_sentence) > 0:
                sentences_sub.append(filter_std.get_sent_tokens(raw_sentence))

        input_txt = filter_std.get_sent_tokens(str(args['--text']))
        file1 = os.path.basename(self.path)
        points_input, points_std = self.model.semantic_properties_model(sentences_sub, user_input=input_txt)
        vis.nearest(points1=points_std, points2=points_input, file1=file1, file2="User Input")


    @staticmethod
    def clean(args):
        """
        :param args: Arguments for which dirs to delete
        :return: Deleted dirs for file system storage
        """
        try:
            print("Purging local storaged")
            if args['--all']:
                shutil.rmtree("/usr/local/var/lispat/submission")
                shutil.rmtree("/usr/local/var/lispat/pdf_data")
                shutil.rmtree("/usr/local/var/lispat/csv_data")
                shutil.rmtree("/usr/local/var/lispat/standard")
                shutil.rmtree("/usr/local/var/lispat/docx_data")
            print("Finished")
        except RuntimeError:
            logger.getLogger().error("Error cleaning storage")
