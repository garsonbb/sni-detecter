#coding=utf-8

# by garson blog garnote.top
import socket, ssl
import queue
from netaddr import IPNetwork,IPRange

def detect (ip,timeout,hostname) :
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    #context.check_hostname = True
    context.load_default_certs()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    ssl_sock = context.wrap_socket(s, server_hostname = hostname)
    try:
        ssl_sock.connect((ip, 443))#219.76.4.4 218.254.1.13
        ca = str(ssl_sock.getpeercert())
        ssl_sock.close()
        s.close()
        if ca.find(hostname) == -1:
            return False
        else:
            return True
    except:
        return False
    return True

#print(detect("219.76.4.4",2))

def usage():
    helps = '''
-i, --in 读入ip文件路径。默认为/task.txt
-o, --out 测试通过ip的保存路径。默认为/passip+输出时间.txt。
-p, --parallels [number] 默认线程数为20。
-t, --timeout [float] 超时时间 单位为s 默认为2s。
-n, --hostname 默认为谷歌。
-h, --help 帮助。
    '''
    print(helps)

def gen_ip(a):
    ipQueue = queue.Queue()
    txt = a
    list1 = txt.split("\n")
    for n in list1:
        list2 = n.split('-')
        if len(list2) == 2:
            tmp = IPRange(list2[0],list2[1])
            for b in tmp:
                ipQueue.put(b)
        elif len(n.split('/')) == 2:
            tmp = IPNetwork(n)
            for b in tmp:
                ipQueue.put(str(b))
    return ipQueue