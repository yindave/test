# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:56:17 2020

@author: user
"""

import re
import nltk

#nltk set proxy here if needed
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('popular')

from nltk.corpus import stopwords
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
CENP=re.compile("[^\u4e00-\u9fa5^.^a-z^A-Z^0-9]") 


user_defined_drop=[]



_get_sentiment=analyzer.polarity_scores

def get_sentiment(text):
    return _get_sentiment(text)['compound']



stop_words = list(stopwords.words('english')) 
punctuations=string.punctuation
to_drop=user_defined_drop+stop_words

def clean_tokenize(text):
    sents=nltk.sent_tokenize(text)
    tokens=[]
    for sent in sents:
        token_i=nltk.word_tokenize(sent)
        token_i=[x for x in token_i if x.lower() not in stop_words]
        token_clean=[CENP.sub(r'', x)  for x in token_i if x not in punctuations]
        token_clean=[x for x in token_clean if x!='']
        tokens=tokens+token_clean

    return tokens
    


if __name__=='__main__':
    print ('ok')
    
    text='What is your name? I do not like apple. Please give me your an apple alright? Holy shit @abk. Fuck KKK!!!***'
    
    res=clean_tokenize(text)
    









