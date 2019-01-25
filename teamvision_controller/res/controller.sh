#! /bin/sh  
  
#启动方法    
start(){  
 now=`date "+%Y%m%d%H%M%S"`  
 exec java -Xms64m -Xmx128m -jar ./libs/DoraemonController-*-SNAPSHOT.jar &
 #java -Xms128m -Xmx2048m -jar test2.jar 5 > log.log &  
 #tail -f ./logs/controller.log  
}  
#停止方法  
stop(){  
 ps -ef|grep DoraemonController|awk '{print $2}'|while read pid  
 do  
    kill -9 $pid  
 done  
}  
  
case "$1" in  
start)  
start  
;;  
stop)  
stop  
;;    
restart)  
stop  
start  
;;  
*)  
printf 'Usage: %s {start|stop|restart}\n' "$prog"  
exit 1  
;;  
esac
