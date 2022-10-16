# 简介

Pascal Voc 格式是目标检测常用的格式。[Pascal Voc 数据集官网](https://links.jianshu.com/go?to=http%3A%2F%2Fhost.robots.ox.ac.uk%2Fpascal%2FVOC%2F)

ASCAL VOC数据集由5个部分构成：JPEGImages，Annotations，ImageSets，SegmentationClass以及SegmentationObject。

- **JPEGImages**：存放的是训练与测试的所有图片。
- **Annotations**：里面存放的是每张图片打完标签所对应的XML文件
- **ImageSets**：ImageSets文件夹下本次讨论的只有Main文件夹，此文件夹中存放的主要又有四个文本文件**test.txt**,**train.txt**,**trainval.txt**,**val.txt**,其中分别存放的是**测试集**图片的文件名、**训练集**图片的文件名、**训练验证集**图片的文件名、**验证集**图片的文件名。
- **SegmentationClass与SegmentationObject**：存放的都是图片，且都是图像分割结果图，对目标检测任务来说没有用。**class segmentation** 标注出每一个像素的类别 。**object segmentation** 标注出每一个像素属于哪一个物体



作者：21b162136419
链接：https://www.jianshu.com/p/8b43094d5ed4
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。