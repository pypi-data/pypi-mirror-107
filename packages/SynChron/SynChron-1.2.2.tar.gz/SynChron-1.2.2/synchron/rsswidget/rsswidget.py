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
from urlextract import URLExtract

cwd = path.dirname(__file__)
package_name = "synchronicity"
from urllib.request import Request, urlopen
try:
    from .. import utils
except:
    from synchron import utils

ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
max_tries = 10
max_len = 250

default_feeds = {
    "genomics":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1tyP_Q3NRDksDSxLk7JOQBB-ROqqN-dqZVK6I3HZvpTHjX5Q1i/?limit=100&utm_campaign=pubmed-2&fc=20210415124733"},
    "stanford":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1f1dJwlpLErIjn2ZoRRJB1J_KUNSf155ij5ulhvcmmeo-QWgpT/?limit=100&utm_campaign=pubmed-2&fc=20210415130057"},
    "nhr":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1dSaW42H3lP37Kc_ElhakcHUr43yaHMxeJEMax91bss1E6gQ8j/?limit=100&utm_campaign=pubmed-2&fc=20210415131515"},
    "covid19":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1vm7YKsZZUUonjgCRs9f_cbRxstX0U_NH7hBAk6IiLCUEVNkEF/?limit=100&utm_campaign=pubmed-2&fc=20210415132645"},
    "supplements":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/18MzaitFJ9iXLrFVyaEyOXbPbXP-K_F4PEZLeYw9x9wBUF2wjk/?limit=50&utm_campaign=pubmed-2&fc=20200708124003"},
    "techcrunch":{
        "type":"techcrunch",
        "url":"https://techcrunch.com/feed/"},
    "startups":{
        "type":"techcrunch",
        "url":"https://techcrunch.com/startups/feed/"},
    "nature_blog":{
        "type":"nature_blog",
        "url":"http://feeds.nature.com/nature/rss/current?x=1"
    },
    "genomeweb":{
        "type":"genomeweb",
        "url":"https://www.genomeweb.com/breaking-news/rss"
    },
    "bioitworld":{
        "type":"bioitworld",
        "url":"https://www.bio-itworld.com/feeds/BioIT_WorldNews_RSS"
    },
    "stanford":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1TuHRxU62XQv0joP9m4YxJoOJgd6ttMxTnxNdgPseZjwteRssh/?limit=100&utm_campaign=pubmed-2&fc=20210427161140"
    },
    "unusual":{
        "type":"pubmed",
        "url":"https://pubmed.ncbi.nlm.nih.gov/rss/search/1xCFUMSbAMYatD8eKGfeJ_0ANNg4o9dwfarY2JtJxHVZbcrE-3/?limit=100&utm_campaign=pubmed-2&fc=20210427161648"
    },
    "pm_jobs":{
        "type":"indeed",
        "url":"https://rss.indeed.com/rss?q=as_and=it+project+manager&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=%24100%2C000%2B&radius=25&l=remote&fromage=1&limit=20&sort=&psf=advsrch&from=advancedsearch"
    },
    "cloud_jobs":{
        "type":"indeed",
        "url":"https://rss.indeed.com/rss?q=as_and=cloud+solutions+architect&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=%24100%2C000%2B&radius=25&l=remote&fromage=1&limit=20&sort=&psf=advsrch&from=advancedsearch"
    },
        "hot_jobs":{
        "type":"indeed",
        "url":"https://rss.indeed.com/rss?q=%28%22cloud+solutions+architect%22+or+%22security+architect%22+or+%22it+project+manager%22+or+aws+or+azure+or+cybersecurity%29+%24100%2C000%2B&l=remote&radius=25"
    }
    }
#################################### Check content: ####################################

def valid_string(check_string,rejects=['404','error','retraction','correction','corrigendum','erratum']):
    if (any(term in check_string for term in rejects)): return False
    return True

def valid_post(post,rejects = ['404','error']):
    post['title'] = utils.clean_text(post['title'])
    return (valid_string(post['title'],rejects) and valid_string(post['url'],rejects))

#################################### Generic RSS Feed: ####################################
def format_rss_result(ref,bebukey=None):
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
    tweet = utils.format_tweet(ref['title'],ref['url'],ref['summary'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    return {
        'tweet':tweet,
        'title':ref['title'],
        'url':ref['url'],
        'summary': parsed['summary'],
        'author':parsed['author'],
        'img':parsed['img'],
        'movies':parsed['movies']
        }

############################## Nature Blog: ##############################
def format_nature_blog_result(ref,bebukey):
    full_url = utils.clean_url(ref['id'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url,ref['summary'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    return {
        'tweet':tweet,
        'title':ref['title'],
        'url':full_url,
        'summary': parsed['summary'],
        'author':parsed['author'],
        'img':parsed['img'],
        'movies':parsed['movies']
        }

#################################### BioITWorld: ####################################
def format_bioitworld_result(ref,bebukey=None):
    full_url = utils.clean_url(ref['link'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url,ref['title'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    return {
        'tweet':tweet,
        'title':ref['title'],
        'url':full_url,
        'summary': parsed['summary'],
        'author':parsed['author'],
        'img':parsed['img'],
        'movies':parsed['movies']
        }

#################################### GenomeWeb: ####################################
def format_genomeweb_result(ref,bebukey=None):
    full_url = utils.clean_url(ref['link'])
    ref['title'] = utils.clean_text(ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url,ref['summary'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    return {
        'tweet':tweet,
        'title':ref['title'],
        'url':full_url,
        'summary': parsed['summary'],
        'author':parsed['author'],
        'img':parsed['img'],
        'movies':parsed['movies']
        }

#################################### Techcrunch: ####################################
def format_techcrunch_result(ref,bebukey=None):
    full_url = utils.clean_url(ref['link'])
    print("Updated URL for post: "+full_url)
    tweet = utils.format_tweet(ref['title'],full_url,ref['summary'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    print(">>> PARSED")
    print(parsed)
    return {
            'tweet':tweet,
            'title':utils.clean_text(ref['title']),
            'url':full_url,
            'summary': parsed['summary'],
            'author':parsed['author'],
            'img':parsed['img'],
            'movies':parsed['movies']
        }

#################################### Pubmed: ####################################
def format_pubmed_result(ref,bebukey=None):
    rejects=['404','error','retraction','correction','corrigendum','erratum']
    full_url = """https://doi.org/{}""".format(ref['dc_identifier'][4:])
    full_url = utils.clean_url(full_url)
    print("Updated URL for post: "+full_url)
    if(not valid_string(ref['title'],rejects)): raise Exception("Rejecting post: "+ref['title'])
    tweet = utils.format_tweet(ref['title'],full_url,ref['summary'],"",bebukey)['tweet']
    parsed = utils.summarize_post(ref)
    return {
            'tweet':tweet,
            'title':utils.clean_text(ref['title']),
            'url':full_url,
            'summary': parsed['summary'],
            'author':parsed['author'],
            'img':parsed['img'],
            'movies':parsed['movies']
        }

#################################### Indeed: ####################################
def format_indeed_result(ref,bebukey=None):
    print("Formatting indeeed result.")
    # print("bebukey "+bebukey)
    url = utils.clean_url(ref['link'])
    extractor = URLExtract()
    req = requests.get(url)
    page = req.text
    urls = extractor.find_urls(page)
    links = urls
    print("Got links.")
    company_url = None
    for link in links:
        if("indeed.com/rc/clk" in link):
            try:
                company_url = utils.unshorten(link)
            except:
                print("Rejecting link: "+link)
            break
    if(not company_url): raise Exception("No links found")
    ref['url'] = company_url
    title = utils.clean_text(ref['title'])
    print("title: "+title)
    intro="👍 JOB ALERT👍 "
    tweet = utils.format_tweet(title,ref['url'],"",intro,bebukey)['tweet']
    # print(tweet)
    return {
        'tweet':tweet,
        'title':title,
        'summary':utils.clean_text(ref['description']),
        'url':ref['url'],
        'source':ref['source']
        }

#################################### Get Result: ####################################
@func_set_timeout(300)
def format_result(res,res_type='rss',bebukey=None):
    # print(bebukey)
    if(res_type == 'pubmed'): return(format_pubmed_result(res,bebukey))
    if(res_type == 'techcrunch'): return(format_techcrunch_result(res,bebukey))
    if(res_type == 'nature_blog'): return(format_nature_blog_result(res,bebukey))
    if(res_type == 'genomeweb'): return(format_genomeweb_result(res,bebukey))
    if(res_type == 'bioitworld'): return(format_bioitworld_result(res,bebukey))
    if(res_type == 'indeed'): return(format_indeed_result(res,bebukey))
    else: return(format_rss_result(res,bebukey))

def get_rss(url,count=1,rss_type='rss',bebukey=None):
    # print(bebukey)
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
                post = format_result(post,rss_type,bebukey)
                # print(post)
                if(valid_post(post),rejects): 
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
                post = format_result(post,rss_type,bebukey)
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
def get_feed(feed_name,count=1,bebukey=None):
    if(feed_name not in default_feeds):
        return get_url(feed_name,bebukey)
    #get_rss(url,type)
    url = default_feeds[feed_name]['url']
    if("pubmed" in default_feeds[feed_name]['type']): return get_rss(url,count,'pubmed',bebukey)
    elif("techcrunch" in default_feeds[feed_name]['type']): return get_rss(url,count,'techcrunch',bebukey)
    elif("nature_blog" in default_feeds[feed_name]['type']): return get_rss(url,count,'nature_blog',bebukey)
    elif("genomeweb" in default_feeds[feed_name]['type']): return get_rss(url,count,'genomeweb',bebukey)
    elif("bioitworld" in default_feeds[feed_name]['type']): return get_rss(url,count,'bioitworld',bebukey)
    elif("indeed" in default_feeds[feed_name]['type']): return get_rss(url,count,'indeed',bebukey)
    
#match something in the url. Less reliable but more flexible
def get_url(url,count=1,bebukey=None):
    #get post based on source
    if("pubmed" in url): return get_rss(url,count,'pubmed',bebukey)#return get_pubmed(url,count)
    elif("techcrunch" in url): return get_rss(url,count,'techcrunch',bebukey)#return get_techcrunch(url,count)
    elif("nature.com" in url): return get_rss(url,count,'nature.com',bebukey)#return get_nature_blog(url,count)
    elif("genomeweb" in url): return get_rss(url,count,'genomeweb',bebukey)#return get_genomeweb(url,count)
    elif("bio-itworld" in url): return get_rss(url,count,'bio-itworld',bebukey)#return get_bioitworld(url,count)
    elif("indeed" in url): return get_rss(url,count,'indeed',bebukey)#return get_bioitworld(url,count)
    else: return get_rss(url,count,'rss')

# Upodated function to allow feed name or just a url
def get_update(feed_name = "techcrunch",c=1,*args,**kwargs):
    if('count' in kwargs): #set count if specified by keyword, else default to c arg
        count = kwargs['count']
    elif(c):
        count = c
    else:
        count = 1
    if('bebukey' in kwargs):
        bebukey = kwargs['bebukey']
    else:
        bebukey = None
    print("Getting %i links."%(count))
    if('url' in kwargs): #if url specified then get url
        print("URL specified in parameters.")
        return get_url(kwargs['url'],count,bebukey)
    elif('name' in kwargs):
        print("Using preconfigured feed.")
        return get_feed(kwargs['name'].lower(),count,bebukey)
    elif(feed_name.lower() in default_feeds): #if
        print("Using preconfigured feed.")
        return get_feed(feed_name.lower(),count,bebukey)
    else: #else try to get as url
        print("Using URL")
        print("Getting RSS based on url: "+feed_name)
        return get_url(feed_name,count,bebukey)

#managed to generalize the get_update function, but keeping this one for compatibility
def get_multiple(feed_name="techcrunch",c=5,*args,**kwargs):
    return get_update(feed_name,c,args,kwargs)

def get_posts(params=None, count=1,**kwargs):
    #get the bebukey
    if('bebukey' in kwargs):
        bebukey = kwargs['bebukey']
    else: 
        bebukey = None 
    feed = None
    url = None
    #get the feed
    if('feed' in kwargs): feed = kwargs['feed']
    elif('name' in kwargs['name']): feed = kwargs['name']
    elif('url' in kwargs): url = kwargs['url']
    else: feed = 'techcrunch'
    if(url): posts = get_url(url,count,bebukey)
    else: posts = get_feed(feed,count,bebukey)
    if(not posts): raise Exception("No posts found!")
    return posts

if __name__ == "__main__":
    print("tw")
    # url="https://www.engadget.com/rss.xml" #test of non-specific rss
    res = get_update("hot_jobs")
    # res = get_rss(url,1)
    # res = get_multiple(count=3,url=feeds['techcrunch']['url'])
    # print(res['tweet']
    # res = get_multiple("techcrunch",3)
    # res = get_url(feeds['bioitworld']['url'])
    print(res)