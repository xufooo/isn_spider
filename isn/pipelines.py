# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class IsnPipeline(object):
	def __init__(self):
		self.file = open('isn_news.txt', mode='wb')
		self.dbObject = self.dbConnect()

	def dbConnect(self):
		conn = pymysql.connect(
				host = 'localhost',
				user = 'isn',
				passwd = '123456',
				charset = 'utf8',
				use_unicode = False
				)
		return conn

	def process_item(self, item, spider):
		self.file.write("category: " + item['category'].encode('GB18030') + "\n")
		self.file.write(item['url'].encode('GB18030') + "\n")
		self.file.write(item['date'].encode('GB18030') + "\n")
		self.file.write(item['title'].encode('GB18030') + "\n")
		self.file.write(item['content'].encode('GB18030') + "\n")
		self.file.write("image_url:\n" + item['img_url'].encode('GB18030') + "\n")
		self.file.write("\n\n")

		cursor = self.dbObject.cursor()
		sql = 'INSERT INTO isn_web.' + item['category'] + '(category, url, date, title, content, img_url) values (%s, %s, %s, %s, %s, %s)'
		try:
			cursor.execute(sql, (item['category'], item['url'], item['date'], item['title'], item['content'], item['img_url']))
			self.dbObject.commit()
		except Exception, e:
			print e
			self.dbObject.rollback()

		cursor.close()
		return item
