import requests
import bs4
import praw
import random
import urllib
import urllib.request
import re
# import nltk
import json
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout
from newspaper import Article, Source, Config

# from .. import utils
try:
    from .. import utils
except:
    from synchron import utils

@func_set_timeout(30)
def check_reddit_post(post):
    rejects = ['reddit.com','redd.it','reddit','nsfw','redd','red']
    print("Checking post: %s"%(post.title))
    if any(term in post.url for term in rejects):
        print("Invalid Post URL")
        return False
    elif any(term in post.title.lower() for term in rejects):
        print("Invalid Post name")
        return False
    else:
        post.title = utils.clean_text(post.title)
        print("Verifying and cleaning URL for post: "+post.url)
        try:
            post.url= utils.clean_url(post.url)
        except Exception as e:
            print(e)
            print("Invalid link. Rejecting post")
            return False
        print("Going with reddit post: %s"%(post.title))
        return True

def format_post(rp,bebukey):
    post = {}
    print("Formatting post")
    tweet = utils.format_tweet(ti=rp.title,url=rp.url,summary="",intro="",bebukey=bebukey)
    summary = utils.summarize_article(rp.url)
    post['tweet']=tweet['tweet']
    post['title'] = rp.title
    post['description'] = summary['summary']
    post['author'] = summary['author']
    post['url'] = tweet['url']
    post['img'] = summary['img']
    post['tags'] = summary['keywords']
    # post['text'] = summary['text']
    # print(pos
    # t)
    return post

def get_reddit_links(ci, cs, ua="Mozilla",subreddit="science",max_attempts=5,count=1,bebukey=None):
    # print(bebukey)
    reddit = praw.Reddit(client_id=ci,client_secret=cs,user_agent=ua)
    #keep trying posts until a good post is obtained
    attempts = 0
    post = False
    while(not post and attempts < max_attempts):
        attempts += 1
        #select subreddit from specified input for each attempt
        sr = utils.clean_text(utils.get_item(subreddit)).lower()
        print("Getting post from subreddit %s. Attempt %d"%(sr, attempts))
        #pick link, but only if not a Reddit link:
        try:
            links = reddit.subreddit(sr).hot(limit=100)
        except Exception as e:
            print(e)
            print("Problem retrieving subreddit %s"%(subreddit))
        #get high-scoring links... really hot
        hot_links = [l for l in links if l.score > 100]
        if(len(hot_links)<count): 
            raise Exception("Too few links in subreddit: %s"%(sr))
        if(count == 1): #case for selecting 1 link
            for i in range(max_attempts):
                post = random.choice(hot_links)
                try:
                    if(check_reddit_post(post)): 
                        try:
                            print("Formatting post")
                            # formatted = utils.format_tweet(ti=post.title,url=post.url,summary="",intro="",bebukey=bebukey)
                            formatted = format_post(post,bebukey)
                            print(formatted['description'])
                            return formatted
                        except FunctionTimedOut:
                            print("Timed out. Rejecting post.")
                        except Exception as e:
                            print(e)
                            print("Post was invalid. Selecting another.")
                except:
                    print("Rejected post.")
        else:
            posts = []
            bads = 0
            while(len(posts)<count):
                post = hot_links.pop(0)
                try:
                    if(check_reddit_post(post)): 
                        try:
                            # formatted = utils.format_tweet(ti=post.title,url=post.url,summary="",intro="",bebukey=bebukey)
                            formatted = format_post(post,bebukey)
                            print(formatted['description'])
                            posts.append(formatted)
                        except FunctionTimedOut:
                            print("Timed out. Rejecting post.")
                        except Exception as e:
                            print(e)
                            print("Post was invalid. Selecting another.")
                    else:
                        bads+=1
                        print("Bad results count: "+str(bads))
                except:
                    bads+=1
                    print("Rejected post")

            return posts


############################# ACCESSORS #############################
def get_update(client_id = "", client_secret = "", user_agent="Mozilla",subreddit="technology",max_attempts=5,bebukey=None):
    print("Getting Reddit post.")
    post = get_reddit_links(client_id,client_secret,user_agent,subreddit,max_attempts,1,bebukey)
    if(not post): raise Exception("No post found!")
    return post

def get_multiple(client_id = "", client_secret = "", user_agent="Mozilla",subreddit="technology",count=5,bebukey=None):
    print("Getting Reddit post.")
    posts = get_reddit_links(client_id,client_secret,user_agent,subreddit,5,count,bebukey)
    if(not posts): raise Exception("No posts found!")
    return posts

#get_posts = the main function. 
#count is required
#additional parameters can be in kwargs
def get_posts(count=1,**kwargs):
    if('subreddit' in kwargs):
        subreddit = kwargs['subreddit']
    else:
        subreddit = "technology"

    if('bebukey' in kwargs):
        bebukey = kwargs['bebukey']
    else: 
        bebukey = None 

    try:
        client_id = kwargs['REDDIT_CLIENT_ID']
        client_secret = kwargs['REDDIT_CLIENT_SECRET']
    except:
        client_id = kwargs['client_id']
        client_secret = kwargs['client_secret']

    posts = get_reddit_links(
        client_id,
        client_secret,
        utils.ua,
        subreddit,
        5,
        count ,
        bebukey)
    if(not posts): raise Exception("No posts found!")
    return posts

if __name__ == "__main__":
    # import env
    with open("env.json",'r') as f:
        env = json.load(f)
    SUBREDDIT= 'science technology cybersecurity'
    user_agent="Python"
    # print(get_update(env.client_id,env.client_secret,env.user_agent,SUBREDDIT))
    posts = get_multiple(env['REDDIT_CLIENT_ID'],env['REDDIT_CLIENT_SECRET'],'useragent',"technology",5,bebukey=env['BEBUKEY'])
    print("Posts: %d"%(len(posts)))
    print(posts)

# def summarize_article(url):
#     config = Config()
#     # config.MAX_SUMMARY=500
#     config.MAX_SUMMARY_SENT=3
#     article = Article(url=url,config=config)
#     article.download()
#     article.parse()
#     article.nlp()
#     return {
#             'title':article.title,
#             'summary':utils.clean_text(article.summary),
#             'url':url,
#             'keywords':"#"+" #".join(article.keywords[0:3]),
#             'img':article.top_image,
#             'author':", ".join(article.authors),
#             'text':article.text,
#             'movies':article.movies
#             }