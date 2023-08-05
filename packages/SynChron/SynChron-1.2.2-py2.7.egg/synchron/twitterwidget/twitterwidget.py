#!/usr/bin/python3
version='1.4'
import tweepy
import json
import random
import nltk
from func_timeout import func_timeout, FunctionTimedOut , func_set_timeout

# from BotStreamListener import BotStreamListener
try:
    from .. import utils
except:
    from synchron import utils
    
################################# TWITTER WIDGET #################################
class TwitterWidget:
    def __init__(self, consumer_key, consumer_secret_key, access_token, access_token_secret,query_string="", hashtags="",min_pop=100):
        self.auth(consumer_key, consumer_secret_key, access_token, access_token_secret)
        self.config(query_string, hashtags,min_pop)
        self.dm={}
        self.tweets=self.api.home_timeline(1000)#get all the tweets you can
        self.prev={}
        print("Loaded Twitter Widget Version %s"%(version))
        print("Indexing previous tweets.")
        for tweet in self.tweets:
            self.index_message(tweet.text)
        print("Indexed %d tweets"%(len(self.prev)))

    def auth(self,consumer_key, consumer_secret_key, access_token, access_token_secret):
        try:
            t = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
            t.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(t)
            print("Loaded Twitter api client.")
        except Exception as e:
            print(e)
            print("[error] Twitter auth has failed.")

    def config(self,query_string="", hashtags="",min_pop=100):
        self.query_string=query_string
        self.hashtags=hashtags
        self.min_pop=min_pop
        if(len(query_string)==0): self.query_string="#news"
        if(len(hashtags)==0): self.hashtags=""

    ################################# CORE TWITTER FNs #################################
    def tweet(self,msg,link="",twitter_source="Twitter Plus"):
        if(self.message_is_duplicate(msg)):
            raise Exception("Message is duplicate")
        else:
            message = msg[:270]
            try:
                if(len(link)>1): 
                    self.api.update_status(status = message,attachment_url = link,source=twitter_source)
                else:
                    self.api.update_status(status = message,source=twitter_source)
            except Exception as e:
                print(e)
                print('[Tweet failed]: ',message)

    def tweet_comment(self,tweet,intro="",addtags=None):
        if(not addtags): 
            htags = self.hashtags
        else:
            htags = addtags
        if(self.message_is_duplicate(tweet.text)):
            raise Exception("Message is duplicate")
        else:
            turl = """https://twitter.com/{}/status/{}""".format(tweet.user.id_str,tweet.id)
            new_text = """{} {}""".format(intro,htags)[:278]
            print("Tweet comment: "+new_text)
            self.tweet(new_text,turl)

    def tweet_reply(self,tweet,msg):
        message = msg[:278]
        self.api.update_status(status = message, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

    def get_top_tweet(self,query_string=None):
        if(not query_string): qs = self.query_string #default to class variable
        tweets = self.api.search(q=qs,rpp=100,count=100,lang='en',RESULT_TYPE='popular')
        pop = [t for t in tweets if int(t.user.followers_count)>self.min_pop and t.in_reply_to_status_id_str is None]
        rand_pop = random.choice(pop)
        return rand_pop

    ################################# ADDDON TWITTER FNs #################################
    def retweet_top_tweet(self,intro="🤔"):
        print("Retweet top tweet")
        top_tweet = self.get_top_tweet()
        self.tweet_comment(top_tweet,intro)

    def reply_top_tweet(self,intro="🤔"):
        print("Reply to top tweet")
        top_tweet = self.get_top_tweet()
        self.tweet_reply(top_tweet,intro)

    def retweet_respond_top_tweet(self,intro="🤔"):
        print("Retweet & reply to top tweet")
        top_tweet = self.get_top_tweet()
        self.reply_to_tweet(top_tweet)
        self.tweet_reply(top_tweet,r)

    ################################# DIRECT MESSAGES #################################
    def check_messages(self,re=False):
        messages = self.api.list_direct_messages()
        new_messages = {}
        for m in messages:
            if m.id not in self.dm:
                self.dm[m.id]=m
                new_messages[m.id] = m
        if(re): return new_messages

    def respond(self,m,r):
        t = str(m.message_create['message_data']['text'])
        sender = str(m.message_create['sender_id'])
        # r = chat.respond(t)
        print('[Message]: {} [Response:] {}'.format(t,r))
        self.api.send_direct_message(sender, r)

    ################################# QC FUNCTIONS #################################
    def index_message(self,msg):
        trunc = msg[0:20]
        self.prev[trunc]=True

    def message_is_duplicate(self,msg):
        return msg[0:20] in self.prev

    ################################# DEFAULT BEHAVIORS #################################
    def get_update(self):
        return self.get_top_tweet()

    def get_multiple(self,count):
        res = []
        for i in range(count):
            res.append(self.get_top_tweet())
        return res

################################# MAIN #################################
if __name__ == "__main__":
    # main()
    print("Twitter Widget")
    import env
    consumer_key = env.API_KEY
    consumer_secret_key = env.API_SECRET_KEY
    access_token = env.ACCESS_TOKEN
    access_token_secret = env.ACCESS_TOKEN_SECRET
    tw = TwitterWidget(consumer_key,consumer_secret_key,access_token,access_token_secret)
    tw.config("#science","")
    print("Configured")
    # print("Get top tweet:")
    tw.retweet_top_tweet()
    # tw.tweet("NASA’s Ingenuity helicopter lifts off of Mars","https://www.sciencemag.org/news/2021/04/nasa-s-ingenuity-helicopter-lifts-mars")