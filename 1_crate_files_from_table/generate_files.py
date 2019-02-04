
# coding: utf-8

# In[1]:


import pandas as pd
import re

def save2txt(row):
    if row[0]<10: row[0] = "0" + str(row[0])
    file_name = str(row[0]).strip() + "_" + row[1].strip() + "_" + row[2].strip()
    print(file_name)
    file = open(file_name+'.py', 'w')
    line = "0) summary-------------------------------------------------------------------------------"
    file.write(file_name+'.py' + '\n' + '\n' + line)
    file.close()
    return row

df = pd.read_csv('calendar.txt', skiprows=0, delimiter="\t")

df['TOPICS'] = df['TOPICS'].str.replace(' ', '_')
df['TOPICS'] = df['TOPICS'].str.replace('\\', 'ibackslash')
df['TOPICS'] = df['TOPICS'].str.replace('/', 'islash')
df['TOPICS'] = df['TOPICS'].str.replace(':', 'icolon')
df['TOPICS'] = df['TOPICS'].str.replace('*', 'istar')
df['TOPICS'] = df['TOPICS'].str.replace('?', 'iquest')
df['TOPICS'] = df['TOPICS'].str.replace('"', 'iquotes')
df['TOPICS'] = df['TOPICS'].str.replace('<', 'iless')
df['TOPICS'] = df['TOPICS'].str.replace('>', 'imore')
df['TOPICS'] = df['TOPICS'].str.replace('|', 'ior')

df['KEY DATES'] = df['KEY DATES'].str.replace(' ', '_')
df['KEY DATES'] = df['KEY DATES'].str.replace('\\', 'ibackslash')
df['KEY DATES'] = df['KEY DATES'].str.replace('/', 'islash')
df['KEY DATES'] = df['KEY DATES'].str.replace(':', 'icolon')
df['KEY DATES'] = df['KEY DATES'].str.replace('*', 'istar')
df['KEY DATES'] = df['KEY DATES'].str.replace('?', 'iquest')
df['KEY DATES'] = df['KEY DATES'].str.replace('"', 'iquotes')
df['KEY DATES'] = df['KEY DATES'].str.replace('<', 'iless')
df['KEY DATES'] = df['KEY DATES'].str.replace('>', 'imore')
df['KEY DATES'] = df['KEY DATES'].str.replace('|', 'ior')

df.apply(save2txt, axis=1)

