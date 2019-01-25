#!/bin/bash 

echo "---------------------------------------------------------"

echo "Teamcat setup start!"



mkdir -p /web/www/teamcat/logs

# 得到当前环境的执行目录

dir=$(cd $(dirname $0); pwd)

cp -rp $dir/* /web/www/teamcat/

cd /web/www/teamcat/

chmod 777 /web/www/teamcat/startup.sh

/usr/python3/bin/pip3 install --upgrade pip

/usr/python3/bin/pip3 install -r /web/www/teamcat/requirements.txt

sh /web/www/teamcat/startup.sh

echo "Teamcat setup complete!"

echo "---------------------------------------------------------"


