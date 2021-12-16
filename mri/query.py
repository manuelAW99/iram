import nltk, string, operator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


class query:
    def __init__(self, text):
        self._text = text
        self._terms = {}
        self._weight = {}
        self.engine_text()
        
    def engine_text(self):
        soup = BeautifulSoup(self._text, features='html.parser')
        text = soup.get_text(strip=True)
        tokens = word_tokenize(text)
        sw = stopwords.words('english')
        clean_tokens = [token for token in tokens if token not in sw]
        stemmer = PorterStemmer()
        stem_tokens = [stemmer.stem(word) for word in clean_tokens if word not in string.punctuation]
        freq = nltk.FreqDist(stem_tokens)
        self._terms = freq    
    
    def tokenizer(self, text):
        current = ''
        for char in text:
            if char == ' ' or char == '\n' or char in string.punctuation:
                if current == '':
                    continue
                current = current.lower()
                if current in self._terms.keys():
                    self._terms[current] += 1
                else:
                    self._terms[current] = 1
                current = ''
            else:
                current += char
        self._terms[current] = 1