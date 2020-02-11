# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:02:59 2020

@author: user
"""

import pandas as pd
import numpy as np
import utilities.misc as um
import utilities.constants as uc
from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.error, urllib.parse
import re
import pdb

### constant
use_proxy=False
proxy_to_use=uc.proxy_to_use


def get_weibo(topic_chinese,date,cookie):
    '''
    Maximum number of pages for each search is 50 
    To minimize the risk of missing too much data, we only scrape for hot topic by date
    Need to manually update the cookie each time, cookie can change after a few hours
    '''
    
    ### input
    topic=topic_chinese
    start=date
    end=date
    # can add region later if need this function
    # we only get hot topic for now, modify url later if need this function
    
    ### start to get information
    pages=np.arange(1,51,1) # maximum number of page for search is 50
    topic_decode=topic.encode('utf-8')
    q=str(topic_decode).replace('\\x','%').replace("b'",'').replace("'",'').upper()
    summary_collector=[]
    
    print ('Start working on topic %s on %s' % (topic_chinese,date.strftime('%Y-%m-%d')))
    for page in pages:
        
        url=('https://s.weibo.com/weibo?q=%s&xsort=hot&suball=1&timescope=custom:%s-0:%s-24&Refer=g&page=%s' 
            % (q,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),page))
        session = requests.Session()
        response = session.get(url,headers={'cookie':cookie},proxies=proxy_to_use if use_proxy else None)
        soup = BeautifulSoup(response.content,features="lxml") 
        
        # check if reaching the last page
        try:
            soup.findAll('div',{'class':'card card-no-result s-pt20b40'})[0].findAll('p')[0]
            is_end=True
        except IndexError:
            is_end=False
        
        if not is_end:
            # short content and actions
            content=soup.findAll('p',{'class':'txt','node-type':'feed_list_content'})
            fwds=soup.findAll('a',{'action-type':'feed_list_forward'})
            comments=soup.findAll('a',{'action-type':'feed_list_comment'})
            likes=soup.findAll('a',{'action-type':'feed_list_like'})
            
            summary=pd.DataFrame(index=np.arange(0,len(content),1),columns=['owner','content','fwd','comment','like'])
            for i in np.arange(0,len(content),1):
                summary.at[i,'content']=re.sub("#","",content[i].text)
                summary.at[i,'owner']=content[i].get('nick-name')
                try:
                    summary.at[i,'fwd']=int(fwds[i].contents[0][4:])
                except:
                    summary.at[i,'fwd']=0
                try:
                    summary.at[i,'comment']=int(comments[i].contents[0][3:])
                except:
                    summary.at[i,'comment']=0
                try:
                    summary.at[i,'like']=int(likes[i].contents[2].contents[0])
                except:
                    summary.at[i,'like']=0
                
            # full content
            content=soup.findAll('p',{'class':'txt','node-type':'feed_list_content_full'})
            summary_full=pd.DataFrame(index=np.arange(0,len(content),1),columns=['owner','content_full'])
            for i in np.arange(0,len(content),1):
                summary_full.at[i,'content_full']=re.sub("#","",content[i].text)
                summary_full.at[i,'owner']=content[i].get('nick-name')
            
            # overwrite with full contentss. 
            # Need to do groupby here as we can have multiple tweets from the same owner
            try:
                summary=pd.concat([summary.groupby('owner').sum(),
                                   summary_full.set_index('owner').groupby('owner').sum()
                                   ],axis=1).fillna(0)
            except:
                pdb.set_trace()
            summary['content']=summary[['content','content_full']].apply(lambda x: x['content'] if x['content_full']==0 else x['content_full'],axis=1)
            summary=summary.drop('content_full',1)
            
            summary_collector.append(summary)
            print ('Finish page %s' % (page))
            
        else:
            print ('Page %s is the end page' % (page-1))
            if len(summary_collector)==0:
                print ('Nothing returned')
                return False
            
            summary_all=pd.concat(summary_collector,axis=0)
            summary_all['topic']=topic
            summary_all['date']=date
            summary_all.index.name='owner'
            
            return summary_all.reset_index()
        
        
if __name__=='__main__':
    print ('ok')
    
    
    cookie='SINAGLOBAL=1939137473236.7695.1359786817801; wvr=6; UOR=cn.wsj.com,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5GrRHKMLMbdJMQDxRPi1695JpX5KMhUgL.FoM01h-N1hBce052dJLoI0jLxK-LBKBLB-2LxK.L1KnLBoeLxKnL1heLB.BLxKqL1h.L12zLxKML1KBLBo-LxKMLB-BL1KzEShM01Btt; webim_unReadCount=%7B%22time%22%3A1580869667884%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D; ALF=1612486248; SSOLoginState=1580950250; SCF=AuNRrR3OOAeW3qjtI0IQx4C0_QxU1OBOXeuhJKBl0eRSrdYHNVYBElW9RuhthsOX4_MkHOgpL4Ka6hpzzytgpxE.; SUB=_2A25zPxK7DeThGeFN41cW-CrKyDyIHXVQTQNzrDV8PUNbmtAfLUbVkW9NQ9OAjktkB3DzCHYOGBrCBwVZgxa-IWQ8; SUHB=03oVaD9G-rimrV; _s_tentry=login.sina.com.cn; Apache=2865394554053.069.1580950476493; ULV=1580950476558:10:4:4:2865394554053.069.1580950476493:1580862453173'

    
    topic='肖战'
    date=pd.datetime(2020,2,5)
    
    weibo=get_weibo(topic,date,cookie)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    












