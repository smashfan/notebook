# 读取和保存

### 1.读取cvs

pd.read_csv

tip：注意用逗号区别的时候不要有空格

# 增

### 增加行

1.loc

```python
data=pd.DataFrame(columns=["x","y"])
data.loc[i]=[,,,,]

data.loc[0:2,'年龄':'职业']
解释：
1.从data中选取列名为年龄到职业之间的所有字段
2.0:2指的是选取行数，选0-2一共3行数据
```

2.append

```python
    import pandas as pd
    
    data = pd.DataFrame()
    a = {"x":1,"y":2}
    data = data.append(a,ignore_index=True)
    print(data)

```

3.concat

### 增加列

```python
一.insert()函数
df.insert(loc=2, column='c', value=3)  # 在最后一列后，插入值全为3的c列
print('插入c列：\n', df)
二、直接赋值法
语法：df[‘新列名’]=新列的值
实例：插入d列
三、reindex()函数
四、concat()函数
五、loc()函数
```



# 删





# 查

### 1.获取Pandas列名的几种方法

```bash
data = pd.read_csv('data/Receipt code January minute trading volume.csv')

print([column for column in data])
```

```bash
print(data.columns.values)

# 打印结果
['COUNT' 'SUCC' 'FAIL' 'WAIT PAY' 'SUCCRatio' 'time']
```

2