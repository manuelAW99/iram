import math as m, numpy as np

class framework:
    def __init__(self, use_nltk):
        self._use_nltk = use_nltk
    
    def use_nltk(self):
        return self._use_nltk
    
    def tf(self, d, t):
        freq = 0
        freq_m = 0
        if t in d.get_terms().keys():
            freq = d.get_term(t)
            if self.use_nltk():
                freq_m = d.get_term_most_common()
            else:
                for k in d.get_terms().keys():
                    if d.get_term(k) > freq_m:
                        freq_m = d.get_term(k)
        return freq/freq_m
    
    def idf(self, n, N):
        return m.log(N/n)
    
    def weight_doc(self, docs, terms, d, t):
        return self.idf(len(terms[t][1]), len(docs)) * self.tf(d, t)
    
    def weight_query(self, docs, terms, a, q, t):
        freq = q.get_term(t)
        freq_m = 0
        if self.use_nltk():
            freq_m = q.get_term_most_common()
        else:
            for k in q.get_terms().keys():
                if q.get_term(k) > freq_m:
                    freq_m = q.get_term(k)
        return (a + (1-a)*(freq/freq_m)) * self.idf(len(terms[t][1]), len(docs))
    
    def cosine_similarity(self, d, q):
        weight = 0
        sum_d, sum_q = 0, 0
        for t in q.get_weights().keys():
            if t in d.get_weights().keys():
                w_d = d.get_weight(t)
                w_q = q.get_weight(t)
                weight += w_d * w_q
        vec_d, vec_q = list(d.get_weights().values()), list(q.get_weights().values())
        sum_d = np.linalg.norm(vec_d)
        sum_q = np.linalg.norm(vec_q)
            
        return (weight/(sum_d * sum_q)) if (sum_d * sum_q) > 0 else 0
    
    