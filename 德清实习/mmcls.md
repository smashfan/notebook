### 一、路径

服务器：65

> /data/fanjunquan/mmclassification/

### 二、数据集

> /data/fanjunquan/mmclassification/data/datasets_3class/   imgenet格式

### 三、运行结果

> /data/fanjunquan/mmclassification/re/classroom/  已经可视化了

### 四、测试方法

- ##### 单张图片 

  环境：conda activate mmaction2

  工作目录：/data/fanjunquan/mmclassification/

  脚本：

```
python demo/image_demo.py  demo/use_phone_110.png  configs/resnet/classroom_resnet.py  work_dirs/classroom/epoch_300.pth

demo/use_phone_110.png ：换成自己的图片
demo/result.py :是结果图
```

- ##### 大量测试

  先把数据集做成 imgenet格式  然后运行相应脚本   之后再说