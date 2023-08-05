import requests
import bs4
import random
import urllib
import urllib.request
import pyshorteners
from newspaper import Article, Source, Config
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout
try:
    from .. import utils
except:
    from synchronicity import utils

msm = ['cnn','businessinsider','zdnet','npr','nytimes','bbc','msnbc','cbs','nbc','abc','wsj','usnews','economist','washingtonpost','forbes']

@func_set_timeout(10)
def google(term):
    news_search='&tbm=nws'
    blog_search='&tbm=blg'
    image_search='&tbm=isch'
    base='https://www.google.com/search?q='
    url=base+term+news_search
    request_result=requests.get( url )
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    raw_links = soup.find_all('a', href=True)
    news_links = []
    for link in soup.find_all('a', href=True):
        hl=link['href'][7:].split('&sa')[0]
        if(('google' not in hl) and ('http' in hl)):# 
            if any(s for s in msm if s in hl): 
                news_links.append(hl)
    return news_links

def summarize_article(url):
    config = Config()
    config.MAX_SUMMARY=150
    config.MAX_SUMMARY_SENT=1
    article = Article(url=url,config=config)
    article.download()
    article.parse()
    article.nlp()
    return {
            'title':article.title,
            'summary':article.summary,
            'url':url,
            'keywords':article.keywords
            }

def get_tweet(url):
    sum = summarize_article(url)
    tweet = utils.format_tweet(sum['title'],url)
    return {
        'tweet':tweet['tweet'],
        'title':tweet['title'],
        'summary':tweet['summary'],
        'url':url,
        'keywords':sum['keywords']
        }

def get_update(term='news'):
    links = google(term)
    print('links:',len(links))
    if(links):return get_tweet(random.choice(links))

#similar to update, but returns updates for all sources
def get_multiple(term='news',count=5):
    links = google(term)
    print('links:',len(links))
    tweets = []
    if(links):
        for url in links:
            try:
                item = get_tweet(url)
                tweets.append(item)
            except FunctionTimedOut:
                print("Timed out. Rejecting post.")
            except Exception as e:
                print(e)
                print("Couldn't get article for link: "+link)
            if(len(tweets)>=count):return tweets
    return tweets

if(__name__ == "__main__"):
    print(get_multiple())
