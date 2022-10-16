1.docker基础知识

# 一、什么是Docker

在学习docker时，在网上看到一篇博文讲得很好，自己总结一下就是，Docker 将应用程序与该程序的依赖，打包在一个文件里面，改文件包括了所有打包得应用程序的所有依赖，像数据库等；直接运行改文件，就可以让程序跑起来，从而不用再去考虑环境问题。**深度学习中不必再在乎环境问题**

```
# 列出本机正在运行的容器

$ docker container ls

# 列出本机所有容器，包括终止运行的容器

$ docker container ls --all
```

# 二.docker常见命令

### 一、帮助启动类命令

- [ 查看版本] `docker version`
- [ 查看Docker概要信息] `docker info`
- [ 查看Docker总体帮助文档] `docker --help`
- [ 查看docker具体命令帮助文档] `docker 具体命令 --help`
- [ 启动Docker] `systemctl start docker`
- [ 停止Docker] `systemctl stop docker`
- [ 重启Docker] `systemctl restart docker`
- [ 查看状态] `systemctl status docker`
- [ 开机启动] `systemctl enable docker`

# 二、镜像命令

## 1.列出本地主机上的镜像

> docker images

参数说明：

> -a：列出所有镜像（含历史镜像）
> -q：只显示镜像ID
> -f：过滤

![img](https://img-blog.csdnimg.cn/08b13b502ead42dca3b6fff0b81574d5.png)
各个选项说明：

> REPOSITORY：表示镜像的仓库源
> TAG：镜像的标签版本号
> IMAGE ID：镜像ID
> CREATED：镜像创建时间
> SIZE：镜像大小

## 2.在远程仓库中搜索镜像

执行命令，默认去[docker hub](https://hub.docker.com/)中搜索

> docker search 镜像名称

参数说明：

```powershell
-f：过滤
--limit 数量：只列出N个镜像，默认25个
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/16b180e09548420283f03b7475373419.png)

| 参数        | 说明             |
| ----------- | ---------------- |
| NAME        | 镜像名称         |
| DESCRIPTION | 镜像说明         |
| STARS       | 点赞数量         |
| OFFICIAL    | 是否是官方的     |
| AUTOMATED   | 是否是自动构建的 |

## 3.下载镜像

> docker pull 镜像名称[:tag]

不加 tag 时，默认下载最新的镜像（即tag为latest）。

## 4.查看占据的空间

查看镜像/容器/数据卷所占的空间：

> docker system df

![在这里插入图片描述](https://img-blog.csdnimg.cn/6cafecbb5ddc4b91ab436b1e3f7512e1.png)

## 5.删除镜像

> docker rmi 镜像名称/ID

可以使用空格分隔，删除多个镜像：

> docker rmi 镜像1 镜像2 镜像3

删除全部镜像：

> docker rmi -f ${docker images -qa}

## 6.虚悬镜像

仓库名、标签都是的镜像，俗称虚悬镜像（dangling image）。

# 三、容器命令

## 1.新建+启动容器

新建容器，需要先下载镜像`docker pull ubuntu`。

执行命令 `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

**参数【OPTIONS】说明：**

- `--name`：为容器指定一个名称
- `-d`：后台运行容器并返回容器ID，也即启动守护式容器
- `-i`：以交互模式（interactive）运行容器，通常与-t同时使用
- `-t`：为容器重新分配一个伪输入终端（tty），通常与-i同时使用。也即启动交互式容器（前台有伪终端，等待交互）
- `-e`：为容器添加环境变量
- `-P`：随机端口映射。将容器内暴露的所有端口映射到宿主机随机端口
- `-p`：指定端口映射

**-p指定端口映射的几种不同形式**：

- `-p hostPort:containerPort`：端口映射，例如-p 8080:80
- `-p ip:hostPort:containerPort`：配置监听地址，例如 -p 10.0.0.1:8080:80
- `-p ip::containerPort`：随机分配端口，例如 -p 10.0.0.1::80
- `-p hostPort1:containerPort1 -p hostPort2:containerPort2`：指定多个端口映射，例如-p 8080:80 -p 8888:3306

## 2.启动交互式容器(前台命令行)

执行命令，以交互方式启动ubuntu镜像

```bash
docker run -it ubuntu /bin/bash
```

**参数说明：**

> -i: 交互式操作。
> -t: 终端。
> ubuntu : ubuntu 镜像。
> /bin/bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash。
> 要退出终端，直接输入 exit:

**两种方式退出交互模式**：

1. `exit;` run进去容器，exit退出，容器停止
2. 使用快捷键`ctrl + P + Q` run进去容器，ctrl+p+q退出，容器不停止

## 3.列出当前所有正在运行的容器

> docker ps [OPTIONS]

![img](https://img-blog.csdnimg.cn/a5c33ca72ca8459a8a21964e99da98d2.png)

**常用参数说明：**

> -a：列出当前所有正在运行的容器+历史上运行过的
> -l：显示最近创建的容器。
> -n：显示最近n个创建的容器。
> -q：静默模式，只显示容器编号。

## 4.启动守护式容器

大部分情况下，我们系统docker容器服务是在后台运行的，可以通过-d指定容器的后台运行模式：

> docker run -d 容器名

**注意事项：**
如果使用`docker run -d ubuntu`尝试启动守护式的ubuntu，然后`docker ps -a` 进行查看, 会发现容器已经退出了。

因为Docker容器如果在后台运行，就必须要有一个前台进程。容器运行的命令如果不是那些一直挂起的命令（例如`top`、`tail`），就会自动退出。

> 这个是docker的机制问题。比如你的web容器，我们以nginx为例，正常情况下,我们配置启动服务只需要启动响应的service即可。例如**service nginx start**
> 但是这样做，nginx为后台进程模式运行，就导致docker前台没有运行的应用，这样的容器后台启动后，会立即自杀因为他觉得他没事可做了。所以最佳的解决方案是，将你要运行的程序以前台进程的形式运行，常见就是命令行模式，表示还有交互操作。

## 5.容器和宿主机文件拷贝

容器内文件拷贝到宿主机：

> docker cp 容器ID:容器内路径 目的主机路径

宿主机文件拷贝到容器中：

> docker cp 主机路径 容器ID:容器内路径

## 6.导入和导出容器

`export`：导出容器的内容流作为一个tar归档文件（对应import命令）；

`import`：从tar包中的内容创建一个新的文件系统再导入为镜像（对应export命令）；

示例：

```bash
# 导出
# docker export 容器ID > tar文件名
docker export abc > aaa.tar

# 导入
# cat tar文件 | docker import - 自定义镜像用户/自定义镜像名:自定义镜像版本号
docker aaa.tar | docker import - test/mytest:1.0.1
```

## 7.将容器生成新镜像

`docker commit`提交容器副本使之成为一个新的镜像。

> docker 启动一个镜像容器后， 可以在里面执行一些命令操作，然后使用docker commit将新的这个容器快照生成一个镜像。

```bash
docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名:[tag]
```

Docker挂载主机目录，可能会出现报错：`cannot open directory .: Perission denied。`

解决方案：在命令中加入参数 `--privileged=true`。

CentOS7安全模块比之前系统版本加强，不安全的会先禁止，目录挂载的情况被默认为不安全的行为，在SELinux里面挂载目录被禁止掉了。如果要开启，一般使用 `--privileged=true`，扩大容器的权限解决挂载没有权限的问题。也即使用该参数，容器内的root才拥有真正的root权限，否则容器内的root只是外部的一个普通用户权限。

## 8.将容器生成新镜像

卷就是目录或文件，存在于一个或多个容器中，由docker挂载到容器，但不属于联合文件系统，因此能够绕过UnionFS，提供一些用于持续存储或共享数据。

特性：卷设计的目的就是数据的持久化，完全独立于容器的生存周期，因此Docker不会在容器删除时删除其挂载的数据卷。

特点：

- 数据卷可以在容器之间共享或重用数据
- 卷中的更改可以直接实施生效
- 数据卷中的更改不会包含在镜像的更新中
- 数据卷的生命周期一直持续到没有容器使用它为止

运行一个带有容器卷存储功能的容器实例：

```bash
docker run -it --privileged=true -v 宿主机绝对路径目录:容器内目录[rw | ro] 镜像名
```

可以使用docker inspect查看容器绑定的数据卷。

权限：

- rw：读写
- ro：只读。如果宿主机写入内容，可以同步给容器内，容器内可以读取。

容器卷的继承：

```bash
# 启动一个容器
docker run -it --privileged=true /tmp/test:/tmp/docker --name u1 ubuntu /bin/bash

# 使用 --volumes-from 继承 u1的容器卷映射配置
docker run -it --privileged=true --volumes-from u1 --name u2 ubuntu
```

## 9.其他命令

- [ 启动已停止运行的容器] `docker start 容器ID或者容器名`
- [ 重启容器] `docker restart 容器ID或容器名`
- [ 停止容器] `docker stop 容器ID或容器名`
- [ 强制停止容器] `docker kill 容器ID或容器名`
- [ 删除已经停止的容器] `docker rm 容器ID或容器名`
- [ 强制删除正在运行的容器] `docker rm -f 容器ID或容器名`
- [ 一次删除多个容器实例] `docker rm -f ${docker ps -a -q}` 或者`docker ps -a -q | xargs docker rm`
- [ 查看容器日志] `docker logs 容器ID或容器名`
- [ 查看容器内部细节] `docker inspect 容器ID或容器名`
- [ 进入正在运行的容器] `docker exec -it 容器ID bashShell`
- [ 重新进入] `docker attach 容器ID`

**`docker exec` 和 `docker attach` 区别**：

- attach直接进入容器启动命令的终端，不会启动新的进程，用exit退出会导致容器的停止
- exec是在容器中打开新的终端，并且可以启动新的进程，用exit退出不会导致容器的停止

如果有多个终端，都对同一个容器执行了 docker attach，就会出现类似投屏显示的效果。一个终端中输入输出的内容，在其他终端上也会同步的显示。

# 在深度学习当中的使用

docker>19.03 就可以使用gpu了

#### 1.安装docker

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

#### 2.安装nvidia-container-toolkit

```
DISTRIBUTION=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$DISTRIBUTION/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit nvidia-docker2
sudo systemctl restart docker
```

启动容器：docker run -it --gpus=all   imges

就可以启动nvidia-smi了

以mindspore为例子

要测试Docker是否正常工作，请运行下面的Python代码并检查输出：

```
import numpy as np
import mindspore.context as context
from mindspore import Tensor
from mindspore.ops import functional as F

context.set_context(mode=context.PYNATIVE_MODE, device_target="GPU")

x = Tensor(np.ones([1,3,3,4]).astype(np.float32))
y = Tensor(np.ones([1,3,3,4]).astype(np.float32))
print(F.tensor_add(x, y))
[[[ 2.  2.  2.  2.],
[ 2.  2.  2.  2.],
[ 2.  2.  2.  2.]],

[[ 2.  2.  2.  2.],
[ 2.  2.  2.  2.],
[ 2.  2.  2.  2.]],

[[ 2.  2.  2.  2.],
```







```bash
sudo docker build -t docker_name . # 打包镜像 使用当前目录的 Dockerfile 创建镜像
sudo nvidia-docker run -p 1234:5678 -it docker_name /bin/bash # 启动并进入容器
sudo docker exec -it container_id /bin/bash  # 进入容器

sudo docker stop container_id # 停止容器
sudo docker start container_id # 启动容器
```