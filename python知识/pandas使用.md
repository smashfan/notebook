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

1.loc

```
data=pd.DataFrame(columns=["x","y"])
data.loc[i]=[,,,,]
```

2.append

```
    import pandas as pd
    
    data = pd.DataFrame()
    a = {"x":1,"y":2}
    data = data.append(a,ignore_index=True)
    print(data)

```

3，concat

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
     
 axis=0:纵向拼接
 axis=1:横向拼接
```

### 增加新列



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

# 修改

pandas修改指定行

dataframe.loc[index]=[index,channel_out,kernel_size]