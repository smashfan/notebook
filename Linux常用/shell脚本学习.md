#### 1.Shell 传递参数

我们可以在执行 Shell 脚本时，向脚本传递参数，脚本内获取参数的格式为：**$n**。**n** 代表一个数字，1 为执行脚本的第一个参数，2 为执行脚本的第二个参数，以此类推……

```shell
echo "Shell 传递参数实例！";
echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";
```

如果使用shell指定参数名称传参，是使用到了“**getopts**”命令

### set -e

`set -e` 命令就可以避免操作失败还继续往下执行的问题。

  linux系统自带的说明是：“Exit immediately if a simple command exits with a non-zero status.”，也就是说，在"set -e"之后出现的代码，一旦出现了返回值非零，整个脚本就会立即退出



#### 文件表达式

-e filename 如果 filename存在，则为真
-d filename 如果 filename为目录，则为真 
-f filename 如果 filename为常规文件，则为真
-L filename 如果 filename为符号链接，则为真
-r filename 如果 filename可读，则为真 
-w filename 如果 filename可写，则为真 
-x filename 如果 filename可执行，则为真
-s filename 如果文件长度不为0，则为真
-h filename 如果文件是软链接，则为真
————————————————
版权声明：本文为CSDN博主「高晓伟_Steven」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/superbfly/article/details/49274889

#### 整数变量表达式

```
-eq 等于
-ne 不等于
-gt 大于
-ge 大于等于
-lt 小于
-le 小于等于

    逻辑非 !                   条件表达式的相反

if [ ! 表达式 ]
if [ ! -d $num ]               如果不存在目录$num


    逻辑与 –a                   条件表达式的并列

if [ 表达式1  –a  表达式2 ]


    逻辑或 -o                   条件表达式的或

if [ 表达式1  –o 表达式2 ]
```

