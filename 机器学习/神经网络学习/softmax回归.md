### softmax(指数归一化函数)

通常在多分类的场景，计算方式如下
$$
\sigma(\mathbf{z})_j=\frac{e^{z_j}}{\sum_{k=1}^K e^{z_k}} \quad \text { for } j=1, \ldots, K
$$

# 为什么深度网络（vgg，resnet）最后都不使用softmax（概率归一）函数，而是直接加fc层？

随着深度学习框架的发展，为了更好的性能，部分框架选择了在使用交叉熵损失函数时默认加上softmax，这样无论你的输出层是什么，只要用了nn.CrossEntropyLoss就默认加上了softmax