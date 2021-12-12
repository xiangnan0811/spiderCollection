import os
import sys
import json
import requests
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR))

from parser.parser import get_tweets
from db.easyMySQL import EasyMySQL
from db.concatSQL import get_insert_and_update_sql
from utils.common import get_token


def get_user_tweets(user_id, token, session, proxies, count=2000):
    """获取指定用户的指定数量的推文信息."""
    params = {
        'userId': user_id,
        'count': count,
        'withTweetQuoteCount': True,
        'includePromotedContent': True,
        'withSuperFollowsUserFields': True,
        'withUserResults': True,
        'withBirdwatchPivots': True,
        'withReactionsMetadata': True,
        'withReactionsPerspective': True,
        'withSuperFollowsTweetFields': True,
        'withVoice': True,
    }
    url = f'https://twitter.com/i/api/graphql/Qg0jD2d__FhsMB48vKFKUQ/UserTweets?variables={quote(json.dumps(params, separators=(",", ":")))}'
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'x-guest-token': token,
    }
    response = session.get(url, headers=headers, proxies=proxies)
    return response


def main(user_id, mysql_connection, count=2000):
    """主函数."""
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    session = requests.Session()
    token = get_token()
    resp = get_user_tweets(user_id, token, session, proxies, count)
    for tweet in get_tweets(resp.json()):
        if tweet:
            tweet_sql = get_insert_and_update_sql(tweet, 'twitter', 'tweet')
            tweet_result = mysql_connection.insert(tweet_sql)
            print(tweet_result)
            print('-' * 100)


if __name__ == '__main__':
    user_id = '1129454955281039360'
    easy_mysql = EasyMySQL('host', 0, 'user', 'password', 'db')
    main(user_id, easy_mysql)
