# SNI-detecter
## 用于发现SNI代理服务器
---
食用方法：
> python sni-detecter.py


> -i, --in 读入ip文件路径。默认为/task.txt

> -o, --out 测试通过ip的保存路径。默认为/passip+输出时间.txt。

> -p, --parallels [number] 默认线程数为20。

> -t, --timeout [float] 超时时间 单位为s 默认为2s。

> -n, --hostname 默认为谷歌。

> -h, --help 帮助。




input文件的格式
> 127.0.0.1-127.0.1.0

OR

> 192.168.1.0/24 

 支持两格式混合，支持多行

hostname 默认用谷歌，避免扫描到大量cdn和bfe。建议用没有cdn的网站作为hostname

博客地址 ： [garnote.top](http://garnote.top)
