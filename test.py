import mri.sri as s, time
from nltk.corpus import wordnet

sri = s.sri()

sri.load_corpus("cran")
query = sri.create_query("in the line are the computer computation")
sri.insert_query(query)
temp = time.time()
rank = sri.ranking(query)
temp = time.time() - temp
print(temp)
"""
print(rank)
Cr = []
for d in range(len(rank)):
    if d > 6 and d < 10:
        Cr.append(rank[d][0])
Cnr = []
for d in range(len(rank)):
    if d <= 6:
        Cnr.append(rank[d][0])
retro = sri.retro(sri._querys[0], Cr, Cnr)
print()
print(retro)
#print(sri._documents[14]._terms['medical'])
"""
"""
def remove_punct_dict(self):
    return dict((ord(punct), None) for punct in string.punctuation)
    
def normalize(self, text):
    return nltk.word_tokenize(text.lower().translate(self.remove_punct_dict()))
    
def lem_tokens(self,lemmer, tokens):
    return [lemmer.lemmatize(token) for token in tokens]
def lem_normalize(self,text, lemmer):
    return self.lem_tokens(lemmer, self.normalize(text))
    
def tokenizer(self, text):
    text_norm = self.normalize(text)
    sent_text = nltk.sent_tokenize(text)
    #word_text = nltk.word_tokenize(text)
    #lemmer = nltk.stem.WordNetLemmatizer()
    #normalize = self.lem_normalize(text, lemmer)
    return text_norm
"""