## 1.安装略

## 2.以caltech_for_user数据集为例子

### 训练

0.制作数据集格式：

```
mmclassification
└── data
    └── my_dataset
        ├── meta
        │   ├── train.txt
        │   ├── val.txt
        │   └── test.txt
        ├── train
        ├── val
        └── test
```

tip：图像文件放一起，重点是anni文件区别训练集和测试集

1.定义数据集类

```python
import mmcv
import numpy as np

from .builder import DATASETS
from .base_dataset import BaseDataset


@DATASETS.register_module()
class MyDataset(BaseDataset):
    CLASSES=[str(i) for i in range(1,257)]
    def load_annotations(self):
        assert isinstance(self.ann_file, str)
        data_infos = []
        with open(self.ann_file) as f:
            samples = [x.strip().split(' ') for x in f.readlines()]
            for filename, gt_label in samples:
                info = {'img_prefix': self.data_prefix}
                info['img_info'] = {'filename': filename}
                info['gt_label'] = np.array(gt_label, dtype=np.int64)
                data_infos.append(info)
            return data_infos

```

tips：直接复制官网

2.数据集注册

```
from .base_dataset import BaseDataset
...
from .filelist import Filelist

__all__ = [
    'BaseDataset', ... ,'Filelist'
]
```

tip：

```
加入到__init__下面
```

2.配置文件

配置文件需要分为

```
_base_ = [
    '../_base_/models/resnet50.py',           # model
    '../_base_/datasets/imagenet_bs32.py',    # data
    '../_base_/schedules/imagenet_bs256.py',  # training schedule
    '../_base_/default_runtime.py'            # runtime setting
]
```

四种，这里需要注意模型文件和数据文件

其中模型主要修改num__class,数据文件需要修改path

```python
# dataset settings
dataset_type = 'MyDataset'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)  # coco数据训练时原始的预处理方式
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', size=224),  # 随机缩放裁剪
    dict(type='RandomFlip', flip_prob=0.5, direction='horizontal'),  # 随机翻转
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='ToTensor', keys=['gt_label']),
    dict(type='Collect', keys=['img', 'gt_label'])  # 图像和标签的集合
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', size=(256, -1)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='ImageToTensor', keys=['img']),
    dict(type='Collect', keys=['img'])
]
 
data_root = 'data/caltech_for_user'  # 你的数据集根目录
data = dict(
    samples_per_gpu=32,  # dataloader.batch_size == self.samples_per_gpu  # 每批次样本数量
    workers_per_gpu=2,  # dataloader.num_workers == self.workers_per_gpu  # 1的话表示只有一个进程加载数据
    train=dict(
        type=dataset_type,
        data_prefix=data_root + '/train',
        ann_file=data_root + '/train.txt',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_prefix=data_root + '/train',
        ann_file=data_root + '/val.txt',
        pipeline=test_pipeline),
    test=dict(
        # replace `data/val` with `data/test` for standard test
        type=dataset_type,
        data_prefix=data_root + '/train',
        ann_file=data_root + '/val.txt',
        pipeline=test_pipeline))
evaluation = dict(interval=1, metric='accuracy')  # 分类，用accuracy

# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(  # backbone: RES-NET
        type='ResNet',
        depth=50,  # resnet18
        num_stages=4,  # resnet18 --- block-depth分别是(2,2,2,2)
        out_indices=(3, ),  # 取第三阶段，也就是最后一阶段的输出，resnet最后输出特征纬度是512
        style='pytorch',
        # torchvision默认预训练模型，这里默认下载放到/home/yons/.cache/torch/hub/checkpoints
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet50'),
        # 预训练模型也可以用官方应用imagenet训练好的
        # https://github.com/open-mmlab/mmclassification/blob/dev/docs/en/model_zoo.md 可下载checkpoint和查看更多，这里下载对应 resnet18_8xb32_in1k.py 的预训练设置
        # init_cfg=dict(
        #     type='Pretrained',
        #     checkpoint='/xxx/checkpoints/'resnet18_batch256_imagenet_20200708-34ab8f90.pth',  
        #     prefix='backbone',
        # ),
        frozen_stages=-1,  # 加入预训练模型时候，冻结前两层（实验证明，冻结部分权重，效果更好）
        
    ),
    neck=dict(type='GlobalAveragePooling'),  # neck：平均池化
    head=dict(
        type='LinearClsHead',
        num_classes=256,  # 二分类（因为是猫狗数据集了，不是imagenet）
        in_channels=2048,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),  # 分类，交叉熵
        topk=(1, 5),
        # topk=(1, 2)  # so you would have to check output.shape and make sure dim1 is larger or equal to maxk.
    )
)

# optimizer
optimizer = dict(type='SGD', lr=0.1/4, momentum=0.9, weight_decay=0.0001)  # momentum：学习率动量 weight_decay:权重惩罚，正则化
optimizer_config = dict(grad_clip=None)  # 设置梯度截断（裁剪）阈值，防止梯度无限大爆炸
# learning policy
lr_config = dict(policy='step', step=[30, 60, 90])  # 100次迭代，每隔设定的这几次，lr就降低0.1倍
runner = dict(type='EpochBasedRunner', max_epochs=100)

# checkpoint saving
checkpoint_config = dict(interval=20)  # 多少次迭代保存一次模型
# yapf:disable
log_config = dict(
    # interval=100,
    interval=40,  # 多少批次 打印一次
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
 
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]

```

shell

```
python tools/train.py  configs/myconfigs/resnet50_for_caltech.py
```



### 推理

推理demo：

```python
# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser

import mmcv
import cv2
from mmcls.apis import inference_model, init_model, show_result_pyplot


def main():
    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--show',
        action='store_true',
        help='Whether to show the predict results by matplotlib.')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    args = parser.parse_args()

    # build the model from a config file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)
    # test a single image
    result = inference_model(model, args.img)
    # show the results
    print(mmcv.dump(result, file_format='json', indent=4))
    print(result)
    model.show_result(args.img,result,show=False,out_file="demo/test.jpg")

if __name__ == '__main__':
    main()

```

```
python demo/image_demo.py ${IMAGE_FILE} ${CONFIG_FILE} ${CHECKPOINT_FILE}

# Example
python demo/image_demo.py demo/demo.JPEG configs/resnet/resnet50_8xb32_in1k.py \
  https://download.openmmlab.com/mmclassification/v0/resnet/resnet50_8xb32_in1k_20210831-ea4938fc.pth
```

集成测试：（测试测试集的图片，并且可视化，以及metrics）

```shell
python tools/test.py  configs/myconfigs/resnet50_for_caltech.py  work_dirs/resnet50_for_caltech/epoch_60.pth  --metrics accuracy  --out demo/test.json   --show-dir data/caltech_for_user/test_vis

--out json文件
--show-dir可视化保存路径
```

https://blog.csdn.net/hzy459176895/article/details/123405552?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-123405552-blog-115312600.t5_refersearch_landing&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-123405552-blog-115312600.t5_refersearch_landing&utm_relevant_index=1

结果为74.



swin_transformer的使用

https://blog.csdn.net/yuzh_/article/details/120842087