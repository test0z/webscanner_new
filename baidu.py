import difflib
import colprint
import re

from Queue import Queue
from bs4 import BeautifulSoup
from sqlinjectclass import SqlInject
import requests
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('-s',dest='plugin',required=True)
parse.add_argument('-u',dest='site')

def getsite(pluginstr,sitestr):
	subdomain=[]
	if pluginstr=='site':
		site='site:'+sitestr
		restr='([a-zA-Z0-9.\-]+)\.'+sitestr
	else:
		
		site='@'+sitestr
		restr='([a-zA-Z0-9\.-]+)<em>@'+sitestr
	for x in range(1,50):

		paradata={'ch':'','wd':site,'pn':10*(x-1)}      	
		url='http://www.baidu.com/s'	

		r=requests.get(url,params=paradata)
		r.cookies['BAIDUID']=r.cookies['BAIDUID']+':SL=0:NR=50'	
		a=requests.get(url,params=paradata,cookies=r.cookies)
		
		domainstr=re.findall(restr,a.text)
		subdomain=domainstr+subdomain

	subdomain=list(set(subdomain))


	for x in subdomain:
		if args.plugin=='site':
			print 'http://'+x+'.'+sitestr
		else:
			print x+'@'+sitestr
	return subdomain

def getip(subdomain,sitestr):
	for x in subdomain:
		_sitestr=x+'.'+sitestr
		_data='host='+_sitestr+'&linetype=%E7%94%B5%E4%BF%A1%2C%E5%A4%9A%E7%BA%BF%2C%E8%81%94%E9%80%9A%2C%E7%A7%BB%E5%8A%A8%2C%E6%B5%B7%E5%A4%96'
		_header={'Content-Type': 'application/x-www-form-urlencoded'}	

		_guid=requests.post('http://ping.chinaz.com/',data=_data,headers=_header)
		_result=re.findall('guid:\'(\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12})\'',_guid.text)
		_enkey=re.findall('enkey=\'(\S+)\'',_guid.text)
		#print _enkey
		for guid in _result[0:3]:
			_data={'guid':guid,'host':_sitestr,'ishost':'false','encode':_enkey[0],'checktype':''}
			_ipresult=requests.post('http://ping.chinaz.com/iframe.ashx?t=ping',data=_data)
			_ip=re.search('(\d+\.){3}\d+',_ipresult.content)
			if _ip:
				print _ip.group()

args=parse.parse_args()
getip(getsite(args.plugin,args.site),args.site)

