import os
import sys
import spacy
import pickle
import shutil
import pandas as pd
import gensim.models.word2vec as w2v
import sklearn.manifold
import multiprocessing
from textblob import TextBlob
from lispat.utils.logger import Logger
from lispat.factory.filtered_factory import FilteredFactory
from lispat.base.constants import DESIRED_TERMS
import mpld3
import webbrowser
from mpld3 import plugins, utils

logger = Logger("Modeling")


class NLPModel:
    def __init__(self):
        self.sent_list = None
        self.nlp = spacy.load('en_core_web_sm')
        self.filter = FilteredFactory()

    def data_frame(self, path):
        '''
        This function takes the test.csv file and turns it into a
        usable dataframe.
        :return:
        '''
        try:
            print(path)
            logger.getLogger().info("Running information on text dataframe.")
            # A word count on each sentence. not sure if helpful...

            train = pd.read_csv(path, names=["ID", "sentence"])
            train['word_count'] = (train['sentence'].apply
                                   (lambda x: len(str(x).split(" "))))
            train['filtered'] = (train['sentence'].apply
                                 (lambda x: self.filter.tokenize(x)))

            train['desired_phrase'] = (train['filtered'].apply(lambda x:
                                       self.filter.get_desired_phrase(x)))
            train['desired_phrase'] = (train['desired_phrase'].apply(lambda x:
                                       self.filter.punctuation(x)))
            train['desired_phrase'] = (train['desired_phrase'].apply(lambda x:
                                       self.filter.stemmer(x)))
            train_pe = train[train['desired_phrase'].map(lambda x: len(x)) > 0]

            train['desired_term'] = (train['filtered'].apply(lambda x:
                                     self.filter.get_desired_terms(x)))
            train_te = train[train['desired_term'].map(lambda x: len(x)) > 0]

            frames = [train_pe, train_te]
            df = pd.concat(frames)
            df.drop('ID', axis=1, inplace=True)

            df.reset_index(drop=True)
            df.reindex()
            print(df)

            headers = ["desired_term", "Desired_phrase",
                       "sentences", "word_count"]

            df.to_csv('/usr/local/var/lispat/csv_data/output.csv',
                      encoding='utf-8', columns=headers)

            logger.getLogger().debug("Showing the ngram for the 30th"
                                     "row in the DF")
            for w in TextBlob(train['sentence'][30]).ngrams(6):
                print(w)

        except RuntimeError:
            logger.getLogger().debug("Error with Dataframe calculation")
            sys.exit(1)

    def save_trained(self, word_array):
        '''
        :param word_array: an array of words that will be saved
         as a object for now..
        :return: None
        '''
        try:

            logger.getLogger().info("Saving the trained model")
            if os.path.isdir("/usr/local/var/lispat/objects"):
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')
            else:
                os.makedirs("/usr/local/var/lispat/objects/")
                obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'wb')

            obj = word_array

            pickle.dump(obj, obj_file)
            logger.getLogger().debug("Object successfully saved")
        except RuntimeError as e:
            logger.getLogger().debug("Run time error saving the object")
            sys.exit(1)

    def compare_doc_similarity(self, path):
        '''
        :param path: path to submission file.
        :return: None

        TODO: Clean this up and make the comparison give better feedback.
        Use Gensim instead of spaCy..
        '''
        try:
            logger.getLogger().info("Comparing document similarity")
            data_path = "/usr/local/var/lispat/pdf_data/"
            txt1 = ""
            try:
                for file in os.listdir(data_path):
                    __file = open(data_path + file, 'rt')
                    __text = __file.read()
                    txt1 += __text
            except RuntimeError as error:
                logger.getLogger().error("Word filter - ", error)

            # This is for using the saved object...
            # logger.getLogger().info("Getting object from disk")
            # obj_file = open("/usr/local/var/lispat/objects/doc.obj", 'rb')

            head, tail = os.path.split(path)
            file = os.path.splitext(tail)[0]
            submitted = open("/usr/local/var/lispat/submission/" + file +
                             ".txt", 'rt')

            # obj = pickle.load(obj_file)
            # txt = " ".join(obj)
            txt2 = submitted.read()

            txt1_len = len(txt1)

            self.nlp.max_length = txt1_len + 1
            doc1 = self.nlp(txt1)
            doc2 = self.nlp(txt2)

            similarity = doc2.similarity(doc1)
            logger.getLogger().debug("Document Similarity is " +
                                     str(similarity))
            shutil.rmtree("/usr/local/var/lispat/submission")

        except RuntimeError as error:
            logger.getLogger().error("Error with comparing the two"
                                     "documents with spaCy")
            shutil.rmtree("/usr/local/var/lispat/submission")
            sys.exit(1)

    def build_sents(self, sentences):
        nlp_array = []
        logger.getLogger().info("Building sentence Array")
        for i, sent in enumerate(sentences):
            nlp_array.append((i, sent))
        return nlp_array

    def semantic_properties_model(self, data, user_input=None):
        logger.getLogger().info("Building model, this may take a second...")

        input_txt = False
        if user_input is not None:
            input_txt = True

        token_count = len(data)
        # Hyper Parameter. Static for now.
        num_features = 1000
        min_word_count = 1
        num_workers = multiprocessing.cpu_count()
        context_size = 7
        downsampling = 1e-5
        seed = 1
        doc2vec = None
        if not os.path.exists("/usr/local/var/lispat/trained"):
            os.makedirs("/usr/local/var/lispat/trained")
        if os.path.isfile("/usr/local/var/lispat/trained/doc2vec.w2v"):
            doc2vec = w2v.Word2Vec.load("/usr/local/var/lispat/trained/doc2vec.w2v")
        else:
            doc2vec = w2v.Word2Vec(
                sg=1,
                seed=seed,
                workers=num_workers,
                size=num_features,
                min_count=min_word_count,
                window=context_size,
                sample=downsampling
            )

            doc2vec.build_vocab(data)
            logger.getLogger().debug("Word2Vec vocabulary length: " + str(len(doc2vec.wv.vocab)))
            doc2vec.train(data, epochs=doc2vec.iter, total_words=token_count)
            doc2vec.save('/usr/local/var/lispat/trained/doc2vec.w2v')

        tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
        all_word_vectors_matrix = doc2vec.wv.syn0
        all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)

        points = pd.DataFrame(
            [
                (word, coords[0], coords[1])
                for word, coords in [
                    (word, all_word_vectors_matrix_2d[doc2vec.wv.vocab[word].index])
                    for word in doc2vec.wv.vocab
                    ]
            ],
            columns=["word", "x", "y"]
        )

        sim = []
        sim_dic = {}
        if input_txt is True:
            """
            This algorithm takes in a use input of txt. 
            It will lower and append the most similar values from the algorithm,
            to a list. From there we need to convert the values from the dataframe
            into a hash table to be able to quickly access values and return 
            rows needed that hold the same coordinates as the value 
            """
            for i in user_input:
                try:
                    sim.append(doc2vec.most_similar(str(i).lower()))
                    sim_dic[i] = doc2vec.most_similar(str(i).lower())
                except Exception:
                    print("Word not found - " + i + " - Moving onto the next")
                    continue

            self.create_html_similarity(sim, user_input)
            ret = []
            f = {}
            for i, row in points.iterrows():
                f[row[0]] = (row[0], row[1], row[2])
            df = pd.DataFrame(columns=['word', 'x', 'y'])
            for row in sim:
                for i in row:
                    ret.append(f[i[0]])

            for i, row in enumerate(ret):
                df.loc[i] = [v for v in row]

            return df, points

        return points

    def print_full(self, x):
        pd.set_option('display.max_rows', len(x))
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 2000)
        pd.set_option('display.float_format', '{:20,.2f}'.format)
        pd.set_option('display.max_colwidth', -1)
        print(x)
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
        pd.reset_option('display.float_format')
        pd.reset_option('display.max_colwidth')

    def create_html_similarity(self, sim, user_input):
        print(sim)
        with open('/usr/local/var/lispat/similar.html', 'w') as file:
            file.write('<html>')
            file.write('<style>')
            file.write('table {font-family: arial, '
                       'sans-serif; border-collapse: '
                       'collapse; width: 100%;}')
            file.write('td, th {border: 1px solid '
                       '#dddddd; text-align: '
                       'left;padding: 8px;')
            file.write('tr:nth-child(even) {background-color: #dddddd;}')
            file.write('</style>')
            file.write('<body>')
            file.write('<h1>Most Similar Words between Standard and User Text Input </h1>')
            file.write('<table>')
            file.write('<tr>')
            for i in user_input:
                file.write('<th> %s </th>' % i)
            file.write('</tr>')
            file.write('<tr>')
            for i in range(0, len(sim[0])):
                file.write('<tr>')
                for j in range(0, len(sim)):
                    file.write('<td> %s </td>' % sim[j][i][0])
                file.write('</tr>')

            file.write('</tr>')
            file.write('</body>')
            file.write('</html>')
        webbrowser.open("file:///usr/local/var/lispat/similar.html")





class ClickInfo(plugins.PluginBase):

    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        obj.elements().on("mouseover",
                          function(d, i){alert("clicked on points[" + i + "]");});    
    }
    """

    def __init__(self, points):
        self.dict_ = {"type": "clickinfo",
                      "id": utils.get_id(points)}
