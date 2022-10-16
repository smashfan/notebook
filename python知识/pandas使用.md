### 1.读取cvs

pd.read_csv

tip：注意用逗号区别的时候不要有空格

### 2.获取Pandas列名的几种方法

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