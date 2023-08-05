from io import StringIO
from html.parser import HTMLParser
import feedparser
import random
import requests
import re
import pyshorteners
import urllib.request
import ssl
import urlextract
from urlextract import URLExtract
from urllib.request import Request, urlopen
ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
max_len = 220 #280 max

########################################## GENERAL: ##########################################
def get_item(lis):
    items = lis.split(' ')
    if(len(items)==1):
        return str(items[0])
    else:
        return str(random.choice(items))

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
    str = re.sub(r'[^a-zA-Z0-9-_#@%&!.;:,| ]','', str)
    return str

def format_tweet(ti,url,summary="",intro=""):
    title = intro+clean_text(ti)
    title_len = len(title)
    max_url = max_len - title_len #shorten url based on title len
    url = shorten_link(url,max_url)
    url_len = len(url)
    max_title = max_len - url_len-3
    truncated=''
    if(len(title)>max_title):
        truncated='...'
    title = title[0:max_title]
    title_len = len(title)
    summary = clean_text(summary)
    return {
        'tweet':"""{}{} {}""".format(title,truncated,url)[0:max_len],
        'title':title,
        'summary':summary,
        'url':url
    }
########################################## URLS: ##########################################
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
    
def shorten_link(url="",max_len=100):
    # print("Shortening link: "+url)
    url = clean_url(url)
    s = pyshorteners.Shortener()
    if(len(url)< max_len):
        return url
    else:
        return s.isgd.short(url)

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