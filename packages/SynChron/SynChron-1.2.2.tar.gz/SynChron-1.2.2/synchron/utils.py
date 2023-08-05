import random
import re
from io import StringIO
from datetime import datetime
#network
import requests
import ssl
import urllib.request
from urllib.request import Request, urlopen
#html processing
from html.parser import HTMLParser
from urlextract import URLExtract
#shorteners
import pyshorteners
# import feedparser
from newspaper import Article, Source, Config

#global variables
ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
max_len = 210 #280 max

########################################## GENERAL: ##########################################
def get_item(lis):
    items = lis.split(' ')
    if(len(items)==1):
        return str(items[0])
    else:
        return str(random.choice(items))

def timestamp():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def datestamp():
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y")

########################################## TEXT CLEANING: ####################################
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    text = s.get_data()
    return text

#strip unicode escape codes and sub with '
def strip_codes(str):
    return re.sub(r'\[?&#\d{4};\]?','\'',str)

def clean_text(str):
    #remove codes
    str = strip_codes(str)
    #remove any HTML tags
    str = strip_tags(str)
    #remove non-alphanumeric characters
    str = re.sub(r'\n',' ',str)
    str = re.sub(r'[^a-zA-Z0-9-_#@%&!.;:*$,|’\'\"\-() ]',' ', str)
    str = re.sub(r'Enlarge this image','',str)
    str = re.sub(r'toggle caption','',str)
    str = re.sub(r'BACKGROUND','',str)
    return str

def summarize_article(url,sent=3):
    print("Summarizing article at url:"+url)
    # print(url)
    config = Config()
    # config.MAX_SUMMARY=500
    config.MAX_SUMMARY_SENT=sent
    article = Article(url=url,config=config)
    article.download()
    article.parse()
    article.nlp()
    return {
            'title':clean_text(article.title),
            'summary':clean_text(article.summary),
            'url':url,
            'keywords':"#"+" #".join(article.keywords[0:3]),
            'img':article.top_image,
            'author':", ".join(article.authors),
            'text':article.text,
            'movies':article.movies
            }

def summarize_post(post):
    if('summary' in post): 
        post['summary'] = clean_text(post['summary'])
    elif('description' in post):
        post['summary'] = clean_text(post['description'])
    elif('abstract' in post):
        post['summary'] = clean_text(post['abstract'])
    try:
        parsed = summarize_article(get_url(post))
        if('author' not in post): post['author'] = parsed['author']
        post['img'] = parsed['img']
        post['movies'] = parsed['movies']
        if('summary' not in post): post['summary'] = parsed['summary']
    except Exception as e:
        print(e)
        post['img'] = ""
        post['author'] = ""
        post['movies'] = ""
    return post

def format_tweet(ti,url,summary="",intro="",bebukey=None):
    title = intro+clean_text(ti)
    title_len = len(title)
    max_url = max_len - title_len #shorten url based on title len
    url = shorten_link(url,max_url,bebukey)
    url_len = len(url)
    max_title = max_len - url_len-6
    truncated=''
    if(len(title)>max_title):
        truncated='...'
    title = title[0:max_title]
    title_len = len(title)
    summary = clean_text(summary)
    return {
        'tweet':"""{}{} {}""".format(title,truncated,url),
        'title':title,
        'summary':summary,
        'url':url
    }
########################################## URLS: ##########################################
def get_url(post):
    if('url' in post): return clean_url(post['url'])
    elif('full_url' in post): return clean_url(post['full_url'])
    elif('link' in post): return clean_url(post['link'])

def clean_url(url):
    try:
        return unshorten(url)
    except Exception as e:
        print(e)
        print("Error cleaning url: "+str(url))
        if('404' in str(e)):
            print("404 - not found.")
            raise Exception("404")
        elif('403' in str(e)):
            print("403 - blocked from visiting, but url may still be OK.")
    return url

#unshorten by visiting URL and returning url of opened site
def unshorten(url):
    req = Request(url, headers={'User-Agent': ua})
    url= urllib.request.urlopen(req,context=ssl._create_unverified_context()).url
    return url

def bebube(link,apikey):
    params={"longDynamicLink": "https://bebu.be/?link="+link, "suffix": { "option": "SHORT" } }
    url = """https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={}""".format(apikey)
    r = requests.post(url, json=params).json()['shortLink']
    return(r)

def shorten_link(url="",max_len=100,bebukey=None):
    # print("Shortening link: "+url)
    url = clean_url(url)
    s = pyshorteners.Shortener()
    if(len(url)< max_len):
        return url
    try:
        print("Getting bebu.be short link")
        short = bebube(url,bebukey)
        print(short)
        return short
    except:
        print("Getting is.gd link")
        short = s.isgd.short(url)
        return short

def follow_link(url,term = "udemy.com",level = 0,max_levels = 2):
    print("Checking url for term: "+url)
    if(term not in url and levels < max_levels):
        request_result=requests.get(url)
        follow_link(request_result,levels+1)
    else:
        return url

def get_hrefs(url):
    request_result=requests.get( url )
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    raw_links = soup.find_all("a", href=True)
    return raw_links

def get_links(url):
    extractor = URLExtract()
    req = requests.get(url)
    page = req.text
    urls = extractor.find_urls(page)
    return urls

########################################## Tests: ##########################################
def test():
    text="Resumption Recommendation Expected - <p><span><span>The <em>Washington Post</em> reports that US officials are expected to give the go-ahead to resume using Johnson & Johnson's !!! #awesome!<span>SARS</span>-<span>CoV</span>-2 vaccine.</spa"
    print(clean_text(text))

if(__name__=='__main__'):
    test()