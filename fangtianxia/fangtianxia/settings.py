import random

BOT_NAME = 'fangtianxia'

SPIDER_MODULES = ['fangtianxia.spiders']
NEWSPIDER_MODULE = 'fangtianxia.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:76.0) Gecko/20100101 Firefox/76.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# 设置下载延时，减少IP被封几率
DOWNLOAD_DELAY = random.random() * 0.8

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    # 'fangtianxia.middlewares.FangtianxiaSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    # 'fangtianxia.middlewares.FangtianxiaDownloaderMiddleware': 543,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 300
}

# Enable or disable extensions
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    # 'fangtianxia.pipelines.FangtianxiaPipeline': 300,
    'fangtianxia.pipelines.MongoPipeline': 300,
}

# MongoDB数据库设置
MONGO_URI = 'XXX'
MONGO_DB = 'FangTianXia'

# IP代理API设置，本项目使用芝麻代理
PROXY_URL = '填入你自己的'

# scrapy_redis配置
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Redis配置
# REDIS_URL = 'XXX'

# Persist
# SCHEDULER_PERSIST = True
