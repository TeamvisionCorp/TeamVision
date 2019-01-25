#!/bin/bash  

echo "---------------------------------------------------------"

echo "nginx setup start!"

# 得到当前环境的执行目录
dir=$(cd $(dirname $0); pwd)

mkdir -p /web/www/logs/

cd /usr/local/teamcat

wget http://nginx.org/download/nginx-1.12.0.tar.gz

tar -zxvf nginx-1.12.0.tar.gz

cd nginx-1.12.0

./configure --prefix=/usr/local/teamcat/nginx --with-http_stub_status_module --with-http_ssl_module

make 

make install

mkdir /usr/local/teamcat/nginx/conf/conf_dir

mkdir -p /web/nginx/logs/

cp $dir/conf/teamcat_fontend_8888.conf /usr/local/teamcat/nginx/conf/conf_dir/

rm -rf /usr/local/teamcat/nginx/conf/nginx.conf

cp -f $dir/nginx.conf /usr/local/teamcat/nginx/conf/

/usr/local/teamcat/nginx/sbin/nginx -c /usr/local/teamcat/nginx/conf/nginx.conf

echo "nginx setup complete!"

echo "---------------------------------------------------------"


