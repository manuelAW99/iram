import mri.sri as s, time
from nltk.corpus import wordnet

sri = s.sri()

sri.load_corpus("cran")

"""
import nltk, string, operator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

if self.use_nltk():
    freq_m = d.get_term_most_common()
                
soup = BeautifulSoup(self._text, features='html.parser')
text = soup.get_text(strip=True)
tokens = word_tokenize(text)
sw = stopwords.words(self.get_language())
clean_tokens = [token for token in tokens if token not in sw]
stemmer = PorterStemmer()
stem_tokens = [stemmer.stem(word) for word in clean_tokens if word not in string.punctuation]
freq = nltk.FreqDist(stem_tokens)
self._terms = freq
"""

query = sri.create_query("in the line are the computer computation")
sri.insert_query(query)


temp = time.time()
rank = sri.ranking(query)
temp = time.time() - temp
print(temp)
