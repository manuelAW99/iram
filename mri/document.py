import string
from nltk.corpus import stopwords

class document:
    def __init__(self, subject, text, language, use_nltk, d_id = -1):
        self._d_id = d_id
        self._subject = subject
        self._text = text
        self._terms = {}
        self._weight = {}
        self._language = language
        self._use_nltk = use_nltk
        self._engine_text()
    
    def get_text(self):
        return self._text
    
    def get_term(self, term):
        return self._terms[term]
    
    def get_terms(self):
        return self._terms
    
    def get_term_most_common(self):
        return self._terms.most_common(1)[0][1]
    
    def get_subject(self):
        return self._subject
    
    def set_subject(self, subject):
        self._subject = subject
        return self._subject
    
    def get_weights(self):
        return self._weight
    
    def get_weight(self, term):
        return self._weight[term]
    
    def set_weight(self, term, value):
        self._weight[term] = value
        return self._weight
    
    def get_language(self):
        return self._language
    
    def use_nltk(self):
        return self._use_nltk
    
    def _engine_text(self):
        current = ''
        for char in self.get_text():
            if char == ' ' or char == '\n' or char in string.punctuation:
                if current == '':
                    continue
                current = current.lower()
                if current in self.get_terms().keys():
                    self._terms[current] += 1
                else:
                    self._terms[current] = 1
                current = ''
            else:
                current += char
        if current in self._terms:
            self._terms[current] += 1
        else:
            self._terms[current] = 1
        
        if self.use_nltk():
            sw = stopwords.words(self.get_language())
            new_terms = {}
            for token in self._terms.keys():
                if token not in sw:
                    new_terms[token] = self._terms[token]
            self._terms = new_terms