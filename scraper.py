from email import header
from statistics import mean
import twint
import pandas as pd
import random as rand
import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from matplotlib import pyplot

import nest_asyncio

# Uncomment to use nltk interface
# nltk.download()
 
nest_asyncio.apply()

SWD = input('Enter Keyword: ')
SWD = SWD + ' OR ' + SWD.lower()
IVAL = int(input('Enter interval (days): '))
LMT = int(input('Enter # of tweets per interval: '))

class TwintModel:
    def __init__(self, start) -> None:
        self.start = start
        self.end = start + datetime.timedelta(days=IVAL)
        self.id = str(rand.randint(1,1000000))
        self.config = self.get_conf()
        
    def get_conf(self):
        c = twint.Config()
        
        c.Search = SWD
        
        c.Lang = 'en'
        c.Limit = LMT
        c.Store_csv = True
        c.Output = 'scrapes/scrape' + self.id + '.csv'
        c.Hide_output = True
        c.Since = self.start.strftime("%Y-%m-%d")
        c.Until = self.end.strftime("%Y-%m-%d")
        
        return c
    

        
    
    def run_scrape(self):
        twint.run.Search(self.config)

class SentModel:
    def __init__(self) -> None:
        self.sia = SentimentIntensityAnalyzer()
    
    def get_sent(self, text):
        return self.sia.polarity_scores(text)['compound']
    

if __name__ == '__main__':
    strdate = input('Enter date (yyyy-mm-dd): ')
    strlist = [int(x) for x in strdate.split('-')]
    sdate = datetime.date(strlist[0], strlist[1], strlist[2])
    
    sm = SentModel()
    sent_avgs = []
    for i in range(int(input('Enter # of data points: '))):
        c = TwintModel(sdate)
        c.run_scrape()
        
        df = pd.read_csv('scrapes/scrape' + c.id + '.csv')
        
        tweets = []
        for index, row in df.iterrows():
            tweets.append(row.tweet)

        tweets_sent = [sm.get_sent(t) for t in tweets]
        sent_avgs.append(dict(date=c.start, avg=mean(tweets_sent)))
        sdate = c.end
    
    for x in sent_avgs:
        print(x['date'], x['avg'])
        
    series = pd.DataFrame(sent_avgs)
    series.plot(x='date', y='avg', kind='line')
    pyplot.show()
    
    