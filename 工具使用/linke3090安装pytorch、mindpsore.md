# 1.环境

ubuntu20.04

nvidia-smi

![image-20220915164909542](linke3090安装pytorch、mindpsore.assets\image-20220915164909542.png)

nvcc-V



![image-20220915164921782](linke3090安装pytorch、mindpsore.assets\image-20220915164921782.png)

## 2.pytorch安装

```
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```

### 3.检查

```
import torch
print(torch.cuda.is_available())
#cuda是否可用；
print(torch.__version__)
# 返回 torch 版本
print(torch.backends.cudnn.version())
# 返回 cudnn 版本
print(torch.version.cuda)
# 返回 cuda 版本
print(torch.cuda.device_count())
# 返回 gpu 数量；
print(torch.cuda.get_device_name(0))
# 返回 gpu 名字，设备索引默认从0开始；
print(torch.cuda.current_device())
# 返回当前设备索引
print(torch.rand(3,3).cuda())

import torch
import torchvision.models as models
device1 = torch.device("cuda:0")
data = torch.randn(1, 3, 224, 224)
data = data.to(device1)
model = models.vgg16()
model=model.to(device1)
res = model(data)
print(res)
```

### 4.mindspore安装

#### 手动安装

|                           软件名称                           |         版本          |                             作用                             |
| :----------------------------------------------------------: | :-------------------: | :----------------------------------------------------------: |
|                            Ubuntu                            |         18.04         |                   运行MindSpore的操作系统                    |
|      [CUDA](https://www.mindspore.cn/install#安装cuda)       |      10.1或11.1       |               MindSpore GPU使用的并行计算架构                |
|     [cuDNN](https://www.mindspore.cn/install#安装cudnn)      |     7.6.x或8.0.x      |            MindSpore GPU使用的深度神经网络加速库             |
|     [Conda](https://www.mindspore.cn/install#安装conda)      | Anaconda3或Miniconda3 |                      Python环境管理工具                      |
|     [GCC](https://www.mindspore.cn/install#安装gcc和gmp)     |   7.3.0到9.4.0之间    |                 用于编译MindSpore的C++编译器                 |
|     [gmp](https://www.mindspore.cn/install#安装gcc和gmp)     |         6.1.2         |                 MindSpore使用的多精度算术库                  |
| [Open MPI](https://www.mindspore.cn/install#安装open-mpi-可选) |         4.0.3         | MindSpore使用的高性能消息传递库（可选，单机多卡/多机多卡训练需要） |
| [TensorRT](https://www.mindspore.cn/install#安装tensorrt-可选) |         7.2.2         | MindSpore使用的高性能深度学习推理SDK（可选，Serving推理需要） |

这里由于一些原因用docker安装。

---

# openmmlab系列安装

### \安装11.0.cuda

安装地址https://developer.nvidia.com/cuda-11.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=2004&target_type=runfilelocal

![image-20220918195517185](D:\alphawork\工具使用\linke3090安装pytorch、mindpsore.assets\image-20220918195517185.png)

```
wget http://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux.run
sudo sh cuda_11.0.2_450.51.05_linux.ru
```



### 1.安装mmcls

0.先安装mmv

```
pip install mmcv-full=={mmcv_version} -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.10.0/index.html
```

1.源码编译mmcls

```
git clone https://ghproxy.com/https://github.com/open-mmlab/mmclassification.git  ##使用代理安装
pip install -v -e .
```

2.测试





### 参考文献

https://zhuanlan.zhihu.com/p/336429888