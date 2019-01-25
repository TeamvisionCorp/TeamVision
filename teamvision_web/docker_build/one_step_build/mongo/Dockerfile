FROM centos:7.5.1804

COPY mongodb-linux-x86_64-3.4.12.tgz /mongodb-linux-x86_64-3.4.12.tgz

#安装YUM源
RUN yum update -y && yum install -y gcc automake autoconf libtool make

#安装清理缓存文件
RUN yum clean all


RUN tar -xf mongodb-linux-x86_64-3.4.12.tgz

RUN mv mongodb-linux-x86_64-3.4.12 mongodb-3.4.12

RUN mv mongodb-3.4.12 /usr/local/mongodb-3.4.12

COPY mongo.conf /usr/local/mongodb-3.4.12

ENV PATH /usr/local/mongodb-3.4.12/bin:$PATH

RUN rm -rf mongodb-linux-x86_64-3.4.12.tgz

RUN mkdir -p /data/mongodb/db
RUN mkdir -p /data/mongodb/logs
RUN touch /data/mongodb/logs/mongodb.log

ENV AUTH no

#启动
CMD ["mongod","-f","/usr/local/mongodb-3.4.12/mongo.conf"]
