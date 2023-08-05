import feedparser
import random
import requests
import re
import json
import pyshorteners
import urllib.request
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout
import time 
from os import path
cwd = path.dirname(__file__)
package_name = "synchronicity"
from urllib.request import Request, urlopen
try:
    from .. import utils
except:
    from synchronicity import utils

ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
max_tries = 10
max_len = 250

#################################### Preconfigured feeds: ####################################
def load_feeds(file='feeds.json'):
    file_path = path.join(cwd, file)
    with open(file_path) as f:
        feeds = json.load(f)
        return feeds
#################################### Check content: ####################################

def valid_string(check_string,rejects=['404','error']):
    if (any(term in check_string for term in rejects)): return False
    return True

def valid_post(post,rejects = ['404','error']):
    post['title'] = utils.clean_text(post['title'])
    return (valid_string(post['title'],rejects) and valid_string(post['url'],rejects))

#################################### Generic RSS Feed: ####################################
def format_rss_result(ref):
    if('url' not in ref):
        if('link' in ref):
            ref['url'] = ref['link']
        else:
            print("Can't identify URL in post.")
            raise Exception("Invalid post")
    try:
        ref['url'] = utils.clean_url(ref['url'])
    except:
        ref['url'] = ref['url']
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],ref['url'])['tweet']
    return {
        'tweet':tweet,
        'title':ref['title'],
        'summary':utils.clean_text(ref['summary']),
        'url':ref['url']
        }

############################## Nature Blog: ##############################
def format_nature_blog_result(ref):
    full_url = utils.clean_url(ref['id'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url)['tweet']
    return {
        'tweet':tweet,
        'title':ref['title'],
        'summary':utils.clean_text(ref['summary']),
        'url':full_url
        }

#################################### BioITWorld: ####################################
def format_bioitworld_result(ref):
    full_url = utils.clean_url(ref['link'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url)['tweet']
    return {
        'tweet':tweet,
        'title':ref['title'],
        'summary':utils.clean_text(ref['summary']),
        'url':full_url
        }

#################################### GenomeWeb: ####################################
def format_genomeweb_result(ref):
    full_url = utils.clean_url(ref['link'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url)['tweet']
    return {
        'tweet':tweet,
        'title':ref['title'],
        'summary':utils.clean_text(ref['summary']),
        'url':full_url
        }

#################################### Techcrunch: ####################################
def format_techcrunch_result(ref):
    full_url = utils.clean_url(ref['link'])
    print("Updated URL for post: "+full_url)
    tweet = utils.format_tweet(ref['title'],full_url)['tweet']
    return {
            'tweet':tweet,
            'title':utils.clean_text(ref['title']),
            'summary':utils.clean_text(ref['summary']),
            'url':full_url
        }

#################################### Pubmed: ####################################
def format_pubmed_result(ref):
    full_url = """https://doi.org/{}""".format(ref['dc_identifier'][4:])
    full_url = utils.clean_url(full_url)
    print("Updated URL for post: "+full_url)
    tweet = utils.format_tweet(ref['title'],full_url)['tweet']
    return {
            'tweet':tweet,
            'title':utils.clean_text(ref['title']),
            'summary':utils.clean_text(ref['summary']),
            'url':full_url
        }

#################################### Indeed: ####################################
def format_indeed_result(ref):
    print("Found result: "+ref['title'])
    url = utils.clean_url(ref['link'])
    print("Getting company URL")
    company_url = url
    links = utils.get_links(url)
    for link in links:
        if("indeed.com/rc/clk" in link):
            company_url = utils.unshorten(link)
            break
    ref['url'] = company_url
    title = utils.clean_text(ref['title'])
    intro="👍 JOB ALERT👍 "
    tweet = utils.format_tweet(title,ref['url'],"",intro)['tweet']
    return {
        'tweet':tweet,
        'title':title,
        'summary':utils.clean_text(ref['description']),
        'url':ref['url'],
        'source':ref['source']
        }
#################################### Get Result: ####################################
@func_set_timeout(10)
def format_result(res,res_type='rss'):
    if(res_type == 'pubmed'): return(format_pubmed_result(res))
    if(res_type == 'techcrunch'): return(format_techcrunch_result(res))
    if(res_type == 'nature_blog'): return(format_nature_blog_result(res))
    if(res_type == 'genomeweb'): return(format_genomeweb_result(res))
    if(res_type == 'bioitworld'): return(format_bioitworld_result(res))
    if(res_type == 'indeed'): return(format_indeed_result(res))
    else: return(format_rss_result(res))

def get_rss(url,count=1,rss_type='rss'):
    rejects = ['404','error']
    NewsFeed = feedparser.parse(url)
    #For single post, select randomly from posts
    tries = 0
    if(count <=1):
        while(tries < max_tries):
            tries += 1
            post = random.choice(NewsFeed.entries)
            print("Getting RSS result. Attempt: %i"%(tries))
            try:
                # post = format_rss_result(post)
                post = format_result(post,rss_type)
                # post = func_timeout(10,format_result, args=(post,rss_type))
                if(valid_post(post),rejects): 
                    # res = format_result(post)
                    res = post
                    return res
            except FunctionTimedOut:
                print("Timed out. Rejecting post.")
            except Exception as e:
                print(e)
                print("Invalid post.")
    else:
        res = []
        for post in NewsFeed.entries:
            try:
                post = format_result(post,rss_type)
                # post = format_rss_result(post)
                if(valid_post(post,rejects)): 
                    res.append(post)
                    print("Retrieved: %i of %i posts"%(len(res),count))
                if(len(res)>=count):
                    return res
            except FunctionTimedOut:
                print("Timed out. Rejecting post.")
            except Exception as e:
                print(e)
                print("Invalid post") 
            if(len(res)>=count): return res
    raise Exception("[Error] Unable to get article.")

#################################### Accessor functions: ####################################
#match feed names
def get_feed(feed_name,count=1):
    feeds = load_feeds()
    #get_rss(url,type)
    url = feeds[feed_name]['url']
    if("pubmed" in feeds[feed_name]['type']): return get_rss(url,count,'pubmed')
    elif("techcrunch" in feeds[feed_name]['type']): return get_rss(url,count,'techcrunch')
    elif("nature_blog" in feeds[feed_name]['type']): return get_rss(url,count,'nature_blog')
    elif("genomeweb" in feeds[feed_name]['type']): return get_rss(url,count,'genomeweb')
    elif("bioitworld" in feeds[feed_name]['type']): return get_rss(url,count,'bioitworld')
    elif("indeed" in feeds[feed_name]['type']): return get_rss(url,count,'indeed')
    
#match something in the url. Less reliable but more flexible
def get_url(url,count=1):
    #get post based on source
    if("pubmed" in url): return get_rss(url,count,'pubmed')#return get_pubmed(url,count)
    elif("techcrunch" in url): return get_rss(url,count,'techcrunch')#return get_techcrunch(url,count)
    elif("nature.com" in url): return get_rss(url,count,'nature.com')#return get_nature_blog(url,count)
    elif("genomeweb" in url): return get_rss(url,count,'genomeweb')#return get_genomeweb(url,count)
    elif("bio-itworld" in url): return get_rss(url,count,'bio-itworld')#return get_bioitworld(url,count)
    elif("indeed" in url): return get_rss(url,count,'indeed')#return get_bioitworld(url,count)
    else: return get_rss(url,count,'rss')

# Upodated function to allow feed name or just a url
def get_update(feed_name = "techcrunch",c=1,*args,**kwargs):
    feeds = load_feeds()
    if('count' in kwargs): #set count if specified by keyword, else default to c arg
        count = kwargs['count']
    elif(c):
        count = c
    else:
        count = 1
    print("Getting %i links."%(count))
    if('url' in kwargs): #if url specified then get url
        print("URL specified in parameters.")
        return get_url(kwargs['url'],count)
    elif('name' in kwargs):
        print("Using preconfigured feed.")
        return get_feed(kwargs['name'].lower(),count)
    elif(feed_name.lower() in feeds): #if
        print("Using preconfigured feed.")
        return get_feed(feed_name.lower(),count)
    else: #else try to get as url
        print("Using URL")
        print("Getting RSS based on url: "+feed_name)
        return get_url(feed_name,count)

def get_multiple(feed_name="techcrunch",c=5,*args,**kwargs):
    return get_update(feed_name,c,args,kwargs)

if __name__ == "__main__":
    # url="https://www.engadget.com/rss.xml" #test of non-specific rss
    res = get_update("hot_jobs")
    # res = get_rss(url,1)
    # res = get_multiple(count=3,url=feeds['techcrunch']['url'])
    # print(res['tweet']
    # res = get_multiple("techcrunch",3)
    # res = get_url(feeds['bioitworld']['url'])
    print(res)