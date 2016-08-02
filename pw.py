from itertools import *
import sys
def PasswordDic(username):
    dic=[]
    dictlist=[]
    f=open('dict.txt','r')
    for pwd in f:
        dic.append(pwd.strip())
    f.close()
    for (Pwd,UsernameStr) in product(username,dic):
        dictlist.append(Pwd+UsernameStr)
    f=open('pw.txt','a')
    for line in dictlist:
        f.write(line+'\n')
    f.close()
    return dictlist   
def main():
    
    if len(sys.argv)<2:
        print 'error'
        return
    PasswordDic([sys.argv[1]])



if __name__=='__main__':
    main()

