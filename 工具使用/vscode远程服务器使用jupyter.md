1.首先连接上远程服务器

2.服务器上启动jupyter服务

jupyter nootbook -allow-root

3.vscode上连接这个服务器

## 在win10中通过ssh连入服务器

```text
ssh -L [本地端口]:localhost:[远程端口] [远程用户名]@[远程IP] -p [ssh连接端口]
```

示例

```bash
ssh -L 8155:localhost:8892  Zyh@10.200.0.217 -p 22
```

在浏览器输入

```text
http://localhost:8155
```



作者：澄心
链接：https://zhuanlan.zhihu.com/p/448198672
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## Jupyter notebook 更换kernel

由于jupyter notebook访问的时候，默认使用了anaconda的base环境，这里就需要更换环境。

具体方式如下：

1. 安装ipykernel：

```text
(base) [root]# conda activate your_eniv 
(your_eniv) [root]# conda install nb_conda_kernels
Collecting package metadata (current_repodata.json): done
Solving environment: done
```

\2. 激活conda环境： source activate 环境名称，将环境写入notebook的kernel中

```text
python -m ipykernel install --user --name 环境名称 --display-name "显示的名称"
```

\3. 打开notebook服务器：jupyter notebook，浏览器打开对应地址，就会有对应的环境提示了。

![img](https://pic4.zhimg.com/80/v2-9af4dc9a15d1c5e6fa1571d1bd47b37b_720w.jpg)





注意: 1.自己需要添加内核进去

​          2.jupyter notebook 启动进去可能一些没有权限,需要sudo  并且加上 --allow-root 