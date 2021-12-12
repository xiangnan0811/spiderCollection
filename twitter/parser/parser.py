import re
from typing import Tuple
from datetime import datetime


def get_user_item(data: dict) -> Tuple[dict, str]:
    """自用户首页响应中解析用户信息，并返回用户信息字典及用户ID."""
    user = data.get('data', {}).get('user', {}).get('result', {})
    # twitter 返回的用户ID，纯数字
    user_id = user.get("rest_id", '')
    if not user_id:
        return {}, ''
    # 用户其余信息 legacy
    legacy = user.get("legacy", {})
    # 注册时间
    created_at = legacy.get("created_at", 0)
    if created_at:
        created_at = int(datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").timestamp())
    # 简介
    description = legacy.get("description", '').replace("'", '').replace('"', '')
    # fast_followers_count
    fast_followers_count = legacy.get("fast_followers_count", 0)
    # 喜欢数
    favourites_count = legacy.get("favourites_count", 0)
    # 粉丝数
    followers_count = legacy.get("followers_count", 0)
    # 关注数
    friends_count = legacy.get("friends_count", 0)
    # 收听数
    listed_count = legacy.get("listed_count", 0)
    # 位置
    location = legacy.get("location", '').replace("'", '').replace('"', '')
    # 图片视频数
    media_count = legacy.get("media_count", 0)
    # 昵称
    name = legacy.get("name", '').replace("'", "").replace('"', '')
    # 正常粉丝数
    normal_followers_count = legacy.get("normal_followers_count", 0)
    # 主页横幅图
    profile_banner_url = legacy.get("profile_banner_url", '').replace("'", "").replace('"', '')
    # 头像
    profile_image_url = legacy.get("profile_image_url_https", '').replace('_normal', '').replace("'", "").replace('"', '')
    # screen_name
    screen_name = legacy.get("screen_name", '').replace("'", "").replace('"', '')
    # statuses_count
    statuses_count = legacy.get("statuses_count", 0)

    return {
        'id': user_id,
        'created_at': created_at,
        'description': description,
        'fast_followers_count': fast_followers_count,
        'favourites_count': favourites_count,
        'followers_count': followers_count,
        'friends_count': friends_count,
        'listed_count': listed_count,
        'location': location,
        'media_count': media_count,
        'name': name,
        'normal_followers_count': normal_followers_count,
        'profile_banner_url': profile_banner_url,
        'profile_image_url': profile_image_url,
        'screen_name': screen_name,
        'statuses_count': statuses_count,
    }, user_id


def get_tweets(data):
    """解析用户的推文信息."""
    tweets = []
    instructions = data.get('data', {}).get('user', {}).get('result', {}).get('timeline', {}).get('timeline', {}).get('instructions', {})
    if instructions and isinstance(instructions, list) and instructions[0]:
        tweets = instructions[0].get("entries", [])
    for tweet in tweets:
        tweet_result = tweet.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
        legacy = tweet_result.get('legacy', {})
        tweet_id = legacy.get("id_str", '')
        if not tweet_id:
            continue
        user_id = legacy.get("user_id_str", '')
        full_text = legacy.get("full_text", '').replace("'", r"\'").replace('"', r'\"')
        favorite_count = legacy.get("favorite_count", '0')
        lang = legacy.get("lang", '').replace("'", r"\'").replace('"', r'\"')
        source = legacy.get("source", '').replace("'", r"\'").replace('"', r'\"')
        if source:
            source = re.findall(r'follow">(.*?)</a>', source)
            if source:
                source = source[0]
        quote_count = legacy.get("quote_count", '0')
        reply_count = legacy.get("reply_count", '0')
        retweet_count = legacy.get("retweet_count", '0')
        quoted_tweet_id = legacy.get("quoted_status_id_str", '0')
        created_at = legacy.get("created_at", 0)
        if created_at:
            created_at = int(datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").timestamp())
        yield {
            'id': tweet_id,
            'user_id': user_id,
            'full_text': full_text,
            'favorite_count': favorite_count,
            'lang': lang,
            'source': source,
            'quote_count': quote_count,
            'reply_count': reply_count,
            'retweet_count': retweet_count,
            'quoted_tweet_id': quoted_tweet_id,
            'created_at': created_at,
        }
