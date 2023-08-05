import json
import random
from pkg_resources import resource_filename
from os import path
cwd = path.dirname(__file__)
package_name = "synchronicity"

try:
    from .. import utils
except:
    from synchronicity import utils
    
def get_multiple(count=5):
    posts = []
    for i in range(count):
        posts.append(get_update())
    return posts

def create_random_tweet():
    quote = get_random_quote()
    tweet = """{} - {}""".format(quote['quoteText'], quote['quoteAuthor'])
    return tweet

def get_quotes():
    file_path = path.join(cwd,'quotes-list.json')
    print(file_path)
    with open(file_path,'r') as f:
        quotes_json = json.load(f)
        return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()
    random_quote = random.choice(quotes)
    return random_quote

def test():
    print("Test quotes.")
    utils.test()

def get_update():
    return {'tweet':create_random_tweet()}

def get_multiple(count=1):
    res = []
    for i in range(count):
        res.append(get_update())
    return res
    
if(__name__ == "__main__"):
    print("Running in: "+cwd)
    print(get_update())