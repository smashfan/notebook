简单来说，**现在Deep Learning有这么多不同前端（framework），有这么多不同的后端（hardware），是否能找到一个桥梁更有效实现他们之间的优化和影射呢？**



![img](https://pic3.zhimg.com/80/v2-8f27732e5d4dce0de5be46751bfc3d26_720w.webp)

和编程语言一样

![img](https://pic3.zhimg.com/80/v2-64db6352bd23eb839ea4517ff70f2ba2_720w.webp)



换句话说，这也正是重演了LLVM出现时的场景：**大量不同的编程语言和越来越多的硬件架构之间需要一个桥梁**。LLVM的出现，让不同的前端后端使用统一的 LLVM IR ,如果需要支持新的编程语言或者新的设备平台，只需要开发对应的前端和后端即可。同时基于 LLVM IR 我们可以很快的开发自己的编程语言。比如，LLVM创建者Chris Lattner后来加入了Apple，又创建了Swift语言，可以看作是LLVM的前端。

![img](https://pic1.zhimg.com/80/v2-6b41d46810a892e4cb966c249d7c449c_720w.webp)

**当然，IR本质上是一种中间表示形式，是一个完整编译工具的一部分。而我们下面讨论的TVM，XLA都是围绕特定IR构建的优化和编译工具。**

参考“：

https://zhuanlan.zhihu.com/p/29254171