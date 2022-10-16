python中with的作用其实就是省去了开启关闭的功能，比如使用python打开.txt文件，需要先open，最后读写完了，需要close。

在线程中也是这样的，我们给资源加上锁Lock，使用前需要

1. 定义锁：lock = threading.Lock()

2. 启动 lock.acquire()

3. 用完之后的释放lock.release()

而是用with lock则省去了上面的内容，如下代码：

```python
import threading
import time
num=0  #全局变量多个线程可以读写，传递数据
mutex=threading.Lock() #创建一个锁
class Mythread(threading.Thread):
    def run(self):
        global num
        with mutex:  #with Lock的作用相当于自动获取和释放锁(资源)
            for i in range(1000000): #锁定期间，其他线程不可以干活
                num+=1
        print(num)
mythread=[]
for i  in range(5):
    t=Mythread()
    t.start()
    mythread.append(t)
for t in mythread:
    t.join()
print("game over")

'''
    with mutex:  #with表示自动打开自动释放锁
        for i in range(1000000): #锁定期间，其他人不可以干活
            num+=1
#上面的和下面的是等价的
    if mutex.acquire(1):#锁住成功继续干活，没有锁住成功就一直等待，1代表独占
        for i in range(1000000): #锁定期间，其他线程不可以干活
            num+=1
        mutex.release() #释放锁

————————————————
```

版权声明：本文为CSDN博主「bboysky45」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_18668137/article/details/103702117