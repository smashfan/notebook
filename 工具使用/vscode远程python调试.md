方法1：

1.create a lauch.json file

2.打开launch.json

3.添加如下代码

```
 {
   "name": "Python: Current File",
   "type": "python",
   "request": "launch",
   "program": "${file}",
   "console": "integratedTerminal",
   "cwd": "${fileDirname}"  // 设置相对路径，在debug时可以切换到当前文件所在的目录
},
```

方法2

pip install ptvsd

```
import ptvsd
ptvsd.enable_attach(address = ('0.0.0.0', 5678))
ptvsd.wait_for_attach()
```

```
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "port": 5678,  //这个端口随便设置
    "host": your_ip,   //这是远程服务器的ip
    // "pathMappings": [
    //     {
    //         "localRoot": "${workspaceFolder}",
    //         "remoteRoot": "."
    //     }
    // ]
}
```

