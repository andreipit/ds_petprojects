
# coding: utf-8

# # This is version, that compares all words of 2 texts

# In[87]:


# nltk.download('popular') # run it once
# nltk.download('punkt')   # run it once (try without it)
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import pandas as pd

# doc1 = 'This is a function to test document_path_similarity.'
# doc2 = 'Use this function to see if your code in doc_to_synsets \
# and similarity_score is correct!'
with open('plato.txt', 'r', encoding='utf8') as f: doc1 = f.read()
with open('socrates.txt', 'r', encoding='utf8') as f: doc2 = f.read()



def convert_tag(tag):
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'} # Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets
    try: return tag_dict[tag[0]]
    except KeyError: return None
    
    
# input: 'This is a function to test document_path_similarity.'
# output: # [Synset('be.v.01'), Synset('angstrom.n.01'), Synset('function.n.01'), Synset('test.v.01')]
def text_to_synsets_list(doc): # convert string to similar string with changed words (to similar or delete, if there is not similar)
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
    
s1 = text_to_synsets_list(doc1) # [be angstrom function test]
s2 = text_to_synsets_list(doc2) # [use function see code inch be correct]
compare_2_sysnet_lists(s1, s2) #0.8865208947358074


# # Test

# In[89]:


# get word synsets
from nltk.corpus import wordnet as wn
# available parts of speech'n', 'a', 'r', 'v'
wn.synsets('star', 'n')             # [Synset('star.n.01'), Synset('ace.n.03'), Synset('star.n.03'), Synset('star.n.04'), Synset('star.n.05'), Synset('headliner.n.01'), Synset('asterisk.n.01'), Synset('star_topology.n.01')]


# In[90]:


# evaluate their similarity
word_0 = wn.synsets('star', 'n')[0] # Synset('star.n.01')
word_1 = wn.synsets('star', 'n')[0] # Synset('ace.n.03')
word_0.path_similarity(word_1)      #0.1111111111111111

