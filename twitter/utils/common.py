import re
import requests


def get_token():
    """获取游客token."""
    url = 'https://twitter.com/potus'
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
    return token[0]


if __name__ == '__main__':
    token = get_token()
    print(token)
