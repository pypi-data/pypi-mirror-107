import requests
import bs4
import random
import urllib
import urllib.request
from newspaper import Article, Source, Config
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout
try:
    from .. import utils
except:
    from synchron import utils

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
    # config.MAX_SUMMARY=150
    config.MAX_SUMMARY_SENT=3
    article = Article(url=url,config=config)
    article.download()
    article.parse()
    article.nlp()
    return {
            'title':article.title,
            'summary':utils.clean_text(article.summary),
            'url':url,
            'keywords':"#"+" #".join(article.keywords[0:3]),
            'img':article.top_image,
            'author':", ".join(article.authors),
            'text':article.text,
            'movies':article.movies
            }

def get_tweet(url,bebukey=None):
    sum = summarize_article(url)
    tweet = utils.format_tweet(sum['title'],url,"","",bebukey)
    return {
        'tweet':tweet['tweet'],
        'title':tweet['title'],
        'summary':sum['summary'],
        'url':url,
        'keywords':sum['keywords']
        }

def get_update(term='news',bebukey=None):
    links = google(term)
    print('links:',len(links))
    if(links):return get_tweet(random.choice(links),bebukey)

#similar to update, but returns updates for all sources
def get_multiple(term='news',count=5,bebukey=None):
    links = google(term)
    print('links:',len(links))
    tweets = []
    if(links):
        for url in links:
            try:
                item = get_tweet(url,bebukey)
                tweets.append(item)
            except FunctionTimedOut:
                print("Timed out. Rejecting post.")
            except Exception as e:
                print(e)
                print("Couldn't get article for link: "+link)
            if(len(tweets)>=count):return tweets
    return tweets

#call with **spread
def get_posts(count=1,**kwargs):
    if('term' in kwargs):
        term = kwargs['term']
    else:
        term = "technology"

    if('bebukey' in kwargs):
        bebukey = kwargs['bebukey']
    else: 
        bebukey = None 

    posts = get_multiple(
        term,
        count,
        bebukey)
    if(not posts): raise Exception("No posts found!")
    return posts

if(__name__ == "__main__"):
    print(get_multiple())
