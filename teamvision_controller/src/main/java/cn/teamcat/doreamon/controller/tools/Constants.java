package cn.teamcat.doreamon.controller.tools;

import java.io.FileInputStream;
import java.util.Properties;

/**
 * 常量
 * @author Sirui.Zhang 
 *
 */
public class Constants {            
	//邮件


	public static final String LOGO = "res/logo.jpg";
	public static final String ALIVE_CMD = "alive";
	//build_message
	public static final String TQ_DONE_ERROR = "TQ Done Error: can not make task tqdone";
	public static final String SEND_FAIL = "Task Send Error: agent can not work,";
	public static final String HISTORY_ERROR = "Can not find history from ci_task_history";
	public static final String STOP_FAIL = "Task Send Error: task stop fail: ";
	public static final String RUNNING_ERROR = "Running Error agent offline";
	public static final String GET_HISTORY_FAIL = "Task Clean Error : can not get history info";
	public static final String ASSIGN_FAIL_FROM_INTERFACE = "Task Assign Error: can not get agent info from interface";
	public static final String WAIT_TIMEOUT = "Task Assign Timeout Error: no agent can be used";
	public static final String RUN_TIMEOUT = "Task Run Timeout Error: ";
	public static final String TIMER_ERROR = "Timer Error: task history can not insert";
	public static final String SOCKET_TIMEOUT_ERROR = "Socket Error: Scoket contacted timeout";
	public static final String MQ_TIMEOUT_ERROR = " message queue write failed";

	
	public class ChineseMsg{
		public static final String TASK_TOO_MACH_EMAIL_SUBJECT = "当前未处理任务过多";
		public static final String DISASTER_EMAIL_SUBJECT = "当前有Disaster任务";
		public static final String TIMER_ERROR_SUBJECT = "TeamCat Report-Timer插入任务失败";
		public static final String RTX_TITLE = "TeamCat-";
		public static final String RTX_MSG = "，请查看邮件";
		public static final String TASK_COMPLETE = "任务构建完成";
		public static final String TASK_FAIL = "任务构建失败";
		public static final String TASK_ABORTED = "任务构建已被放弃";
		public static final String DEPLOY_TASK_START = "任务部署开始";
		public static final String DEPLOY_TASK_COMPLETE = "任务部署完成";
		public static final String DEPLOY_TASK_FAIL = "任务部署失败";
		public static final String DEPLOY_TASK_ABORTED = "任务部署已被放弃";
		public static final String AUTO_TEST_TASK_COMPLETE = "自动化测试执行完成";
		public static final String AUTO_TEST_TASK_FAIL = "自动化测试执行失败";
		public static final String AUTO_TEST_TASK_ABORTED = "自动化测试已被放弃";
	}
	
	public static class API {
		public static final String POST_AUTO_TESTING_RESULTS = TEAMCAT_BASE_URL + "api/ci/auto_testing_results";
		public static final String POST_SIMPLE_MQ = TEAMCAT_BASE_URL + "api/common/simple_mq";
		public static final String GET_TASK = TEAMCAT_BASE_URL + "api/ci/task/get_task";
		public static final String CITASBASIC = TEAMCAT_BASE_URL + "api/ci/task_basic/";
		public static final String GET_CITASKLIST = TEAMCAT_BASE_URL + "api/ci/task_basic/list";
		public static final String GET_AGENTTASK = TEAMCAT_BASE_URL + "api/common/task_queues";
		public static final String CITASK = TEAMCAT_BASE_URL + "api/ci/task/";
		public static final String GET_TASKQUEUES = 	TEAMCAT_BASE_URL + "api/common/task_queues";
		public static final String GET_TASKRESULTS = 	TEAMCAT_BASE_URL + "api/ci/auto_testing_results";
		public static final String PATCH_TASKRESULT = 	TEAMCAT_BASE_URL + "api/ci/auto_testing_result";
		public static final String GET_CASERESULTS = 	TEAMCAT_BASE_URL + "api/ci/auto_case_results";
		public static final String DELETETASKQUEUE = 	TEAMCAT_BASE_URL + "api/common/task_queue/";
		public static final String GET_CITASK= 	TEAMCAT_BASE_URL + "api/ci/task_basic";
		public static final String GET_PROJECTDETAIL= 	TEAMCAT_BASE_URL+"api/project/";
		public static final String GET_TASKHISTORIES = 	TEAMCAT_BASE_URL;		
		public static final String GET_DICCONFIG= 	TEAMCAT_BASE_URL+"api/common/dicconfig/";
		public static final String PATCH_TASKQUEUE = 	TEAMCAT_BASE_URL + "api/common/task_queue";
		public static final String PATCH_TASKHISTORY = 	TEAMCAT_BASE_URL + "api/ci/task_history";
		public static final String PATCH_TASKHISTORYURL = 	TEAMCAT_BASE_URL + "api/ci/task/";
		public static final String POST_TASKFLOWHISTORYURL = 	TEAMCAT_BASE_URL + "api/ci/task_flow/";
		public static final String POST_TASKFLOWSECTIONHISTORYURL = 	TEAMCAT_BASE_URL + "api/ci/flow_history/";
		public static final String POST_TASKFLOWSECTIONHISTORYIDURL = 	TEAMCAT_BASE_URL + "api/ci/section_history/";
		public static final String SETOFFLINEAGENTID = 	TEAMCAT_BASE_URL + "api/common/agent";	
		public static final String SETOFFLINETASKQUEUES = 	TEAMCAT_BASE_URL + "api/common/task_queue";	
		public static final String GET_AGENTS = 	TEAMCAT_BASE_URL + "api/common/agents";
		public static final String GET_AGENT = 	TEAMCAT_BASE_URL + "api/common/agent";
		public static final String GET_PROJECTLIST = 	TEAMCAT_BASE_URL + "api/project/list";
		public static final String GET_PROJECT = 	TEAMCAT_BASE_URL + "api/project";
		public static final String GET_SECTIONTASKS = 	TEAMCAT_BASE_URL + "api/ci/task_flow/section/";
		public static final String GET_TASKFLOW = 	TEAMCAT_BASE_URL + "api/ci/task_flow/";
		public static final String GET_PROJECTISSUESTATUS = 	TEAMCAT_BASE_URL + "api/project/issue/status";
		public static final String GET_DAILYSTATISTICSBYDATE = 	TEAMCAT_BASE_URL + "api/project/issue/daily_statistics";
		public static final String GET_VERSIONSTATISTICSBY = 	TEAMCAT_BASE_URL + "api/project/issue/version_statistics";
		public static final String GET_SEVERITIES = 	TEAMCAT_BASE_URL + "api/project/issue/severities";
		public static final String GET_CATERGORIES = 	TEAMCAT_BASE_URL + "api/project/issue/categories";
		public static final String GET_RESOLVETYPES = 	TEAMCAT_BASE_URL + "api/project/issue/resolve_results";
		public static final String GET_PROJECT_VERSION = 	TEAMCAT_BASE_URL + "api/project/";
		public static final String GET_MEMBERS = TEAMCAT_BASE_URL + "api/project/project_members/";	
		public static final String POST_DAILY_STATISTICS = TEAMCAT_BASE_URL + "api/project/issue/daily_statistics";	
		public static final String POST_VERSION_STATISTICS = TEAMCAT_BASE_URL + "api/project/issue/version_statistics";	
		public static final String DEPLOY_SERVERS = TEAMCAT_BASE_URL + "api/ci/deploy_servers";
		public static final String DEPLOY_SERVICE = TEAMCAT_BASE_URL + "api/ci/deploy_service/";	
		public static final String CI_TASK_HISTORY = TEAMCAT_BASE_URL + "api/ci/task_history/";
		public static final String CI_TASK = TEAMCAT_BASE_URL + "api/ci/task/";
		public static final String TEST_TASK_HISTORY = TEAMCAT_BASE_URL + "api/ci/task_history/";
		public static final String AUTH_USER = TEAMCAT_BASE_URL + "api/auth/user/";
		public static final String PROJECT_VERSIONS = TEAMCAT_BASE_URL + "api/project/project_versions/";
		public static final String TQ_DONE = TEAMCAT_BASE_URL + "api/ci/task/tq_done";
		public static final String PARAMETER_GROUPS = TEAMCAT_BASE_URL + "api/ci/task/<task_id>/parameter_groups/";
		public static final String TESTING_RESULTS = TEAMCAT_BASE_URL + "api/ci/auto_testing_results";
		public static final String TASK_BASIC = TEAMCAT_BASE_URL + "api/ci/task_basic/";	
		public static final String CASE_RESULTS = TEAMCAT_BASE_URL + "api/ci/auto_case_results";
		public static final String CHANGE_LOG = TEAMCAT_BASE_URL + "api/ci/task_history/<history_id>/change_log";
		public static final String QR_CODE_IMG = TEAMCAT_BASE_URL + "/ci/history/download_package/mobile?file_id=$FileID&history_id=$HistoryID";
		public static final String RTX = "http://10.12.0.254:8012/SendNotify.cgi";
		public static final String DASHBOARD = TEAMCAT_BASE_URL + "ci/dashboard";
		public static final String PARAMETER_GROUP = TEAMCAT_BASE_URL + "api/ci/task/parameter_group/";
		public static final String TASK_RESULT = TEAMCAT_BASE_URL + "api/ci/auto_testing_results";
		public static final String CASE_RESULT = TEAMCAT_BASE_URL + "api/ci/auto_case_results";
		public static final String TEST_HISTORY = TEAMCAT_BASE_URL + "ci/testing/$CITaskID/history";
		public static final String CASETAGS = TEAMCAT_BASE_URL + "api/ci/case_tags";
		public static final String AUTOCASES = TEAMCAT_BASE_URL + "/api/ci/auto_cases";
		
	}
	
	public static final String TEAMCAT_BASE_URL = getProperty("INTERFACE_BASE_URL");
	public static final String EMAIL_IS_AUTH=getProperty("EMAIL_IS_AUTH");
	
		
		private static String getProperty(String property){
			try {
				Properties properties = new Properties();
				FileInputStream fis = new FileInputStream("controller.properties");
				properties.load(fis);  
				return properties.getProperty(property);
			} catch (Exception e) {
				return "";
			}
		}
}
