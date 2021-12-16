import os, math, pickle, numpy as np, operator
from nltk.corpus import wordnet
from mri import document as doc, query as q, framework as fw
#import document as doc, query as q, framework as fw

class sri:
    def __init__(self):
        self._corpus = None
        self._count = 0
        self._querys = []
        self._fw = fw.framework()
        self._rep = representation()
    
    def select_corpus(self):
        os.chdir("./corpus/")
        data = [element for element in os.listdir()]
        os.chdir('..')
        return data
    
    def load_corpus(self, corpus):
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
        return self._rep._documents
    
    def parse(self, corpus, file):
        docs = []
        text = ''
        subject = ''
        if corpus == 'newsgroup':
            while True:
                line = file.readline()
                if not line:
                    break
                if line.split()[0] != 'From:':
                    continue
                else:
                    while True:
                        text += line
                        if len(line.split()) > 0 and line.split()[0] == 'Subject:':
                            subject = line
                        line = file.readline()
                        if not line or len(line.split())> 1 and (line.split()[0] == 'Newsgroup:'):
                            if subject != '':
                                docs.append([subject, text])
                            text = ''
                            break
            file.close()
            return docs
        
        elif corpus == 'reuters':
            while True:
                line = file.readline()
                if not line:
                    break
                if line.find('<REUTERS')!= -1:
                    while True:
                        line = file.readline()
                        if line.find('</REUTERS>') == -1:
                            title = line.find("<TITLE>")
                            if title != -1:
                                subject = line[7:len(line)-9]
                            text += line
                        else:
                            docs.append([subject,text])
                            subject = ''
                            text = ''
                            break
            file.close()
            return docs
        
        elif corpus == 'cran':
            line = file.readline()
            while True:
                if not line:
                    break
                if line.split()[0] == '.I':
                    if subject != '':
                        docs.append([subject, text])
                        subject = ''
                        text = ''
                    line = file.readline()
                    line = file.readline()
                    while line != '.A\n':
                        subject += line
                        line = file.readline()
                    while line != '.W\n':
                        line = file.readline()
                    while True:
                        line = file.readline()
                        if not line or (len(line.split()) > 1 and line.split()[0] == '.I'):
                            break
                        text += line
                        
            file.close()
            return docs
        else:
            pass
    
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
                doc = self.parse(self._corpus, file)
                docs.append(doc)
                file.close()
        return docs
    
    def add_document(self, d, text):
        self._rep._documents.append(doc.document(d, text))
        return self._rep._documents
    
    
    def inverted_indexes(self):
        for doc in self._rep._documents:
            for t in doc._terms.keys(): 
                if t in self._rep._terms.keys():
                    self._rep._terms[t][0] = self._rep._terms[t][0] + doc._terms[t]
                    self._rep._terms[t][1].append(doc)
                else: self._rep._terms[t] = [doc._terms[t], [doc]]
    
    def calc_weight(self):
        for t in self._rep._terms.keys():
            for d in self._rep._terms[t][1]:
                w = self._fw.weight_doc(self._rep._documents, self._rep._terms, d, t)
                d._weight[t] = w
        return self._rep._documents
    
    def calc_weight_q(self, q):
        for t in q._terms.keys():
            if t in self._rep._terms.keys():
                w = self._fw.weight_query(self._rep._documents, self._rep._terms,.5, q, t)
                q._weight[t] = w
            else:
                count = 0
                w = 0
                for syn in wordnet.synsets(t):
                    for lemma in syn.lemmas():
                        if lemma.name() in self._rep._terms.keys():
                            w += self._fw.weight_query(self._rep._documents, self._rep._terms,.5, q, lemma.name())
                            count += 1
                if w != 0 : q._weight[t] = w/count
                
        return q._weight
    
    def insert_query(self, text):
        query = q.query(text)
        self.calc_weight_q(query)
        self._querys.append(query)  
        return query
        
    def ranking(self, q):
        rank = {}
        for d in self._rep._documents:
            cs = self._fw.cosine_similarity(d, q)
            rank[d] = cs
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[:20]
    
    
class representation:
    def __init__(self):
        self._documents = []
        self._terms = {}
        