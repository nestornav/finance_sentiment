import os
import json
import time
import tweepy
from datetime import date, datetime

from config import BEARER_TOKEN, DIR_DATA

def get_tw_cli():
    # Auth is based on the Twitter API 2 version
    cli = tweepy.Client(BEARER_TOKEN)
    return cli

def get_dir_path():
    dir_dump = os.path.join(os.getcwd(), DIR_DATA)
    if not os.path.join(dir_dump):
        os.mkdir(dir_dump)
    return dir_dump

def get_twetts():
    field = ['context_annotations','entities','created_at']
    content = '(#NASDAQ100 OR #investing OR #forex OR #traiding OR #stocks OR #stokkmarket) OR economy OR stock OR market OR bonds  -is:retweet'
    query = f'{content}'
    token = None
    next_t = True
    cli = get_tw_cli()
    dir_dump = get_dir_path()
    file_path = os.path.join(dir_dump, 'tweets.json')

    with open(file_path, 'w') as fh:
        while next_t:
            response = cli.search_recent_tweets(query,
                                                tweet_fields=field,
                                                max_results=100,
                                                start_time=datetime.strptime('2023-01-26', '%Y-%m-%d'),
                                                next_token=token)
            if 'next_token' in response.meta:
                next_token = response.meta['next_token']
                for tweet in response.data:
                    fh.write(json.dumps(get_line(tweet), default=json_serial) + "\n")

            else:
                next_t = False

            time.sleep(4)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def get_line(x):
    line = {}
    keys = ['id', 'text', 'created_at']
    for k in keys:
        line[k] = x[k]

    return line

if __name__ == '__main__':
    get_twetts()
