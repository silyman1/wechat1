#—*—coding=utf-8
from app import app
import hashlib
import requests
import time
import reply
import receive
import joke
import weather
import xml.etree.ElementTree as ET
from flask import request,make_response
@app.route('/wechat',methods = ['GET','POST'])
def wechat_auth():
	print 'coming'
	if request.method == 'GET':
		if len(request.args) > 3:
			token = 'wechatme'
			query = request.args
			print query
			signature = query['signature']
			timestamp = query['timestamp']
			nonce = query['nonce']
			echostr = query['echostr']
			s = [timestamp, nonce, token]
			s.sort()
			s = ''.join(s)
			sha1str = hashlib.sha1(s.encode('utf-8')).hexdigest()
			if sha1str == signature:
				return make_response(echostr)
			else:
				return make_response("认证失败")
		else:
			return "认证失败"
	else:
		rec_msg = receive.parse_xml(request.stream.read())
		if rec_msg.MsgType == 'text':
			content = unicode(rec_msg.Content,"utf-8")
			if content.startswith(u"段子",0,2):
				q = joke.Qiushibaike_Spider()
				item = q.oneitem()
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName, rec_msg.ToUserName, item+"--------------\n%s"%getTime() )
			elif content.endswith(u"天气"):
				city = content.replace(u"天气",u'')
				print city
				w = weather.Weather_Spider()
				data = w.getweather(city)
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName,rec_msg.ToUserName,"%s \n %s"%(data,getTime()))
			else:
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName,rec_msg.ToUserName,"回复段子可获取最新糗事百科段子、回复城市+天气可查看该城市天气\n %s"%(getTime()))
			return rep_text_msg.send()
		elif  rec_msg.MsgType =="image":
			rep_img_msg = reply.ImageMsg(rec_msg.FromUserName,rec_msg.ToUserName,rec_msg.MediaId)
			return rep_img_msg.send()
		else:
			return 'dongdongdong'
@app.route('/hello',methods = ['GET','POST'])
def hello():
	return "hello"
def getTime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())