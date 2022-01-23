import string

"""
Función encargada de parsear los diferentes
cuerpos de documentos con los que trabajará
el sistema
"""
def parse(corpus, file):
        
        if corpus == 'newsgroup':
            return parse_newsgroup(file)
        elif corpus == 'reuters':
            return parse_reuters(file)
        elif corpus == 'cran':
            return parse_cran(file)
        elif corpus == 'time':
            return parse_time(file)
        elif corpus == 'npl':
            return parse_npl(file)
        else:
            raise(Exception("This corpus not exist"))
            
"""
Parser del corpus Cranfield
"""
def parse_cran(file):
    docs = []
    d_id = ''
    text = ''
    subject = ''
    in_subject = 0
    in_text = 0
    while True:
        line = file.readline()
        if len(line.split())>0:
            if line.split()[0]=='.I':
                if in_text:
                    docs.append([subject, text, d_id])
                    in_text=0
                    subject=''
                    text=''
                    d_id=''
                d_id = line.split()[1]
            elif line.split()[0]=='.A':
                in_subject = 0
                line = file.readline()
                text+=line
            elif line.split()[0]=='.B':
                line = file.readline()
                text+=line
            elif line.split()[0]=='.W':
                in_text = 1
            elif in_text:
                text+=line
            elif line.split()[0]=='.T':
                in_subject = 1
            elif in_subject:
                subject+=line
        elif not line:
            docs.append([subject, text, d_id])
            break
      
    return docs

"""
Parser del corpus Reuters
"""
def parse_reuters(file):
    docs = []
    text = ''
    subject = ''
    line = file.readline()
    d_id = 0
    while line:
        line = file.readline()
        title = line.find("<TITLE>")
        if title != -1:
            subject = line[7:len(line)-9]
            text += subject+'\n'
        body = line.find('<BODY>')
        if body != -1:
            text += line[body+6:]
            line = file.readline()
            while True:
                endbody = line.find('</BODY>')
                if endbody != -1:
                    d_id += 1
                    docs.append([subject,text, d_id])
                    subject = ''
                    text = ''
                    break
                text += line
                line = file.readline()
    return docs
        
"""
Parser del corpus Newsgroup
"""
def parse_newsgroup(file):
    docs = []
    text = ''
    subject = ''
    d_id = 1
    s = 1
    while True:
        line = file.readline()
        if not line:
            break
        text += line
        if s and line.split()[0] == 'Subject:':
            s = 0
            subject = ' '.join(line.split()[1:])
    docs.append([subject,text,d_id])
    return docs

"""
-----------------------------------
Colecciones encontradas en Internet
-----------------------------------
"""

"""
Parser del corpus Time
"""
def parse_time(file):
    docs = []
    text = ''
    subject = ''
    d_id = 1
    file.readline()
    while True:
        line = file.readline()
        if not line:
            break
        if len(line.split()) > 0 and line.split()[0] == '*TEXT':
            docs.append([subject,text,d_id])
            subject = ''
            text = ''
            d_id+=1
        text += line
    return docs

"""
Parser del corpus NPL
"""
def parse_npl(file):
    docs = []
    text = ''
    subject = ''
    d_id = 1
    while True:
        line = file.readline()
        if not line:
            break
        if len(line.split()) > 0 and line.split()[0] == '/':
            docs.append([subject,text,d_id])
            subject = ''
            text = ''
            d_id+=1
            continue
        text += line
    return docs