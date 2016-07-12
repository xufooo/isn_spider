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
			item = IsnItem()
#            item['title'] = sel.xpath('a/text()').extract_first()
			item['url'] = sel.xpath('a/@href').extract_first()
#            item['date'] = sel.xpath('span/text()').extract_first()
			url = response.urljoin(sel.xpath('a/@href').extract_first())
#            yield item
			yield scrapy.Request(url, callback = self.parse_dir_contents)


	def parse_dir_contents(self, response):
		item = IsnItem()
		item['title'] = response.xpath("//tr[1]/td[1]/text()").extract()[1].strip()
		item['date'] = response.xpath("//tr[2]/td/span/text()").extract()[0].strip()
		item['url'] = response.url
		yield item
