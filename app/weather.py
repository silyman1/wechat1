#—*—coding=utf-8

import requests
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class Weather_Spider(object):
	base_url ='http://www.sojson.com/open/api/weather/json.shtml?city='
	def getweather(self,city):
		url = self.base_url+str(city).encode('utf-8')
		response = requests.get(url).text
		content = json.loads(response)
		city = content.get('city')
		print city
		quality = content.get('data').get('quality')
		print type(quality)
		T = content.get('data').get('wendu')
		print type(T)
		date =content.get('date')
		print type(date)
		return u'城市：'+city+'\n'+u'日期:'+date+'\n'+u'温度：'+ T +'℃'+'\n'+u'空气质量:'+quality+'\n'