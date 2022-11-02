## 一、EDA（Exploratory Data Analysis）与数据预处理

**1.1 数据EDA**

  探索性数据分析（Exploratory Data Analysis，简称EDA），是指对已有的数据（原始数据）进行分析探索，通过作图、制表、方程拟合、计算特征量等手段探索数据的结构和规律的一种数据分析方法。一般来说，我们最初接触到数据的时候往往是毫无头绪的，不知道如何下手，这时候探索性数据分析就非常有效。

  对于图像分类任务，我们通常首先应该统计出每个类别的数量，查看训练集的数据分布情况。通过数据分布情况分析赛题，形成解题思路。（洞察数据的本质很重要。）

1、写出一系列你自己做的假设，然后接着做更深入的数据分析。

2、记录自己的数据分析过程，防止出现遗忘。

3、把自己的中间的结果给自己的同行看看，让他们能够给你一些更有拓展性的反馈、或者意见。（即open to everybody）

4、可视化分析结果

## 二、Baseline选择

### 完整流程

第一部分（数据处理）

1. 数据预处理

   数据增强：离线和在线

   离线：在训练模型的时候，每一个epoch都会进行数据增强，重新调用transform.copmpose()的compose操作会让内部的随机性，每一次输出的图像都不一样，因此 变相的认为数据增多了

2. 自定义数据集

3. 定义数据加载器

第二部分（模型训练）

1. 模型组网
2. 模型封装（Model对象是一个具备训练、测试、推理的神经网络。）
3. 模型配置（配置模型所需的部件，比如优化器、损失函数和评价指标。）
4. 模型训练&验证

第三部分（提交结果）

1. 模型预测

2. 生成提交结果（pandas）

   

   ### 常用调参技巧

### mmcls框架基础

#### 训练

```
python tools/train.py  configs/myconfigs/resnet50_for_caltech.py  单gpu

```



#### 推理

```shell
提交result：
python 

可视化结果：
python tools/test.py  configs/myconfigs/resnet50_for_caltech.py  work_dirs/resnet50_for_caltech/epoch_60.pth  --metrics accuracy  --out demo/test.json   --show-dir data/caltech_for_user/test_vis

--out json文件
--show-dir可视化保存路径
```



#### 1.先用mmcls提交答案

#### 了解配置

```
配置文件和检查点命名约定
我们遵循以下约定来命名配置文件。建议贡献者遵循相同的风格。配置文件名分为四部分：算法信息、模块信息、训练信息和数据信息。逻辑上，不同的部分用下划线连接'_'，同一部分的单词用破折号连接'-'。

{algorithm info}_{module info}_{training info}_{data info}.py
algorithm info：算法信息、模型名称和神经网络架构，如resnet等；

module info： 模块信息用于表示一些特殊的颈部、头部和预训练信息；

training info：训练信息，一些训练进度，包括batch size，lr schedule，data augment等；

data info：数据信息、数据集名称、输入大小等，如imagenet、cifar等；
```

如果您想检查配置文件，您可以运行以查看完整的配置。`python tools/misc/print_config.py /PATH/TO/CONFIG`



#### data transformations

就是在pipeline管道里面对数据进行变换，不会增加数据集数量大小

#### batch augmentation



### 训练策略

lr：随着batch*gpu的正比关系



> ### 热身策略
>
> 前期训练容易波动，热身是降低波动的技巧。随着warmup，学习率将从次要值逐渐增加到期望值。
>
> 在MMClassification中，我们`lr_config`用来配置预热策略，主要参数如下：
>
> - `warmup`：预热曲线类型。请从 'constant'、'linear'、'exp' 和 中选择一个`None`，并且`None`表示禁用预热。
> - `warmup_by_epoch`: 是否按 epoch 预热，默认为 True，如果设置为 False，则通过 iter 预热。
> - `warmup_iters`：预热迭代次数，当 时`warmup_by_epoch=True`，单位为epoch；当 时`warmup_by_epoch=False`，单位为迭代次数（iter）。
> - `warmup_ratio`：预热初始学习率将计算为。`lr = lr * warmup_ratio`
>
> ## 自定义动量时间表
>
> 我们支持动量调度器根据学习率修改模型的动量，这可以使模型以更快的方式收敛。
>
> Momentum 调度器通常与 LR 调度器一起使用，例如，使用以下配置来加速收敛。更多细节请参考[CyclicLrUpdater](https://github.com/open-mmlab/mmcv/blob/f48241a65aebfe07db122e9db320c31b685dc674/mmcv/runner/hooks/lr_updater.py#L327) 和[CyclicMomentumUpdater](https://github.com/open-mmlab/mmcv/blob/f48241a65aebfe07db122e9db320c31b685dc674/mmcv/runner/hooks/momentum_updater.py#L130)的实现。



一句话原则： AI performance = data(70%) + model(CNN、RNN、Transformer、Bert、GPT 20%) + trick(loss、[warmup](https://www.zhihu.com/search?q=warmup&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2576569581})、optimizer、attack-training etc 10%) 记住：数据决定了AI的上线，模型和trick只是去逼近这个上线，还是那句老话：garbage in， garbage out。 下面具体分享在NLP领域的一些具体trick：



作者：昆特Alex
链接：https://www.zhihu.com/question/540433389/answer/2576569581
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



### 优化方法

1.数据集分割

目前分割方法是





backbone选择：resnet50，88，swin 88，89

尝试：

1.step=[30,60,90]  lr=0.1，samples_per_gpu=256,frozen_stages=4, 85

2.step=[20,40，60,90]  lr=0.1，samples_per_gpu=256,frozen_stages=2,  88

3.step=[30,60,90]  lr=0.1，samples_per_gpu=64,frozen_stages=2, 88 

4.step=[20,40,60]  lr=0.1，samples_per_gpu=64,frozen_stages=2, 89

5.step=[20,40,60]  lr=0.1，samples_per_gpu=64,frozen_stages=2, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    89.9

 6.step=[20,40,60]  lr=0.1/4，samples_per_gpu=64,frozen_stages=-1, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    88

 7.step=[20,40,60]  lr=0.1/4，samples_per_gpu=64,frozen_stages=1, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]     88

 8.step=[20,40,60]  lr=0.1，samples_per_gpu=128*1,frozen_stages=1, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    89.2

 9.step=[20,40,60]  lr=0.2，samples_per_gpu=64,frozen_stages=2, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    89.7



batch提高，会降低准确率，小batch的的时候。梯度下降是随机的

10.step=[20,40,60]  lr=0.1，samples_per_gpu=32,frozen_stages=2, swin式数据增强，

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    90.5  不稳定

11.lr_config = dict(

​    policy='CosineAnnealing',

​    min_lr=0,

​    by_epoch=False,

​    warmup='linear',

​    warmup_iters=1500,

​    warmup_ratio=0.25) 90.4

12.step=[30,60,90] 90.05



> https://xihe.mindspore.cn/competition/3/0/leaderboard
>
> https://aistudio.baidu.com/aistudio/projectdetail/1551646 飞浆比赛总结
>
> https://blog.csdn.net/cyj972628089/article/details/126321929

如何将top5提升到top1







# ms框架



```
Epoch:[  0/ 80], step:[  100/  251], loss:[1.839/3.199], time:47.745 ms, lr:0.10000
Epoch:[  0/ 80], step:[  200/  251], loss:[1.505/2.377], time:52.330 ms, lr:0.10000
Epoch time: 18681.407 ms, per step time: 74.428 ms, avg loss: 2.167
--------------------
Epoch: [  1 /   1], Train Loss: [1.100], Accuracy:  0.748
Epoch:[  1/ 80], step:[   49/  251], loss:[0.648/0.855], time:47.115 ms, lr:0.10000
Epoch:[  1/ 80], step:[  149/  251], loss:[1.158/0.813], time:47.547 ms, lr:0.10000
Epoch:[  1/ 80], step:[  249/  251], loss:[0.804/0.822], time:47.734 ms, lr:0.10000
Epoch time: 12654.279 ms, per step time: 50.415 ms, avg loss: 0.822
--------------------
Epoch: [  2 /   1], Train Loss: [0.859], Accuracy:  0.789
Epoch:[  2/ 80], step:[   98/  251], loss:[0.560/0.476], time:48.066 ms, lr:0.10000
Epoch:[  2/ 80], step:[  198/  251], loss:[0.501/0.549], time:47.576 ms, lr:0.10000
Epoch time: 12559.779 ms, per step time: 50.039 ms, avg loss: 0.563
--------------------
Epoch: [  3 /   1], Train Loss: [0.994], Accuracy:  0.785
Epoch:[  3/ 80], step:[   47/  251], loss:[0.306/0.365], time:62.698 ms, lr:0.10000
Epoch:[  3/ 80], step:[  147/  251], loss:[0.184/0.353], time:50.215 ms, lr:0.10000
Epoch:[  3/ 80], step:[  247/  251], loss:[0.618/0.376], time:53.250 ms, lr:0.10000
Epoch time: 12664.179 ms, per step time: 50.455 ms, avg loss: 0.376
--------------------
Epoch: [  4 /   1], Train Loss: [0.766], Accuracy:  0.807
Epoch:[  4/ 80], step:[   96/  251], loss:[0.327/0.232], time:48.122 ms, lr:0.10000
Epoch:[  4/ 80], step:[  196/  251], loss:[0.725/0.267], time:47.928 ms, lr:0.10000
Epoch time: 12506.892 ms, per step time: 49.828 ms, avg loss: 0.266
--------------------
Epoch: [  5 /   1], Train Loss: [0.421], Accuracy:  0.818
Epoch:[  5/ 80], step:[   45/  251], loss:[0.196/0.191], time:47.476 ms, lr:0.10000
Epoch:[  5/ 80], step:[  145/  251], loss:[0.248/0.169], time:52.678 ms, lr:0.10000
Epoch:[  5/ 80], step:[  245/  251], loss:[0.216/0.206], time:51.391 ms, lr:0.10000
Epoch time: 12420.039 ms, per step time: 49.482 ms, avg loss: 0.205
--------------------
Epoch: [  6 /   1], Train Loss: [0.172], Accuracy:  0.815
Epoch:[  6/ 80], step:[   94/  251], loss:[0.136/0.143], time:48.135 ms, lr:0.10000
Epoch:[  6/ 80], step:[  194/  251], loss:[0.102/0.157], time:48.406 ms, lr:0.10000
Epoch time: 12514.013 ms, per step time: 49.857 ms, avg loss: 0.166
--------------------
Epoch: [  7 /   1], Train Loss: [0.180], Accuracy:  0.823
Epoch:[  7/ 80], step:[   43/  251], loss:[0.227/0.104], time:56.644 ms, lr:0.10000
Epoch:[  7/ 80], step:[  143/  251], loss:[0.149/0.115], time:47.504 ms, lr:0.10000
Epoch:[  7/ 80], step:[  243/  251], loss:[0.054/0.120], time:47.525 ms, lr:0.10000
Epoch time: 12442.266 ms, per step time: 49.571 ms, avg loss: 0.120
--------------------
Epoch: [  8 /   1], Train Loss: [0.180], Accuracy:  0.820
Epoch:[  8/ 80], step:[   92/  251], loss:[0.064/0.096], time:51.308 ms, lr:0.10000
Epoch:[  8/ 80], step:[  192/  251], loss:[0.085/0.102], time:48.052 ms, lr:0.10000
Epoch time: 12596.127 ms, per step time: 50.184 ms, avg loss: 0.099
--------------------
Epoch: [  9 /   1], Train Loss: [0.021], Accuracy:  0.816
Epoch:[  9/ 80], step:[   41/  251], loss:[0.062/0.065], time:47.976 ms, lr:0.10000
Epoch:[  9/ 80], step:[  141/  251], loss:[0.172/0.068], time:50.360 ms, lr:0.10000
Epoch:[  9/ 80], step:[  241/  251], loss:[0.031/0.068], time:59.603 ms, lr:0.10000
Epoch time: 12557.937 ms, per step time: 50.032 ms, avg loss: 0.068
--------------------
Epoch: [ 10 /   1], Train Loss: [0.073], Accuracy:  0.829
Epoch:[ 10/ 80], step:[   90/  251], loss:[0.009/0.049], time:49.522 ms, lr:0.10000
Epoch:[ 10/ 80], step:[  190/  251], loss:[0.013/0.062], time:56.948 ms, lr:0.10000
Epoch time: 12427.954 ms, per step time: 49.514 ms, avg loss: 0.064
--------------------
Epoch: [ 11 /   1], Train Loss: [0.064], Accuracy:  0.840
Epoch:[ 11/ 80], step:[   39/  251], loss:[0.035/0.073], time:47.650 ms, lr:0.10000
Epoch:[ 11/ 80], step:[  139/  251], loss:[0.013/0.058], time:53.887 ms, lr:0.10000
Epoch:[ 11/ 80], step:[  239/  251], loss:[0.131/0.058], time:58.067 ms, lr:0.10000
Epoch time: 12602.395 ms, per step time: 50.209 ms, avg loss: 0.058
--------------------
Epoch: [ 12 /   1], Train Loss: [0.069], Accuracy:  0.839
Epoch:[ 12/ 80], step:[   88/  251], loss:[0.067/0.041], time:48.134 ms, lr:0.10000
Epoch:[ 12/ 80], step:[  188/  251], loss:[0.008/0.042], time:47.991 ms, lr:0.10000
Epoch time: 12598.711 ms, per step time: 50.194 ms, avg loss: 0.043
--------------------
Epoch: [ 13 /   1], Train Loss: [0.086], Accuracy:  0.836
Epoch:[ 13/ 80], step:[   37/  251], loss:[0.016/0.029], time:47.748 ms, lr:0.10000
Epoch:[ 13/ 80], step:[  137/  251], loss:[0.056/0.032], time:53.158 ms, lr:0.10000
Epoch:[ 13/ 80], step:[  237/  251], loss:[0.053/0.031], time:47.523 ms, lr:0.10000
Epoch time: 12485.930 ms, per step time: 49.745 ms, avg loss: 0.031
--------------------
Epoch: [ 14 /   1], Train Loss: [0.021], Accuracy:  0.840
Epoch:[ 14/ 80], step:[   86/  251], loss:[0.010/0.029], time:50.105 ms, lr:0.10000
Epoch:[ 14/ 80], step:[  186/  251], loss:[0.019/0.024], time:48.315 ms, lr:0.10000
Epoch time: 12452.528 ms, per step time: 49.612 ms, avg loss: 0.024
--------------------
Epoch: [ 15 /   1], Train Loss: [0.013], Accuracy:  0.846
Epoch:[ 15/ 80], step:[   35/  251], loss:[0.049/0.023], time:47.580 ms, lr:0.10000
Epoch:[ 15/ 80], step:[  135/  251], loss:[0.033/0.020], time:53.511 ms, lr:0.10000
Epoch:[ 15/ 80], step:[  235/  251], loss:[0.033/0.025], time:48.160 ms, lr:0.10000
Epoch time: 12512.023 ms, per step time: 49.849 ms, avg loss: 0.025
--------------------
Epoch: [ 16 /   1], Train Loss: [0.025], Accuracy:  0.842
Epoch:[ 16/ 80], step:[   84/  251], loss:[0.032/0.016], time:54.054 ms, lr:0.10000
Epoch:[ 16/ 80], step:[  184/  251], loss:[0.029/0.020], time:47.961 ms, lr:0.10000
Epoch time: 12522.570 ms, per step time: 49.891 ms, avg loss: 0.022
--------------------
Epoch: [ 17 /   1], Train Loss: [0.007], Accuracy:  0.840
Epoch:[ 17/ 80], step:[   33/  251], loss:[0.024/0.019], time:48.929 ms, lr:0.10000
Epoch:[ 17/ 80], step:[  133/  251], loss:[0.006/0.021], time:48.425 ms, lr:0.10000
Epoch:[ 17/ 80], step:[  233/  251], loss:[0.018/0.019], time:48.352 ms, lr:0.10000
Epoch time: 12552.577 ms, per step time: 50.010 ms, avg loss: 0.020
--------------------
Epoch: [ 18 /   1], Train Loss: [0.033], Accuracy:  0.843
Epoch:[ 18/ 80], step:[   82/  251], loss:[0.011/0.021], time:48.066 ms, lr:0.10000
Epoch:[ 18/ 80], step:[  182/  251], loss:[0.009/0.018], time:50.955 ms, lr:0.10000
Epoch time: 12556.601 ms, per step time: 50.026 ms, avg loss: 0.019
--------------------
Epoch: [ 19 /   1], Train Loss: [0.051], Accuracy:  0.843
Epoch:[ 19/ 80], step:[   31/  251], loss:[0.013/0.019], time:47.613 ms, lr:0.10000
Epoch:[ 19/ 80], step:[  131/  251], loss:[0.012/0.019], time:49.140 ms, lr:0.10000
Epoch:[ 19/ 80], step:[  231/  251], loss:[0.028/0.021], time:47.711 ms, lr:0.10000
Epoch time: 12495.927 ms, per step time: 49.785 ms, avg loss: 0.021
--------------------
Epoch: [ 20 /   1], Train Loss: [0.003], Accuracy:  0.842
Epoch:[ 20/ 80], step:[   80/  251], loss:[0.005/0.014], time:51.739 ms, lr:0.10000
Epoch:[ 20/ 80], step:[  180/  251], loss:[0.002/0.014], time:50.198 ms, lr:0.10000
Epoch time: 12614.246 ms, per step time: 50.256 ms, avg loss: 0.014
--------------------
Epoch: [ 21 /   1], Train Loss: [0.028], Accuracy:  0.848
Epoch:[ 21/ 80], step:[   29/  251], loss:[0.006/0.010], time:50.572 ms, lr:0.10000
Epoch:[ 21/ 80], step:[  129/  251], loss:[0.009/0.010], time:47.507 ms, lr:0.10000
Epoch:[ 21/ 80], step:[  229/  251], loss:[0.007/0.013], time:53.189 ms, lr:0.10000
Epoch time: 12482.447 ms, per step time: 49.731 ms, avg loss: 0.013
--------------------
Epoch: [ 22 /   1], Train Loss: [0.006], Accuracy:  0.847
Epoch:[ 22/ 80], step:[   78/  251], loss:[0.006/0.015], time:48.225 ms, lr:0.10000
Epoch:[ 22/ 80], step:[  178/  251], loss:[0.002/0.013], time:50.999 ms, lr:0.10000
Epoch time: 12428.742 ms, per step time: 49.517 ms, avg loss: 0.014
--------------------
Epoch: [ 23 /   1], Train Loss: [0.003], Accuracy:  0.845
Epoch:[ 23/ 80], step:[   27/  251], loss:[0.053/0.016], time:52.324 ms, lr:0.10000
Epoch:[ 23/ 80], step:[  127/  251], loss:[0.012/0.013], time:53.169 ms, lr:0.10000
Epoch:[ 23/ 80], step:[  227/  251], loss:[0.061/0.015], time:48.443 ms, lr:0.10000
Epoch time: 12600.694 ms, per step time: 50.202 ms, avg loss: 0.014
--------------------
Epoch: [ 24 /   1], Train Loss: [0.013], Accuracy:  0.847
Epoch:[ 24/ 80], step:[   76/  251], loss:[0.009/0.015], time:47.596 ms, lr:0.10000
Epoch:[ 24/ 80], step:[  176/  251], loss:[0.005/0.012], time:47.874 ms, lr:0.10000
Epoch time: 12536.427 ms, per step time: 49.946 ms, avg loss: 0.011
--------------------
Epoch: [ 25 /   1], Train Loss: [0.006], Accuracy:  0.846
Epoch:[ 25/ 80], step:[   25/  251], loss:[0.010/0.009], time:49.236 ms, lr:0.10000
Epoch:[ 25/ 80], step:[  125/  251], loss:[0.014/0.009], time:59.762 ms, lr:0.10000
```

```

```

