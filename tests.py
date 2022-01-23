import mri.sri as s, time
from matplotlib import pyplot as plt
from nltk.corpus import wordnet

sri = s.sri()

sri.load_corpus("cran")



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
time_t = []
tuples = []
mean_t = []
def test():
    for i in range(len(querys)):
        time_p = time.time()
        query = sri.create_query(querys[i])
        sri.compare_query(query)
        query = sri.insert_query(query)
        rank = sri.ranking(query) if len(query.get_relevants()) == 0 else sri.retro(query)
        time_p = time.time() - time_p
        rr = 0
        ri = 0
        nr = 0
        ni = 0
        for d in rank:
            if d[0]._d_id in rel[str(i+1)]:
                rr+=1
                query.set_relevant(d[0])
            else:
                ri+=1
            query.set_not_relevant(d[0])
        nr = len(rel[str(i+1)])-rr
        p = rr/(rr+ri) if rr+ri >0 else 0
        r = rr/(rr+nr) if rr+nr >0 else 0
        if r == 0 and p == 0:
            f1 = 0
        elif r == 0 and p != 0:
            f1 = 2/(1/p)
        elif r!=0 and p == 0:
            f1 = 2/(1/r)
        else:
            f1 = 2/((1/r) + (1/p))
        #f1 = (2*p*r)/(p+r) if p + r > 0 else 0
        pre.append(p)
        recall.append(r)
        F1.append(f1)
        tuples.append([r,p])
        time_t.append(time_p)

test()
test()
pos = 0
list_length = len(tuples)  
for i in range(0, list_length):  
    for j in range(0, list_length-i-1):  
        if (tuples[j][pos] > tuples[j + 1][pos]):  
            temp = tuples[j]  
            tuples[j]= tuples[j + 1]  
            tuples[j + 1]= temp  

for i in tuples:
    mean_t.append(((i[0]+i[1])/2))
 
aaaa = []   
for i in range(len(pre)):
    aaaa.append(mean(pre[:i]))
    
bbbb = []
for i in range(len(pre)):
    bbbb.append(mean(recall[:i]))
    
print(means_p)
print(means_r)
print(means_f1)


x = [25,50,75,100,125,150,175,200,225]
means_p = [mean(pre[:25]),mean(pre[:50]), mean(pre[:75]), mean(pre[:100]), 
         mean(pre[:125]),mean(pre[:150]),mean(pre[:175]),mean(pre[:200]),mean(pre)]

means_r = [mean(recall[:25]),mean(recall[:50]), mean(recall[:75]), mean(recall[:100]), 
         mean(recall[:125]),mean(recall[:150]),mean(recall[:175]),mean(recall[:200]),mean(recall)]

means_f = [mean(F1[:25]),mean(F1[:50]), mean(F1[:75]), mean(F1[:100]), 
         mean(F1[:125]),mean(F1[:150]),mean(F1[:175]),mean(F1[:200]),mean(F1)]

plt.plot(x,means_p, label = 'Precisión')
plt.plot(x,means_r, label = 'Recobrado')
plt.plot(x,means_f1, label = 'F1')
plt.xlabel('consultas')
plt.ylabel('valor')
plt.title("Métricas de Evaluación\numbral: 0.145 | nltk: 1")
plt.grid(True)
leg = plt.legend(loc=9,ncol=2, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()

means_t = [mean(time_t[:25]),mean(time_t[:50]), mean(time_t[:75]), mean(time_t[:100]), 
         mean(time_t[:125]),mean(time_t[:150]),mean(time_t[:175]),mean(time_t[:200]),mean(time_t)]
plt.plot(x, means_t, label='Time vs. Querys')
plt.xlabel('consultas')
plt.ylabel('tiempo')
plt.title("Tiempo que demora la recuperación\numbral: 0.12 | nltk: 0")
plt.grid(True)
plt.show()


"""
------------------------------------
Basura
------------------------------------

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