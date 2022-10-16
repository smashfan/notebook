/etc/profile，/etc/bashrc 是系统全局环境变量设定

~/.profile，~/.bashrc用户家目录下的私有环境变量设定

1首先读入的是全局环境变量设定档/etc/profile，然后根据其内容读取额外的设定的文档，如
/etc/profile.d和/etc/inputrc
2然后根据不同使用者帐号，去其家目录读取~/.bash_profile，如果这读取不了就读取~/.bash_login，这个也读取不了才会读取
~/.profile，这三个文档设定基本上是一样的，读取有优先关系
3然后在根据用户帐号读取~/.bashrc
至于~/.profile与~/.bashrc的不区别
都具有个性化定制功能
~/.profile可以设定本用户专有的路径，环境变量，等，它只能登入的时候执行一次
~/.bashrc也是某用户专有设定文档，可以设定路径，命令别名，每次shell script的执行都会使用它一次

————————————————
版权声明：本文为CSDN博主「qing101hua」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qing101hua/article/details/53086318



https://blog.csdn.net/qq_41739313/article/details/120079555?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-120079555-blog-125402585.t5_refersearch_landing&spm=1001.2101.3001.4242.1&utm_relevant_index=3