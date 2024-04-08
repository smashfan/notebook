安装GCC:

sudo apt install gcc-10 g++-10

备份原来的gcc和g++

sudo mv /usr/bin/gcc /usr/bin/gcc.bak

sudo mv /usr/bin/g++ /usr/bin/g++.bak

链接到gcc-10:

sudo ln -s /usr/bin/gcc-10 /usr/bin/gcc

sudo ln -s /usr/bin/g++-10 /usr/bin/g++
