get类型函数

直接上代码：

```python
class TestMain:

    def __init__(self):

   	 print('TestMain:__init__')

    self.a = 1

if __name__ == '__main__':

t = TestMain()

print(t.a)
```

在没有任何get函数的情况下很简单，打印结果是：

TestMain:__init__1

但是如果访问一个不存在的属性：

```
if __name__ == '__main__':

t = TestMain()

print(t.a)

print(t.b) # 访问了一个不存在的属性
```

结果是：

```
TestMain:__init__

Traceback (most recent call last):1File"C:/Users/sk-leilin/Desktop/mpdp-code-master/test.py", line 19, in print(t.b)

AttributeError:'TestMain' object has no attribute 'b'
```

---



可以看见报错了，下我们来测试一下__getattr__函数：

```python
class TestMain:

def __init__(self):

print('TestMain:__init__')

self.a = 1

def __getattr__(self, item):

print('TestMain:__getattr__')

return 2

if __name__ == '__main__':

t = TestMain()

print(t.a)

print(t.b)
```

打印结果是：

TestMain:__init__1TestMain:__getattr__2

我们仍然访问了一个本来不存在的t.b，为什么这里没有报错呢，因为我们定义了__getattr__函数，而且让它直接返回了2，也就是说，如果定义了这个函数后，访问不存在的属性，会自动调用这个函数作为返回值。

接下来我们看一下__getattribute__这个函数:

```
class TestMain:

def __init__(self):

print('TestMain:__init__')

self.a = 1

def __getattr__(self, item):

print('TestMain:__getattr__')

return 2

def __getattribute__(self, item):

print('TestMain:__getattribute__')

return 3

if __name__ == '__main__':

t = TestMain()

print(t.a)

print(t.b)

打印结果是：

TestMain:__init__

TestMain:__getattribute__3TestMain:__getattribute__3
```

可以看到，无论是访问存在的t.a还是不存在的t.b，都访问到了__getattribute__这个函数，也就是说，只要定义了这个函数，那么属性的访问，都会走到这个函数里面。

我们在看下面的代码：

```
class TestMain:

def __init__(self):

print('TestMain:__init__')

self.a = 1

def __getattr__(self, item):

print('TestMain:__getattr__')

return 2

def __getattribute__(self, item):

print('TestMain:__getattribute__')

if item == 'c':

raise AttributeError

return 3

if __name__ == '__main__':

t = TestMain()

print(t.a)

print(t.b)

print(t.c)

我们知道只要定义了__getattribute__函数，就肯定执行这个函数来获取属性，这次我们增加了判断如果访问c这个属性，我们抛出异常，最后的结果是：

TestMain:__init__

TestMain:__getattribute__3TestMain:__getattribute__3TestMain:__getattribute__

TestMain:__getattr__2

也就是说，如果__getattribute__抛出了AttributeError异常，那么会继续访问__getattr__函数的。
```

总结：

如果定义了__getattribute__，那么无论访问什么属性，都是通过这个函数获取，包括方法，t.f()这种也是访问的这个函数，此时这个函数应该放回一个方法，如果像例子中，仍然返回一个数字，你会获得一个TypeError: 'int' object is not callable错误

只要定义了__getattribute__方法，不管你访问一个存在的还是不存在的属性，都由这个方法返回，比如访问t.a，虽然a存在，但是只要定义了这个访问，那么就不是访问最开始的a了

如果__getattribute__抛出了AttributeError异常，并且定了了__getattr__函数，那么会调用__getattr__这个函数，不论这个属性到底是不是存在

也就是说属性访问的一个大致优先级是：__getattribute__ > __getattr__ > __dict__

单独说一说__get__函数

上面说了__getattribute__和__getattr__，这里单独说一下__get__，因为这个涉及到其它的概念，就是描述器(Descriptor)。

一个类只要实现了__get__，__set__，__delete__中任意一个方法，我们就可以叫它描述器(descriptor)。如果只定义了__get__我们叫非资料描述器(non-data descriptor)，如果__set__，__delete__任意一个/或者同时出现，我们叫资料描述器(data descriptor)。

首先明确一点，拥有这个方法的类，应该(也可以说是必须)产生一个实例，并且这个实例是另外一个类的类属性(注意一定是类属性，通过self的方式产生就不属于__get__范畴了)。

也就是说拥有这个方法的类，那么它的实例应该属于另外一个类/对象的一个属性。 直接看代码吧：

```
class TestDes:

    def __get__(self, instance, owner):

        print(instance, owner)

        return 'TestDes:__get__'

class TestMain:

    des = TestDes()

if __name__ == '__main__':

    t = TestMain()

    print(t.des)

    print(TestMain.des)

其中TestDes定义了__get__方法，在TestMain中，定义了一个类属性des，是TestDes的一个实例，我们访问t.des或者TestMain.des的时候访问的就是访问了TestDes的__get__方法。

打印结果是：

<__main__.TestMain object at 0x0000022563D5D3C8> TestDes:__get__

NoneTestDes:__get
```

其中，__get__方法的第一个参数是实际拥有者的实例对象，如果没有则为None，第二个参数是实际所属的类。

看一下下面的代码：

```
class TestDes:

    def __get__(self, instance, owner):

        print(instance, owner)

        return 'TestDes:__get__'

class TestMain:

    def __init__(self):

        self.des = TestDes()

if __name__ == '__main__':

    t = TestMain()

    print(t.des)

\# print(TestMain.des) #很明显这里会报错

我们通过__init__来产生了一个实例的des属性，这时候，print(t.des)访问的就不是__get__函数了，实际打印结果是：

<__main__.TestDes object at 0x00000165A77ECCF8>

也就是当成一个普通的实例来处理的。
```

非资料描述器，也就是只有__get__，不管是类还是实例去访问，默认都获得的是__get__的返回值，但是，如果中间有任何一次重新赋值，那么，这个实例获得的是新的值(对象)，已经和原来的描述器完全脱离了关系

资料描述器，比如有__set__方法，后期通过实例对描述器进行赋值，那么访问的是__set__，并且永远关联起来。但是如果通过修改类属性的方式复制，那么也会被重新获取新的值(对象)。

看下面的代码：

class TestDes:

def __get__(self, instance, owner):

print('TestDes:__get__', instance, owner)

return 'TestDes:__get__'

class TestMain:

des = TestDes()

if __name__ == '__main__':

t = TestMain()

print(t.des)

print(TestMain.des)

print()

t.des = 1

print(t.des)

print(TestMain.des)

print()

TestMain.des = 1

print(t.des)

print(TestMain.des)

上面是一个非资料描述器，打印结果是：

TestDes:__get__ <__main__.TestMain object at 0x000002C9BCCF0080> TestDes:__get__

TestDes:__get__ NoneTestDes:__get__1TestDes:__get__ NoneTestDes:__get__1

1

具体根据上面的描述行为进行分析，就可以得出结果了。

我们在看一下资料描述器：

class TestDes:

def __get__(self, instance, owner):

print('TestDes:__get__', instance, owner)

return 'TestDes:__get__'

def __set__(self, instance, value):

print('TestDes:__set__', instance, value)

\# 其它代码没有修改

打印结果如下：

TestDes:__get__ <__main__.TestMain object at 0x000002140A46D390> TestDes:__get__

TestDes:__get__ NoneTestDes:__get__

TestDes:__set__<__main__.TestMain object at 0x000002140A46D390> 1TestDes:__get__<__main__.TestMain object at 0x000002140A46D390> TestDes:__get__

TestDes:__get__ NoneTestDes:__get__1

1

总结

__getattribute__和__getattr__用于实例访问属性使用，拥有__get__方法的类是只能其实例属于类属性的时候生效

只要有__getattribute__，任何属性访问都是这个的返回值，以下都是在__getattribute__不存在或者有AttributeError异常发生的情况下描述的

访问不存在的属性，__getattr__生效

访问存在的属性，如果是描述器，描述器生效

如果通过实例对描述器进行赋值操作，又有资料和非资料描述器的区分，如果定义了__set__，那么此方法生效，并且仍然是原始的资料描述器，否则被赋值为新对象

描述器赋值如果是通过类的属性方式赋值，而不是类的实例方式赋值，描述器失效

针对描述器的说明： 描述器是被__getattribute__调用的，如果重写了这个方法，将会阻止自动调用描述器，资料描述器总是覆盖了实例的__dict__， 非资料描述器可能覆盖实例的__dict__。





https://zhuanlan.zhihu.com/p/62569340

```
class Cat:
    class_level = '贵族'
    def __init__(self,name,type,speed,age):
        self.name = name
        self.type= type
        self.speed = speed
        self.age = age


    def run(self):
        print('%s岁的%s%s正在以%s的速度奔跑' % (self.age,self.type,self.name,self.speed))

    def __getattr__(self, item):
        print('你找的属性不存在')

    def __setattr__(self, key, value):
        print('你在设置属性')

    def __delattr__(self, item):
        print('你在删除属性')

xiaohua = Cat('小花','波斯猫','10m/s',10)
xiaohua.run() #10岁的波斯猫小花正在以10m/s的速度奔跑
```

