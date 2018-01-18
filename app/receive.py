#—*—coding=utf-8

import xml.etree.ElementTree as ET

def parse_xml(receive_data):
	if len(receive_data) == 0:
		return None
	xmldata = ET.fromstring(receive_data)
	msg_type = xmldata.find('MsgType').text
	if msg_type == 'text':
		return TextMsg(xmldata)
	elif msg_type == 'image':
		return ImageMsg(xmldata)
#消息基类
class Msg(object):
	def __init__(self, xmlData):
		self.ToUserName = xmlData.find('ToUserName').text
		self.FromUserName = xmlData.find('FromUserName').text
		self.CreateTime = xmlData.find('CreateTime').text
		self.MsgType = xmlData.find('MsgType').text
		self.MsgId = xmlData.find('MsgId').text

#文本消息类
class TextMsg(Msg):
	def __init__(self, xmlData):
		Msg.__init__(self, xmlData)
		self.Content = xmlData.find('Content').text.encode("utf-8")

#图片消息类
class ImageMsg(Msg):
	def __init__(self, xmlData):
		Msg.__init__(self, xmlData)
		self.PicUrl = xmlData.find('PicUrl').text
		self.MediaId = xmlData.find('MediaId').text