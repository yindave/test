# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:23:26 2020

@author: user
"""

from aip import AipNlp
import pandas as pd
import numpy as np
import utilities.misc as um
import utilities.constants as uc
import re


APP_ID = '18384134'
API_KEY = 'IssRzCQo10CtCbQnUWr3KyHH'
SECRET_KEY = 'gHcoDNbGfhpvGsc50EcZlZvQRmPgFjoY'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def _clean_text(text):
    # with punctuation removed the nltk can work better
    CENP=re.compile("[^\u4e00-\u9fa5^.^a-z^A-Z^0-9]") 
    return CENP.sub(r'', text) 

def get_sentiment_simple(text):
    try:
        return client.sentimentClassify(_clean_text(text))['items'][0]['sentiment']
    except:
        return -1

def get_sentiment_positive_proba(text):
    try:
        return client.sentimentClassify(_clean_text(text))['items'][0]['positive_prob']
    except:
        return -1

def tokenize(text):
    items=client.lexer(_clean_text(text))['items']
    collector=[]
    for i,item in enumerate(items):
        s_i=pd.Series(index=['item','pos','ne'],data=[item['item'],item['pos'],item['ne']]).rename(i)
        collector.append(s_i)
    res=pd.concat(collector,axis=1).T
    res['prop']=res[['pos','ne']].sum(1)
    return res.drop(['pos','ne'],axis=1)

def tokenize_df(df,text_col,
                prop_to_remove=['d','p','c','u','xc','w','r','f']):
    '''
    With reference to this https://ai.baidu.com/docs#/NLP-Python-SDK/top
    By default we remove prep, punctuation etc
    '''
    
    WORDS_TO_REMOVE=['微博','视频','收起','全文','有','没有','一个','做','来','会',
                     '说','是','链接']
    if len(df)!=0:
        collector=[]
        for text in df[text_col].values:
            res=tokenize(text)
            collector.append(res)
        output=pd.concat(collector,axis=0)
        
        return output[(~output['prop'].isin(prop_to_remove)) 
                      & (~output['item'].isin(WORDS_TO_REMOVE))]
    else:
        return False













