from django.shortcuts import render, HttpResponse, redirect
from tweetanalysis import tweety
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
# Create your views here.


def index(request):
    if request.method == 'POST':
        redirect(request, 'result.html')
    return render(request, 'index-search.html')


def scatterplot(df):
    plt.figure(figsize=(8, 6))
    for i in range(0, df.shape[0]):
        plt.scatter(df.loc[i, 'Polarity'],
                    df.loc[i, 'Subjectivity'], color='Blue')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    ans1 = base64.b64encode(image_png)
    ans1 = ans1.decode('utf-8')
    buffer.flush()
    buffer.close()
    return ans1


def barplot(df):
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    df['Analysis'].value_counts().plot(kind='bar')
    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    image_png = buffer1.getvalue()
    ans2 = base64.b64encode(image_png)
    ans2 = ans2.decode('utf-8')
    buffer1.flush()
    buffer1.close()
    return ans2


def result(request):
    if request.method == 'POST':
        query = request.POST.get('hashtage')
        query2 = request.POST.get('number')
        try:
            df = tweety.Analyzer(query, query2)

            ans1 = scatterplot(df)

            ans2 = barplot(df)

            ptweets = df[df.Analysis == 'Positive']
            ptweets = ptweets['Tweet']

            posper = (ptweets.shape[0]/df.shape[0])*100

            negtweets = df[df.Analysis == 'Negative']
            negtweets = negtweets['Tweet']

            negper = (negtweets.shape[0]/df.shape[0])*100

            netweets = df[df.Analysis == 'Neutral']
            netweets = netweets['Tweet']

            neutper = (netweets.shape[0]/df.shape[0])*100
            pos = 0
            neg = 0
            neu = 0
            if('Positive' in df['Analysis'].value_counts()):
                pos = df['Analysis'].value_counts()['Positive']
            if('Negative' in df['Analysis'].value_counts()):
                neg = df['Analysis'].value_counts()['Negative']
            if('Neutral' in df['Analysis'].value_counts()):
                neu = df['Analysis'].value_counts()['Neutral']
            return render(request, 'result.html', context={'chart': ans1, 'plot': ans2, 'pos': pos, 'neg': neg, 'neu': neu, 'posper': posper, 'negper': negper, 'neutper': neutper})
        except:
            return render(request, 'Error.html', context={"id": query})
