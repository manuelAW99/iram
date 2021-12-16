import streamlit as st
import mri.sri as s
import webbrowser
from os import remove

SRI = s.sri()

st.header("irAM 🔍")
col1, col2 = st.columns([9,1])
with col1:
    query = st.text_input('Insert your query')
with col2:
    st.caption('Search')
    st.button('🔍')

options = SRI.select_corpus()
corpus = st.sidebar.selectbox("Select corpus", options)
documents = SRI.load_corpus(corpus)
    

#doc = st.sidebar.selectbox('Select document', [d._label for d in documents])
#check = st.sidebar.checkbox('Show')

#if doc is not None and check : st.write(SRI._terms.keys())

if query != '':
    q = SRI.insert_query(query)
    r = SRI.ranking(SRI._querys[len(SRI._querys)-1])
    i = 0
    for d in r:
        i += 1
        with st.expander("Subject: "+d[0]._label):
            st.write(d[0]._text[:500]+'\n...')
            if st.button('See more',key=i):
                file = open('./cache/current.txt', 'w+')
                file.write(d[0]._text)
                file.close()
                webbrowser.open_new_tab('./cache/current.txt')
                file.close()
                remove('./cache/current.txt')


def current_corpus(data):
    os.chdir("./" + data)
    elements = os.listdir()
    corpus = ''
    for archive in elements:
        file = open(archive,'r', errors= 'ignore')
        current_file = file.read()
        
    os.chdir('..')




