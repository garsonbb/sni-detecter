# by garson blog garnote.top
import sys, getopt
import threadpool
import time
from detect import *

rin = 'task.txt'
output = 'replace'
timeout = 2
parallels = 20
mod = True
ips = []
passip = []

times = 0
n = 0
def main():
    try:
        opts ,args = getopt.getopt(sys.argv[1:],'i:o:t:p:h:m',['in','out','help','timeout','parallels'])
    except getopt.GetoptError as err:
        usage()
        sys.exit('parameter error')
    global rin ,output,timeout,parallels,ips,mod
    for o, a in opts:
        if o in ('-i','--in'):
            rin = a
        elif o in ('-o','--out'):
            output = a
        elif o in ('-h','--help'):
            usage()
            sys.exit()
        elif o in ('-t','--timeout'):
            timeout = a
        elif o in ('-p','--parallels'):
            parallels = a
        elif o == '-m':
            mod = False
    file_obj = open(rin)
    try:
        txt = file_obj.read()
        ips = gen_ip(txt)
        print('读入了'+ str(len(ips)) +'个ip')
    finally:
        file_obj.close()
if __name__ == '__main__':
    main()

def worker (ip,t,m):
    global times ,n ,passip
    if detect(ip,t) == True:
        passip.append(ip)
        print ('√   '+ip)
    else:
        if m == False:
            print ('x   '+ip)
    times += 1
    if times == n :
        global output
        print ('√   finish  ' + '本次扫描了'+ str(times) +'个ip,'+'SNI_IP有'+ str(len(passip)) +'个。')
        if output == 'replace':
            name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            output = 'PassIp '+ name +'.txt'
        f = open (output,'w')
        try:
            for v in passip:
                f.writelines(v)
        finally:
            f.close()
            print('bye,文件已写出到'+output)



pool = threadpool.ThreadPool(parallels)
requests = []
n = len(ips)
for a in ips:
    c = [a,timeout,mod]
    var =[(c,None)]
    requests += threadpool.makeRequests(worker,var)
[pool.putRequest(req) for req in requests]
print('Working')
pool.wait()