

# 参考

> https://docs.microsoft.com/zh-cn/windows/wsl/install-manual
>
> https://zhuanlan.zhihu.com/p/509079404

# 环境

查询方法：设置->系统->关于

系统：win10 21H2

操作系统内部版本：19044.1889

# 安装方法

#### 1.开启windows的WSL与虚拟平台 支持

#### 2.wsl --install  自动在默认路径安装ubuntu

如果希望选择其他类型的发行版，可以通过如下名利查看当前支持的发行版。

wsl --list --online

然后选择需要版本通过 wsl --install -d <发行版名称> 进行安装

#### 3.安装下载 Linux 内核更新包（升级wsl2 需要）

- [适用于 x64 计算机的 WSL2 Linux 内核更新包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

#### 4.将 WSL 2 设置为默认版本

```
wsl --set-default-version 2
```

# 使用方法：

1.命令行启动

```
wsl -d Ubuntu-20.04
```

2.点击图标运行

3.windows Terminal 配置启动

### Windows Terminal 中 WSL2 默认打开路径配置

在启动目录中输入

![在这里插入图片描述](https://img-blog.csdnimg.cn/d776ef5b425a484b99154eb7c3c4d67e.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_Q1NETiBAbXVtdTE1Nw==,size_50,color_FFFFFF,t_70,g_se,x_16)



### 文件访问

##### 在wsl访问windows

1

```
explorer.exe .
```

在windows文件夹会出现

2

```
cd /mnt/盘符 例如进入D盘：cd /mnt/d
```

可以出现window下的文件

##### 在windows访问wsl

```
\\wsl$\Ubuntu-18.04\
```

### 常用命令

```
# 启动默认版本的wsl

wsl

# 查看当前的wsl版本以及状态

wsl -l -v  

# 立即终止所有正在运行的分发和 WSL 2 轻型工具虚拟机。

wsl --shutdown

# 查看当前的默认wsl

wsl --list

# 启动指定的wsl版本

# 如要启动Ubuntu20

wsl -d Ubuntu-20.04

# 如要启动Debian

wsl -d Debian
```

# 迁移D盘

#### 1） 停止正在运行的wsl

```
wsl --shutdown
```



#### 2）将需要迁移的Linux，进行导出

```
wsl --export Ubuntu D:/export.tar
```



#### 3）导出完成之后，将原有的Linux卸载

```
wsl --unregister Ubuntu
```



#### 4） 然后将导出的文件放到需要保存的地方，进行导入即可

```
wsl --import Ubuntu D:\export\ D:\export.tar --version 2
```

**总结：**

最简单的办法是，采用wsl 命令行 直接安装Ubuntu发行版；然后采用 迁移指令，将其迁移到其他目录中，避免C盘爆满。



# 联网问题

> 问题描述：
>
> WSL安装完成之后，可以登录，但是无法联网下载工具。
>
> 报下述错误：
>
> temprary failure resolving 'archive.ubuntu.com'
>
> 解决办法：
>
> 依次执行下述命令即可。
>
> sudo rm /etc/resolv.conf
> sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
> sudo bash -c 'echo "[network]" > /etc/wsl.conf'
> sudo bash -c 'echo "generateResolvConf = false" >> /etc/wsl.conf'
> sudo chattr +i /etc/resolv.conf
> ————————————————
> 版权声明：本文为CSDN博主「AlphaDough」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
> 原文链接：https://blog.csdn.net/jimmiez/article/details/122270552

# 安装ohmyzsh



# 深度学习使用

### 1.nvidia-smi的使用

​	windows上安装最新的nvdia驱动

### 2.安装anaconda

> wsl2 + ubuntu 安装anaconda
> 找到清华大学anaconda镜像【链接如下】，找到相应的安装包【选择时间排序，找到最新的linux安装包】，右击选择复制链接
> anaconda | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror
>
> 在ubuntu-shelll下，建立一个空文件夹download【这里的路径是/home/yourname/download】，进入download文件夹
> 使用wget命令安装 。【shell下的粘贴是鼠标右键点击
> wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh
> 1
> 修改下载的文件的属性为 可执行
> ##chmod +x YYY 其中YYY为指定文件 x为可执行属性
> chmod +x ./Anaconda...【tab按键补齐命令】
> 1
> 2
> 运行该文件
> ./Anaconda...【tab按键补齐命令】
> 1
> 一路yes，安装完成之后会出现提示
> modified /home/yourname/.bashrc
> #表明已经将anaconda环境配置到当前目录下
> 1
> 2
>
> ```bash
> conda init bash
> ```
>
> ————————————————
> 版权声明：本文为CSDN博主「任我行:)」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
> 原文链接：https://blog.csdn.net/weixin_44641240/article/details/123312375

### 3.安装docker

1. 更新包列表

```text
sudo apt update
```

\2. 安装必须的包

```text
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

\3. 为国内的 azure 仓库添加 GPG Key

```text
curl -fsSL https://mirror.azure.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

\4. 添加 docker 仓库到 Apt 源

```text
sudo add-apt-repository "deb [arch=amd64] https://mirror.azure.cn/docker-ce/linux/ubuntu bionic stable"
```

\5. 再次更新包列表

```text
sudo apt update
```

\5. 安装 docker

```text
sudo apt install docker-ce
```

\6. 验证 docker 安装是否成功

```text
docker --version
```

\7. 安装 docker compose （可选）

```text
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

#### 4.安装nvidia-container-toolkit

```
DISTRIBUTION=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$DISTRIBUTION/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit nvidia-docker2
sudo systemctl restart docker
```

启动容器：docker run -it --gpus=all   imges

就可以启动nvidia-smi了

### 5.docker安装mindspore-gpu 略

### 6.安装mindspore-GPU

1.安装cuda10.1 cudnn7.6.4

ImportError: libcudnn.so.7: cannot open shared object file: No such file or directory

export LD_LIBRARY_PATH="/usr/local/cuda-10.1/lib64/"

source ~/.bashrc（重点要source一下）