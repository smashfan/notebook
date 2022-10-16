Deep Learning Workload Scheduling in GPU Datacenters: Taxonomy, Challenges and Vision



### Abstact

> Deep learning (DL) shows its prosperity in a wide variety of fields. The development of a DL model is a time-consuming and resource-intensive procedure. Hence, dedicated GPU accelerators have been collectively constructed into a GPU datacenter. An efficient scheduler design for such GPU datacenter is crucially important to reduce the operational cost and improve resource utilization. However, traditional approaches designed for big data or high performance computing workloads can not support DL workloads to fully utilize the GPU resources. Recently, substantial schedulers are proposed to tailor for DL workloads in GPU datacenters. This paper surveys existing research efforts for both training and inference workloads. We primarily present how existing schedulers facilitate the respective workloads from the scheduling objectives and resource consumption features. Finally, we prospect several promising future research directions. More detailed summary with the surveyed paper and code links can be found at our project website: https://github.com/S-Lab-SystemGroup/Awesome-DL-Scheduling-Papers.

深度学习（DL）在各种领域都显示出它的繁荣。开发一个DL模型是一个耗时和资源密集的过程。因此，专用的GPU加速器已被集体构建成一个GPU数据中心。**为这样的GPU数据中心设计一个有效的调度器对于降低运营成本和提高资源利用率至关重要**。然而，为大数据或高性能计算工作负载设计的传统方法不能支持DL工作负载来充分利用GPU资源。最近，人们提出了大量的调度器来为GPU数据中心的DL工作负载量身定做。本文调查了**训练和推理工作负载**的现有研究工作。我们主要介绍了现有的调度器如何从调度目标和资源消耗的特点来促进各自的工作负载。最后，我们展望了几个有希望的未来研究方向。更详细的摘要与调查的论文和代码链接可以在我们的项目网站找到：https://github.com/S-Lab-SystemGroup/Awesome-DL-Scheduling-Papers。



### conclusion and outlooks

> The scheduler design is an ever-lasting topic in the system research community. The prosperity of DL workloads considerably pushes forward the progress of this research area in all stages of scheduling. The unique features exhibited by DL workloads advocate novel DL scheduler design to manage the GPU resources and jobs in a more intelligent and efficient manner. Our comprehensive summary draws three conclusions. First, new works prefer to adopt advanced algorithms (e.g., RL, MAML), which can significantly improve the scheduling performance. Second, it is necessary to take advantages of emerging hardware resources (e.g., heterogeneous GPU, GPU colocation and sharing, elastic training) when designing efficient schedulers. Third, new scheduling systems are motivated by the emerging DL workloads and applications, as well as users’ new requirements.
>
> DL workload scheduling in GPU datacenters remains premature. There are multiple interesting future research directions, as summarized below.
>
> DL workloads. The diverse DL workloads pose different challenges to the scheduler. Domainspecific schedulers are required for extreme efficiency for specific applications. Therefore, a set of novel DL workloads with special resource requirements (e.g., HPO, hybrid workloads) call for more research efforts. Searching-based DL workloads like HPO eagerly rely on being served as early as possible to get search results earlier and thus optimize the search direction. Training extremely large models like Transformers needs extensive and high-performance resources. Surging needs from DL jobs for debugging purposes should also be balanced with those production jobs under hybrid situations. Otherwise, the under-efficiency problem will arise. Another important direction is the co-design of both the scheduling system and DL framework. Better scheduling decisions could be made by negotiating the fine-grained resource demand of workloads and delegating framework-level control to the scheduling system.
>
> Scheduling decision making. Many existing schedulers may encounter problems with GPU datacenters at scale. First, a lot of scheduling systems require additional information about the workload from users or online profiling, posing great challenges when facing numerous workloads and resources. Second, some schedulers form the decision-making process as an optimation problem, which cannot be solved within an acceptable time online. Other systems such as online monitoring of DL workloads, resource management, and coordination also add difficulty to the operations of large-scale GPU datacenters.
>
> Underlying hardware resources. GPU datacenters are also growing at an alarming speed. It is common for modern GPU datacenters to contain heterogeneous and complex generations of GPUs and other accelerators. Schedulers need to make scheduling decisions based on different affinities between workloads and GPUs. GPUs may also reveal different capabilities for serving the workloads, e.g., hardware-level support for multiplexing, advanced support for low-precision ALU. Other resources like emerging networking topology also draw the attention of schedulers for performance efficiency.



调度器设计是系统研究界的一个永恒的话题。DL工作负载的繁荣大大推动了这个研究领域在调度的各个阶段的进展。DL工作负载所表现出的独特特征主张采用新颖的DL调度器设计，以更加智能和高效的方式管理GPU资源和工作。我们的综合总结得出了三个结论。首先，新的工作倾向于采用先进的算法（如RL，MAML），这可以显著提高调度性能。第二，在设计高效的调度器时，有必要利用新兴的硬件资源（如异构的GPU，GPU主机和共享，弹性训练）的优势。第三，新的调度系统是由新兴的DL工作负载和应用，以及用户的新要求所激发的。  

在GPU数据中心的DL工作负载调度仍然不成熟。未来有多个有趣的研究方向，总结如下。

### TIP

```


先进算法RL MAML

另一个重要方向是调度系统和DL框架的共同设计。可以通过协商工作负载的细粒度资源需求并将框架级别的控制委托到调度系统来做出更好的计划决策。
```



DL工作负载。多样化的DL工作负载对调度程序构成了不同的挑战。特定域的特定调度程序是特定应用的极端效率所必需的。因此，一组具有特殊资源需求的新型DL工作负载（例如HPO，混合工作负载）要求进行更多的研究工作。基于搜索的DL工作负载（例如HPO）热切地依靠尽早使用以提早获得搜索结果，从而优化搜索方向。培训诸如变形金刚之类的极大模型需要广泛和高性能的资源。在混合情况下，DL工作的飙升需求也应与这些生产工作保持平衡。否则，效率不足问题将会出现。另一个重要方向是调度系统和DL框架的共同设计。可以通过协商工作负载的细粒度资源需求并将框架级别的控制委托到调度系统来做出更好的计划决策。

调度决策。许多现有的调度程序可能会大规模遇到GPU数据中心问题。首先，许多调度系统都需要有关用户或在线分析的工作量的更多信息，在面对众多工作量和资源时面临巨大的挑战。其次，一些调度程序将决策过程形成作为优化问题，无法在在线可接受的时间内解决。其他系统，例如对DL工作负载，资源管理和协调的在线监视也为大规模GPU数据中心的运营带来了困难。

基础硬件资源。 GPU数据中心也以惊人的速度增长。现代GPU数据中心通常包含异质和复杂的GPU和其他加速器。调度程序需要根据工作负载和GPU之间的不同亲和力做出调度决策。 GPU还可能揭示服务负载服务的不同功能，例如，硬件级别的支持，用于多路复用，对低精度ALU的高级支持。其他资源（例如新兴网络拓扑结构）也引起了调度程序的注意力，以提高性能效率。