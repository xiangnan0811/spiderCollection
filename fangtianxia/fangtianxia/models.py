from datetime import datetime, timedelta


class ProxyModel:
    """代理设置模块."""
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.balcked = False

        data_str, time_str = self.expire_str.split(" ")
        year, month, day = data_str.split("-")
        hour, minute, second = time_str.split(":")
        # 获取代理过期时间
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
        # 获取代理，格式 http://ip:port
        self.proxy = "https://{}:{}".format(self.ip, self.port)

    @property
    def is_expired(self):
        """代理有过期时间，在代理即将过期时设置更新信号."""
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=5):
            return True
        else:
            return False
