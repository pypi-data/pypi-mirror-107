import requests
import bs4
import praw
import random
import urllib.request
import re
import nltk
import pyshorteners
from urlextract import URLExtract
import urllib.request
from urllib.request import Request, urlopen
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout

default_ua = "Mozilla Firefox Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
max_len = 240
try:
    from .. import utils
except:
    from synchronicity import utils

def get_udemy_info(url):
    max_len = 260
    #test
    req = Request(url, headers={'User-Agent': default_ua})
    res= urllib.request.urlopen(req)
    reqs = requests.get(url)
    soup = bs4.BeautifulSoup(res.read(), 'html.parser')
    course_title = soup.find(class_='clp-lead__title').text
    course_title = utils.clean_text(course_title)
    course_subtitle = soup.find(class_='clp-lead__headline').text
    course_subtitle = utils.clean_text(course_subtitle)
    language = ""
    course_language = soup.find(class_='clp-lead__locale').text.lower().strip()
    img_src = ""
    images = soup.findAll("img")
    for img in images:
        if("course" in img['src']):
            if('?' in img['src']): img_src = img['src'].split('?')[0]
    return {
        "title":course_title,
        "subtitle":course_subtitle,
        "language":course_language,
        "img":img_src
    }

#Grab Udemy course info from link
def get_udemy_link(url):
    extractor = URLExtract()
    req = requests.get(url)
    page = req.text
    # urls = extractor.find_urls(str(soup))
    urls = extractor.find_urls(page)
    for url in urls:
        if('udemy.com' in url):
            print("Extracting info from link: "+str(url))
            try:
                coupon = url.split('=')[1]
            except:
                coupon = None
            try:
                info = get_udemy_info(url)
                return {
                    "title":info['title'],
                    "subtitle":info['subtitle'],
                    "url":url,
                    "coupon":coupon,
                    "language":info['language'],
                    "img":info['img']
                }  
            except Exception as e:
                print(e)
                print("Unable to extract info from url: "+str(url))

@func_set_timeout(10)
def get_udemy_post(red):
    max_len = 240
    utags = "#udemyfreebies #udemycoupon #udemy #udemyfree #udemysale #udemyflashsale"
    url = red.url
    udemy = get_udemy_link(url)
    title = udemy['title']#+" "+udemy['subtitle']
    title_len = len(title)
    max_url = max_len-title_len #shorten url based on title len
    try:
        url = utils.shorten_link(udemy['url'],max_url)[0:max_len]
    except:
        print("Unable to shorten url")
    url_len = len(url)
    max_title = max_len - url_len
    truncated=''
    if(len(title)>max_title):
        truncated='...'
        title = title[0:max_title]
    title_len = len(title)
    if(udemy['coupon']):
        coupon_text="FREE COUPON CODE: "+udemy['coupon']
    else:
        coupon_text = ""
    post = """🔥SALE!🔥 
{} 
{} 
{} {}""".format(title,coupon_text,udemy['url'],utags)
    post_2="""{} 
{}...
{} 
{}""".format(title,udemy['subtitle'],coupon_text,udemy['url'])
    udemy['tweet']=post[0:278]
    udemy['tweet_2']=post_2
    return udemy

def get_reddit_link(ci, cs, subreddit="udemyfreebies"):
    reddit = praw.Reddit(client_id=ci,client_secret=cs, user_agent=default_ua)
    links = reddit.subreddit(subreddit).hot(limit=100)
    links = [l for l in links]
    pick_link = random.choice(links)
    return(pick_link)

def get_reddit_all(ci,cs,subreddit="udemyfreebies"):
    reddit = praw.Reddit(client_id=ci,client_secret=cs, user_agent=default_ua)
    links = reddit.subreddit(subreddit).hot(limit=100)
    links = [l for l in links]
    # pick_link = random.choice(links)
    return(links)

def get_update(client_id, client_secret,subreddit="udemyfreebies"):
    max_tries = 5
    attempt = 0
    while(attempt<max_tries):
        attempt+=1
        try:
            red = get_reddit_link(client_id,client_secret,subreddit)
            post = get_udemy_post(red)
            if('english' in post['language'].lower()):
                return post
                break
            else:
                print("Post isn't English. Skipping.")
        except FunctionTimedOut:
                print("Timed out. Rejecting post.")
        except Exception as e:
            print(e)
            print("Encountered problem getting link. Attempt: "+str(attempt))

def get_multiple(client_id, client_secret, post_number=5):
    posts = get_reddit_all(client_id,client_secret)
    tweets = []
    for red in posts:
        if(len(tweets)<post_number):
            try:
                print("Post: %s"%(red.title))
                post = get_udemy_post(red)
                if('english' in post['language']):
                    tweets.append(post)
                else:
                    print("Post isn't English. Skipping.")
            except FunctionTimedOut:
                print("Timed out. Rejecting post.")
            except Exception as e:
                print(e)
                print("Unable to add post: %s"%(red.title))
        else:
            break
    return tweets

def test():
    with open('page.html', 'r') as f:
        contents = f.read()
        soup = bs4.BeautifulSoup(contents, 'html.parser')
        # print(soup)
        # print("udemy.com" in contents)
        # print(soup.findall('form'))
        # for el in soup.find_all('form'):
        #     # print(el)
        #     if("udemy" in el):
        #         print(el)
        extractor = URLExtract()
        urls = extractor.find_urls(str(soup))
        for url in urls:
            if('udemy.com' in url):
                print(url)
                coupon = url.split('=')[1]
                print("coupon: %s"%(coupon))

if __name__ == "__main__":
    import env
    print(get_update(env.client_id,env.client_secret))
    # posts = get_multiple(env.client_id,env.client_secret,2)
    # print("Posts: %d"%(len(posts)))
    # print(posts)

    # test()