一.切换分支
输入命令“git branch -a”，查看远程分支
输入命令“git checkout dev”，切换到分支dev
输入命令“git status”，查看分支状态，比如是否有未保存的修改、未解决的冲突





### git fetch 和git pull 的差别

git fetch 相当于是从远程获取最新到本地，不会自动merge
git fetch orgin master //将远程仓库的master分支下载到本地当前branch中
git log -p master ..origin/master //比较本地的master分支和origin/master分支的差别
git merge origin/master //进行合并
git pull：相当于是从远程获取最新版本并merge到本地
git pull origin master
git pull <远程主机名> <远程分支名>:<本地分支名>
————————————————
版权声明：本文为CSDN博主「那些年的代码」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_44018338/article/details/98882963





###  显示出branch1和branch2中差异的部分

```
git diff branch1 branch2 --stat
```

 



# Git 配置

> ```
> 1.查看git配置信息
> $ git config --list
> 
> 2.查看git用户名、密码、邮箱的配置
> $ git config user.name
> $ git config user.password
> $ git config user.email
> 
> 3.设置git用户名、密码、邮箱的配置
> $ git config user.name “freedom”
> $ git config user.password “123456”
> $ git config user.email “1548429568@qq.com”
> 
> 4.设置git用户名、密码、邮箱的配置（全局配置）
> $ git config --global user.name 用户命
> $ git config --global user.name freedom
> $ git config --global user.password 密码
> $ git config --global user.password abc0506abc
> $ git config --global user.password 邮箱
> $ git config --global user.email “1548429568@qq.com”
> 
> 5.修改git用户名、密码、邮箱的配置（跟设置语法一样，没有用户名就添加，有了用户名就修改）
> $ git config user.name “freedom”
> 
> 4.修改git用户名、密码、邮箱的配置（全局配置）
> $ git config --global user.name “freedom”
> ————————————————
> 版权声明：本文为CSDN博主「默茉」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
> 原文链接：https://blog.csdn.net/weixin_43081805/article/details/125355169
> ```
>
> 



### git 整个流程

```
# 添加所有变更文件

git add .

# 添加 指定 文件

git add test01.py  test02.py

# 添加  文件名  test 开头的文件

git add test*

# 添加 后缀为 .py 的文件

git add *.py

git commit -m [备注文本]
git commit -m "提交备注"
# origin 、 mycode 数据源名称  master 分支名
git push [数据源] [分支名]
git push origin master
git push origin dev
 
# 强制推送（谨慎操作）
git push -f [数据源] [分支名]
git push -f origin master
git push origin master
git push origin dev
 
# 强制推送（谨慎操作）
git push -f [数据源] [分支名]
git push -f origin master
```

### git 查看commit修改信息

```
1.git log 查看本地commit记录
2.git show commitid
```



### 如何利用git解决冲突







### git clash代理

```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```

