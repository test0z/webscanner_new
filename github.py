# -*- coding: utf-8 -*-
import requests
import re

def getNum():
	_url='https://github.com/search?utf8=%E2%9C%93&q=%40hundsun.com&type=Repositories&ref=searchresults'
	_cookie={'logged_in':'yes','dotcom_user':'gitinfogain',' user_session':'boax_vy0ZrQysUJmpzYIQ7oUmxPDoDHehZUhTLSARIomO--AV3TA3JfTQGTf-hKn3wQvjXL6WMY8fy1s',' _gh_sess':'eyJsYXN0X3dyaXRlIjoxNDY3MjY5MzM5MjMzLCJmbGFzaCI6eyJkaXNjYXJkIjpbImFuYWx5dGljc19kaW1lbnNpb24iXSwiZmxhc2hlcyI6eyJhbmFseXRpY3NfZGltZW5zaW9uIjp7Im5hbWUiOiJkaW1lbnNpb241IiwidmFsdWUiOiJMb2dnZWQgSW4ifX19LCJzZXNzaW9uX2lkIjoiZTViNGI2ZDg1YjkyZDRmNGEzMjhjNjg3MDAwMzExZGYifQ%3D%3D--d0b3b8f2bda43454c56043d4e7328fa91995fb18','_ga':'GA1.2.939215265.1467269274','tz':'Asia%2FShanghai'}
	try:

		result=requests.get(url=_url,cookies=_cookie,verify=False)
		
	except requests.exceptions.RequestException as e:
		print "Error: {}".format(e)
		return False
	f=open('fuckgit.html','w')
	f.write(result.content)
	f.close()
	_Num=re.findall('Code<span class="counter">(.+)</span>',result.content)
	if len(_Num):
		print _Num[0]

getNum()