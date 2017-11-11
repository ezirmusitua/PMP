# -*- coding: utf-8 -*-
from scrapy import Spider

from crawler.items import ProxyItemLoader, Proxy


class KxdailiSpider(Spider):
    name = 'kxdaili'
    allowed_domains = ['kxdaili.com']
    start_urls = ['http://www.kxdaili.com/ipList/%d.html' % i for i in range(1, 11)]

    def parse(self, response):
        rows = response.css('div.tab_c_box.buy_tab_box > table > tbody >tr:not(:first-child)')
        proxies = []
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            _types = row.css('td:nth-child(4)::text').extract()[0]
            loader.add_value('type', _types.split(','))
            proxies.append(loader.load_item())
        return proxies