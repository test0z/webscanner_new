import requests
import sys	

def getstatus(_url):
	try:
		result=requests.get(url=_url,verify=False,timeout=2.5)
	except requests.exceptions.RequestException as e:
		print "Error: {}".format(e)
		return False
	print url,' is open'
def main():
	_ports=[21,22,23,80,81,443,873,1099,1433,3306,3389,7001,7002,8000,8001,8009,8080,8090,8099,9000,9001,9002,9200]
	print 1
	for _port in _ports:
		_url='http://'+sys.argv[1]+':'+str(_port)+'/'
		print _url
		getstatus(_url)

if __name__=="__main__":
	print '1'
	main()