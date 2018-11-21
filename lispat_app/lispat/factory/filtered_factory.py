

class FilteredFactory:

    def __init__(self):
        self.tokens = []
        self.stripped = None
        self.stop_words = None
        self.integers = None
        self.long_words = None
        self.lemmatization = None
        self.stemmer = None

    def lower(self, w):
        self.tokens.append(w)
        return w.lower()

    def translate(self, table, w):
        translated = w.translate(table)
        self.stripped.append(translated)
        return
