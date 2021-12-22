import mri.sri as s
from nltk.corpus import wordnet

sri = s.sri()

sri.load_corpus("cran")
sri.insert_query("in the line are the computer computation")

rank = sri.ranking(sri._querys[0])
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