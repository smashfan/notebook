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

policies=[AutoContrast,Equalize,Invert,Rotate，Posterize，Solarize，SolarizeAdd，ColorTransform，Contrast，Brightness，Sharpness，Shear，Translate]    90.5

11.lr_config = dict(

​    policy='CosineAnnealing',

​    min_lr=0,

​    by_epoch=False,

​    warmup='linear',

​    warmup_iters=1500,

​    warmup_ratio=0.25) 90.1