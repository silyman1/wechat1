#—*—coding=utf-8

import requests
from bs4 import BeautifulSoup

import sys

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
response = requests.get('http://www.dianping.com/shop/69698308/review_more/p1',headers=headers)
soup = BeautifulSoup(response.text,'lxml')

authors = soup.find_all('div',attrs={'class':'dper-info'})
marks= soup.find_all('div',attrs={'class':'review-words Hide'})
print '111'
length = len(authors)
print length
for i in range(length):
	print authors[i].text.encode('gbk','ignore').strip()
	print marks[i].text.encode('gbk','ignore').strip()