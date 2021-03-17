import time
import requests
import json
from pprint import pprint
from Constants import Constants
from ConfigReader import ConfigReader	
import os.path
from datetime import date
from datetime import datetime, timedelta
import json
import requests

class Utils:

	def loadDataFromFile(file):
		try:
			f = open(file,"r")
			data = json.loads(f.read())
			f.close()
			return data
		except Exception as e:
			print(e)
			raise e
	
	def makeRequestUrl(url,cookie_header,raw_data,method_type):
		if url:
			if cookie_header != Constants.NONE:
				cookies=cookie_header
			else:
				cookies='';
			if raw_data != Constants.NONE:
				data_send=Utils.convertFormDataToJson(raw_data)
				#print(data_send)
			else:
				data_send='';
		try:
			if method_type == Constants.HTTP_METHOD_TYPE_GET:
				return requests.get(url,cookies=cookies)
			elif method_type == Constants.HTTP_METHOD_TYPE_POST:
				#print(data_send)
				return requests.post(url,data=data_send,cookies=cookies)
		except Exception as e:
			print(e)
		return Constants.EXCEPTION_QUERY

	def convertTextToJson(text):
		dict1 = {}
		command, description = text.strip().split(None, 1)
		dict1[command] = description.strip()
		return dict1

	def convertFormDataToJson(formdata):
		dict2 = {}
		for data in formdata.split(Constants.AMPERCENT):
			d_list = data.split(Constants.EQUALS)
			dict2[d_list[0]]=d_list[1].strip()
		return dict2
