# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import scrapy
from isn.items import IsnItem
from scrapy.utils.markup import remove_tags
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class ISNSpider(scrapy.Spider):
	name = "isnspider"
	allowed_domains = ["isn.xidian.edu.cn"]
	start_urls = [
		"http://isn.xidian.edu.cn/kfjl/xsjl.htm",
		"http://isn.xidian.edu.cn/xwgg/xwdt.htm",
		"http://isn.xidian.edu.cn/xwgg/tzgg.htm",
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
		next_page_url = response.urljoin(response.xpath("//div[@class='liebiaorf']//a[@class='Next']/@href").extract_first())
		yield scrapy.Request(next_page_url, callback = self.parse)


	def parse_dir_contents(self, response):
		item = IsnItem()
		item['category'] = response.xpath("//div[@class='neirongt']//table//tr/td").xpath('string(.)').extract()[0].split('>')[-2].strip()
		print item['category']
		item['title'] = response.xpath("//div[@class='neirongf viewbox']//form/table/tr[1]/td").xpath('string(.)').extract_first().strip()
		item['date'] = response.xpath("//div[@class='neirongf viewbox']//table/tr[2]/td/span/text()").extract()[0].strip()
		item['content'] = remove_tags("".join(response.xpath("//div[@class='neirongf viewbox']//form/table//div[@id='vsb_newscontent']//p").extract()))
		img_relative_url = response.xpath("//div[@class='neirongf viewbox']//form/table//div[@id='vsb_newscontent']//p/img/@src").extract()
		item['img_url'] = "\n".join([urljoin_rfc(get_base_url(response), ru) for ru in img_relative_url])
		item['url'] = response.url
		yield item
