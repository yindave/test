# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:35:23 2020

@author: user
"""

import pandas as pd
import pdb
import twitter


consumer_key = 'TSa4wica64R6phmKh3S4OPp7d'
consumer_secret = 'LMqcIJKHilKbVzRUn8rGSG4OmYjQPGGKHPlVILLCIcsICNhDqE'
access_token = '344846030-pLd0078cG0TQw6qsx5tZHxIdIuJTAPlArFChPetQ'
access_token_secret = 'ql6zlnOykXKtRRnJFuKFVmC60c1WYoDGxauzCBxtTCEyA'

myself='davehanzhang'
max_count=200

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret,                      
                  tweet_mode='extended',
                  sleep_on_rate_limit=True)
api.VerifyCredentials()



def _combine_tweet_list(input_list,start_date,end_date):
    
    if len(input_list)!=0:
        res_all=input_list
        collector=[]
        for res_i in res_all:
            
            index_i=['user_id','user_name','tweet_id',
                     'date','likes','retweets','lang',
                     'hashtags','mentions_id','mentions_name','text']
            data_i=[]
            data_i.append(res_i.user.id)
            data_i.append(res_i.user.screen_name)
            data_i.append(res_i.id)
            data_i.append(res_i.created_at)
            data_i.append(res_i.favorite_count)
            data_i.append(res_i.retweet_count)
            data_i.append(res_i.lang)
            data_i.append([i.text for i in res_i.hashtags])
            data_i.append([i.id for i in res_i.user_mentions])
            data_i.append([i.screen_name for i in res_i.user_mentions])
            data_i.append(res_i.full_text)
            
            tweet_i=pd.Series(index=index_i,data=data_i)
            collector.append(tweet_i)
        output_i=pd.concat(collector,axis=1).T
        output_i['date']=pd.to_datetime(output_i['date'])
        output_i['date']=output_i['date'].map(lambda x: pd.datetime(x.year,x.month,x.day))
        output_i=output_i[(output_i['date']>=start_date) & (output_i['date']<=end_date)]
      
        return output_i
    
    else:
        return pd.Series()



def _combine_tweet_list_recurall(id_i,start_date,end_date):
    collector=[]
    input_list=api.GetUserTimeline(user_id=id_i,count=max_count)
    
    def _iterate(input_list,id_i,start_date,end_date):
        output_i=_combine_tweet_list(input_list,start_date,end_date)
        if len(output_i)!=0:
            collector.append(output_i)
            max_id=input_list[-1].id-1
            input_list=api.GetUserTimeline(user_id=id_i,count=max_count,
                                           max_id=max_id)
            return _iterate(input_list,id_i,start_date,end_date)
        else:
            return pd.concat(collector) if len(collector)!=0 else pd.Series()
        
    return _iterate(input_list,id_i,start_date,end_date)




def get_all_tweets_from_friends(start_date,end_date):
    
    friends=api.GetFriends(screen_name=myself)

    start_date=start_date
    end_date=end_date
    collector=[]

    for i,f in enumerate(friends):
        id_i=f.id
        tweets_i=_combine_tweet_list_recurall(id_i,start_date,end_date)
        print ('finished friend number %s/%s, total tweet collected is %s' % (i+1,len(friends),len(tweets_i)))
        collector.append(tweets_i)
        
    return pd.concat(collector,axis=0)



if __name__=='__main__':
    print('ok')
#    
#    start=pd.datetime(2019,12,1)
#    end=pd.datetime(2020,2,12)
#
#    res=get_all_tweets_from_friends(start,end)
#    












































