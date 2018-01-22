#—*—coding=utf-8
from app import app
import hashlib
import requests
import time
import json
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
			elif content.startswith(u"斗图"):
				get_list()
				media_id = get_mediaid()
				rep_img_msg = reply.ImageMsg(rec_msg.FromUserName,rec_msg.ToUserName,media_id)
				return rep_img_msg.send()
			else:
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName,rec_msg.ToUserName,"回复段子可获取最新糗事百科段子、回复城市+天气可查看该城市天气\n %s"%(getTime()))
			return rep_text_msg.send()
		elif  rec_msg.MsgType =="image":
			media_id = get_mediaid()
			rep_img_msg = reply.ImageMsg(rec_msg.FromUserName,rec_msg.ToUserName,media_id)
			return rep_img_msg.send()
		else:
			return 'dongdongdong'
@app.route('/hello',methods = ['GET','POST'])
def hello():
	return "hello"
def getTime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def get_mediaid():
	upload_url = 'https://api.weixin.qq.com/cgi-bin/material/add_material'
	params = {
		'access_token':get_token(),
		'type':'image'
	}
	file_path = r'E:\gitprojects\test\a.jpg'
	files = {'media':open(file_path,'rb')}
	response = requests.post(url=upload_url,params = params,files=files)
	dict = response.json()
	return dict['media_id']
def get_token():
	params = {
		'grant_type':'client_credential',
		'appid':'wxb6f15704b47df7c2',
		'secret':'a239af3ab271dc39ca0fad597e653b2d'
	}
	token_url = 'https://api.weixin.qq.com/cgi-bin/token'
	response=requests.get(url = token_url,params=params)
	result = response.json()
	return result['access_token']
def get_list():
	url="https://api.weixin.qq.com/cgi-bin/material/batchget_material"
	params = {
		'access_token':get_token(),
	}
	datas={
		"type":"image",
		"offset":0,
		"count":20
	}
	data = json.dumps(datas)
	a=requests.post(url=url,params= params,data =data)
	print(a.text)