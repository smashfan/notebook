# CoDL: Efficient CPU-GPU Co-execution for Deep Learning Inference on Mobile Devices

## ABSTRACT 

> Concurrent inference execution on heterogeneous processors is critical to improve the performance of increasingly heavy deep learning (DL) models. However, available inference frameworks can only use one processor at a time, or hardly achieve speedup by concurrent execution compared to using one processor. This is due to the challenges to 1) reduce data sharing overhead, and 2) properly partition each operator between processors. By solving the challenges, we propose CoDL, a concurrent DL inference framework for the CPU and GPU on mobile devices. It can fully utilize the heterogeneous processors to accelerate each operator of a model. It integrates two novel techniques: 1) hybridtype-friendly data sharing, which allows each processor to use its efficient data type for inference. To reduce data sharing overhead, we also propose hybrid-dimension partitioning and operator chain methods; 2) non-linearity- and concurrency-aware latency prediction, which can direct proper operator partitioning by building an extremely light-weight but accurate latency predictor for different processors. Based on the two techniques, we build the end-to-end CoDL inference framework, and evaluate it on different DL models. The results show up to 4.93× speedup and 62.3% energy saving compared with the state-of-the-art concurrent execution system.

异构处理器上的并发推理执行对于提高越来越重的深度学习（DL）模型的性能至关重要。然而，现有的推理框架一次只能使用一个处理器，或者与使用一个处理器相比，很难通过并发执行实现加速。这是因为存在以下挑战：1）减少数据共享的开销；2）在处理器之间正确划分每个运算器。

通过解决这些挑战，我们提出了CoDL，一个用于移动设备上CPU和GPU的并发DL推理框架。它可以充分利用异构处理器来加速模型的每个运算器。它整合了两项新技术。1）**混合类型友好的数据共享**，它允许每个处理器使用其有效的数据类型进行推理。为了减少数据共享的开销，我们还提出了**混合维度分区和算子链方法**；2）非线性和并发感知的**延迟预测**，它可以通过为不同的处理器建立一个极其轻量级但精确的延迟预测器来指导适当的算子分区。

基于这两种技术，我们建立了端到端的CoDL推理框架，并对不同的DL模型进行了评估。结果显示，与最先进的并发执行系统相比，速度提高了4.93倍，能耗节省了62.3倍。

关键词：CPU-GPU协同执行 深度学习推理 移动设备



## 1 INTRODUCTION 

> Deep Learning (DL) is now the pillar for diverse mobile applications. On-device inference is gaining momentum compared to the on-cloud counterpart, due to the advantages in privacy protection, internet resilience, and low cloud-operation overhead. However, current on-device inference can only achieve acceptable responsiveness for some simple models, but not for others. For example, YOLO [23] for object detection takes over two hundred milliseconds to run on major mobile processors, i.e., mobile CPUs or GPUs. To improve responsiveness, a nature thought is whether it is beneficial to concurrently utilize heterogeneous processors on a mobile device.
>
> Fortunately, we identify that the specific design of mobile systemon-chips (SoCs) provides this opportunity for two causes: 1) comparable CPU and GPU performance. Different from server GPUs which run orders-of-magnitude faster than the CPUs, mobile CPUs and GPUs have similar performance for DL inference [15, 29]. They can therefore run side by side; 2) a unified memory. Different from server machines which usually have separate memories for the CPU and GPU, the mobile CPU and GPU use a unified memory [12]. It can avoid data copying between different memories.
>
> However, current inference frameworks can only use one processor at a time, hindered by two major challenges of concurrent execution (co-execution). The first is how to reduce data sharing overhead. Albeit with a unified memory, considerable overhead is still needed to ensure the coherence of shared data. For example, to run an operator of a model concurrently on the CPU and GPU, the output of the last operator needs to be shared between the two processors. This leads to processor synchronization, data mapping, as well as potential data transformation if different data types are used by different processors. Without proper strategy, the data sharing overhead can easily over weigh the gain from concurrency. The second is how to fairly partition each operator of a model between processors. Online measurements for different partitioning candidates are infeasible. A latency predictor which is light-weight and accurate, and more importantly, aware of all possible overhead introduced by concurrency is required.
>
> To the best of our knowledge, existing works cannot well address the above challenges. 𝜇layer [15] and Optic [29] enable the co-execution of CPU and GPU on mobile devices. However, for the first challenge, they use the same data type (i.e., buffer type) for both the CPU and GPU to simplify data sharing. As we will show in Sec. 2, this design makes CPU+GPU co-execution even slower than the GPU alone, due to the use of inefficient data type for the GPU. For the second challenge, to direct operator partitioning, they model the operator latency by linear regression on the number of computations (i.e., FLOPs). Though this model is light-weight, the prediction accuracy is very poor (< 10%). The reason is that the FLOPs-based predictor cannot capture the real latency behavior. There are also latency predictors [6, 31, 33] that use complex black-box machine learning models to capture latency behavior and achieve high accuracy. However, these models suffer from big running overhead. For example, the model size of nn-Meter [33] for a convolution operator is >800 MB, too heavy to run on mobile devices for real-time prediction. Besides, none of these predictors considers the concurrency-related overhead.
>
> To address the challenges, we propose CoDL, a CPU+GPU concurrent DL inference framework that can fully utilize the heterogeneous processors to accelerate a model. The design of CoDL stems from two key findings. 1) Different processors prefer different data type for optimal performance. For example, we observe using the image type on Adreno GPU can achieve 3.5× speedup compared to the buffer type for convolution. It is necessary to use the efficient type for each processor for co-execution; 2) To make the latency predictor both accurate and light-weight, it is imperative to incorporate platform features into the model, rather than a pure black-box learning.
>
> Based on the two findings, CoDL integrates two new techniques. 1) Hybrid-type-friendly data sharing. It allows the heterogeneous processors to use different data types for inference. Then, to reduce data sharing overhead, we propose hybrid-dimension partitioning and operator chain methods. Hybrid-dimension partitioning can select the optimal partitioning dimension for each operator shape to achieve the tradeoff between data sharing overhead and processor utilization. Operator chain makes sure the operators on a chain only require local data to execute rather than the shared data from the other processor, to avoid data sharing overhead. 2) Non-linearityand concurrency-aware latency prediction. CoDL can conduct online and fair operator partitioning by building a light-weight but accurate latency predictor. Our insight is that the high complexity of other learned latency predictors is to capture the non-linear latency response caused by different algorithms and execution blocks. We therefore analytically formulate the calculation of blocks for each algorithm to extract the non-linearity. Only the linear component is learned by an extremely light-model (∼500 B v.s. 800 MB of nnMeter) linear-regression model. Besides, our predictor is the first to consider all the concurrency-related overhead
>
> Based on the two techniques, we build the end-to-end CoDL framework. For a given model, the best data partitioning and sharing plan for each operator can be worked out based on the predictor. CoDL then coordinates the processors to execute the plan. We implement CoDL based on the state-of-the-art (SOTA) mobile inference framework MACE [19]. The experiments on commercial off-theshelf (COTS) mobile devices, including Snapdragon 855, 865 and 888, and Kirin 990, demonstrate that CoDL can achieve on-average 3.43× speedup and 62.3% energy saving in comparison with the SOTA co-execution system. By taking the non-linear features into account, our predictor achieves 86.21% and 82.69% accuracy on predicting the runtime latency of operators on CPU and GPU, respectively, with low inference overhead (< 1 ms for an operator). Furthermore, with one-time collected data samples (6000 samples with running time less than 1.5 hours), the predictor can be trained in an on-device manner with latency ranging
>
> The main contributions are as follows: • In-depth analysis on the performance bottleneck of concurrent CPU+GPU execution; • Propose hybrid-type-friendly data sharing between CPU and GPU, which utilizes hybrid-dimension partitioning and operator chain to reduce sharing overhead. • Propose the extremely light-weight but accurate non-linearityand concurrency-aware latency prediction. • Implement the end-to-end CoDL framework and demo





深度学习（DL）现在是各种移动应用的支柱。与云端推理相比，设备上推理的势头越来越猛，因为它在隐私保护、互联网弹性和低云端操作开销方面具有优势。然而，目前的设备上推理只能对一些简单的模型实现可接受的响应性，而对其他模型则不能。例如，用于物体检测的YOLO[23]在主要的移动处理器，即移动CPU或GPU上运行需要超过两百毫秒。为了提高响应速度，一个自然的想法是在移动设备上同时利用异构处理器是否有益。

幸运的是，我们发现，移动系统芯片（SoC）的具体设计提供了这种机会，原因有二。1）相当的CPU和GPU性能。与服务器GPU运行速度比CPU快几个数量级不同，移动CPU和GPU在DL推理方面具有相似的性能[15, 29]。因此，它们可以并排运行；2）一个统一的内存。与通常为CPU和GPU配备独立存储器的服务器机器不同，移动CPU和GPU使用一个统一的存储器[12]。它可以避免不同存储器之间的数据复制。

然而，目前的推理框架一次只能使用一个处理器，受到并发执行（co-execution）的两大挑战的阻碍。首先是如何减少数据共享的开销。尽管有统一的内存，但仍然需要相当大的开销来保证共享数据的一致性。例如，要在CPU和GPU上并发地运行一个模型的运算器，最后一个运算器的输出需要在两个处理器之间共享。这导致了处理器同步、数据映射以及潜在的数据转换，如果不同的数据类型被不同的处理器使用。如果没有适当的策略，数据共享的开销很容易超过并发性带来的收益。第二个问题是如何在处理器之间公平地划分模型的每个运算符。对不同分区候选者的在线测量是不可行的。需要一个轻量级的、准确的延迟预测器，更重要的是，要意识到并发性带来的所有可能的开销。

据我们所知，现有的工作不能很好地解决上述挑战。 μlayer[15]和Optic[29]能够在移动设备上实现CPU和GPU的共同执行。然而，对于第一个挑战，他们为CPU和GPU使用相同的数据类型（即缓冲区类型）来简化数据共享。正如我们将在第2节中所展示的，这种设计使得CPU GPU共同执行的速度甚至比单独的GPU还要慢，因为对GPU使用了低效的数据类型。对于第二个挑战，为了指导运算器分区，他们**通过对计算数量（即FLOPs）的线性回归来模拟运算器延迟。虽然这个模型很轻巧，但预测的准确性很差（<10%）。**原因是基于FLOPs的预测器不能捕捉真正的延迟行为。还有一些延迟预测器[6, 31, 33]使用复杂的黑盒机器学习模型来捕捉延迟行为，并达到较高的准确性。然而，这些模型有很大的运行开销。例如，**nn-Meter[33]的模型大小为>800 MB，太重了**，无法在移动设备上运行进行实时预测。此外，这些预测器都没有考虑与并发有关的开销。

为了应对这些挑战，我们提出了CoDL，一个CPU GPU并发的DL推理框架，可以充分利用异构处理器来加速模型。CoDL的设计源于两个关键的发现。

1）不同的处理器喜欢不同的数据类型以获得最佳性能。例如，我们观察到在Adreno GPU上使用图像类型比起缓冲区类型的卷积可以实现3.5倍的加速。有必要为每个处理器使用有效的类型来共同执行；

2）为了使延迟预测器既准确又轻便，必须将平台特征纳入模型，而不是纯粹的黑箱学习。

![image-20220915164813987](D:\alphawork\论文阅读\CoDL.assets\image-20220915164813987.png)

基于这两个发现，CoDL整合了两项新技术。

1）混合类型友好的数据共享。它允许异构处理器使用不同的数据类型进行推理。然后，为了减少数据共享的开销，我们提出了混合维度分区和算子链方法。混合维度分区可以为每个运算器形状选择最佳的分区维度，以实现数据共享开销和处理器利用率之间的权衡。算子链确保链上的算子只需要执行本地数据，而不是来自其他处理器的共享数据，以避免数据共享开销。

2）非线性和并发感知的延迟预测。我们的见解是，其他学习的延迟预测器的高复杂性是为了捕捉不同算法和执行块引起的非线性延迟反应。因此，我们以分析的方式制定每个算法的计算块，以提取非线性。只有线性成分是由一个极轻的模型（500B∼800MB的nnMeter）线性回归模型学习的。此外，我们的预测器是第一个考虑所有与并发有关的开销的预测器。



基于这两种技术，我们建立了端到端的CoDL框架。对于一个给定的模型，可以根据预测器为每个操作者制定出最佳的数据分区和共享计划。然后，CoDL协调处理器来执行该计划。我们在最先进的（SOTA）移动推理框架MACE[19]的基础上实现了CoDL。在商用现成（COTS）移动设备（包括骁龙855、865和888以及麒麟990）上的实验表明，与SOTA共同执行系统相比，CoDL可以实现平均3.43倍的速度提升和62.3倍的能耗节省。通过考虑非线性特征，我们的预测器实现了86.21
和82.69
我们的预测器在预测CPU和GPU上的操作者的运行时间延迟方面分别达到了86.21和82.69的准确率，而且推理开销很低（一个操作者的开销<1ms）。此外，通过一次性收集的数据样本（6000个样本，运行时间小于1.5小时），预测器可以以设备上的方式进行训练，延迟范围为

主要贡献如下。

- 深入分析了CPU和GPU并发执行的性能瓶颈； 
- 提出CPU和GPU之间的混合型友好数据共享，利用混合维度分区和运算器链来减少共享开销。
- 提出了极其轻量级但精确的非线性和并发感知的延迟预测。
- 实现端到端的CoDL框架，并证明它优于最先进的解决方案。

## 2 MOTIVATION AND ANALYSIS

> To direct CoDL design, we first explore the performance bottlenecks of processor co-execution by analyzing the SOTA inference systems. We evaluate 𝜇Layer [15] and MACE [19] as the SOTA co-execution and single-processor execution system, respectively. This section shows the results on Snapdragon 855 for example. Fig. 1 compares their inference latency for different models. Surprisingly, the CPU+GPU co-execution of 𝜇Layer is slower than the CPU or GPU alone of MACE. For PoseNet [35], it even leads to ∼ 2× slowdown.
>
> A unified data type is not efficient for heterogeneous processor co-execution. To simplify data sharing, current co-execution systems use a common data type for different processors. For example, the buffer type is supported by both the CPU and GPU, and thus used by 𝜇Layer. Buffer type organizes data into contiguous and pointer-accessible chunks. However, we identify that the image type can be much more efficient than buffer on Adreno GPUs. Image type organizes data into multi-dimensional chunks to facilitate rendering tasks. It leverages the fast L1 texture cache on GPU to accelerate the data access. Fig. 2 illustrates the performance difference of using image and buffer type for 3×3 convolution with different input shapes. The latency is reduced by 3.5× using the image type, compared to the buffer type.
>
> We analyze the systems in depth and expose the performance issues of the current co-execution system: 1) the use of unified data type for different processors; 2) the neglect of data sharing overhead; and 3) the unbalanced workload partitioning. We will next discuss these issues in detail, as well as the implications for CoDL design.
>
> Therefore, to fully utilize each heterogeneous processor, the corresponding efficient data type should be used.
>
> The data sharing overhead for co-execution is not negligible, especially for small operators. Co-execution introduces data sharing overhead to make sure data coherence between processors. It is overlooked by current co-execution systems. Fig. 3 demonstrates the process and latency components of an operator co-execution on the CPU and GPU. Assuming the operator input is generated by the last operator on the GPU and now shared between the CPU and GPU for co-execution. On top of operator computation, the extra overhead is from 1) data transformation, if different data type is used; 2) data mapping, which maps the input to the CPU address space; 3) synchronization, which informs the other processor the completion of mapping (pre-sync) or computation (post-sync).; and 4) data unmapping, which unmaps the output from the CPU address space.
>
> We identify that this overhead is not negligible. Particularly for small operators, it easily becomes the dominant overhead and offsets the gain brought by the CPU-GPU co-execution. Fig. 4 demonstrates an example. Given that the co-execution reduces the execution latency from 1126𝜇𝑠 to 599𝜇𝑠, the data sharing overhead contributes 1074 𝜇𝑠, leading to a 1.5× slowdown.
>
> Therefore, the co-execution system should aim to reduce the overhead and concurrently execute the operator only when the gain outperforms the overhead. Balanced workload partitioning for co-execution requires a light-weight and accurate latency predictor. Current co-execution systems usually use predicted latency by a light-weight model to direct the workload partitioning between processors. For instance, 𝜇Layer uses a FLOPs-based linear model to predict the latency. The light-weight latency model is suitable for the online prediction. However, it is too inaccurate (< 10% according to our measurements, details in Sec. 7). The inaccurate latency prediction in turn leads to the poor inference performance, due to the unbalanced workload. Fig. 5 demonstrates an operator of a popular model as an example. The FLOPsbased predictor leads to a 4× slowdown by allocating 60% of the operator on the GPU, given that the optimal partitioning ratio is 90%.
>
> The reason for the inaccurate prediction is that the latency is not simply a linear relationship with FLOPs, but greatly impacted by the platform features such as the algorithm implementation and data block size [26, 33]. As shown in Fig. 6, the latency shows a non-linear response as the FLOPs increases for the GPU and CPU.
>
> There are also works aiming for the accurate latency prediction, e.g., nn-Meter [33], which use black-box machine learning methods to learn the latency response based on a number of operator hyperparameters. However, suffering from the lack of knowledge on the underlying platform features, the black-box methods obtain satisfactory accuracy at the cost of large model size (e.g., over 800 MB for convolution by nn-Meter) and infeasible execution time (e.g., more than 80 ms on a PC by nn-Meter). It is unpractical to be deployed on mobile devices. Therefore, a latency predictor that can incorporate platform features and thus be both light-weight and accurate is required for the co-execution system.

为了指导CoDL的设计，我们首先通过分析SOTA推理系统来探索处理器协同执行的性能瓶颈。我们对μLayer[15]和MACE[19]分别作为SOTA协同执行和单处理器执行系统进行评估。本节以Snapdragon 855为例展示结果。图1比较了它们对不同模型的推理延迟。令人惊讶的是，μLayer的CPU GPU联合执行系统比MACE的CPU或GPU单独执行系统要慢。对于PoseNet[35]，它甚至导致了2倍的速度下降。

我们深入分析了这些系统，并揭露了当前协同执行系统的性能问题：1）不同处理器使用统一的数据类型；2）忽视了数据共享的开销；3）不平衡的工作负载划分。接下来我们将详细讨论这些问题，以及对CoDL设计的影响。

统一的数据类型对于异构处理器的协同执行并不高效。为了简化数据共享，目前的协同执行系统对不同的处理器使用一个共同的数据类型。例如，CPU和GPU都支持缓冲区类型，因此μLayer也使用这种类型。缓冲区类型将数据组织成连续的、可由指针访问的块状。然而，我们发现，在Adreno GPU上，图像类型比缓冲区要有效得多。图像类型将数据组织成多维块，以促进渲染任务。它利用了GPU上的快速L1纹理缓存来加速数据访问。图2说明了在不同输入形状的3×3卷积中使用图像和缓冲区类型的性能差异。与缓冲区类型相比，使用图像类型的延时减少了3.5倍。

因此，为了充分利用每个异构处理器，应该使用相应的高效数据类型。

共同执行的数据共享开销是不可忽视的，特别是对小运营商来说。共同执行引入了数据共享开销，以确保处理器之间的数据一致性。它被目前的协同执行系统所忽视。图3展示了CPU和GPU上运算器协同执行的过程和延迟部分。假设运算器输入是由GPU上的最后一个运算器产生的，现在在CPU和GPU之间共享，以便共同执行。在运算器计算的基础上，额外的开销来自1）数据转换，如果使用不同的数据类型；2）数据映射，将输入映射到CPU地址空间；3）同步，通知其他处理器映射（前同步）或计算（后同步）的完成；以及4）数据解映射，从CPU地址空间解映射输出。

我们发现，这种开销是不可忽视的。特别是对于小操作者来说，它很容易成为主要的开销，抵消了CPU-GPU共同执行带来的收益。图4展示了一个例子。鉴于共同执行将执行延迟从1126μs减少到599μs，数据共享开销贡献了1074μs，导致了1.5倍的速度下降。

因此，共同执行系统应该以减少开销为目标，只有当收益超过开销时才并发执行运算器。**共同执行的平衡工作负载分区需要一个轻量级和准确的延迟预测器。目前的协同执行系统通常使用轻量级模型的预测延迟来指导处理器之间的工作负载分配。例如，μLayer使用一个基于FLOPs的线性模型来预测延时。轻量级的延迟模型适用于在线预测。然而，它太不准确了（< 10**
**根据我们的测量，详情见第7章）。由于不平衡的工作量，不准确的延迟预测反过来导致了推理性能的下降。图5展示了一个流行模型的操作者，作为一个例子。基于FLOPs的预测器通过在GPU上分配60%的运算器导致了4倍的速度下降，因为最佳分区比例为90%。**

**预测不准确的原因是，延迟与FLOPs不是简单的线性关系，而是受到平台特征的极大影响，如算法实现和数据块大小[26, 33]。如图6所示，随着FLOPs的增加，GPU和CPU的延迟呈现出非线性响应。**

也有一些旨在准确预测延迟的工作，例如nn-Meter[33]，它使用黑盒机器学习方法来学习基于一些操作者超参数的延迟响应。然而，由于缺乏对底层平台特征的了解，黑盒方法在获得令人满意的准确性的同时，也付出了巨大的模型尺寸（例如，nn-Meter的卷积超过800MB）和不可行的执行时间（例如，nn-Meter在PC上超过80ms）。在移动设备上部署它是不切实际的。因此，共同执行系统需要一个能够纳入平台特征的延迟预测器，从而既轻巧又准确。





1.预测模型是测量协同运算的时间开销



2.方案功耗增加，能耗降低

限制性和未来的工作。CoDL主要有两个限制。首先，由于CPU和GPU的同时运行，CoDL比单处理器解决方案消耗更多的能量。我们计划对预测器进行扩展，以模拟CPU和GPU在DNN模型推理中的功耗行为，这样CoDL就可以在能耗和延迟之间取得平衡。其次，CoDL很难实现轻量级DL模型的加速，如MobileNet[24]，因为分区引起的数据共享开销很容易支配CPU和GPU的并发运行给小运算器带来的收益。