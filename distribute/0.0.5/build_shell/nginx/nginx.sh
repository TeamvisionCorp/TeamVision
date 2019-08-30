#!/bin/bash  

echo "---------------------------------------------------------"

echo "nginx setup start!"

# 得到当前环境的执行目录
dir=$(cd $(dirname $0); pwd)

mkdir -p /web/www/logs/

cd /usr/local/teamvision

wget http://nginx.org/download/nginx-1.12.0.tar.gz

tar -zxvf nginx-1.12.0.tar.gz

cd nginx-1.12.0

./configure --prefix=/usr/local/teamvision/nginx --with-http_stub_status_module --with-http_ssl_module

make 

make install

mkdir /usr/local/teamvision/nginx/conf/conf_dir

mkdir -p /web/nginx/logs/

cp $dir/conf/nginx.api.conf /usr/local/teamvision/nginx/conf/conf_dir/
cp $dir/conf/teamvision_fontend.conf /usr/local/teamvision/nginx/conf/conf_dir/

rm -rf /usr/local/teamvision/nginx/conf/nginx.conf

cp -f $dir/nginx.conf /usr/local/teamvision/nginx/conf/

/usr/local/teamvision/nginx/sbin/nginx -c /usr/local/teamvision/nginx/conf/nginx.conf

echo "nginx setup complete!"

echo "---------------------------------------------------------"


