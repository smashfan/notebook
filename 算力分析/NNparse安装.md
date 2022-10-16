### NN parse安装记录

> window 10
>
> GPU- 1050
>
> cuda-10.1
>
> pytorch =1.8.0

### 1. 创建环境



```
conda create -n nnparse python=3.7
conda activate nnparse

conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.2 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/    
//出现错误，无法import torch 原因 镜像的win和linux问题 

conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.2 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/win-64/    
//ok   ，但是无法用cuda。系统cuda版本低

conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=10.1  -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/win-64/ 

//完全正确，cuda匹配
nividia-smi path：C:\Program Files\NVIDIA Corporation\NVSMI
```

### PIP清华源

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

### 2.删除环境

```
conda remove -n your_env_name(虚拟环境名称) --all  
```

