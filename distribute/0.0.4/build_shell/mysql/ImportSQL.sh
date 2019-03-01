#!/bin/bash

echo "---------------------------------------------------------"
# 得到当前环境的执行目录
dir=$(cd $(dirname $0); pwd)

echo "开始导入sql"
mysql -uroot -p123456  < $dir/team_vision.sql

mysql -uroot -p123456  < $dir/privileges.sql

echo "Mysql setup complete!"

echo "---------------------------------------------------------"


