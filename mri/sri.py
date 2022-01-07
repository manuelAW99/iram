import os, math, pickle, numpy as np, operator
from nltk.corpus import wordnet
from mri import document as doc, query as q, framework as fw, parser

class sri:
    def __init__(self):
        self._corpus = None
        self._count = 0
        self._querys = []
        self.load_config()
        self._fw = fw.framework(self.use_nltk)
    
    """
    Work with corpus
    """
    def select_corpus(self):
        os.chdir("./corpus/")
        data = [element for element in os.listdir()]
        os.chdir('..')
        return data
    
    def load_corpus(self, corpus):
        self._rep = representation()
        self._corpus = corpus
        try:
            with open('./cache/'+corpus+'.rep','rb') as f:
                self._rep = pickle.load(f)
                f.close()
        except:
            r = "./corpus/" + corpus
            docs = self.explore_dir(r, [], r[:])
            for archive in docs:
                for d in archive:
                    self.add_document(d[0], d[1])
                    self._count += 1
            os.chdir('../..')
            self.inverted_indexes()
            self.calc_weight()
            with open('./cache/'+corpus+'.rep', 'wb') as f:
                pickle.dump(self._rep, f)
                f.close()
        return self._rep.get_documents()
    
    def explore_dir(self, r, docs, p):
        os.chdir(r)
        elements = os.listdir()
        for path in elements:
            if os.path.isdir(path):
                n_p = p+'/'+path
                self.explore_dir(path, docs, n_p)
                os.chdir('..')
            else:
                file = open(path,'r', errors='ignore')
                doc = parser.parse(self._corpus, file)
                docs.append(doc)
                file.close()
        return docs
    
    """
    Work with documents
    """
    def add_document(self, d, text):
        self.get_rep().get_documents().append(doc.document(d, text, self.language, self.use_nltk))
        return self.get_rep().get_documents()
    
    
    def inverted_indexes(self):
        for doc in self.get_rep().get_documents():
            for t in doc.get_terms().keys(): 
                if t in self.get_rep().get_terms().keys():
                    self.get_rep().set_term_in(t, self.get_rep().get_term_in(t, 0) + doc.get_term(t), 0)
                    self.get_rep().get_term_in(t, 1).append(doc)
                else: 
                    self.get_rep().set_term(t, [doc.get_term(t), [doc]])
    
    def calc_weight(self):
        for t in self.get_rep().get_terms().keys():
            for d in self.get_rep().get_term_in(t, 1):
                w = self.get_framework().weight_doc(self.get_rep().get_documents(), 
                                                    self.get_rep().get_terms(), d, t)
                d.set_weight(t, w)
        return self.get_rep().get_documents()
    
    """
    Work with querys
    """
    def get_querys(self):
        return self._querys
    
    def clean_querys(self):
        self._querys = []
        
    def create_query(self, text):
        query = q.query(text, self.use_nltk)
        return query
        
    def insert_query(self, query):
        self.calc_weight_query(query)
        self.get_querys().append(query)
        return query
    
    def compare_query(self, query):
        for q in self.get_querys():
            sim = self.get_framework().cosine_similarity(query, q)
            if sim > self.query_sim:
                for d in q.get_relevants():
                    query.set_relevant(d)
                for d in q.get_not_relevants():
                    query.set_not_relevant(d)
        return query
        
    def calc_weight_query(self, query):
        for t in query._terms.keys():
            if t in self.get_rep().get_terms().keys():
                w = self.get_framework().weight_query(self.get_rep().get_documents(), 
                                                      self.get_rep().get_terms(),self.querys_weight, query, t)
                query.set_weight(t, w)
        if self.use_nltk:
            for syn in wordnet.synsets(t):
                for lemma in syn.lemmas():
                    if lemma.name() in self.get_rep().get_terms().keys() and lemma.name() not in query.get_weights().keys():
                        w = .5 * self.get_framework().weight_query(self.get_rep().get_documents(), self.get_rep().get_terms(),
                                                                   self.querys_weight, query, lemma.name())
                        query.set_weight(lemma.name(), w)
        return query.get_weights()
      
    def ranking(self, q):
        rank = {}
        for d in self.get_rep().get_documents():
            cs = self.get_framework().cosine_similarity(d, q)
            if cs > 0:
                rank[d] = cs
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    
    def retro(self, q0):
        query = self.rocchio(q0, self.rocchio_values[0], self.rocchio_values[1], 
                             self.rocchio_values[2], q0.get_relevants(), q0.get_not_relevants())
        return self.ranking(query)
    
    def rocchio(self, q0, a , b, c, Cr, Cnr):
        qm = self.create_query(q0.get_text())
        self.calc_weight_query(qm)
        for t in qm.get_weights().keys():
            qm.set_weight(t, a*q0.get_weight(t))
        
        for d in Cr:
            for t in d.get_weights().keys():
                if t in qm.get_weights().keys():
                    qm.set_weight(t, qm.get_weight(t) + d.get_weight(t)*(b/len(Cr)))
                else:
                    qm.set_weight(t, d.get_weight(t))
            
        for d in Cnr:
            for t in d.get_weights().keys():
                if t in qm.get_weights().keys():
                    qm.set_weight(t, qm.get_weight(t) - d.get_weight(t)*(c/len(Cnr)))
                else:
                    qm.set_weight(t, d.get_weight(t))
        
        return qm
        
    def get_rep(self):
        return self._rep
    
    def get_framework(self):
        return self._fw
    
    def load_config(self):
        file = open('mri/config.cfg','r')
        self.language = file.readline().split()[2]
        self.query_sim = float(file.readline().split()[2])
        self.rocchio_values = [float(val) for val in file.readline().split()[2:]]
        self.querys_weight = float(file.readline().split()[2])
        self.use_nltk = int(file.readline().split()[2])
class representation:
    def __init__(self):
        self._documents = []
        self._terms = {}
        
    def get_documents(self):
        return self._documents
    
    def get_term(self, term):
        return self._terms[term]
    
    def get_terms(self):
        return self._terms
    
    def get_term_in(self, term, index):
        return self._terms[term][index]
    
    def set_term(self, term, value):
        self._terms[term] = value
        return self._terms
    
    def set_term_in(self, term, value, index):
        self._terms[term][index] = value
        return self._terms
        