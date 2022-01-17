import mri.sri as s, time
from matplotlib import pyplot as plt
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

def parse_query():
    file = open('./test/cran.qry','r')
    querys = []
    current_text = ''
    while 1:
        line = file.readline()
        c_line = len(line.split())
        if c_line and (line.find('.I')!=-1 or not line):
            if current_text != '':
                querys.append(current_text)
                current_text = ''
        elif c_line and line.find('.W')!=-1:
            continue
        else:
            current_text += line
        if not line:
            break
    return querys

def parse_rel():
    file = open('./test/cranqrel','r')
    querys = {}
    while 1:
        line = file.readline()
        if not line:
            break
        c_q = line.split()[0]
        if c_q in querys.keys():
            querys[c_q].append(line.split()[1])
        else:
            querys[c_q] = [line.split()[1]]
    return querys

def mean(l):
    mean = 0
    if len(l) > 0:
        for e in l:
            mean += float(e)
        mean /= len(l)
    return mean


querys = parse_query()
rel = parse_rel()
pre = []
recall = []
F1 = []

for i in range(len(querys)):
    query=sri.create_query(querys[i])
    sri.insert_query(query)
    rank = sri.ranking(query)
    rr = 0
    ri = 0
    nr = 0
    ni = 0
    for d in rank:
        if d[0]._d_id in rel[str(i+1)]:
            rr+=1
        else:
            ri+=1
    nr = len(rel[str(i+1)])-rr
    p = rr/(rr+ri) if rr+ri >0 else 0
    r = rr/(rr+nr) if rr+nr >0 else 0
    f1 = 2/(1/p + 1/r) if p != 0 and r != 0 else 0
    pre.append(p)
    recall.append(r)
    F1.append(f1)
    
means_p = [mean(pre[:1]),mean(pre[:5]), mean(pre[:15]), mean(pre[:35]), 
         mean(pre[:60]),mean(pre[:80]),mean(pre[:120]),mean(pre[:160]),mean(pre)]

means_r = [mean(recall[:1]),mean(recall[:5]), mean(recall[:15]), mean(recall[:35]), 
         mean(recall[:60]),mean(recall[:80]),mean(recall[:120]),mean(recall[:160]),mean(recall)]

means_f1 = [mean(F1[:1]),mean(F1[:5]), mean(F1[:15]), mean(F1[:35]), 
         mean(F1[:60]),mean(F1[:80]),mean(F1[:120]),mean(F1[:160]),mean(F1)]

print(means_p)
print(means_r)
print(means_f1)

x = [1,5,15,35,60,80,120,160,225]
plt.plot(x,means_p, label = 'Precision')
plt.plot(x,means_r, label = 'Recall')
plt.plot(x,means_f1, label = 'F1')
plt.xlabel('Documents')
plt.ylabel('Value')
plt.grid(True)
leg = plt.legend(loc=9,ncol=2, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()

