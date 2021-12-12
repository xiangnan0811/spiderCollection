import re
import json
import requests
from datetime import datetime
from urllib.parse import quote

from spiders.twitter import TwitterSpider


class TweetSpider(TwitterSpider):

    def __init__(self, proxy=None):
        super().__init__(proxy)
        self.session = requests.Session()

    @property
    def headers(self):
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'x-guest-token': self.get_token()[0],
        }
        return headers

    def request_tweets(self, user_id, count=1000):
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
        response = self.session.get(url, headers=self.headers, proxies=self.proxies)
        return response

    def get_tweets(self, data):
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

    def get_user_tweets(self, user_id, count=1000):
        """获取用户推文信息."""
        response = self.request_tweets(user_id, count)
        data = self.trans_respose_to_json(response)
        tweets = []
        for tweet in self.get_tweets(data):
            print(f'成功获取用户 -> {user_id:^25s} <- 的推文，内容为 -> {tweet["full_text"][:50]}')
            tweets.append(tweet)
        return tweets


if __name__ == '__main__':
    user_id = '1129454955281039360'
    tweet_spider = TweetSpider()
    tweets = tweet_spider.get_tweets(user_id=user_id, count=10)
    print(tweets)
