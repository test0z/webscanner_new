
import win32ras

try:
    hdl, retcode = win32ras.Dial (None, None, (vpn_name, ip, "", username, password, ""), None)
except:
    print 'error'
