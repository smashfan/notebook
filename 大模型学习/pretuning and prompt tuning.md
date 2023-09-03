#### **Pre-trainedFine-tuning**的问题：

在大多数的下游任务微调时， **下游任务的目标与预训练的目标差距过大** 导致提升效果不明显， **微调过程中依赖大量的监督语料** 等。

#### Prompt-Tuning的动机旨在解决目前传统Fine-tuning的两个痛点问题：

**降低语义差异（Bridge the gap between Pre-training and Fine-tuning）** ：预训练任务主要以Masked Language Modeling（MLM）为主，而下游任务则重新引入新的训练参数，因此两个阶段的目标通常有较大差异。因此需要解决如何缩小Pre-training和Fine-tuning两个阶段目标差距过大的问题；

 **避免过拟合（Overfitting of the head）** ：由于在Fine-tuning阶段需要新引入额外的参数以适配相应的任务需要，因此在样本数量有限的情况容易发生过拟合，降低了模型的泛化能力。因此需要面对预训练语言模型的过拟合问题。



作者：kaiyuan
链接：https://zhuanlan.zhihu.com/p/618871247
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。