FROM centos:7.5.1804

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#安装YUM源
RUN yum -y update && yum -y install epel-release && yum -y install redis


#安装清理缓存文件
RUN yum clean all

#修改绑定IP地址
RUN sed -i -e 's@bind 127.0.0.1@bind 0.0.0.0@g' /etc/redis.conf
#关闭保护模式
RUN sed -i -e 's@protected-mode yes@protected-mode no@g' /etc/redis.conf

#启动
ENTRYPOINT [ "/usr/bin/redis-server","/etc/redis.conf"]
CMD []
