---------------
项目结构
---------------

teamcat-agent-parent 主项目
 |- doc    文档目录
 |- source    子项目
 ....   |- teamcat-agent    Agent项目
 ....   |- teamcat-driver    Driver接口库项目
 ....   |- teamcat-driver-steptask  Driver实现 


---------------
版本管理
---------------
版本配置位于：Doraemon项目pom.xml文件project/properties/release-version元素，所有子项目和打包发布版本号都引用此处的版本信息。


---------------
生成发布包
---------------
发布包生成过程使用Ant脚本完成。build.xml用于构建发布包。生成后的发布包位于distribute目录下。

生成发布包命令: ant


--------------
本地参数 agent.properties
--------------
agent.key=3
server.host= http://teamcat.cn
