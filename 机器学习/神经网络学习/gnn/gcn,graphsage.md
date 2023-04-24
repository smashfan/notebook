https://www.zhihu.com/search?type=content&q=gcn%E5%92%8Cgraph%20sage

## GCN原理

假设我们手头上有一批图数据，其中有N个节点，每个节点都有自己的特征，这些特征组成了一个N×D的矩阵X。节点间的关系也会组成一个N×N的邻接矩阵A。特征矩阵X及节点关系矩阵A将一起输入至GCN[[1\]](#ref_1)。

GCN层与层之间的连接方式如下，其中H是每一层的特征，W是每一层需学习的权重矩阵，σ是非线性激活函数。

![img](gcn,graphsage.assets/v2-770ea7b998cde68f3e04ac67cb2838fe_b.png)

稍等一下，这个公式是不是看着有点眼熟，如果把 D~−1/2A~D~−1/2\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}扔掉不管，那不就是传统意义上的DNN吗？所以说GCN实质是针对图结构，对传统DNN的改进而已。现在我们把目光聚焦在“改进点” D~−1/2A~D~−1/2\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}上 ，看看GCN到底对传统的DNN做了哪些骚操作。

作者：阿亮
链接：https://zhuanlan.zhihu.com/p/199251885
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。





gcn和graphsagehttps://zhuanlan.zhihu.com/p/74242097