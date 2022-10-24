# python字符串形式的列表转列表

```python
直接用python里的eval( )函数
>>> fruits = "['apple','orange','banana']"
>>> import ast
>>> fa = ast.literal_eval(fruits)
>>> print(fa)
['apple', 'orange', 'banana']
>>> print(type(fa))
<class 'list'>
>>> fb = eval(fruits)
>>> print(fb)
['apple', 'orange', 'banana']
>>> print(type(fb))
<class 'list'>
channel_out=eval(channel_out)
kernel_size=eval(kernel_size)

```

