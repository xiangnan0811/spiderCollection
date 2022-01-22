import re
import time
import json
from datetime import datetime, timedelta
from typing import Tuple
from functools import wraps

import requests


class TwitterSpider:

    token = None

    def __init__(self, proxy=None):
        self.proxies = self._get_proxies(proxy)
        self.token = self.get_token()

    def retry(try_count=3, delay=0):
        """Retry calling the decorated function using an exponential backoff.

        :param tries: number of times to try (not retry) before giving up
        """
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                n = 0
                while n < try_count:
                    result = f(*args, **kwargs)
                    if result:
                        return result
                    else:
                        n += 1
                        time.sleep(delay)
                        print(f'{f.__name__} failed {n} times, retrying...')
                else:
                    raise ValueError(f'{f.__name__} failed after {n} tries')
            return wrapper
        return decorator

    def _get_proxies(self, proxy=None) -> dict:
        if proxy is None:
            proxy = '127.0.0.1:7890'
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }

    @retry()
    def _get_token(self) -> str:
        url = 'https://twitter.com/potus'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }
        response = requests.get(url, headers=headers, proxies=self.proxies)
        token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
        if token and (token_str := token[0]):
            return token_str
        return ""

    def get_token(self, token_expire_time: int = 30) -> Tuple[str, datetime]:
        if self.token is None or self.token[1] < (datetime.now() - timedelta(minutes=token_expire_time)):
            return self._get_token(), datetime.now()
        return self.token

    def trans_respose_to_json(self, response: requests.Response) -> dict:
        """将response转换为json.

        @param:     resp : 目标网页响应
        @Returns:   响应结果字典
        """
        try:
            return json.loads(response.text)
        except json.decoder.JSONDecodeError:
            return {}


if __name__ == '__main__':
    twitter = TwitterSpider()
    print(twitter.token)
