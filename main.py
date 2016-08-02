import sys
import getopt
from ctypes import *
from Queue import Queue
import argparse
import scan
import banner
from discuz import DiscuzScan



def version():
    
    print '''\n\n--------------------------------------------------------------------------------

        Scanner/0.13-dev - Simple Web Application Vul scanner    Z
    

[!] legal disclaimer: Usage of Scanner for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicablelocal, state and federal laws. Developers assume no liability and are not respon sible for any misuse or damage caused by this program
                                                                   
--------------------------------------------------------------------------------

'''
    # define command line parameters and help page
def cmdargs():
    

    parser = argparse.ArgumentParser(
    usage = '\n\n   ./%(prog)s --plugin=simple --target <arg> | --targets-range <arg> | --targets-list <arg>',
    formatter_class = argparse.RawDescriptionHelpFormatter,
    epilog =
    'examples:\n\n'

    '  attack single target\n'
    '  usage: ./%(prog)s --plugin=simple --target="http://www.kendingbucunzai.com/"'

    '  checking out ip alive in ip-range\n'
    '  usage: ./%(prog)s --plugin=path --target="http://i-security.cc/" --delay=2'
    '  usage: ./%(prog)s --plugin=ipalive --target=192.168.0-10.1-254 --delay=2',
    add_help = False
    )

    options = parser.add_argument_group('options', '')
    #Scanner Function
    options.add_argument('--plugin', default='simple', dest='plugin',
            help='just do simple scan (default: simple)')

    options.add_argument('--targetrange', default=False, metavar='<ip/range>',
            help='ip address/ip range/domain (e.g.: 192.168.0-3.1-254)')
    options.add_argument('--targetlist', default=False, metavar='<file>',
            help='list of targets')
    options.add_argument('--target', default=False, metavar='<string>',
            help='list of targets')

    options.add_argument('--u', default='admin', metavar='<username>',
            help='single username (default: admin)')
    options.add_argument('--U', default=False, metavar='<file>',
            help='list of usernames')
                           
    options.add_argument('--delay', default=20, metavar='<sec>',
            help='timeout in seconds (default: 20)')
    
    args = parser.parse_args()

    if (args.target == False) and (args.targetrange == False) and (args.targetlst == False):
        print ''
        parser.print_help()
        sys.exit(0)
    return args

def useragent():
    print"useragent"
    
def main():
    version()
    args=cmdargs()
    Scanner=banner.PathScan()
    if args.target:
        HOSTLIST.append(args.target)
        print args.target
    if args.plugin:
        if args.plugin=='simple':           
            Scanner.serverbanner(HOSTLIST[0])
            Scanner.path(HOSTLIST[0])
        if args.plugin=='path':
            Scanner.path(HOSTLIST[0])
        if args.plugin=='banner':
            Scanner.serverbanner(HOSTLIST[0])
        if args.plugin=='sql':
            print 'SQL Injection scan start'
            Scanner.urllist(HOSTLIST[0])
            Scanner.sqlinjectscan(HOSTLIST[0])
            
        if args.plugin=='discuz':
            DiscuzScan().DzScan(HOSTLIST[0])
    


if __name__=='__main__':
    
    HOSTLIST=[]
    main()
