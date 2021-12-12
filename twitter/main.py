from spiders.user import UserSpider
from spiders.tweet import TweetSpider


def get_screen_names(file_path) -> list:
    """获取用户 screen_name 列表.

    @param:    file_path: 用户 screen_name 文件路径
    """
    screen_names = []
    with open(file_path, 'r') as f:
        for name in f.readlines():
            screen_names.append(name.strip())
    return screen_names


def get_user_tweets(user_id, count):
    tweet_spider = TweetSpider()
    tweets = tweet_spider.get_user_tweets(user_id=user_id, count=count)
    print(tweets)


def get_user_info() -> dict:
    """依据用户 screen_names 获取用户信息.

    @Returns:  用户信息 dict
    """
    user_file_path = './data/users.txt'
    screen_names = get_screen_names(user_file_path)
    print(len(screen_names))
    user_spider = UserSpider()
    for screen_name in screen_names[:10]:
        u = user_spider.get_user(screen_name)
        if u:
            print(f'成功获取用户 -> {u["name"][:20]:^20s} <- id 为 -> {u["id"]:^25s} <- 的信息')
        else:
            print(f'获取用户 -> {screen_name} <- 信息失败')


if __name__ == '__main__':
    # get_user_info()
    get_user_tweets(user_id='1349149096909668363', count=10)
