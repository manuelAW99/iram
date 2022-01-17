import math as m, numpy as np
from nltk.stem import PorterStemmer

class framework:
    def __init__(self, use_nltk, sim):
        self._sim = sim
        self._use_nltk = use_nltk
    
    def use_nltk(self):
        return self._use_nltk
    
    def get_sim(self):
        return self._sim
    
    def tf(self, d, t):
        freq = 0
        freq_m = 1
        if t in d.get_terms().keys():
            freq = d.get_term(t)
            for k in d.get_terms().keys():
                if d.get_term(k) > freq_m:
                    freq_m = d.get_term(k)
        return freq/freq_m
    
    def idf(self, n, N):
        return m.log(N/n)
    
    def weight_doc(self, docs, terms, d, t):
        return self.idf(len(terms[t][1]), len(docs)) * self.tf(d, t)
    
    def weight_query(self, docs, terms, a, q, t):
        tf = self.tf(q, t)
        idf = self.idf(len(terms[t][1]), len(docs))
        return (a + (1-a)*(tf)) * idf
    
    def cosine_similarity(self, d, q, tree):
        weight = 0
        sum_d, sum_q = 0, 0
        if self.use_nltk():
            stemmer = PorterStemmer()
            for t in q.get_weights().keys():
                stem_term = stemmer.stem(t)
                if stem_term in tree.keys():
                    family = [tt for tt in tree[stem_term] if tt in d.get_weights().keys()]
                    mean = self.mean(family, d)
                    for tt in family:
                        w_d = d.get_weight(tt)
                        w_q = q.get_weight(t)
                        if t == tt:
                            weight += (w_d * w_q)
                        else:
                            weight += self.get_sim()*(w_d* w_q)
        else:
            for t in q.get_weights().keys():
                if t in d.get_weights().keys():
                    w_d = d.get_weight(tt)
                    w_q = q.get_weight(t)
                    weight += (w_d * w_q)
                
        vec_d, vec_q = list(d.get_weights().values()), list(q.get_weights().values())
        sum_d = np.linalg.norm(vec_d)
        sum_q = np.linalg.norm(vec_q)
          
        return (weight/(sum_d * sum_q)) if (sum_d * sum_q) > 0 else 0
    
    def mean(self, terms, doc):
        mean = 0
        if len(terms) > 0:
            for t in terms:
                mean += doc.get_weight(t)
            mean /= len(terms)
        return mean