def parse(corpus, file):
        
        if corpus == 'newsgroup':
            return parse_newsgroup(file)
        elif corpus == 'reuters':
            return parse_reuters(file)
        elif corpus == 'cran':
            return parse_cran(file)
        else:
            NotImplemented
            
def parse_cran(file):
    docs = []
    text = ''
    subject = ''
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
    return docs

def parse_reuters(file):
    docs = []
    text = ''
    subject = ''
    line = file.readline()
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
                    docs.append([subject,text])
                    subject = ''
                    text = ''
                    break
                text += line
                line = file.readline()
    return docs
        

def parse_newsgroup(file):
    docs = []
    text = ''
    subject = ''
    s = 1
    while True:
        line = file.readline()
        if not line:
            break
        text += line
        if s and line.split()[0] == 'Subject:':
            s = 0
            subject = ' '.join(line.split()[1:])
    docs.append([subject,text])
    return docs

def tokenizer(terms, text):
       current = ''
       for char in text:
           if char == ' ' or char == '\n' or char in string.punctuation:
               if current == '':
                   continue
               current = current.lower()
               if current in terms.keys():
                   terms[current] += 1
               else:
                   terms[current] = 1
               current = ''
           else:
               current += char
       terms[current] = 1