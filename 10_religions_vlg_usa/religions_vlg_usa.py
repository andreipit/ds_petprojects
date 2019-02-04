
# coding: utf-8

# # Input data from Volgograd

# In[1]:


import pandas as pd
import numpy as np
# religion_volgograd = pd.read_csv('religion_volgograd.csv', skiprows=0, delimiter="\t").reset_index(drop=True)
religion_volgograd = pd.DataFrame(
        [['Русская православная церковь',268,'Christianity'],
         ['Старообрядцы',11,'Christianity'],
         ['Римско-католическая церковь',5,'Christianity'],
         ['Ислам',43,'Islam'],
         ['Буддизм',2,'Other'],
         ['Иудаизм ортодоксальный',4,'Judaism'],
         ['Иудаизм современный',0,'Judaism'],
         ['Евангельские христиане - баптисты',19,'Christianity'],
         ['Христиане веры Евангельской',8,'Christianity'],
         ['Евангельские христиане',16,'Christianity'],
         ['Пятидесятники',9,'Christianity'],
         ['Адвентисты седьмого дня',15,'Christianity'],
         ['Лютеране',4,'Christianity'],
         ['Методисткая церковь',1,'Christianity'],
         ['Пресвитерианская церковь',3,'Christianity'],
         ['Свидетели Иеговы',0,'Christianity'],
         ['Иные вероисповедания',9,'Other']
        ],
        columns=['religion','amount','group']
)

religion_volgograd


# In[2]:


vlg = pd.DataFrame()
for group, frame in religion_volgograd.groupby('group'):
    row = pd.Series({'religios group' : group, 'percent' : 100 * sum(frame['amount'])/sum(religion_volgograd['amount'])})
    vlg = vlg.append(row,ignore_index=True)
vlg


# # Input data from USA

# In[3]:


# religion_usa = pd.read_csv('religion_usa.csv', skiprows=0, delimiter="\t").reset_index(drop=True)
religion_usa = pd.DataFrame(
        [['Christianity',73.7,'Christianity'],
         ['Judaism',2.1,'Judaism'],
         ['Islam',0.8,'Islam'],
         ['Other non-Christian religion',2.5,'Other'],
        ],
        columns=['religion','amount','group']
)

religion_usa


# In[4]:


usa = pd.DataFrame()
for group, frame in religion_usa.groupby('group'):
    row = pd.Series({'religios group' : group, 'percent' : 100 * sum(frame['amount'])/sum(religion_usa['amount'])})
    usa = usa.append(row,ignore_index=True)
usa


# # Plot

# In[5]:


def draw_points_2d(v2=[[0,0],[0,0],[0,0]], size =[300,200,500], size_mult = 300, clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)], annotation =['name1','name2','name3'], an_clr=(0,0,1), an_antiheight=3, grid_size=[-4,5], axis_length=[5,1], origin=[0,0], title="Comparison of the religions of Volgograd (Russia) and the USA (%)", ylabel="oy", xlabel="ox"):
    import numpy as np
    import matplotlib.pyplot as plt
    import pylab
    x = np.arange(grid_size[0], grid_size[1]).tolist() #grid wide
    y = np.arange(grid_size[0], grid_size[1]).tolist() #grid height
    for v in v2:
        plt.scatter([v[0]], [v[1]], s=size[v2.index(v)]*size_mult, c=clr[v2.index(v)]) # plt.scatter([0.1,0.5], [0.4,0.8], s=[300, 5])
        plt.annotate(annotation[v2.index(v)], (v[0],v[1]), color=an_clr, xytext=(v[0]+2/an_antiheight,v[1]+2/an_antiheight), #textcoords='offset points', 
            ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5), arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0') )
    plt.plot([origin[0],origin[0]], [origin[1],origin[1]+axis_length[1]]) #oy
    plt.plot([origin[0],axis_length[0]], [origin[1],origin[1]]) #ox
    plt.grid()
    plt.title(title)
    y = range(4)
    pylab.yticks(y, ['', 'Volgograd (Russia)','','USA'])

    plt.show()
    
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [12,9]    
draw_points_2d(
    v2=[[1,1],[2,1],[3,1],[4,1],[1,3],[2,3],[3,3],[4,3]], 
    size =[vlg.loc[0]['percent'],vlg.loc[1]['percent'],vlg.loc[2]['percent'],vlg.loc[3]['percent'],usa.loc[0]['percent'],usa.loc[1]['percent'],usa.loc[2]['percent'],usa.loc[3]['percent']], 
    clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.), (1.,0.,1.), (1.,0.,0.), (0.,1.,0.), (0.,0.,1.), (1.,0.,1.)], 
    annotation =['Christianity '+str(vlg.loc[0]['percent'].round()),'Islam '+str(vlg.loc[1]['percent'].round()),'Judaism '+str(vlg.loc[2]['percent'].round()),'Other '+str(vlg.loc[3]['percent'].round()),'Christianity '+str(usa.loc[0]['percent'].round()),'Islam '+str(usa.loc[1]['percent'].round()),'Judaism '+str(usa.loc[2]['percent'].round()),'Other '+str(usa.loc[3]['percent'].round())], 
    an_clr=(0,0,1), 
    an_antiheight=2, 
    grid_size=[0,5], 
    axis_length=[5,5], 
    origin=[0,0]
)

