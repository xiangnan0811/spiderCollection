# -*- coding: utf-8 -*-

BOT_NAME = 'yitu'

SPIDER_MODULES = ['yitu.spiders']
NEWSPIDER_MODULE = 'yitu.spiders'


# default UA
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    # 'yitu.middlewares.YituSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    # 'yitu.middlewares.YituDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

# Enable or disable extensions
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    # 'yitu.pipelines.YituPipeline': 300,
    'yitu.pipelines.SaveImagePipeline': 300
}

# Image Storage Path
IMAGES_STORE = './images'