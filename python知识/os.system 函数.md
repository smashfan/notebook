- system函数可以将字符串转化成命令在服务器上运行；其原理是每一条system函数执行时，其会创建一个子进程在系统上执行命令行，子进程的执行结果无法影响主进程；
- 上述原理会导致当需要执行多条命令行的时候可能得不到预期的结果；

```python
import os

os.system('cd /usr/local')
os.mkdir('aaa.txt)
```

开启的进程的路径是执行python文件的路径

**使用system执行多条命令**

为了保证system执行多条命令可以成功，多条命令需要在同一个子进程中运行；

```text
import os

os.system('cd /usr/local && mkdir aaa.txt')
# 或者
os.system('cd /usr/local ; mkdir aaa.txt')
```





参考文献：

https://zhuanlan.zhihu.com/p/51716674