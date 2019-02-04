
# coding: utf-8

# In[1]:


#--------------------------------------------------------------
#--------------------------------------------------------------
# 1) READ DATA
#--------------------------------------------------------------
#--------------------------------------------------------------
import numpy as np
import nltk # nltk.download('popular') # run it once    # nltk.download('punkt')   # run it once (try without it)
from nltk.corpus import wordnet as wn
import pandas as pd

MINSIM = 0.5 # for test data = 0.1     # minimal similarity between 2 files. If similarity is more - put files in 1 folder.


# test data
# doc0 = 'This is a function to test document_path_similarity.'
# doc1 = 'Use this function to see if your code in doc_to_synsets and similarity_score is correct!'
# doc2 = 'According to the Times, one of their key findings was a financial disclosure form from Barrys Senate confirmation proceedings in 1999 to be a federal appellate judge'
# doc3 = 'Again, it seemed completely random. One person reported receiving the alert on their T-Mobile Samsung Note while experiencing absolute radio silence from their iPhone X on the same carrier.)'
# doc4 = 'They added that the agency is also unsure why some people received the alert before others. Quartz has asked for more detail on why this is the case.'
# doc5 = 'The most common monkey species found in animal research are the grivet, the rhesus macaque, and the crab-eating macaque, which are either wild-caught or purpose-bred.'
# docs = [ doc0,doc1,doc2,doc3,doc4,doc5]

# real data
fnames = ['plato.txt','socrates.txt','airplane.txt','electricity.txt','monkey.txt','bear.txt']
docs=[]
for name in fnames:
    with open('../input/'+name, 'r', encoding='utf8') as f: docs.append(f.read())
        
# with open('../input/plato.txt', 'r', encoding='utf8') as f: doc0 = f.read()
# with open('../input/socrates.txt', 'r', encoding='utf8') as f: doc1 = f.read()
# with open('../input/airplane.txt', 'r', encoding='utf8') as f: doc2 = f.read()
# with open('../input/electricity.txt', 'r', encoding='utf8') as f: doc3 = f.read()
# with open('../input/monkey.txt', 'r', encoding='utf8') as f: doc4 = f.read()
# with open('../input/bear.txt', 'r', encoding='utf8') as f: doc5 = f.read()


def convert_tag(tag):
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'} # Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets
    try: return tag_dict[tag[0]]
    except KeyError: return None
    
def text_to_synsets_list(doc): # convert string to similar string with changed words (to similar or delete, if there is not similar)
    # input: 'This is a function to test document_path_similarity.'
    # output: # [Synset('be.v.01'), Synset('angstrom.n.01'), Synset('function.n.01'), Synset('test.v.01')]
    words = nltk.word_tokenize(doc)                     # ['This', 'is', 'a', 'function', 'to', 'test', 'document_path_similarity', '.']
    words_n_pos = nltk.pos_tag(words)                   # [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('function', 'NN'), ('to', 'TO'), ('test', 'VB'), ('document_path_similarity', 'NN'), ('.', '.')]
    poses = [y for x,y in words_n_pos]                  # ['DT', 'VBZ', 'DT', 'NN', 'TO', 'VB', 'NN', '.']
    # just renames by first letter
    wntag = [convert_tag(x) for x in poses]             # [None, 'v', None, 'n', None, 'v', 'n', None]
    #mix words and PoS first letters
    ans = list(zip(words,wntag))                       # [('This', None), ('is', 'v'), ('a', None), ('function', 'n'), ('to', None), ('test', 'v'), ('document_path_similarity', 'n'), ('.', None)]
    # similar words from WordNet
    synsets = [wn.synsets(x,y) for x,y in ans]          # [[], [Synset('be.v.01'),  Synset('exist.v.01'),  Synset('equal.v.01'),...
    # remove empty groups and all synsets expect 1 in each groups
    final = [val[0] for val in synsets if len(val) > 0] 
    return final # [Synset('be.v.01'), Synset('angstrom.n.01'), Synset('function.n.01'), Synset('test.v.01')]

def compare_2_sysnet_lists(s1, s2):
    scores_best =[]
    for i in s1:
        #print(i, 'first')        # Synset('be.v.01')  /n  Synset('angstrom.n.01')  /n  Synset('function.n.01')  /n  Synset('test.v.01')
        scores_all =[]
        for j in s2:
            # print(j) # 4 loops of: Synset('use.v.01')   Synset('function.n.01')   Synset('see.v.01')   Synset('code.n.01')   Synset('inch.n.01')   Synset('be.v.01')   Synset('correct.a.01')
            # if words are similar - path_similarity returns 1 (be and be)
            #print(i.path_similarity(j)) # 0.33 0.14 0.25 0.14 0.11 1.0 0.33 None 0.1 None 0.1 0.25 None None None ...
            similarity = i.path_similarity(j)
            if (similarity != None): scores_all.append(similarity)
        if scores_all: scores_best.append(max(scores_all))
    # scores_best                     # [1.0, 0.25, 1.0, 0.2]      
    return sum(scores_best)/len(scores_best) # 0.6125
    

def find_topics_of_string(s, topic_count):
    import pickle
    import gensim #anaconda prompt -> pip install -U gensim
    from sklearn.feature_extraction.text import CountVectorizer
    data = [s]
    vect = CountVectorizer(min_df=0, max_df=1, stop_words='english', token_pattern='(?u)\\b\\w\\w\\w+\\b')
    X = vect.fit_transform(data)
    corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)
    id_map = dict((v, k) for k, v in vect.vocabulary_.items())
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, id2word=id_map, num_topics=1, passes=25, random_state=34) # wait too long
    return ldamodel.print_topics(num_topics=1, num_words=topic_count) #[0][1].split('+')[0].split('*')[1]
    
def clean_topics(top): #[(0,   '0.031*"plato" + 0.011*"socrates")] => ['plato', 'socrates']
    return [x.split('*')[1].replace('"', '').rstrip() for x in top[0][1].split('+')]    
    
def list_to_sentence(doc):
    return ''.join(e+' ' for e in doc).rstrip()

#--------------------------------------------------------------
#--------------------------------------------------------------
# 2) GET FOREACH DOC:
# - TOPICS => [(0, '0.333*"document_path_similarity" + 0.333*"function" + 0.333*"test"')] 
# - THEN SYNSETS LIST (GOOD FOR COMPARING) => [Synset('function.n.01'), Synset('trial.n.02')]
#--------------------------------------------------------------
#--------------------------------------------------------------

synsets=[]
for doc in docs:
#    synsets.append( (text_to_synsets_list(list_to_sentence(clean_topics(find_topics_of_string(doc[0], 1000)))) , doc[1] ) )
   synsets.append( text_to_synsets_list(list_to_sentence(clean_topics(find_topics_of_string(doc, 1000)))) )

# test print all similarities
# for i in range(len(docs)):
#     for j in range(len(docs)):
#         if not j==i:
#             sim = compare_2_sysnet_lists(synsets[i], synsets[j])
#             sim = (int(sim*100))/100
#             print(sim,fnames[i],fnames[j])
# 0.67 plato.txt socrates.txt
# 0.5 plato.txt airplane.txt
# 0.36 plato.txt electricity.txt
# 0.47 plato.txt monkey.txt
# 0.48 plato.txt bear.txt
# 0.66 socrates.txt plato.txt
# 0.48 socrates.txt airplane.txt
# 0.37 socrates.txt electricity.txt
# 0.42 socrates.txt monkey.txt
# 0.45 socrates.txt bear.txt
# 0.49 airplane.txt plato.txt
# 0.47 airplane.txt socrates.txt
# 0.39 airplane.txt electricity.txt
# 0.42 airplane.txt monkey.txt
# 0.43 airplane.txt bear.txt
# 0.5 electricity.txt plato.txt
# 0.53 electricity.txt socrates.txt
# 0.57 electricity.txt airplane.txt
# 0.4 electricity.txt monkey.txt
# 0.43 electricity.txt bear.txt
# 0.45 monkey.txt plato.txt
# 0.42 monkey.txt socrates.txt
# 0.43 monkey.txt airplane.txt
# 0.29 monkey.txt electricity.txt
# 0.5 monkey.txt bear.txt
# 0.5 bear.txt plato.txt
# 0.49 bear.txt socrates.txt
# 0.47 bear.txt airplane.txt
# 0.34 bear.txt electricity.txt
# 0.54 bear.txt monkey.txt


# print(compare_2_sysnet_lists(s1, s2) #0.6789118246687038  plato vs socrates
# compare_2_sysnet_lists(doc1, doc3) #0.5099787370815394   plato vs airplane

#--------------------------------------------------------------
#--------------------------------------------------------------
# 3) SEPARATE DOCS TO FOLDERS => [['plato.txt', 'socrates.txt', 'airplane.txt', 'monkey.txt'], ['electricity.txt', 'bear.txt']]
#--------------------------------------------------------------
#--------------------------------------------------------------

folders=[]
def in_folders(name):
    for folder in folders:
        for file in folder:
            if file == name: return True
    return False

def separate_by_folders(synsets, fnames): # [[Synset('function.n.01'), Synset('trial.n.02')], [Synset('code.n.01'), ...], [...]]
    for i in range(len(synsets)):
        if not in_folders(fnames[i]):
            folder = []
            folder.append(fnames[i])
            for j in range(len(synsets)):
                if not in_folders(fnames[j]):
                    if not j==i:
                        similarity = compare_2_sysnet_lists(synsets[i],synsets[j])
                        if similarity>MINSIM:
                            #print(fnames[j], i, j)
                            folder.append(fnames[j])
            folders.append(folder)
    return folders # [['plato.txt', 'socrates.txt', 'airplane.txt', 'monkey.txt'], ['electricity.txt', 'bear.txt']]
folders = separate_by_folders(synsets, fnames) 
print('files in folders=',folders)

#--------------------------------------------------------------
#--------------------------------------------------------------
# 3) FIND NAME FOREACH FOLDER BY TOPIC SEARCH.
# FOREACH DOC:
# INPUT - [ [Synset('absolute.a.01'), Synset('alert.n.01'), ...] , [], [] ]
# OUTPUT - "function_harmonize_people"
#--------------------------------------------------------------
#--------------------------------------------------------------

def convert_synsets_to_one_sentence(synsets): # [ [Synset('absolute.a.01'), Synset('alert.n.01'), ...] , [], [] ]
    import re
    result=[]
    for line in synsets:    # [Synset('absolute.a.01'), Synset('alert.n.01'), ...] 
        newline=[]
        for word in line:   # Synset('absolute.a.01')
            regex = re.compile(r'^Synset\(\'(.*?)(\.).*$', re.IGNORECASE)
            newline.append(regex.sub(r'\1',str(word)))
        result.append(list_to_sentence(newline))
    return list_to_sentence(result)                         # ['absolute alert ... macaque ...']

def get_topics(line, count=3): # "function trial code ... correct"
    return list_to_sentence(clean_topics(find_topics_of_string(line,count))).replace(' ', '_') # function_harmonize_people
   
def find_folder_names(folders):    
    folder_names = []
    for i in range(len(folders)):
        folder_synsets = []
        # get list of lists of synsets for current doc
        for file in folders[i]: folder_synsets.append(synsets[fnames.index(file)]) # result: [ [Synset('absolute.a.01'), Synset('alert.n.01'), ...] , [], [] ]
        # list of lists of synsets for this doc => one string sentence
        sentence = convert_synsets_to_one_sentence(folder_synsets) # result=str: "function trial code ... correct"
        folder_name = get_topics(sentence,3)              # result=str: "function_harmonize_people"
        folder_names.append(folder_name)
    return folder_names # ['function_harmonize_people', 'research_receive_person']
folder_names = find_folder_names(folders) 
print('folders=',folder_names)


#--------------------------------------------------------------
#--------------------------------------------------------------
# 4) CREATE FOLDERS AND MOVE FILES THERE
#--------------------------------------------------------------
#--------------------------------------------------------------

import os
import shutil
for i in range(len(folders)):
    folder = folder_names[i]
    if not os.path.exists(folder):
        os.makedirs('../input/'+folder)
        for file in folders[i]: shutil.move('../input/' + file, '../input/' + folder + '/' + file)    
    
    
# for MINSIM 0.5:
#     files in folders= [['plato.txt', 'socrates.txt', 'airplane.txt'], ['electricity.txt'], ['monkey.txt', 'bear.txt']]
#     folders= ['state_use_make', 'make_push_charge', 'state_include_animal']

