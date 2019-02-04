
# coding: utf-8

# In[1]:


import time
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pandas as pd
import numpy as np

last_df = pd.DataFrame()

def surf_web():
    # load urls & queries
    queries=[]
    urls=[]
    for line in open('search_query.txt',encoding="utf8"): queries.append(line.rstrip())
    for line in open('urls.txt'): urls.append(line.rstrip())

    # init df
    df = pd.DataFrame(columns = ['url', 'query', 'count'])
    for u in urls:
        for q in queries:
            df = df.append(pd.Series({'url': u, 'query': q, 'count': 0}) , ignore_index=True)

    # download page and count words
    for url in urls:
        fhand = urllib.request.urlopen(url)    #same as file.open
        for line in fhand:
            line = line.decode().strip()
            for query in queries:
                if query in line:
                    df['count'][(df['url']==url) & (df['query']==query)] += 1

    return df[(df['count']!=0)]

def save_df2html(df):
    HEADER = '''
    <html>
        <head>

        </head>
        <body>
    '''
    FOOTER = '''
        </body>
    </html>
    '''
    with open('result.html', 'w', encoding='utf8') as f:
        f.write(HEADER)
        f.write(df.to_html(classes='df'))
        f.write(FOOTER)

  
def save_df2sql(df):
    import sqlite3
    import urllib.request
    conn = sqlite3.connect('result.sqlite')
    cur = conn.cursor()
    cur.execute('''
    DROP TABLE IF EXISTS Search''')
    cur.execute('''
    CREATE TABLE Search (url TEXT, query TEXT, count INTEGER)''')
    df.apply(lambda row: cur.execute('''INSERT INTO Search (url, query, count) VALUES ( ?, ?, ? )''', ( str(row['url']), str(row['query']), int(row['count']))), axis=1)
    conn.commit()
        
        
def sent_email():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #parse txt
    emails=[]
    with open('email.txt') as file:
        for line in file: emails.append(line.rstrip())
    fromaddr = emails[1]
    pwd = emails[3]
    toaddr = emails[5]
    
    #attach test.html
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE MAIL"
    body = open('result.html',encoding='utf8').read()
    # body = "YOUR MESSAGE HERE"
    msg.attach(MIMEText(body, 'plain'))
    
    #ligin and send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def update():
    global last_df
    df = surf_web()
    if last_df.equals(df):
        print('df is same -> no notification')
    else:
        last_df = df
        save_df2html(df)
        save_df2sql(df)
        sent_email()
        print('notification sent')

# loop & wait, loop & wait...
i = 0
while True:
    i += 1
    update ()
    time.sleep(10)
    if i==2: break

