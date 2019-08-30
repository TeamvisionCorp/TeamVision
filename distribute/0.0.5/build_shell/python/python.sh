#!/bin/bash  

echo "---------------------------------------------------------"

echo "Python setup start!"

mkdir -p /usr/local/teamcat

cd /usr/local/teamcat

# 安装依赖

yum groupinstall 'Development Tools'  -y

yum install zlib-devel bzip2-devel openssl-devel ncurese-devel -y

# 安装Python 3.5.4

wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz

tar -zxvf Python-3.5.4.tgz

mv Python-3.5.4 python3.5

cd python3.5

./configure --prefix=/usr/python3

make

make install

echo "Python setup complete!"

echo "---------------------------------------------------------"


