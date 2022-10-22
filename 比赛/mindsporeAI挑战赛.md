### 训练

```
python tools/train.py  configs/myconfigs/resnet50_for_caltech.py  单gpu

```













1.先用mmcls提交答案

了解配置

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





backbone选择：resnet50，88，swin 88，89

尝试：

1.step=[30,60,90]  lr=0.1，samples_per_gpu=256,frozen_stages=4, 85

2.step=[20,40，60,90]  lr=0.1，samples_per_gpu=256,frozen_stages=2,  88

3.step=[30,60,90]  lr=0.1，samples_per_gpu=64,frozen_stages=2, 88 

4.step=[20,40,60]  lr=0.1，samples_per_gpu=64,frozen_stages=2, 89