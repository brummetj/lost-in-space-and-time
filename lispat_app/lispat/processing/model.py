import gensim
from lispat.utils.logger import Logger
logger = Logger("Modeling")

class GensimModel:
    def __init__(self):
        self.train = None
        self.model = None

    def train(self, docs):

        self.model = gensim.models.Word2Vec(
            docs,
            size=150,
            window=10,
            min_count=2,
            workers=10
        )
        self.model.train(docs, total_examples=len(docs), epochs=10)

    def get_model(self):
        return self.model
