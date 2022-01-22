import os, math, pickle, numpy as np, operator
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

from mri import document as doc, query as q, framework as fw, parser

class sri:
    """
    Con este método inicializamos la clase sri,
    tendremos un corpus, donde guardaremos el 
    nombre del corpus que estamos usando, count
    como contador de documentos y querys como
    lista de las querys que han sido realizadas
    Además de esto se carga el archivo de confi-
    guración y se crea una instancia de la clase
    framework, la cual es la encargada de reali-
    zar los cálculos algebraicos correspondientes.
    """
    def __init__(self):
        self._corpus = None
        self._count = 0
        self._querys = []
        self.load_config()
        self._fw = fw.framework(self.use_nltk, self.sim)
    
    """
    Trabajo con el corpus.
    """
    
    """
    select_corpus se encarga de leer de la carpeta
    /corpus donde se encuentran todos los corpus
    que estaremos usando.
    """
    def select_corpus(self):
        os.chdir("./corpus/")
        data = [element for element in os.listdir()]
        os.chdir('..')
        return data
    
    """
    Con este método cargamos el corpus seleccionado,
    creamos una instancia de representación en la que
    serán guardados los términos y los documentos lue-
    go de ser analizados.
    """
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
                    self.add_document(d[0], d[1], d[2])
                    self._count += 1
            os.chdir('../..')
            self.inverted_indexes()
            self.calc_weight()
            if self.use_nltk:
                self.tree_terms()
            with open('./cache/'+corpus+'.rep', 'wb') as f:
                pickle.dump(self._rep, f)
                f.close()
        return self._rep.get_documents()
    
    """
    Con este método se explora un directorio mediante
    un DFS, se utiliza para cargar y parsear todos los
    archivos que pertenecen al corpus en uso.
    """
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
    Trabajo con documentos
    """
    
    """
    Con este método creamos un objeto document y lo
    agregamos a la lista de documentos de la repre-
    sentación.
    """
    def add_document(self, d, text, d_id = -1):
        self.get_rep().get_documents().append(doc.document(d, text, 
                                                           self.language, self.use_nltk, d_id))
        return self.get_rep().get_documents()
    
    """
    inverted_indexes se encarga de hallar la represen-
    tación de términos invertidos del sistema.
    """
    def inverted_indexes(self):
        for doc in self.get_rep().get_documents():
            for t in doc.get_terms().keys(): 
                if t in self.get_rep().get_terms().keys():
                    self.get_rep().set_term_in(t, self.get_rep().get_term_in(t, 0) + doc.get_term(t), 0)
                    self.get_rep().get_term_in(t, 1).append(doc)
                else: 
                    self.get_rep().set_term(t, [doc.get_term(t), [doc]])
    
    """
    Con calc_weight se calcula el peso de los términos
    en cada documento en el que aparecen.
    """
    def calc_weight(self):
        for t in self.get_rep().get_terms().keys():
            for d in self.get_rep().get_term_in(t, 1):
                w = self.get_framework().weight_doc(self.get_rep().get_documents(), 
                                                    self.get_rep().get_terms(), d, t)
                d.set_weight(t, w)
        return self.get_rep().get_documents()
    
    """
    El árbol de términos es un diccionario donde aparecen
    asociados todos los términos que hay en el sistema con
    sus respectivas raíces semánticas.
    """
    def tree_terms(self):
        for term in self.get_rep().get_terms().keys():
            stemmer = PorterStemmer()
            stem_term = stemmer.stem(term)
            self.get_rep().set_terms_tree(stem_term, term)
            
            
    """
    Work with querys
    """
    
    """
    get_querys no hace más que devolver la lista de consultas
    realizadas hasta el momento.
    """
    def get_querys(self):
        return self._querys
    
    """
    Este método limpia la lista de consultas.
    """
    def clean_querys(self):
        self._querys = []
    
    """
    Método para generar una instancia de query.
    """ 
    def create_query(self, text):
        query = q.query(text, self.use_nltk, self.language)
        return query
        
    """
    Definición para instertar una query en el sistema.
    """
    def insert_query(self, query):
        self.calc_weight_query(query)
        self.get_querys().append(query)
        return query
    
    """
    Este método tiene como objetivo comparar dos querys,
    con el propósito de si, dos consultas son muy pareci-
    das, los documentos relevantes de una pueden ser aso-
    ciadas a la otra.
    """
    def compare_query(self, query):
        for q in self.get_querys():
            sim = self.get_framework().cosine_similarity(query, q, self.get_rep().get_terms_tree())
            if sim > self.query_sim:
                for d in q.get_relevants():
                    query.set_relevant(d)
                for d in q.get_not_relevants():
                    query.set_not_relevant(d)
        return query
    
    """
    calc_weight_query calcula el peso de los términos den-
    tro de una query.
    """ 
    def calc_weight_query(self, query):
        for t in query._terms.keys():
            if t in self.get_rep().get_terms().keys():
                w = self.get_framework().weight_query(self.get_rep().get_documents(), 
                                                      self.get_rep().get_terms(),self.absorber, query, t)
                query.set_weight(t, w)
        if self.use_nltk:
            for syn in wordnet.synsets(t):
                for lemma in syn.lemmas():
                    if lemma.name() in self.get_rep().get_terms().keys() and lemma.name() not in query.get_weights().keys():
                        w = self.sin * self.get_framework().weight_query(self.get_rep().get_documents(), self.get_rep().get_terms(),
                                                                   self.absorber, query, lemma.name())
                        query.set_weight(lemma.name(), w)
        return query.get_weights()
    
    """
    Función de ranking, encargada de devolver los documentos
    más similares a la query.
    """
    def ranking(self, q):
        rank = {}
        for d in self.get_rep().get_documents():
            cs = self.get_framework().cosine_similarity(d, q, self.get_rep().get_terms_tree())
            if cs > self.umbral:
                rank[d] = cs
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    
    """
    Función de retroalimentación.
    """
    def retro(self, q0):
        query = self.rocchio(q0, self.rocchio_values[0], self.rocchio_values[1], 
                             self.rocchio_values[2], q0.get_relevants(), q0.get_not_relevants())
        return self.ranking(query)
    
    """
    Algoritmo de Rocchio, encargado de realizar la búsque-
    da de la nueva consulta para realizar la retroalimenta-
    ción.
    """
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
    
    """
    Devuelve la representación del sistema.
    """    
    def get_rep(self):
        return self._rep
    
    """
    Devuelve el framework del sistema.
    """ 
    def get_framework(self):
        return self._fw
    
    """
    Carga las configuraciones del sistema desde el archivo
    /config.cfg.
    """
    def load_config(self):
        file = open('mri/config.cfg','r')
        self.language = file.readline().split()[2]
        self.query_sim = float(file.readline().split()[2])
        self.rocchio_values = [float(val) for val in file.readline().split()[2:]]
        self.absorber = float(file.readline().split()[2])
        self.sim = float(file.readline().split()[2])
        self.sin = float(file.readline().split()[2])
        self.umbral = float(file.readline().split()[2])
        self.use_nltk = int(file.readline().split()[2])
   
"""
Clase que se encargará de representar los datos del
sistema.
"""
class representation:
    """
    Poseerá una lista de documentos, un diccionario
    de términos y un diccionario de árboles de térmi-
    nos. El resto de los métodos son para acceder o
    modificar los datos de la instancia.
    """
    def __init__(self):
        self._documents = []
        self._terms = {}
        self._terms_tree = {}
        
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
    
    def get_terms_tree(self):
        return self._terms_tree
    
    def set_terms_tree(self, root, term):
        if root in self.get_terms_tree().keys():
            self._terms_tree[root].append(term)
        else:
            self._terms_tree[root] = [term]
        return self.get_terms_tree()
    
    def term_in_tree(self, term):
        if term in self._terms_tree.keys():
            return 1
        else:
            return 0