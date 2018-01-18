#—*—coding=utf-8
from app import app
import hashlib
import time
import reply
import receive
import joke
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
			if content.startswith(u"笑话",0,2):
				q = joke.Qiushibaike_Spider()
				item = q.oneitem()
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName, rec_msg.ToUserName, item+"--------------\n%s"%getTime() )
			else:
				rep_text_msg = reply.TextMsg(rec_msg.FromUserName,rec_msg.ToUserName,"复述：%s \n %s"%(rec_msg.Content,getTime()))
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