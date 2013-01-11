from pyquery import PyQuery as pq
import pycurl
import cStringIO
import sys



def check(domain, proxy):
    ip, port = proxy.split(':')
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.CONNECTTIMEOUT, 3)
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.PROXY, ip)
    c.setopt(pycurl.PROXYPORT, int(port))
    c.setopt(pycurl.URL, 'http://' + domain + '/')
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    try:
      c.perform()
    except pycurl.error, e:
	    return False
    return True
    

domain = sys.argv[1]

f = open('proxy_list', 'r')
s = open('success', 'w')
proxy_list = f.readlines()
success = []
for line in proxy_list:
    if check(domain, line):
        success.append(line)
        print(line + ' OK')
    else :
        print(line + ' Failed')
s.writelines(success);
f.close()
s.close()
