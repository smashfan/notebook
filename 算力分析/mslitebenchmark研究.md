### 调试/home/data/code/mindspore/build.sh

1.调用81:  source mindspore/lite/build_lite.sh





### 编译benchmark增加调试信息

方法：build_lite.sh line775 line778,改成debug（暂时不知道DEBUG_MOD如何设置）



### 调试benchmark以及源码阅读、

#### 代码结构：

- mian.cc (入口函数)
- run_benchmark.cc (执行代码)
- benchmark_base.cc
- benchmark_unifieda.cc
- benchmark_c_api.cc
- mindspore/lite/tools/common/flag_parser.cc
- mindspore/lite/tools/common/string_util.cc



#### 调试流程：

1.首先会按照命名空间遍历

2.进入 mindspore::lite::RunBenchmark(argc, argv)函数及mindspore/lite/tools/benchmark/run_benchmark.cc

具体实现在mindspore/lite/tools/benchmark/benchmark_unified_api.cc

MarkPerformance//测性能





inputs到底怎么生成的





#### 代码逻辑暂定：

模型读取

创建配置上下文

模型创建加载和编译 compile graph

输入数据

执行推理

loadinput()

generateinputData()





获取输出

内存释放