# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Qiushibaike_Spider(object):
	base_url = 'https://www.qiushibaike.com/8hr/page/'
	def oneitem(self):
		page_num = random.randint(1,13)
		url1 = self.base_url +str(page_num)+'/'
		response = requests.get(url1)
		soup = BeautifulSoup(response.text,'lxml')
		items_list = soup.find_all('div',class_='content')
		length = len(items_list)
		item_num = random.randint(0,length-1)
		print items_list[item_num].text.strip()
		return items_list[item_num].text.strip()