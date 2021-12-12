import os
import sys
import re
import json
from urllib.parse import quote

import requests

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

# from db.concatSQL import get_insert_and_update_sql
from db.easyMySQL import EasyMySQL
from parser.parser import get_user_item, get_tweets
from spiders.user_tweets import get_user_tweets


def get_token(screen_name, session, proxies):
    """获取游客token."""
    url = f'https://twitter.com/{screen_name}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    response = session.get(url, headers=headers, proxies=proxies)
    token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
    return token[0]


def get_user_info(screen_name, token, session, proxies):
    """获取用户基本信息."""
    params = {
        'screen_name': screen_name,
        'withSafetyModeUserFields': False,
        'withSuperFollowsUserFields': False,
    }
    url = f'https://twitter.com/i/api/graphql/_Eo_tPE2WYM3C3gar4jwig/UserByScreenName?variables={quote(json.dumps(params, separators=(",", ":")))}'
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'x-guest-token': token,
    }
    response = session.get(url, headers=headers, proxies=proxies)
    return response


def get_resp_json(resp):
    """将response转换为json."""
    try:
        return json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        return {}


def main(screen_name, mysql_connection, proxies):
    """主函数."""
    session = requests.Session()
    token = get_token(screen_name, session, proxies)
    user_resp = get_user_info(screen_name, token, session, proxies)
    user_data = get_resp_json(user_resp)
    user, user_id = get_user_item(user_data)
    print(f'user: {user_id}')
    if user:
        # user_sql = get_insert_and_update_sql(user, 'twitter', 'user')
        # user_result = mysql_connection.insert(user_sql)
        print('*' * 100)
        # print(f'用户 {user["name"]} 入库结果：{user_result}')
        tweet_resp = get_user_tweets(user_id, token, session, proxies, count=10)
        tweet_data = get_resp_json(tweet_resp)
        for tweet in get_tweets(tweet_data):
            if tweet:
                # tweet_sql = get_insert_and_update_sql(tweet, 'twitter', 'tweet')
                # tweet_result = mysql_connection.insert(tweet_sql)
                # print(f'推文 {tweet["id"]} 入库结果：{tweet_result}')
                print(f'推文 {tweet["id"]}')
                print('-' * 100)


if __name__ == '__main__':
    users = []
    with open('data/users.txt', 'r') as f:
        for u in f.readlines():
            users.append(u.strip())
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    easy_mysql = EasyMySQL('host', 0, 'user', 'password', 'db')
    print(len(users))
    for user in users[:10]:
        main(user, mysql_connection=easy_mysql, proxies=proxies)
