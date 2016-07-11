# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import scrapy
from isn.items import IsnItem

class ISNSpider(scrapy.Spider):
    name = "isnspider"
    allowed_domains = ["isn.xidian.edu.cn"]
    start_urls = [
            "http://isn.xidian.edu.cn/xwgg.htm",
            ]

    def parse(self, response):
        for sel in response.xpath("//div[@class='liebiaorf']/ul/li"):
            print sel
            item = IsnItem()
            item['title'] = sel.xpath('a/text()').extract_first()
            item['url'] = 'http://isn.xidian.edu.cn/' + sel.xpath('a/@href').extract_first()
            item['date'] = sel.xpath('span/text()').extract_first()
            yield item
