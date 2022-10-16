什么是dockerfile?
Dockerfile是一个包含用于组合映像的命令的文本文档。可以使用在命令行中调用任何命令。 Docker通过读取Dockerfile中的指令自动生成映像。

docker build命令用于从Dockerfile构建映像。可以在docker build命令中使用-f标志指向文件系统中任何位置的Dockerfile。


docker build -f /path/to/a/Dockerfile
Docker通过dockerfile来自动构建镜像.

Dockerfile是什么

Dockerfile是一个创建镜像所有命令的文本文件, 包含了一条条指令和说明, 每条指令构建一层, 通过docker build命令,根据Dockerfile的内容构建镜像,因此每一条指令的内容, 就是描述该层如何构建.有了Dockefile, 就可以制定自己的docker镜像规则,只需要在Dockerfile上添加或者修改指令, 就可生成docker 镜像.

Dockerfile文件格式 

Dockerfile 文件组成如下:

##  Dockerfile文件格式


# This dockerfile uses the ubuntu image
# VERSION 2 - EDITION 1
# Author: docker_user
# Command format: Instruction [arguments / command] ..


# 1、第一行必须指定 基础镜像信息
FROM ubuntu


# 2、维护者信息
MAINTAINER docker_user docker_user@email.com


# 3、镜像操作指令
RUN echo "deb http://archive.ubuntu.com/ubuntu/ raring main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf


# 4、容器启动执行指令
CMD /usr/sbin/nginx
Dockerfile 四部分说明：

一开始必须要指明所基于的镜像名称, 关键字是FROM, 这是必须的.

接下来是维护者信息关键字是MAINTAINER, 非必须, 但良好的习惯有利于后期的职责明确.

后面是镜像操作指令, 如RUN等, 每执行一条RUN命令,镜像添加新的一层.

最后是CMD指令,来指明运行容器时的操作命令.

Dockerfile文件说明
Docker以从上到下的顺序运行Dockerfile的指令。为了指定基本映像，第一条指令必须是FROM。一个声明以＃字符开头则被视为注释。可以在Docker文件中使用RUN，CMD，FROM，EXPOSE，ENV等指令。

FROM：指定基础镜像，必须为第一个命令

格式：
　　FROM <image>
　　FROM <image>:<tag>
　　FROM <image>@<digest>
示例：
　　FROM mysql:5.6
注：
　　tag或digest是可选的，如果不使用这两个值时，会使用latest版本的基础镜像
示例
//指定一个阿里云的远程仓库里面的镜像为基础镜像
FROM registry.aliyuncs.alpine-java:8_server
MAINTAINER: 维护者信息

格式：
    MAINTAINER <name>
示例：
    MAINTAINER Jasper Xu
    MAINTAINER sorex@163.com
    MAINTAINER Jasper Xu <sorex@163.com>
示例：
//维护者信息
MAINTAINER devops@inone.com
RUN：构建镜像时执行的命令

RUN用于在镜像容器中执行命令，其有以下两种命令执行方式：
shell执行
格式：
    RUN <command>
exec执行
格式：
    RUN ["executable", "param1", "param2"]
示例：
    RUN ["executable", "param1", "param2"]
    RUN apk update
    RUN ["/etc/execfile", "arg1", "arg1"]
注：
　　RUN指令创建的中间镜像会被缓存，并会在下次构建中使用。如果不想使用这些缓存镜像，可以在构建时指定--no-cache参数，如：docker build --no-cache
示例：
//创建一个iccck的目录
RUN mkdir -p /iccck

WORKDIR：工作目录，类似于cd命令

格式：
    WORKDIR /path/to/workdir
示例：
    WORKDIR /a  (这时工作目录为/a)
    WORKDIR b  (这时工作目录为/a/b)
    WORKDIR c  (这时工作目录为/a/b/c)
注：
　　通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY等命令都会在该目录下执行。在使用docker run运行容器时，可以通过-w参数覆盖构建时所设置的工作目录。
示例：
//进到该目录下
WORKDIR /iccck
EXPOSE：指定于docker用于与外界交互的端口

格式：
    EXPOSE <port> [<port>...]
示例：
    EXPOSE 80 443
    EXPOSE 8080
    EXPOSE 11211/tcp 11211/udp
注：
　　EXPOSE并不会让容器的端口访问到主机。要使其可访问，需要在docker run运行容器时通过-p来发布这些端口，或通过-P参数来发布EXPOSE导出的所有端口
示例：
//外界可以通过该端口访问dockers中的该文件
EXPOSE 9901
ADD：将本地文件添加到容器中，tar类型文件会自动解压(网络压缩资源不会被解压)，可以访问网络资源，类似wget

格式：
    ADD <src>... <dest>
    ADD ["<src>",... "<dest>"] 用于支持包含空格的路径
示例：
    ADD hom* /mydir/          # 添加所有以"hom"开头的文件
    ADD hom?.txt /mydir/      # ? 替代一个单字符,例如："home.txt"
    ADD test relativeDir/     # 添加 "test" 到 `WORKDIR`/relativeDir/
    ADD test /absoluteDir/    # 添加 "test" 到
示例：
//添加这个jar包到此目录下
ADD ./iwiti-icchk.jar ./
CMD：构建容器后调用，也就是在容器启动时才进行调用。

格式：
    CMD ["executable","param1","param2"] (执行可执行文件，优先)
    CMD ["param1","param2"] (设置了ENTRYPOINT，则直接调用ENTRYPOINT添加参数)
    CMD command param1 param2 (执行shell内部命令)
示例：
    CMD echo "This is a test." | wc -
    CMD ["/usr/bin/wc","--help"]
注：
 　　CMD不同于RUN，CMD用于指定在容器启动时所要执行的命令，而RUN用于指定镜像构建时所要执行的命令。
示例：
//启动容器
CMD java -Djava.security.egd=file:/dev/./urandom -jar iwiti-icchk.jar
————————————————
版权声明：本文为CSDN博主「鹏神丶明月天」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_48964306/article/details/125993680