#coding=utf-8

# by garson blog garnote.top
import socket, ssl
from netaddr import IPNetwork

def detect (ip,timeout,hostname) :
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
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
    txt = a
    temp = []
    list1 = txt.split("\n")
    for n in list1:
        list2 = n.split('-')
        if len(list2) == 2:
            tmp = iprange(list2[0],list2[1])
            for b in tmp:
                temp.append(b)
        elif len(n.split('/')) == 2:
            tmp = IPNetwork(n)
            for b in tmp:
                temp.append(str(b))
    return temp

def ip2num(ip):#ip to int num
    lp = [int(x) for x in ip.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]


def num2ip(num):# int num to ip
    ip = ['', '', '', '']
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])


def iprange(ip1,ip2):
    num1 = ip2num(ip1)
    num2 = ip2num(ip2)
    temp = []
    tmp = num2 - num1
    n = 0
    if tmp < 0:
        return None
    else:
        for num in range(num1,num2 + 1):
            temp.append(num2ip(num1 + n))
            n +=1
        return(temp)


#print(iprange('192.168.199.1','192.168.200.1'))
