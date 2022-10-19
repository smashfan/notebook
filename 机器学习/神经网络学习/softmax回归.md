### softmax(指数归一化函数)

通常在多分类的场景，计算方式如下
$$
\sigma(\mathbf{z})_j=\frac{e^{z_j}}{\sum_{k=1}^K e^{z_k}} \quad \text { for } j=1, \ldots, K
$$