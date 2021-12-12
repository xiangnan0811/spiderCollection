import json
from datetime import datetime
from urllib.parse import quote

import requests

from spiders.twitter import TwitterSpider


class UserSpider(TwitterSpider):

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

    def request_user(self, screen_name):
        """获取用户基本信息."""
        params = {
            'screen_name': screen_name,
            'withSafetyModeUserFields': True,
            'withSuperFollowsUserFields': True,
        }
        url = f'https://twitter.com/i/api/graphql/_Eo_tPE2WYM3C3gar4jwig/UserByScreenName?variables={quote(json.dumps(params, separators=(",", ":")))}'
        response = self.session.get(url, headers=self.headers, proxies=self.proxies)
        return response

    def get_user_item(self, data: dict) -> dict:
        """自用户首页响应中解析用户信息，并返回用户信息字典及用户ID."""
        user = data.get('data', {}).get('user', {}).get('result', {})
        # twitter 返回的用户ID，纯数字
        user_id = user.get("rest_id", '')
        if not user_id:
            return {}
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
        }

    def get_user(self, screen_name):
        """获取用户信息."""
        response = self.request_user(screen_name)
        data = self.trans_respose_to_json(response)
        user_item = self.get_user_item(data)
        return user_item


if __name__ == '__main__':
    users = []
    with open('data/users.txt', 'r') as f:
        for u in f.readlines():
            users.append(u.strip())
    print(len(users))
    user_spider = UserSpider()
    for user in users[:3]:
        u = user_spider.get_user(user)
        if u:
            print(f'成功获取用户 -> {u["name"]:^20s} <- id 为 -> {u["id"]:^25s} <- 的信息')
        else:
            print(f'获取用户 -> {user} <- 信息失败')
