import math as m, numpy as np

class framework:    
    def tf(self, d, t):
        freq = 0
        freq_m = 0
        if t in d._terms.keys():
            freq = d._terms[t]
            freq_m = d._terms.most_common(1)[0][1]
        return freq/freq_m
    
    def idf(self, n, N):
        return m.log(N/n)
    
    def weight_doc(self, docs, terms, d, t):
        return self.idf(len(terms[t][1]), len(docs)) * self.tf(d, t)
    
    def weight_query(self, docs, terms, a, q, t):
        freq = q._terms[t]
        freq_m = q._terms.most_common(1)[0][1]
        return (a + (1-a)*(freq/freq_m)) * self.idf(len(terms[t][1]), len(docs))
    
    def cosine_similarity(self, d, q):
        weight = 0
        sum_d, sum_q = 0, 0
        for t in q._weight.keys():
            if t in d._weight.keys():
                w_d = d._weight[t]
                w_q = q._weight[t]
                weight += w_d * w_q
        vec_d, vec_q = list(d._weight.values()), list(q._weight.values())
        sum_d = np.linalg.norm(vec_d)
        sum_q = np.linalg.norm(vec_q)
            
        return weight/(sum_d * sum_q)
        
        #return weight
    
    
        