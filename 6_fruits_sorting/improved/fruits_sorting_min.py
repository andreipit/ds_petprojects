
# coding: utf-8

# #### 1) Create model

# In[9]:


get_ipython().magic('matplotlib notebook')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruits = pd.read_table('fruit_data_my.txt')
lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique())) #{1: 'apple', 2: 'mandarin', 3: 'orange', 4: 'lemon'}

X = fruits[['mass', 'width', 'height', 'color_score']]
y = fruits['fruit_label']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)              # default is 75% / 25% train-test split

knn = KNeighborsClassifier(n_neighbors = 6)                                            # Create classifier object
knn.fit(X_train, y_train)                                                              # Train the classifier
knn.score(X_test, y_test)                                                              # Estimate the accuracy


# #### 2) Use

# In[10]:


fruit_prediction = knn.predict([[208, 6.7, 11.2, 48]]) # lemon
#fruit_prediction = knn.predict([[264, 7.8, 9.4, 38]]) # orange
#fruit_prediction = knn.predict([[142, 6.3, 6.7, 23]]) # mandarin
#fruit_prediction = knn.predict([[276, 8.3, 8.7, 65]]) # apple
lookup_fruit_name[fruit_prediction[0]]                #Use the trained k-NN classifier model to classify new, previously unseen objects


# #### 3) Visualize

# In[11]:


from adspy_shared_utilities import plot_fruit_knn
plot_fruit_knn(X_train, y_train, 5, 'uniform')   # we choose 5 nearest neighbors

