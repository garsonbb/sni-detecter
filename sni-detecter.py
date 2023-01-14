#coding=utf-8

# by garson blog garnote.top
import sys, getopt
import queue
import time
from detect import *
import concurrent.futures


rin = 'task.txt'
output = 'replace'
timeout = 5
parallels = 100
hostname = 'google.com'
passip = []

times = 0
n = 0

def main():
    try:
        opts ,args = getopt.getopt(sys.argv[1:],'i:o:t:p:n:h',['in=','out=','timeout=','parallels=','hostname=','help'])
    except getopt.GetoptError as err:
        usage()
        print(err)
        sys.exit('parameter error')
    global rin ,output ,timeout ,parallels ,hostname,ipQueue
    for o, a in opts:
        if o in ('-i','--in'):
            rin = a
        elif o in ('-o','--out'):
            output = a
        elif o in ('-h','--help'):
            usage()
            sys.exit()
        elif o in ('-t','--timeout'):
            timeout = int(a)
        elif o in ('-n' , '--hostname'):
            hostname = a
        elif o in ('-p','--parallels'):
            parallels = int(a)
    file_obj = open(rin)
    try:
        txt = file_obj.read()
        ipQueue = gen_ip(txt)
        print('读入了'+ str(ipQueue.qsize()) +'个ip')
    finally:
        file_obj.close()
if __name__ == '__main__':
    main()


def worker (t,h):
    global times ,passip ,ipQueue
    try:
        ip = ipQueue.get(timeout=5)
    except:
        pass
    else:
        r = detect(ip,t,h)
        times += 1
        if r == True:
            passip.append(ip)
            printx ('√   '+ip , 1)
    printx()



def printx (text = '',type = 0):
    global times,n
    p = int((times/n)*30)
    t1 = '##############################' #30
    t2 = '                              ' #30
    if type == 1:
        sys.stdout.write('                                                      \r')
        sys.stdout.flush()
        print(text)
    else:
        sys.stdout.write('[' + t1[0:p] + t2 [0:30-p] + ']' + '\r')
        sys.stdout.flush()


executor = concurrent.futures.ThreadPoolExecutor(parallels)
n = ipQueue.qsize()

all_task = [executor.submit(worker,timeout,hostname) for i in range(n)]

print('Working')
printx()

concurrent.futures.wait(all_task)
executor.shutdown(wait=True)

print ('√   finish  ' + '本次扫描了'+ str(times) +'个ip,'+'SNI_IP有'+ str(len(passip)) +'个。')
if output == 'replace':
    name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    output = 'PassIp '+ name +'.txt'
f = open (output,'w')
try:
    for v in passip:
        f.writelines(v+'\n')
finally:
    f.close()
    print('bye,文件已写出到'+output+'，按Enter退出。')
    input()