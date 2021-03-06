import string
from nltk.corpus import stopwords

class query:
    def __init__(self, text, use_nltk, language):
        self._text = text
        self._terms = {}
        self._weight = {}
        self._relevant = []
        self._not_relevant = []
        self._language = language
        self._use_nltk =  use_nltk
        self._engine_text()
        
    def get_text(self):
        return self._text
    
    def get_term(self, term):
        return self._terms[term]
    
    def get_terms(self):
        return self._terms
    
    def get_term_most_common(self):
        return self._terms.most_common(1)[0][1]
    
    def get_weights(self):
        return self._weight
    
    def get_weight(self, term):
        return self._weight[term]
    
    def set_weight(self, term, value):
        self._weight[term] = value
        return self._weight
    
    def set_relevant(self, doc):
        if doc not in self._relevant:
            self._relevant.append(doc)
        return self._relevant
    
    def set_not_relevant(self, doc):
        if doc not in self._not_relevant:
            self._not_relevant.append(doc)
        return self._not_relevant
    
    def get_relevants(self):
        return self._relevant
    
    def get_not_relevants(self):
        return self._not_relevant
    
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
            sw = stopwords.words(self._language)
            new_terms = {}
            for token in self._terms.keys():
                if token not in sw:
                    new_terms[token] = self._terms[token]
            self._terms = new_terms