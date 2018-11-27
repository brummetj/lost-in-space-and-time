import tensorflow as tf
import heapq
import pickle
import numpy as np
from lispat.utils.logger import Logger
from keras.optimizers import RMSprop
from keras.layers import LSTM, Dropout
from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Dropout, RepeatVector


logger = Logger("Prediction Model")


class Predict:

    def __init__(self):

        np.random.seed(42)
        tf.set_random_seed(42)

        file = r"/usr/local/var/lispat/pdf_data/A.6_NIST 800-53 Security and Privacy Controls for Federal Information Systems and Organizations.txt"

        self.data = open(file).read().lower()

        self.corpus_length = len(self.data)
        self.chars = sorted(list(set(self.data)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        self.unique_chars = len(self.chars)
        # Cutting data to chunks of 40 characters
        # ? Should modify to average character per sentence?
        self.SEQUENCE_LENGTH = 40
        # Sequence spacing
        self.step = 3
        self.sentences = []
        self.next_chars = []

        self.model_file_name = file + "_model.h5"
        self.history_file_name = file + "_history.p"

    def train(self):
        for i in range(0, len(self.data) - self.SEQUENCE_LENGTH, self.step):
            self.sentences.append(self.text[i: i + self.SEQUENCE_LENGTH])
            self.next_chars.append(self.text[i + self.SEQUENCE_LENGTH])

        self.training_samples = len(self.sentences)

        self.X = np.zeros((len(self.sentences), self.SEQUENCE_LENGTH,
                           len(self.chars)), dtype=np.bool)

        self.y = np.zeros((len(self.sentences), len(self.chars)),
                          dtype=np.bool)

        for i, sentence in enumerate(self.sentences):
            for t, char in enumerate(sentence):
                self.X[i, t, self.char_indices[char]] = 1
            self.y[i, self.char_indices[self.next_chars[i]]] = 1

        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=(self.SEQUENCE_LENGTH,
                                              len(self.chars))))
        self.model.add(Dense(len(self.chars)))
        self.model.add(Activation('softmax'))

        self.optimizer = RMSprop(lr=0.01)

        self.model.compile(loss='categorical_crossentropy',
                           optimizer=self.optimizer, metrics=['accuracy'])

        self.history = self.model.fit(self.X, self.y, validation_split=0.05,
                                      batch_size=128, epochs=20,
                                      shuffle=True).history

        self.model.save(self.model_file_name)

        pickle.dump(self.history, open(self.history_file_name, "wb"))

        self.history = pickle.load(open(self.history_file_name, "rb"))

    def prepare_input(self, text):
        x = np.zeros((1, self.SEQUENCE_LENGTH, len(self.chars)))
        for t, char in enumerate(text):
            x[0, t, self.char_indices[char]] = 1.

        return x

    def sample(self, preds, top_n=3):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds)
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)

        return heapq.nlargest(top_n, range(len(preds)), preds.take)

    def predict_completion(self, text):
        #self.model = load_model(self.model_file_name)
        original_text = text
        generated = text
        completion = ''
        while True:
            x = self.prepare_input(self.data)
            preds = self.model.predict(x, verbose=0)[0]
            next_index = self.sample(preds, top_n=1)[0]
            next_char = self.indices_char[next_index]
            self.data = self.data[1:] + next_char
            completion += next_char

            if (len(original_text + completion) + 2 > len(original_text) and
               next_char == ' '):
                return completion

    def predict_completions(self, text, n=3):
        self.model = load_model('/usr/local/var/lispat/keras_model.h5')
        x = self.prepare_input(text)
        preds = self.model.predict(x, verbose=0)[0]
        next_indices = self.sample(preds, n)
        return [self.indices_char[idx] + self.predict_completion(text[1:]
                + self.indices_char[idx]) for idx in next_indices]

    def output(self, line):
        for l in line:
            seq = l[:40].lower()
            print(seq)
            print(self.predict_completions(seq, 5))
            print()

    def stats(self):
        print(f'Corpus Length:  {self.corpus_length}')
        print(f'Unique Characters:  {self.unique_chars}')
        print(f'Training Samples: {self.trianing_samples}')
