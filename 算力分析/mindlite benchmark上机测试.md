### 在上的手机上运行mindsporelite的benchmark

### 环境

上位机：

ubuntu18.04

下位机：

1.红米

2.芯片：



### 准备工作

#### 1.代码上传

​	

```
adp push mindspore-lite
```

#### 2.模型转换以及上传

通过pytorch转化为onnx，然后再转为mindsporelite使用的ms文件

代码见D:\mindsporecode\torchtoonnx.py



#### 3.配置环境&&运行benchmark