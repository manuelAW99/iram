import nltk, string, operator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

class document:
    def __init__(self, subject, text):
        self._subject = subject
        self._text = text
        self._terms = {}
        self._weight = {}
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
    
    def _engine_text(self):
        soup = BeautifulSoup(self._text, features='html.parser')
        text = soup.get_text(strip=True)
        tokens = word_tokenize(text)
        sw = stopwords.words('english')
        clean_tokens = [token for token in tokens if token not in sw]
        stemmer = PorterStemmer()
        stem_tokens = [stemmer.stem(word) for word in clean_tokens if word not in string.punctuation]
        freq = nltk.FreqDist(stem_tokens)
        self._terms = freq
