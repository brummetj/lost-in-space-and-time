import os
import spacy
import scattertext as st

nlp = spacy.load('en')


class Visualization:

    def __init__(self):
        pass

    def standard(self, dataframe):
        corpus = st.CorpusFromPandas(dataframe, category_col='Document Type',
                                     text_col='Text', nlp=nlp).build()

        html = st.produce_scattertext_explorer(corpus, category='submission',
                                               category_name='Submission',
                                               not_category_name='Standard',
                                               width_in_pixels=1000)

        open("Standard-Visual.html", 'wb').write(html.encode('utf-8'))

    def empath(self, dataframe):
        feat_builder = st.FeatsFromOnlyEmpath()
        empath_corpus = st.CorpusFromParsedDocuments(dataframe,
                                                     category_col=
                                                     'Document Type',
                                                     feats_from_spacy_doc=
                                                     feat_builder,
                                                     parsed_col='Text').build()

        html = st.produce_scattertext_explorer(empath_corpus,
                                               category='submission',
                                               category_name='Submission',
                                               not_category_name='Standard',
                                               width_in_pixels=1000,
                                               use_non_text_features=True,
                                               use_full_doc=True,
                                               topic_model_term_lists=
                                               feat_builder.
                                               get_top_model_term_lists())

        open("Empath-Visual.html", 'wb').write(html.encode('utf-8'))

    def gitc(self, dataframe):
        general_inquirer_feature_builder = st.FeatsFromGeneralInquirer()

        corpus = st.CorpusFromPandas(dataframe, category_col='Document Type',
                                     text_col='Text',
                                     nlp=st.whitespace_nlp_with_sentences,
                                     feats_from_spacy_doc=
                                     general_inquirer_feature_builder).build()

        html = st.produce_frequency_explorer(corpus, category='submission',
                                             category_name='Submission',
                                             not_category_name='Standard',
                                             use_non_text_features=True,
                                             use_full_doc=True,
                                             term_scorer=st.LogOddsRatioUninformativeDirichletPrior(),
                                             grey_threshold=1.96,
                                             width_in_pixels=1000,
                                             topic_model_term_lists=general_inquirer_feature_builder.get_top_model_term_lists())

        open("GITC-Visual.html", 'wb').write(html.encode('utf-8'))

    def chrctrstc(self, dataframe):
        corpus = (st.CorpusFromPandas(dataframe, category_col='Document Type',
                                      text_col='Text',
                                      nlp=st.whitespace_nlp_with_sentences)
                  .build().get_unigram_corpus().compact(
                  st.ClassPercentageCompactor(term_count=5, term_ranker=
                                              st.OncePerDocFrequencyRanker)))

        html = st.produce_characteristic_explorer(corpus, category='submission',
                                                  category_name='Submission',
                                                  not_category_name='Standard',)
        open('Characteristic-Visual.html', 'wb').write(html.encode('utf-8'))
