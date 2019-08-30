#!/bin/bash
echo "---------------------------------------------------------"

echo "Redis setup start!"

# 得到当前环境的执行目录

dir=$(cd $(dirname $0); pwd)

cd $dir/redis-3.2.8/src/

make MALLOC=libc 

make install PREFIX=/usr/local/teamcat/redis

nohup /usr/local/teamcat/redis/bin/redis-server /$dir/redis-3.2.8/redis.conf &

echo "Redis setup complete!"

echo "---------------------------------------------------------"

