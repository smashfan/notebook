# 创建

```python
data = {'name': ['John', 'Mike', 'Mozla', 'Rose', 'David', 'Marry', 'Wansi', 'Sidy', 'Jack', 'Alic'],
        'age': [20, 32, 29, np.nan, 15, 28, 21, 30, 37, 25],
        'gender': [0, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        'isMarried': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}
```



# 读取和保存

### 1.读取cvs

pd.read_csv

tip：注意用逗号区别的时候不要有空格

**读取的时候去除多的索引**

dataframe=pd.read_csv("dataset.csv",index_col=0)

注意，这个容易把index的title变没

保存的时候不保存索引

dataframe.to_csv("dataset.csv"，index=None)

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

​	一,基本语法

```
pd.concat(
     objs,      
     axis=0,     
     join='outer',
     ignore_index=False,
     keys=None,      
     levels=None,     
     names=None,      
     verify_integrity=False,     
     copy=True)
     
 axis=0:纵向拼接 注意index
 axis=1:横向拼接  会出现空值none
```

### 增加新列

```
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

### 两个表相同的行合并成一个表

```

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

### 2取值

```python
pandas.DataFrame.at
根据行索引和列表取出一个值
df.at[4,"B"]
或者 df.iloc[5].at['B']
或者
df.loc['cobra', 'shield']
df.loc[name='cobra',"shild"] 必须要行号和列才能取得唯一的值

所以需要data1.loc[data1.name==name,"out"].index.tolist()[0]
```



# 修改

pandas修改指定行

dataframe.loc[index]=[index,channel_out,kernel_size]