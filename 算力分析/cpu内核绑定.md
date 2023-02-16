# 如何将进程、线程与CPU核进行绑定

> 本文首发于微信公众号【DeepDriving】，欢迎关注。

## 概念

`CPU`绑定指的是在多核`CPU`的系统中将进程或线程绑定到指定的`CPU`核上去执行。在`Linux`中，我们可以利用`CPU affinity`属性把进程绑定到一个或多个`CPU`核上。

`CPU Affinity`是进程的一个属性，这个属性指明了进程调度器能够把这个进程调度到哪些`CPU`上。该属性要求进程在某个指定的`CPU`上尽量长时间地运行而不被迁移到其他处理器。

`CPU Affinity`分为2种：`soft affinity`和`hard affinity`。`soft affinity`只是一个建议，如果不可避免，调度器还是会把进程调度到其它的`CPU`上去执行；`hard affinity`则是调度器必须遵守的规则， `2.6`以上版本的`Linux`内核可以让开发人员可以编程实现`hard affinity`。

## 使用hard affinity的意义

- ***提高CPU缓存命中率***

`CPU`各核之间是不共享缓存的，如果进程频繁地在多个`CPU`核之间切换，则会使旧`CPU`核的`cache`失效，失去了利用`CPU`缓存的优势。如果进程只在某个`CPU`上执行，可以避免进程在一个`CPU`上停止执行，然后在不同的`CPU`上重新执行时发生的缓存无效而引起的性能成本。

- ***适合对时间敏感的应用***

在实时性要求高应用中，我们可以把重要的系统进程绑定到指定的`CPU`上，把应用进程绑定到其余的`CPU`上。这种做法确保对时间敏感的应用程序可以得到运行，同时可以允许其他应用程序使用其余的计算资源。

## 如何将进程与CPU核进行绑定

- ***系统函数***

在`Linux`中，用结构体`cpu_set_t`来表示`CPU Affinity`掩码，同时定义了一系列的宏来用于操作进程的可调度`CPU`集合：

```
#define _GNU_SOURCE
#include <sched.h>
void CPU_ZERO(cpu_set_t *set);
void CPU_SET(int cpu, cpu_set_t *set);
void CPU_CLR(int cpu, cpu_set_t *set);
int CPU_ISSET(int cpu, cpu_set_t *set);
int CPU_COUNT(cpu_set_t *set);
```

具体的作用如下：

```
CPU_ZERO()：清除集合的内容，让其不包含任何CPU。
CPU_SET()：添加cpu到集合中。
CPU_CLR()：从集合中移除cpu
CPU_ISSET() ：测试cpu是否在集合中。
CPU_COUNT()：返回集合中包含的CPU数量。
```

在`Linux`中，可以使用以下两个函数设置和获取进程的`CPU Affinity`属性：

```
#define _GNU_SOURCE
#include <sched.h>
int sched_setaffinity(pid_t pid, size_t cpusetsize,const cpu_set_t *mask);
int sched_getaffinity(pid_t pid, size_t cpusetsize,cpu_set_t *mask);
```

另外可以通过下面的函数获知当前进程运行在哪个`CPU`上：

```
int sched_getcpu(void);
```

如果调用成功，该函数返回一个非负的`CPU`编号值。

- ***例程***

```
#define _GNU_SOURCE
#include <sched.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
cpu_set_t set;
int parentCPU, childCPU;
int j;
int cpu_num = -1;
if (argc != 3) {
fprintf(stderr, "Usage: %s parent-cpu child-cpu\n", argv[0]);
exit(EXIT_FAILURE);
}
parentCPU = atoi(argv[1]);
childCPU = atoi(argv[2]);
CPU_ZERO(&set);
switch (fork()) {
case -1: { /* Error */
fprintf(stderr, "fork error\n");
exit(EXIT_FAILURE);
}
case 0: { /* Child */
CPU_SET(childCPU, &set);
if (sched_setaffinity(getpid(), sizeof(set), &set) == -1) {
fprintf(stderr, "child sched_setaffinity error\n");
exit(EXIT_FAILURE);
}
sleep(1);
if (-1 != (cpu_num = sched_getcpu())) {
fprintf(stdout, "The child process is running on cpu %d\n", cpu_num);
}
exit(EXIT_SUCCESS);
}
default: { /* Parent */
CPU_SET(parentCPU, &set);
if (sched_setaffinity(getpid(), sizeof(set), &set) == -1) {
fprintf(stderr, "parent sched_setaffinity error\n");
exit(EXIT_FAILURE);
}
if (-1 != (cpu_num = sched_getcpu())) {
fprintf(stdout, "The parent process is running on cpu %d\n", cpu_num);
}
wait(NULL); /* Wait for child to terminate */
exit(EXIT_SUCCESS);
}
}
}
```

程序首先用`CPU_ZERO`清空`CPU`集合，然后调用`fork()`函数创建一个子进程，并调用`sched_setaffinity()`函数给父进程和子进程分别设置`CPU Affinity`，输入参数`parentCPU`和`childCPU`分别指定父进程和子进程运行的`CPU`号。指定父进程和子进程运行的`CPU`为1和0，程序输出如下：

```
# ./affinity_test 1 0
The parent process is running on cpu 1
The child process is running on cpu 0
```

## 如何将线程与CPU核进行绑定

- ***系统函数***

前面介绍了进程与`CPU`的绑定，那么线程可不可以与`CPU`绑定呢？当然是可以的。在`Linux`中，可以使用以下两个函数设置和获取线程的`CPU Affinity`属性：

```
#define _GNU_SOURCE
#include <pthread.h>
int pthread_setaffinity_np(pthread_t thread, size_t cpusetsize, const cpu_set_t *cpuset);
int pthread_getaffinity_np(pthread_t thread, size_t cpusetsize, cpu_set_t *cpuset);
```

- ***例程***

```
#define _GNU_SOURCE
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
static void *thread_start(void *arg) {
......
struct thread_info *tinfo = arg;
thread = tinfo->thread_id;
CPU_ZERO(&cpuset);
CPU_SET(tinfo->thread_num, &cpuset);
s = pthread_setaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
if (s != 0) {
handle_error_en(s, "pthread_setaffinity_np");
}
CPU_ZERO(&cpuset);
s = pthread_getaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
if (s != 0) {
handle_error_en(s, "pthread_getaffinity_np");
}
for (j = 0; j < cpu_num; j++) {
if (CPU_ISSET(j, &cpuset)) { //如果当前线程运行在CPU j上，则输出信息
printf(" thread %d is running on cpu %d\n", tinfo->thread_num, j);
}
}
pthread_exit(NULL);
}
int main(int argc, char *argv[])
{
......
cpu_num = sysconf(_SC_NPROCESSORS_CONF); //获取系统的CPU数量
tinfo = calloc(cpu_num, sizeof(struct thread_info));
if (tinfo == NULL) {
handle_error_en(0, "calloc");
}
for (j = 0; j < cpu_num; j++) { //有多少个CPU就创建多少个线程
tinfo[j].thread_num = j;
s = pthread_create(&tinfo[j].thread_id, NULL, thread_start, &tinfo[j]);
if (s != 0) {
handle_error_en(s, "pthread_create");
}
}
for (j = 0; j < cpu_num; j++) {
s = pthread_join(tinfo[j].thread_id, NULL);
if (s != 0) {
handle_error_en(s, "pthread_join");
}
}
......
}
```

程序首先获取当前系统的`CPU`数量`cpu_num`，然后根据`CPU`数量的数量创建线程，有多少个`CPU`就创建多少个线程，每个线程都运行在不同的`CPU`上。在4核的机器中运行结果如下：

```
$ ./thread_affinity
thread 1 is running on cpu 1
thread 0 is running on cpu 0
thread 3 is running on cpu 3
thread 2 is running on cpu 2
```

## 用taskset命令实现进程与CPU核的绑定

`Linux` 的`taskset`命令用于设置或检索由`pid`指定的运行进程的`CPU Affinity`，或者以给定的`CPU Affinity`属性启动新的进程。`CPU Affinity`属性用位掩码来表示，其中最低位对应第一逻辑`CPU`，最后一位与最后一个逻辑`CPU`对应。检索到的掩码仅反映与物理系统上的`CPU`相对应的位。如果给出无效的掩码（即当前系统上没有对应的有效的`CPU`掩码），则返回错误。掩码通常以十六进制形式给出。例如：

```
0x00000001 表示CPU #0,
0x00000003 表示CPU #0 和 #1,
0x0000000f 表示CPU #0 ~ #3
```

`taskset`命令的选项如下：

```
-a, --all-tasks
设置或检索所有由pid指定的进程的CPU Affinity属性。
-c, --cpu-list numbers
指定处理器的数值列表，而不是位掩码。数字用逗号分隔，可以包括范围。比如：0,5,8-11。
-p, --pid
操作由pid指定的进程，不启动新的进程。
```

**下面以`Ubuntu16.04`中的`taskset`命令说明该命令的使用方法：**

- **显示进程运行的CPU核**

```
命令：taskset -p 1
结果：pid 1‘s current affinity mask: f
说明：f表示进程1运行在CPU#0~CPU#3上
```

- **指定进程运行在某个特定的CPU核上**

```
命令：taskset -cp 1,2 7737
结果：pid 7737's current affinity list: 0-3
pid 7737's new affinity list: 1,2
说明：该操作把进程7737限定在CPU#1~CPU#2上运行。
```

- **进程启动时指定CPU核**

```
命令：taskset -c 1-2 ./get_affinity
结果：This process is running on cpu 1
This process is running on cpu 2
说明：get_affinity程序通过sched_getaffinity()函数获取当前进程的CPU Affinity属性并输出提示信息。
```

## 总结

本文通过几个简单的例子介绍了`Linux`环境下进程、线程与`CPU`的绑定方法，希望对大家有参考意义。