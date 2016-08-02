import datetime


now=datetime.date(2010,01,01)
datelist=[]
for x in range(1,365*5):
    now1=now+datetime.timedelta(seconds=3600*24*x)
    now1=now1.strftime("%Y-%m-%d").replace('-','',2)
    datelist.append(now1)

print datelist
with open('datelist.txt','w') as fw:
          for x in datelist:
              fw.write(x[2:6]+'\n')
