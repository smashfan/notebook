https://blog.csdn.net/m0_72502585/article/details/126                  166764

# 一、什么是负载

负载实际上表示的是进程运行对系统的“压力”情况，它和进程消耗CPU时间是两个概念，比如：
10个进程在运行队列runqueue中，和1个进程在runqueue中，虽然在runquque中的进程并没有正在消耗CPU时间，实际上这两种情况下，系统的压力是不同的，此时这些进程并没有在消耗CPU时间，而是在等待，但是依然对负载产生影响。

因此
负载（task load）：**负载是一个瞬时量，即表示在某一个时间点，runnable状态的task对CPU造成的压力；**
瞬时负载 Li = load weight *（t/1024）
CPU使用率（task utility）：**是一个累积量，表示一段时间内某个task占用总时间片的比例；**
Ui = Max CPU capacity *（t/1024）
我们平时看的/proc/loadavg是负载，但是它是计算的一段时间的值，是个趋势变化；

跟踪任务的utility主要是为任务寻找合适算力的CPU。例如在手机平台上4个大核+4个小核的结构。一个任务本身逻辑复杂，需要有很长的执行时间，也就是说其utility比较大，那么需要将其安排到算力和任务utility匹配的CPU上，例如大核CPU上。PELT算法也会跟踪CPU上的utility，根据CPU utility选择提升或者降低该CPU的频率。CPU load和Task load主要用于负载均衡算法，即让系统中的每一个CPU承担和它的算力匹配的任务负载。