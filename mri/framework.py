from nltk.stem import PorterStemmer
from math import log
from numpy.linalg import norm

class framework:
    """
    Clase encargada de realizar todas las operaciones
    algebraicas del SRI.
    """
    def __init__(self, use_nltk, sim):
        """
        Se inicializa una instancia del framework
        
        :param use_nltk: Parámetro que indica si la la librería
                         NLTK está siendo utilizada.
        :type use_nltk: bool
        :param sim: Parámetro para indicar cuánto se van a valorar
                    los términos que pertenezcan a la misma familia
        :type sim: float
        
        :rtype: framework
        """
        self._sim = sim
        self._use_nltk = use_nltk
    
    def use_nltk(self):
        """
        Función que devuelve el estado del uso de NLTK
        
        :rtype: bool
        :return: self._use_nltk
        """
        return self._use_nltk
    
    def get_sim(self):
        """
        Función que devuelve el valor de la similitud
        entre términos de la misma familia.
        
        :rtype: float
        :return: self._sim
        """
        return self._sim
    
    def tf(self, d, t):
        """
        Función que calcula el tf de un término
        en un documento.
        
        :param d: Documento a analizar
        :type d: document
        :param t: Término que se está analizando
        :type t: string
        :rtype: float
        :return: freq/freq_m
        """
        freq = 0
        freq_m = 1
        if t in d.get_terms().keys():
            freq = d.get_term(t)
            for k in d.get_terms().keys():
                if d.get_term(k) > freq_m:
                    freq_m = d.get_term(k)
        return freq/freq_m
    
    def idf(self, n, N):
        """
        Función que calcula el idf de un término
        en un documento.
        
        :param n: Cantidad de documentos en los que 
                  aparece el término.
        :type n: int
        :param N: Cantidad de documentos del corpus
        :type N: int
        :rtype: float
        :return: log(N/n)
        """
        return log(N/n)
    
    def weight_doc(self, docs, terms, d, t):
        """
        Función que calcula el peso de un término
        en un documento.
        
        :param docs: Lista de documentos del sistema
        :type docs: list
        :param terms: Diccionario de índices invertidos
        :type terms: dict
        :param d: Documento a analizar
        :type d: document
        :param t: Término a analizar
        :type t: string
        
        :rtype: float
        :return: idf * tf
        """
        tf = self.tf(d, t)
        idf = self.idf(len(terms[t][1]), len(docs))
        return idf * tf
    
    def weight_query(self, docs, terms, a, q, t):
        """
        Función que calcula el peso de un término
        en una consulta.
        
        :param docs: Lista de documentos del sistema
        :type docs: list
        :param terms: Diccionario de índices invertidos
        :type terms: dict
        :param a: Valor del amortiguador usado
        :type a: float
        :param q: Consulta a analizar
        :type q: query
        :param t: Término a analizar
        :type t: string
        
        :rtype: float
        :return: (a + (1-a)*(tf)) * idf
        """
        tf = self.tf(q, t)
        idf = self.idf(len(terms[t][1]), len(docs))
        return (a + (1-a)*(tf)) * idf
    
    def cosine_similarity(self, d, q, tree):
        """
        Función que calcula la similitud de una consulta
        con un documento.
    
        :param d: Documento a analizar
        :type d: document
        :param q: Consulta a analizar
        :type q: query
        :param tree: Diccionario de familias de términos
        :type tree: dict
        
        :rtype: float
        :return: (weight/(sum_d * sum_q)) if (sum_d * sum_q) > 0 else 0
        """
        weight = 0
        sum_d, sum_q = 0, 0
        if self.use_nltk():
            stemmer = PorterStemmer()
            for t in q.get_weights().keys():
                stem_term = stemmer.stem(t)
                if stem_term in tree.keys():
                    family = [tt for tt in tree[stem_term] if tt in d.get_weights().keys()]
                    """
                    Prueba con la media:
                    
                    mean = self.mean(family, d)
                    w_q = q.get_weight(t)
                    weight += (mean * w_q)
                    """
                    for tt in family:
                        w_d = d.get_weight(tt)
                        w_q = q.get_weight(t)
                        if t == tt:
                            weight += (w_d * w_q)
                        else:
                            weight += self.get_sim()*(w_d * w_q)
        else:
            for t in q.get_weights().keys():
                if t in d.get_weights().keys():
                    w_d = d.get_weight(t)
                    w_q = q.get_weight(t)
                    weight += (w_d * w_q)
                
        vec_d, vec_q = list(d.get_weights().values()), list(q.get_weights().values())
        sum_d = norm(vec_d)
        sum_q = norm(vec_q)
          
        return (weight/(sum_d * sum_q)) if (sum_d * sum_q) > 0 else 0
    
    def mean(self, terms, doc):
        """
        Función que calcula la media del peso de
        una lista de términos en un documento.
    
        :param terms: Lista de términos
        :type terms: list
        :param doc: Documento en el cuál se analizará el peso
        :type doc: document
        
        :rtype: float
        :return: mean
        """
        mean = 0
        if len(terms) > 0:
            for t in terms:
                mean += doc.get_weight(t)
            mean /= len(terms)
        return mean