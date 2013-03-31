from pyquery import PyQuery as pq
import pycurl
import cStringIO
import sys
import pdb

from selenium import webdriver

from Queue import Queue

import threading
import time
from datetime import datetime, timedelta

g = webdriver.PhantomJS()





def wait_for_element(client,by="",value=""):

    #if options.use_phantomjs:
    #   sleep(1);
    for i in range (0,18):
        rv = client.find_elements(by=by,value=value)
        if rv != []:
            return rv[0]
        sleep(1)
    print "Element search failed"
    return None


def wait_for_elements(client,by="",value=""):

    #if options.use_phantomjs:
    #   sleep(1);
    for i in range (0,18):
        rv = client.find_elements(by=by,value=value)
        if rv != []:
            return rv
        sleep(1)
    print "Element search failed"
    return None



def getProxyList():

    plist = []

    g.get('http://www.proxynova.com/proxy-server-list/?pxl=ea')
    proxy_list = wait_for_elements(g,by='css',value='#tbl_proxy_list tbody tr')
    

    for proxy in proxy_list:
        
        #pdb.set_trace()
        ip = proxy.find_elements(by='css',value='.row_proxy_ip')
        if ip == []:
            continue
        else:
            ip = ip[0]
        port = proxy.find_elements(by='css',value='.row_proxy_port')
        if port==[]:
            continue
        else:
            port = port[0]
        plist.append(ip.text+':'+port.text)
        #print ip.text+':'+port.text

    return plist


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

proxy_list = getProxyList()

num_worker_threads = 10

q = Queue()
success = []

for p in proxy_list:
    q.put(p)

def worker():
    while not q.empty():
        line = q.get()
        line = line.encode('ascii','ignore')
        if check(domain, line):
            success.append(line)
            print(line + ' OK')
       # else :
            #print(line + ' Failed')
        q.task_done()

for i in range(num_worker_threads):
            t = threading.Thread(target=worker)
            t.start()

