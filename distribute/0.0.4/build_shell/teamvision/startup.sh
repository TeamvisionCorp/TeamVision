#!/bin/bash
# 得到当前环境的执行目录

dir=$(cd $(dirname $0); pwd)
cd $dir
wget http://projects.unbit.it/downloads/uwsgi-2.0.17.1.tar.gz
tar zxf  uwsgi-2.0.17.1.tar.gz
cd uwsgi-2.0.17.1
/usr/python3/bin/python3.5 uwsgiconfig.py --build
$dir/uwsgi-2.0.17.1/uwsgi --ini $dir/web_uwsgi.ini
$dir/uwsgi-2.0.17.1/uwsgi --ini $dir/websocket_uwsgi.ini
