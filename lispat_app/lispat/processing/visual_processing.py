import os
import csv
import spacy
import pandas as pd
import scattertext as st

nlp = spacy.load('en')


class Visualization:

    def __init__(self, sub_path=None, std_path=None):
        """
        :param sub_path: All data coming from submission
        :param std_path: All data coming from standard
        """

        sub_file = os.path.basename(sub_path)
        std_file = os.path.basename(std_path)

        _sub_file = open(sub_path, 'rt')
        _sub_text = _sub_file.read()
        _std_file = open(std_path, 'rt')
        _std_text = _std_file.read()

        csv_filename = "test.csv"

        with open(csv_filename, 'w') as out_file:
            myFields = ['Document', 'Text']
            writer = csv.DictWriter(out_file, fieldnames=myFields)
            writer.writeheader()
            writer.writerow({'Document': sub_file, 'Text': _sub_text})
            writer.writerow({'Document': std_file, 'Text': _std_text})

            dataframe = pd.read_csv(csv_filename, names=["Document", "Text"])

            corpus = st.CorpusFromPandas(dataframe, category_col='Document', text_col='Text',nlp=nlp).build()

            html = st.produce_scattertext_explorer(corpus, category='FDA Content of Premarket Submissions for Management of Cybersecurity in Medical Devices (2014).txt', category_name='Submission', not_category_name='Standard', width_in_pixels=1000)
            open("Text-Visualization.html", 'wb').write(html.encode('utf-8'))
