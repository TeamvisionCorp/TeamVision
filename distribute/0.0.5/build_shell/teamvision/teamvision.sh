#!/bin/bash 

echo "---------------------------------------------------------"

echo "teamvision setup start!"



mkdir -p /web/www/teamvision/logs

# 得到当前环境的执行目录

dir=$(cd $(dirname $0); pwd)

cp -rp $dir/* /web/www/teamvision/

cd /web/www/teamvision/

chmod 777 /web/www/teamvision/startup.sh

/usr/python3/bin/pip3 install --upgrade pip

/usr/python3/bin/pip3 install -r /web/www/teamvision/requirements.txt

sh /web/www/teamvision/startup.sh

echo "teamvision setup complete!"

echo "---------------------------------------------------------"


