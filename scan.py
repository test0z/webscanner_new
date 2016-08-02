# -*- coding: utf-8 -*-
import urllib2, urllib,cookielib,re,os,socket,httplib,zlib
class scanclass(object):
     
    def GetData(self,url,method='',postdata='',regstr='',header={}):
        TIMEOUT=20
        resultlist=[{},0,'','']
        socket.setdefaulttimeout(TIMEOUT)
        
        try:
            cookie = cookielib.CookieJar()
            cookieProc = urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)
        i_headers = ["User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"]
        if postdata=='':
            if header=={}:
                req = urllib2.Request(url)                
            else:
                req = urllib2.Request(url,headers=header)
            
        else:
            if header=={}:
                req=urllib2.Request(url,urllib.urlencode(postdata))
            else:
                req=urllib2.Request(url,urllib.urlencode(postdata),headers=header)
            
        req.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5")
        if method:
            req.get_method = lambda: method
            try:
                
                response=opener.open(req)
                resultlist[1]=response.getcode()
                htmlfile=response.read()
                print '1'   
            except:
                return resultlist
          
        else:
            try:
                response = urllib2.urlopen(req)
                htmlfile = response.read()
                                
            except urllib2.HTTPError,e:    
                resultlist[1]=e.code
                resultlist[0]=e.geturl()
                print '3'
                
                resultlist[2]=dict(e.info())
                return resultlist
            except urllib2.URLError,e:

                resultlist[0]='Failed to reach the server'
                print '4'
                resultlist[2]=0
                return resultlist
            except httplib.BadStatusLine,e:
                resultlist[0]='httplib.BadStatusLine:'
                
                print 'httplib.BadStatusLine:'
                return resultlist
            except socket.error,e:
                print e
                resultlist[0]='time out'
                return resultlist

            
        resultlist[0]=response.geturl()
        if (resultlist[0]!=url):
            resultlist[1]=301
        else:
            resultlist[1]=200
                
        print '2'
        resultlist[3]=dict(response.headers).get('content-length', 0)

        if regstr=='':
            resultlist[2]=dict(response.info())       
            print '5'
            if resultlist[3]==0:
                resultlist[3]=len(htmlfile)
            return resultlist

        
        else:
                print '6'
                EncodeMethod=dict(response.info()).get('content-encoding',1)
              
                if EncodeMethod=='gzip':
                    htmlfile= zlib.decompress(htmlfile, 16+zlib.MAX_WBITS);                    
                    if resultlist[3]==0:
                        resultlist[3]=len(htmlfile)
                    if regstr=='*':
                        resultlist[2]=htmlfile
                        return resultlist
                    result=re.findall(regstr,htmlfile)

                    resultlist[2]=result
                    return resultlist
                    
                else:
                    if regstr=='*':
                        resultlist[2]=htmlfile
                        return resultlist
                    result=re.findall(regstr,htmlfile)
                    resultlist[2]=result
                    return resultlist
