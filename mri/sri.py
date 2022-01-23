import os, math, pickle, numpy as np, operator
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

from mri import document as doc, query as q, framework as fw, parser

class sri:
    def __init__(self):
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
        self._corpus = None
        self._count = 0
        self._querys = []
        self.load_config()
        self._fw = fw.framework(self.use_nltk, self.sim)
    
    """
    ---------------------
    Trabajo con el corpus
    ---------------------
    """

    def select_corpus(self):
        """
        Método que se encarga de leer de la carpeta
        /corpus donde se encuentran todos los corpus
        que estaremos usando.
        
        rtype: str
        return: data
        """
        os.chdir("./corpus/")
        data = [element for element in os.listdir()]
        os.chdir('..')
        return data
    
    def load_corpus(self, corpus):
        """
        Con este método cargamos el corpus seleccionado,
        creamos una instancia de representación en la que
        serán guardados los términos y los documentos lue-
        go de ser analizados.
        
        param corpus: Cuerpo de documentos seleccionado
        type corpus: str
        
        rtype: list
        return: self._rep.get_documents()
        """
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
    
    def explore_dir(self, r, docs, p):
        """
        Con este método se explora un directorio mediante
        un DFS, se utiliza para cargar y parsear todos los
        archivos que pertenecen al corpus en uso.
        
        param r: Ubicación actual de la terminal
        type r: str
        param docs: Lista donde serán guardados los documentos
        type docs: list
        param p: Directorio a explorar
        type p: str
        
        rtype: list
        return: docs
        """
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
    ----------------------
    Trabajo con documentos
    ----------------------
    """
    
    def add_document(self, subject, text, d_id = -1):
        """
        Con este método creamos un objeto document y lo
        agregamos a la lista de documentos de la repre-
        sentación.
        
        param subject: Tema o título del documento
        type subject: str
        param text: Texto del documento
        type text: str
        param d_id: Identificador del documento
        type d_id: int
        
        rtype: list
        return: self.get_rep().get_documents()
        """
        self.get_rep().get_documents().append(doc.document(subject, text, 
                                                           self.language, self.use_nltk, d_id))
        return self.get_rep().get_documents()
    
    def inverted_indexes(self):
        """
        Método que se encarga de hallar la represen-
        tación de términos invertidos del sistema.
        
        rtype: None
        """
        for doc in self.get_rep().get_documents():
            for t in doc.get_terms().keys(): 
                if t in self.get_rep().get_terms().keys():
                    self.get_rep().set_term_in(t,
                                               self.get_rep().get_term_in(t, 0)
                                               + doc.get_term(t),
                                               0)
                    self.get_rep().get_term_in(t, 1).append(doc)
                else: 
                    self.get_rep().set_term(t, [doc.get_term(t), [doc]])
    
    def calc_weight(self):
        """
        Función que calcula el peso de los términos
        en cada documento en el que aparecen.
        
        rtype: list
        return: self.get_rep().get_documents()
        """
        for t in self.get_rep().get_terms().keys():
            for d in self.get_rep().get_term_in(t, 1):
                w = self.get_framework().weight_doc(self.get_rep().get_documents(), 
                                                    self.get_rep().get_terms(), d, t)
                d.set_weight(t, w)
        return self.get_rep().get_documents()
    
    def tree_terms(self):
        """
        El árbol de términos es un diccionario donde aparecen
        asociados todos los términos que hay en el sistema con
        sus respectivas raíces semánticas.
        
        rtype: None
        """
        for term in self.get_rep().get_terms().keys():
            stemmer = PorterStemmer()
            stem_term = stemmer.stem(term)
            self.get_rep().set_terms_tree(stem_term, term)
            
            
    """
    ---------------------
    Trabajo con consultas
    ---------------------
    """
    
    def get_querys(self):
        """
        Este método no hace más que devolver la lista
        de consultas realizadas hasta el momento.
        
        rtype: list
        return: self._querys
        """
        return self._querys
    
    def clean_querys(self):
        """
        Este método limpia la lista de consultas.
        
        rtype: None
        """
        self._querys = []
    
    def create_query(self, text):
        """
        Método para generar una instancia de query.
        
        param text: Texto introducido en la consulta
        type text: str
        
        rtype: query
        return: query
        """ 
        query = q.query(text, self.use_nltk, self.language)
        return query
        
    def insert_query(self, query):
        """
        Método para insertar una query en el sistema.
        
        param query: Consulta a introducir en el sistema
        type query: query
        
        rtype: query
        return: query
        """
        for q in self.get_querys():
            if q.get_text() == query.get_text():
                query = q
                return query
        self.calc_weight_query(query)
        self.get_querys().append(query)
        return query
    
    def compare_query(self, query):
        """
        Este método tiene como objetivo comparar dos querys,
        con el propósito de si, dos consultas son muy pareci-
        das, los documentos relevantes de una pueden ser aso-
        ciadas a la otra.
        
        param query: Consulta a comparar con el resto de consultas
        type query: query
        
        rtype: query
        return: query
        """
        for q in self.get_querys():
            sim = self.get_framework().cosine_similarity(query,
                                                         q,
                                                         self.get_rep().get_terms_tree())
            if sim > self.query_sim:
                for d in q.get_relevants():
                    query.set_relevant(d)
                for d in q.get_not_relevants():
                    query.set_not_relevant(d)
        return query
    
    def calc_weight_query(self, query):
        """
        Este método calcula el peso de los términos den-
        tro de una query.
        
        param query: Consulta a calcular el peso de sus términos
        type query: query
        
        rtype: dict
        return: query.get_weights()
        """ 
        for t in query._terms.keys():
            if t in self.get_rep().get_terms().keys():
                w = self.get_framework().weight_query(self.get_rep().get_documents(), 
                                                      self.get_rep().get_terms(),
                                                      self.absorber,
                                                      query,
                                                      t)
                query.set_weight(t, w)
        if self.use_nltk:
            for syn in wordnet.synsets(t):
                for lemma in syn.lemmas():
                    if (lemma.name() in self.get_rep().get_terms().keys() and
                        lemma.name() not in query.get_weights().keys()):
                        w = self.sin * self.get_framework().weight_query(self.get_rep().get_documents(),
                                                                         self.get_rep().get_terms(),
                                                                         self.absorber,
                                                                         query,
                                                                         lemma.name())
                        query.set_weight(lemma.name(), w)
        return query.get_weights()
    
    def ranking(self, q):
        """
        Función de ranking, encargada de devolver los documentos
        más similares a la query.
        
        param q: Consulta a calcularle el ranking
        type q: query
        
        rtype: dict
        return: sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
        """
        rank = {}
        for d in self.get_rep().get_documents():
            cs = self.get_framework().cosine_similarity(d, q, 
                                                        self.get_rep().get_terms_tree())
            if cs > self.umbral:
                rank[d] = cs
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    
    def retro(self, q0):
        """
        Función de retroalimentación.
        
        param q0: Consulta inicial realizada por el usuario
        type q0: query
        
        rtype: dict
        return: self.ranking(query)
        """
        query = self.rocchio(q0,
                             self.rocchio_values[0],
                             self.rocchio_values[1], 
                             self.rocchio_values[2],
                             q0.get_relevants(),
                             q0.get_not_relevants())
        return self.ranking(query)
    
    def rocchio(self, q0, a , b, c, Cr, Cnr):
        """
        Algoritmo de Rocchio, encargado de realizar la búsque-
        da de la nueva consulta para realizar la retroalimenta-
        ción.
        
        param q0: Consulta inicial realizada por el usuario
        type q0: query
        param a: Coeficiente de valor de términos iniciales
        type a: float
        param b: Coeficiente de valor de documentos relevantes
        type b: float
        param c: Coeficiente de valor de documentos no relevantes
        type c: float
        
        rtype: query
        return: qm
        """
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
        """
        Devuelve la representación del sistema.
        
        rtype: representation
        return: return self._rep
        """ 
        return self._rep
    
    def get_framework(self):
        """
        Devuelve el framework del sistema.
        
        rtype: framework
        return: self._fw
        """ 
        return self._fw
    
    def load_config(self):
        """
        Carga las configuraciones del sistema desde el archivo
        /config.cfg.
        
        rtype: None
        """
        file = open('mri/config.cfg','r')
        self.language = file.readline().split()[2]
        self.query_sim = float(file.readline().split()[2])
        self.rocchio_values = [float(val) for val in file.readline().split()[2:]]
        self.absorber = float(file.readline().split()[2])
        self.sim = float(file.readline().split()[2])
        self.sin = float(file.readline().split()[2])
        self.umbral = float(file.readline().split()[2])
        self.use_nltk = int(file.readline().split()[2])
   
class representation:
    """
    Clase que se encargará de representar los datos del
    sistema.
    
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