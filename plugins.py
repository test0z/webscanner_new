from threading import Thread
from Queue import Queue
from time import sleep
import urllib,urllib2,cookielib,socket


#NUM是并发线程总数

q = Queue()
NUM = 8

def working():
    while True:
        arguments = q.get()
        Urlfind(arguments)        
        q.task_done()

def Urlfind(url):
    socket.setdefaulttimeout(20)
    w=open('code.txt','a')
    headers_values = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
             "Accept": "text/plain","Cookie": "__utma=225961425.1925687246.1398402498.1398402498.1398402498.1; __utmb=225961425.2.10.1398402498; __utmc=225961425; __utmz=225961425.1398402498.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __atuvc=2%7C17"}
    req = urllib2.Request(url,headers=headers_values)    
    try:  
      page = urllib2.urlopen(req)
      print 'plugins find:',page.geturl()
      w.write(url)
      w.write('\n')
    except urllib2.HTTPError, e:  
      print e.code
      print 'The url is :',url,'\n'
    except urllib2.URLError, e:  
      print "Error Reason:", e.reason
    w.close()
    
def Mutlthread():     
  for i in range(NUM):
      t = Thread(target=working)
      t.setDaemon(True)
      t.start()
  f=open('plugins.txt','r')
  for line in f:
    line="http://www.xxx.com/wp-content/plugins/"+line.strip('\n') 
    q.put(line)
  f.close()      
  q.join()


if __name__ == "__main__":

    Mutlthread()
   
    
 
