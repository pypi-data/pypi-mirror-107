import requests
import bs4
import praw
import random
import urllib
import urllib.request
import re
import nltk
import pyshorteners
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout

# from .. import utils
try:
    from .. import utils
except:
    from synchronicity import utils

@func_set_timeout(10)
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


def get_reddit_links(ci, cs, ua="Mozilla",subreddit="science",max_attempts=5,count=1):
    reddit = praw.Reddit(
        client_id=ci,
        client_secret=cs,
        user_agent=ua
    )
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
                if(check_reddit_post(post)): 
                    try:
                        formatted = utils.format_tweet(post.title,post.url)
                        return formatted
                    except FunctionTimedOut:
                        print("Timed out. Rejecting post.")
                    except Exception as e:
                        print(e)
                        print("Post was invalid. Selecting another.")
        else:
            posts = []
            bads = 0
            while(len(posts)<count):
                post = hot_links.pop(0)
                if(check_reddit_post(post)): 
                    try:
                        posts.append(utils.format_tweet(post.title,post.url))
                    except FunctionTimedOut:
                        print("Timed out. Rejecting post.")
                    except Exception as e:
                        print(e)
                        print("Post was invalid. Selecting another.")
                else:
                    bads+=1
                    print("Bad results count: "+str(bads))

            return posts

def get_update(client_id = "", client_secret = "", user_agent="Mozilla",subreddit="technology",max_attempts=5):
    print("Getting Reddit post.")
    post = get_reddit_links(client_id,client_secret,user_agent,subreddit,max_attempts)
    if(not post): raise Exception("No post found!")
    return post

def get_multiple(client_id = "", client_secret = "", user_agent="Mozilla",subreddit="technology",count=5):
    print("Getting Reddit post.")
    posts = get_reddit_links(client_id,client_secret,user_agent,subreddit,5,count)
    if(not posts): raise Exception("No posts found!")
    return posts

if __name__ == "__main__":
    import env
    SUBREDDIT= 'science technology cybersecurity'
    user_agent="Python"
    # print(get_update(env.client_id,env.client_secret,env.user_agent,SUBREDDIT))
    posts = get_multiple(env.client_id,env.client_secret,env.user_agent,"technology",5)
    print("Posts: %d"%(len(posts)))
    print(posts)