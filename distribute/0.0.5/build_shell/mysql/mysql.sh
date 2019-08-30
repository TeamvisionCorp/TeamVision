#!/bin/bash

echo "---------------------------------------------------------"
# 得到当前环境的执行目录
dir=$(cd $(dirname $0); pwd)
echo "====================================================="  
echo "setup MySQL 5.7.10 on centos7_64bit "  
echo "your computer is $CPU_NUMBERS processes ,mysql Memory is $MYSQL_MEM M"   
echo "you will input mysql's user 'root' password '123456'and mysql's memory"  
echo "====================================================="  
sleep 1  

read -n1 -p "are you sure setup[y/n]?" answer  
 case $answer in   
 Y | y)  
       echo   
       echo "start setup....";;  
 N | n)  
       echo   
       echo "Cancel setup...."  
       exit 10 ;;  
   *)  
       echo   
       echo "error input parameter....."   
       exit 11 ;;  
 esac  

#check if user is root  

if [ $(id -u) != "0" ];then  
   echo "Error: You must be root to run this script!"  
   exit 1  
fi  

echo "Mysql setup start!"

echo "----------------------------------start download repo -----------------------------"

cd $dir

wget http://repo.mysql.com/mysql57-community-release-el7-11.noarch.rpm

echo "----------------------------------start install repo -----------------------------"

sudo rpm -ivh $dir/mysql57-community-release-el7-11.noarch.rpm

echo "----------------------------------start install mysql -----------------------------"

sudo yum install mysql-server mysql-client libmysqlclient-dev mysql-devel MySQL-python -y

sudo service mysqld start

echo "----------------------------------get mysql password -----------------------------"

mysqlpassword=`grep 'temporary password' /var/log/mysqld.log |awk '{print $NF}'`

echo "mysql -uroot -p${mysqlpassword}"

mysql -uroot -p${mysqlpassword}  -e "set global validate_password_policy=0"

mysql -uroot -p${mysqlpassword}  -e "set global validate_password_length=4"

echo "----------------------------------set mysql password '123456'--------------
----------------"

mysql -uroot -p${mysqlpassword}  -e "ALTER USER 'root'@'localhost' IDENTIFIED BYY
 '123456'"
echo "开始导入sql"
mysql -uroot -p123456  < $dir/team_vision.sql

mysql -uroot -p123456  < $dir/privileges.sql

echo "Mysql setup complete!"

echo "---------------------------------------------------------"


