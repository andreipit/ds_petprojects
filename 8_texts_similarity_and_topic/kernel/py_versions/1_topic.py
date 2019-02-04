
# coding: utf-8

# In[105]:


import pickle
import gensim #anaconda prompt -> pip install -U gensim
from sklearn.feature_extraction.text import CountVectorizer

# text = 'This is a function to test document_path_similarity.'    # test example
with open('plato.txt', 'r', encoding='utf8') as f: text = f.read()
    
def find_topics_of_string(s, topic_count):
    data = [s]
    vect = CountVectorizer(min_df=0, max_df=1, stop_words='english', token_pattern='(?u)\\b\\w\\w\\w+\\b')
    X = vect.fit_transform(data)
    corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)
    id_map = dict((v, k) for k, v in vect.vocabulary_.items())
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, id2word=id_map, num_topics=1, passes=25, random_state=34) # wait too long
    return ldamodel.print_topics(num_topics=1, num_words=topic_count) #[0][1].split('+')[0].split('*')[1]
    
def clean_topics(top): #[(0,   '0.031*"plato" + 0.011*"socrates")] => ['plato', 'socrates']
    return [x.split('*')[1].replace('"', '').rstrip() for x in top[0][1].split('+')]    
    
clean_topics(find_topics_of_string(text, 5)) #['plato', 'socrates', 'dialogues', 'forms', 'republic']

