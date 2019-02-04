
# coding: utf-8

# In[39]:


# plot graph: connected -> like similar movie (-ies)

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite

df = pd.read_csv('Employee_Movie_Choices.txt', skiprows=0, delimiter="\t")
employees = set(df['#Employee'])
movies = set(df['Movie'])

def plot_graph(G, weight_name=None):
    get_ipython().magic('matplotlib notebook')
    import matplotlib.pyplot as plt
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None
    if weight_name:
        weights = [int(G[u][v][weight_name]) for u,v in edges]
        labels = nx.get_edge_attributes(G,weight_name)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights);
    else:
        nx.draw_networkx(G, pos, edges=edges);
        
G = nx.read_edgelist('Employee_Movie_Choices.txt', delimiter="\t")
for node in G.nodes():
    label="employee" if node in employees else "movie"
    G.add_node(node, type=label)
G = bipartite.weighted_projected_graph(G, employees)
plot_graph(G)        


# In[41]:


# Find correlation - more good friends vs more similar movies

relation = nx.read_edgelist('Employee_Relationships.txt' ,data=[('relationship_score', int)]) # relation.nodes() # ['Andy', 'Claude', 'Frida', 'Georgia', 'Joan', 'Lee', 'Pablo', 'Vincent']
relation_df = pd.DataFrame(list(relation.edges(data=True)), columns=['From', 'To', 'relationship_score'])
employees_df = pd.DataFrame(list(G.edges(data=True)), columns=['From', 'To', 'movies_score'])
temp_df = employees_df.copy()
temp_df.rename(columns={"From":"From1", "To":"From"}, inplace=True)
temp_df.rename(columns={"From1":"To"}, inplace=True)
final_df = pd.concat([employees_df, temp_df])
res_df = pd.merge(final_df, relation_df, on = ['From', 'To'], how='right')
res_df['movies_score'] = res_df['movies_score'].map(lambda x: x['weight'] if type(x)==dict else None)
res_df['relationship_score'] = res_df['relationship_score'].map(lambda x: x['relationship_score'])
res_df['movies_score'].fillna(value=0, inplace=True)
res_df['movies_score'].corr(res_df['relationship_score'])

