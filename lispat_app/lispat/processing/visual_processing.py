import os
import spacy
import scattertext as st

nlp = spacy.load('en')


class Visualization:

    def __init__(self):
        pass

    def standard(self, dataframe):
        corpus = st.CorpusFromPandas(dataframe, category_col='Document',
                                     text_col='Text', nlp=nlp).build()

        html = st.produce_scattertext_explorer(corpus, category='Submission',
                                               category_name='Submission',
                                               not_category_name='Standard',
                                               width_in_pixels=1000)

        open("Standard-Visualization.html", 'wb').write(html.encode('utf-8'))
