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
> $ git config --global user.name "fjq"
> git config --global user.email "smashfan@mail.ustc."
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





先提交暂存（add），再拉取，pull拉取完之后（根据提示是否有冲突）再commi提交。如果有冲突就解决冲突

### git clash代理

```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```







### 多人同步问题

> 场景：因为有事情需回到学校搞毕设，同事在公司说接口代码有问题，需要修改；
>
> 我用笔记本把代码同步到笔记本，然后做了一些修改、提交。修改完成。
>
> 第二天我来到公司（公司里用台式机，不是自己的笔记本），忘了先git pull到本地之后，直接在台式机上的代码进行编写，突然想起忘了pull了，然后想用git pull来更新本地代码。结果报错：
>
> error: Your local changes to the following files would be overwritten by merge:
>
> 意思是我台式机上新修改的代码的文件，将会被git服务器上的代码覆盖；我当然不想刚刚写的代码被覆盖掉，看了git的手册，发现可以这样解决：
>
>
> 方法1：如果你想保留刚才本地修改的代码，并把git服务器上的代码pull到本地（本地刚才修改的代码将会被暂时封存起来）
>
>
> git stash
> git pull origin master
> git stash pop
>
>
> 如此一来，服务器上的代码更新到了本地，而且你本地修改的代码也没有被覆盖，之后使用add，commit，push 命令即可更新本地代码到服务器了。
>
> 
>
> 方法2、如果你想完全地覆盖本地的代码，只保留服务器端代码，则直接回退到上一个版本，再进行pull：
>
> git reset --hard
> git pull origin master
>
>
> 注：其中origin master表示git的主分支。
>
>
> ————————————————
> 版权声明：本文为CSDN博主「misaka去年夏天」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
> 原文链接：https://blog.csdn.net/misakaqunianxiatian/article/details/51103734