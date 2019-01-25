doraemon_controller

---------------
生成发布包
---------------
发布包生成过程使用Ant脚本完成。build.xml用于构建发布包。生成后的发布包位于distribute目录下。

生成发布包命令: ant


--------------
本地参数 controller.properties
--------------
INTERFACE_BASE_URL = http://teamcat.cn/
EMAIL_IS_AUTH = false
TASK_FLOW_SWITCH = false
	
--------------
使用说明
--------------
将发布包解压后可用sh脚本启动

开始
controller.sh start
关闭
controller.sh stop
重启
controller.sh restart