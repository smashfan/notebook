# 增

os.mkdir: 创建一级目录

os.makedirs

# 删

- os.remove()删除文件

# 查

### 查路径下的文件

1.os.listdir()

排序：path_list.sort(key=lambda x:int(x[:-4]))

### 读写txt

```python
with open('D:\\test.txt','a',encoding='utf-8') as f:
  text = '\n奔涌吧，后浪'
  f.write(text)
 
f=open("fle","w")
#循环读取每一行
l=f.readlines()
```

### 
