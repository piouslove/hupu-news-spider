#!/user/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from lxml import etree

class HPnews:

	def __init__(self):
		self.page = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : self.user_agent }
		self.news = []
		self.enable = False

	def getpage(self,page):
		try:
			url = "https://voice.hupu.com/nba/" + str(page)			
			request = urllib2.Request(url,headers = self.headers)
			response = urllib2.urlopen(request)
			html = response.read().decode('utf-8')
			selector = etree.HTML(html)
			return selector
			
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"链接虎扑失败，原因为：",e.reason
				return None

	def getnews(self,page):
		selector = self.getpage(page)
		news_perpage = []
		titles = selector.xpath("//div[@class='news-list']/ul/li/div/h4/a/text()")
		hrefs = selector.xpath("//div[@class='news-list']/ul/li/div/h4/a/@href")
		times = selector.xpath("//div[@class='news-list']/ul/li/div/span[@class='other-left']/a/@title")
		news_perpage.append(times)
		news_perpage.append(titles)
		news_perpage.append(hrefs)
		return news_perpage

	def loadnews(self):
		if self.enable == True:
			if len(self.news) < 2:
				news_perpage = self.getnews(self.page)
				if news_perpage:
					self.news.append(news_perpage)
					self.page += 1

	def readnews(self,news_perpage,page):
		for i in range(len(news_perpage[0])):
			input = raw_input()
			self.loadnews()
			if input == "quit":
				self.enable = False
				return
			print u"第%d页\t时间:%s\t标题:%s\t链接:%s\n" %(page,news_perpage[0][i],news_perpage[1][i],news_perpage[2][i])

	def start(self):
		print u"按回车查看下一条虎扑NBA新闻，输入quit退出"
		self.enable = True
		self.loadnews()
		nowpage = 0
		while self.enable:
			if len(self.news)>0:
				news_perpage = self.news[0]
				nowpage += 1
				del self.news[0]
				self.readnews(news_perpage,nowpage)

spider = HPnews()
spider.start()			








