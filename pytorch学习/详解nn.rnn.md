RNN()里面的参数有：

1. input_size 表示 $xtx_{t}x_{t}$ 的特征维度；
2. hidden_size 表示输出 $hth_{t}h_{t}$ 的特征维度；
3. num_layers 表示网络的层数，默认是1层；
4. nonlinearity 表示[非线性激活函数](https://www.zhihu.com/search?q=非线性激活函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A"80866196"})的选择，默认是tanh，也可以选择 relu；
5. bias 表示是否使用偏置，默认是True；
6. batch_first 这个参数是决定网络的输入维度顺序，默认网络输入是按照(seq, batch, feature) 输入的，也就是序列长度放在最前面，然后是批量，最后是特征维度，如果这个参数设置为True，那么顺序就变为 (batch, seq, feature)；
7. dropout 这个参数接受一个 0-1 的数值，会在网络中除最后一层之外的其他输出层加上 dropout层；
8. bidirectional 默认是False，如果设置为 True，就是双向循环神经网络的结构；

接着再介绍网络接受的输入和输出。网络会接收一个序列输入 xt 和记忆输入 ，h0，xt 的维度是 (seq, batch, feature)，分别表示序列长度、批量和输入的特征维度，h_{0}也叫隐藏状态，它的维度是 (layers∗direction,batch,hidden) ，分别表示层数乘方向（如果单向就是1，双向就是2）、批量和输出的维度。网络会输出 和，output和hn，output 表示网络实际的输出，维度是 (seq,batch,hidden∗direction) ，分别表示序列长度、批量和输出维度上方向， hn 表示记忆单元，维度是 (layer∗direction,batch,hidden) ，分别表示层数乘方向、批量和输出维度。



这里有几个地方要注意一下：

- 第一个要注意的地方就是网络的输入和前面讲过的卷积神经网络不同，因为卷积神经网络的输入是将batch放在前面，而在**循环神经网络中将batch放在中间**，当然可以使用batch_first=True 让batch放在前面；
- 第二个要注意的地方就是网络的输出是 (seq,batch,hidden∗direction) ，这里的 direction=1或者2前面也说过，如果是双向的网络结构，相当于网络从左往右计算一次，再从右往左计算一次，这样就会有两个结果，将两个结果按最后一维拼接起来，就是上面的结果；
- **第三个要注意的地方就是隐藏状态的网络大小、输入和输出都是 (layer∗direction,batch,hidden)** ，因为如果网络有多层，那么每一层都有一个新的记忆单元，而双向网络结构在每一层左右都会有两个不同的记忆单元，所以维度的第一维为 layer*direction；



### demo

```python
import pandas as pd
import pickle
import os
import torch 
from torch import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
class myrnn(nn.Module):
    """Some Information about MyModule"""
    def __init__(self):
        super().__init__()
        self.rnn1=torch.nn.RNN(10, 20, 1)
    def forward(self,x,h0):
        x,hn=self.rnn1(x, h0)
        return x ,hn

rnn = myrnn()
input = torch.randn(5, 1, 10)
h0 = torch.randn(1, 1, 20)
output, hn = rnn(input,h0)
print(output.shape)
print(hn.shape)
```



### 参考文献



作者：月臻
链接：https://zhuanlan.zhihu.com/p/80866196
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

https://pytorch.org/docs/stable/generated/torch.nn.RNN.html#torch.nn.RNN