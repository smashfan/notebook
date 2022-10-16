1.首先连接上远程服务器

2.服务器上启动jupyter服务

jupyter nootbook -allow-root

3.vscode上连接这个服务器



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