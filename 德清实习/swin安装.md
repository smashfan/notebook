### Swin Transformer安装记录

> ubuntu--20.10
>
> GPU--3080
>
> cuda--11.0
>
> torch--1.7.0
>
> mmcv--1.3.8
>
> mmdetection--2.11.0

cuda的安装就不放了，自己百度一下教程，这里就从pytorch安装开始。

所有的git的项目，都可以用 [GitHub Proxy 代理加速 (ghproxy.com)](https://ghproxy.com/) 转链，尤其是swin transformer的权重文件，又大下载的又慢，转完链后就飞快了。



### 1. 创建环境

```powershell
conda create -n swin python=3.7
conda activate swin
```

```
conda install pytorch==1.8.1 torchvision==0.9.1 torchaudio==0.8.1 cudatoolkit=11.3 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/

注意：这里是pytorch 的 linux的源
- https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
```

### 2. 安装pytorch(利用国内源)

[open-mmlab/mmcv: OpenMMLab Computer Vision Foundation (github.com)](https://github.com/open-mmlab/mmcv)

在上边的网址中看好要装那个pytorch版本，例如我是cuda11.0，就只支持pytorch1.7，所以我就去安装pytorch1.7。只需要去下边网址找到对应的把下边-c前边给替换掉就行了。

pytorch所有版本安装网址：[Previous PyTorch Versions | PyTorch](https://pytorch.org/get-started/previous-versions/)

```powershell
conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=11.0 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/
```

校验是否安装成功：

```python
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
device1 = torch.device("cuda:1")
data = torch.randn(1, 3, 224, 224)
data = data.to(device1)
model = models.vgg16()
model=model.to(device1)
res = model(data)
print(res)
```



### 3. 安装其他依赖包

用源非常快

```powershell
pip install cython matplotlib opencv-python termcolor==1.1.0 yacs==0.1.8 -i  https://pypi.mirrors.ustc.edu.cn/simple
```



### 4. 安装mmcv和Swin-Transformer-Object-Detection

mmcv要安装指定版本，不要装最新版！！！【2022/4/13记载】

```powershell
# 安装mmcv
pip install mmcv-full==1.3.8 -f https://download.openmmlab.com/mmcv/dist/cu110/torch1.7.0/index.html

# 安装SwinTransformer
git clone https://github.com/SwinTransformer/Swin-Transformer-Object-Detection.git
pip install -r requirements/build.txt
python setup.py develop
```



### 5. 安装apex

下载地址：https://github.com/NVIDIA/apex

```powershell
git clone https://github.com/NVIDIA/apex.git
cd apex
# pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./			# 我用这个安装报错，不过网上大部分是这个
python setup.py develop		# 用这个安装就可以
```

提醒Successfully installed apex-0.1就是安装成功了。



检验是否安装成功：导入不报错就成功

```
from apex import amp
```



### 6. 下载权重：

将要下载的权重链接复制到 [GitHub Proxy 代理加速 (ghproxy.com)](https://ghproxy.com/) 中，利用新网址加速下载。

权重下载网址：https://github.com/SwinTransformer/Swin-Transformer-Object-Detection

所用demo权重：https://github.com/SwinTransformer/storage/releases/download/v1.0.2/mask_rcnn_swin_tiny_patch4_window7.pth



在Swin-Transformer-Object-Detection/目录下新建一个checkpoints，将权重文件下载到里边。

```powershell
mkdir checkpoints
cd checkpoints
wget https://github.com/SwinTransformer/storage/releases/download/v1.0.2/mask_rcnn_swin_tiny_patch4_window7.pth
```





### 7. 运行demo

回到Swin-Transformer-Object-Detection/目录下

```powershell
python demo/image_demo.py demo/demo.jpg configs/swin/cascade_mask_rcnn_swin_base_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco.py checkpoints/mask_rcnn_swin_tiny_patch4_window7.pth
```



### 8. 训练

```powershell
python tools/train.py configs/swin/mask_rcnn_swin_tiny_patch4_window7_mstrain_480-800_adamw_3x_coco.py  --cfg-options model.pretrained=mask_rcnn_swin_tiny_patch4_window7.pth
1
```
