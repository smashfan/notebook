首先，要解决的问题不同：

TVM和XLA要解决的是如何通过编译的方法分离前端表意与后端多硬件的问题（），这个问题本身曾经在编程语言领域也遇到过，所以借鉴过来。

MNN之流是为了解决常见的深度学习模型高效的跑在手机端的问题。

其次，MNN之类的核心不仅仅是适配多硬件，还有比如：减少最终部署时候的size。控制功耗等手机端的问题。而性能不是唯一最重要的问题了。

所以，你看这些都不是冲着性能去的。

之所以大家都在谈性能是因为性能是唯一可以在**固定模型，固定硬件下，且有一定门槛的可量化比较的指标**了。



作者：大王叫我来巡山
链接：https://www.zhihu.com/question/408026676/answer/1378214457
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。