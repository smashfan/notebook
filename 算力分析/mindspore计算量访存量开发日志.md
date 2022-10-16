

# 流程

### 1.查看mindspore profiler里面的代码

		1.	_get_peak_flops() //得到峰值设备flops
  		2.	_get_op_avg_time_dict()//得到算子平均执行时间
                		3.	。。_compute_task_flops
            		4.	2看pytorch的插件thop

### 3.查看ptflops代码

```python
net_main_module.start_flops_count = start_flops_count.__get__(net_main_module)的意思是什么moudble加入函数属性
```

pytorch_ops,设置flop计算方法

### 4.查看torchsummary代码

1.通过注册register_forward_hook函数，进行记录数值

### 5.查看thop代码

### 6.添加register_forward_hook

### 7.修改cell里面的def _run_forward_hook函数，

### 8.flop，mac计算方式：参考tp-flops的ops-count

2022.9.2 完成初步版本，

conv2d。 relu 。dense 。  pool

# 问题

1.apply没有怎么办

解决：利用cells_

2.def _run_forward_hook 里面返回的是id str 不是object，因此函数里面无法用到object的方法



# 知识点

### 1.mindspore.profiler，mindsight

profiler目前支持在Ascent处理上分析计算量flops。

mindsight是可视化结果

### 2.Cell对象的register_forward_hook功能

用户可以在Cell对象上使用`register_forward_hook`函数来注册一个自定义的Hook函数，用来捕获正向传入Cell对象的数据和Cell对象的输出数据。该功能在静态图模式下和在使用`ms_function`修饰的Cell对象上不起作用。`register_forward_hook`函数接收Hook函数作为入参，并返回一个与Hook函数一一对应的`handle`对象。用户可以通过调用`handle`对象的`remove()`函数来删除与之对应的Hook函数。每一次调用`register_forward_hook`函数，都会返回一个不同的`handle`对象。Hook函数应该按照以下的方式进行定义

### 2.没有apply 用cells_and_name代替

### 3.conv的bias的大小是out_channel数

#### 4.从卷积到全连接，需要自己计算输入通道大小

