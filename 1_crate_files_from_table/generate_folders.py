import pandas as pd
import re
import os
ROOT_FOLDER = 'folders'       
FOLDER_LIST = 'folders_list.txt' # first row must be "name"      

def clean_symbols(df, column):
    df[column] = df[column].str.replace(' ', '_')
    df[column] = df[column].str.replace('\\', '_ibackslash_')
    df[column] = df[column].str.replace('/', '_islash_')
    df[column] = df[column].str.replace(':', '_icolon')
    df[column] = df[column].str.replace('*', '_istar_')
    df[column] = df[column].str.replace('?', '_iquest')
    df[column] = df[column].str.replace('"', '_iquotes_')
    df[column] = df[column].str.replace('<', '_iless_')
    df[column] = df[column].str.replace('>', '_imore_')
    df[column] = df[column].str.replace('|', '_ior_')
    return df
df = pd.read_csv(FOLDER_LIST, skiprows=0, delimiter="\t")
df = clean_symbols(df, 'name')
if not os.path.exists(ROOT_FOLDER): os.makedirs(ROOT_FOLDER)
for i in range(len(df)):
    num = i
    if num < 10: num = str(0) + str(i)
    new_name = ROOT_FOLDER + '/' + (str(num)) + '_' + df.iloc[i]['name']
    if not os.path.exists(new_name): os.makedirs(new_name)
