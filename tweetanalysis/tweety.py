import matplotlib.pyplot as plt
from textblob import TextBlob
import re
import numpy as np
import pandas as pd
import sys
import os
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy


def Analyzer(tweeet_id, n):
    # VARIABLE THAT CONTAINS THE TWITTER CREDETIALS
    ACCESS_TOKEN = "1283415560793886720-r2s1cwXb8deElE039pnVa51KYG0jtV"
    ACCESS_TOKEN_SECRET = "eGUOkGlOZJzZ8gaiIi06vpJrl1tL36FeTWhN7AqwLqsQW"
    CONSUMER_KEY = "eHr7pzNzExEMecdwka201QKe2"
    CONSUMER_SECRET = "lGgtiIFQTA1XWuqvnqKoEoUdsPgokYvomAau76WDEcOyVmAcva"

    # Create Authentication
    authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # access token and access token secret
    authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    # for tweet in posts[0:5]:
    #    print(tweet.full_text + '\n')

    posts = api.user_timeline(screen_name=tweeet_id,
                              count=n, tweet_mode="extended")
    # Create a dataframe with a column called Tweets

    df = pd.DataFrame([" ".join(tweet.full_text.splitlines())
                      for tweet in posts], columns=['Tweet'])
    df

    def cleaning(text):
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'RT[\s]+', '', text)
        text = re.sub(r'https?:\/\/\S+', '', text)
        return text

    df['Tweet'] = df['Tweet'].apply(cleaning)

    # **Subjectivity: personal opinion, emotion or judgment whereas objective refers to factual information.**

    def getsubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # **Polarity: it determines if the text expresses the positive, negative or neutral sentiment of the user**

    def getpolarity(text):
        return TextBlob(text).sentiment.polarity

    df['Subjectivity'] = df['Tweet'].apply(getsubjectivity)
    df['Polarity'] = df['Tweet'].apply(getpolarity)

    #allword = ' '.join([twts for twts in df['Tweet']])
    # wordcloud = WordCloud(width=600, height=400, random_state=21,
    #                      max_font_size=119).generate(allword)

    #plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

    # **Get postive,neutral and positive analysis**

    def getPolarityAnalysis(pol):
        if pol < 0:
            return 'Negative'
        elif pol == 0:
            return 'Neutral'
        else:
            return 'Positive'

    df['Analysis'] = df['Polarity'].apply(getPolarityAnalysis)

    df

    # print all positive tweets
    j = 1
    sortedDF = df.sort_values(by=['Polarity'])
    for i in range(0, sortedDF.shape[0]):
        if(sortedDF.loc[i, 'Analysis'] == 'Positive'):
            print(str(j) + ')' + sortedDF.loc[i, 'Tweet'])
            print()
            j += 1

    # print all negative tweets
    j = 1
    for i in range(0, sortedDF.shape[0]):
        if(sortedDF.loc[i, 'Analysis'] == 'Negative'):
            print(str(j) + ')' + sortedDF.loc[i, 'Tweet'])
            print()
            j += 1

    # Plot subjective and Polarity
    '''
    plt.figure(figsize=(8, 6))
    for i in range(0, df.shape[0]):
        plt.scatter(df.loc[i, 'Polarity'],
                    df.loc[i, 'Subjectivity'], color='Blue')

    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.show()

    # **Percentage of positive,  Negative, Neutral tweets**

    ptweets = df[df.Analysis == 'Positive']
    ptweets = ptweets['Tweet']

    (ptweets.shape[0]/df.shape[0])*100

    negtweets = df[df.Analysis == 'Negative']
    negtweets = negtweets['Tweet']

    (negtweets.shape[0]/df.shape[0])*100

    netweets = df[df.Analysis == 'Neutral']
    netweets = netweets['Tweet']

    (netweets.shape[0]/df.shape[0])*100

    # **Value Count in Plot Bar**

    df['Analysis'].value_counts()

    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    df['Analysis'].value_counts().plot(kind='bar')
    plt.show()
    '''

    return df
