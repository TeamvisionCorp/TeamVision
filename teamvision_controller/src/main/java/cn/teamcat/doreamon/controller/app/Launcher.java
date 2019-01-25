package cn.teamcat.doreamon.controller.app;

import java.util.List;
import java.util.concurrent.RejectedExecutionHandler;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import com.google.common.util.concurrent.ThreadFactoryBuilder;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.config.GlobalConfig;
import cn.teamcat.doreamon.controller.flow.AgentDetecter;
import cn.teamcat.doreamon.controller.flow.DisasterDetecter;
import cn.teamcat.doreamon.controller.flow.IssueStatistics;
import cn.teamcat.doreamon.controller.flow.TaskAssign;
import cn.teamcat.doreamon.controller.flow.TaskClean;
import cn.teamcat.doreamon.controller.flow.TaskSend;
import cn.teamcat.doreamon.controller.flow.TaskSplit;
import cn.teamcat.doreamon.controller.flow.TaskTimeout;
import cn.teamcat.doreamon.controller.flow.Timer;
import cn.teamcat.doreamon.controller.flow.Unlock;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * Controller 入口
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class Launcher{
	static Logger log = Logger.getLogger(Launcher.class);
	static Launcher launcher = new Launcher();
	static HttpClientHelper http = new HttpClientHelper();

	/**
	 * 入口
	 * @param args
	 */

	public static void main(String[] args) {
//		Init.getInitInfo();
		GlobalConfig config = new GlobalConfig();
		int corePoolSize = Runtime.getRuntime().availableProcessors();//返回可用处理器的Java虚拟机的数量
		ThreadFactory tf = new ThreadFactoryBuilder().setNameFormat("FailureRetryTask-pool-%d").build();
		RejectedExecutionHandler handler=new ThreadPoolExecutor.AbortPolicy();
		ScheduledThreadPoolExecutor exec = new ScheduledThreadPoolExecutor(corePoolSize, tf,handler);//建立线程池
		exec.scheduleAtFixedRate(new Runnable() {//每隔一段时间就触发Controller
			@Override
			public void run() {
				try {
					Launcher.controller();
				} catch (Exception e) {
					// donothing
				}
			}
		}, 0,  config.getControllerInterval(), TimeUnit.MILLISECONDS);
		log.info("Controller"+config.getControllerInterval());
        exec.scheduleAtFixedRate(new Runnable() {//每隔一段时间就触发Timer
        	@Override
        	public void run() {
        		log.info("Timmer star");
        		try {
        			Timer timer = new Timer();
        			timer.detectCITask();
				} catch (Exception e) {
					// donothing
				}
        	}
        }, 0, config.getTimerInterval(), TimeUnit.MILLISECONDS);
        log.info("Timer"+config.getTimerInterval());
        exec.scheduleAtFixedRate(new Runnable() {//每隔一段时间就触发DisasterDetecter
            @Override
            public void run() {
            	log.info("DisasterDetecter star");
            	try {
            		DisasterDetecter detcter = new DisasterDetecter();
            		detcter.detectDisaterTask();
				} catch (Exception e) {
					// donothing
				}
            }
        }, 0, config.getDisasterInterval(), TimeUnit.MILLISECONDS);
        log.info("DisasterDetecter"+config.getDisasterInterval());
        exec.scheduleAtFixedRate(new Runnable() {//每隔一段时间就触发AgentDetcter
            @Override
            public void run() {
            	log.info("AgentDetcter star");
            	try {
            		AgentDetecter agentDetecter = new AgentDetecter();
            		agentDetecter.detectAlive();
				} catch (Exception e) {
					// donothing
				}
            }
        }, 0, config.getAgentDetcterInterval(), TimeUnit.MILLISECONDS);
        log.info("AgentDetcter"+config.getAgentDetcterInterval());
        exec.scheduleAtFixedRate(new Runnable() {//每隔一段时间就触发IssueStatstic
            @Override
            public void run() {
            	try {
            		IssueStatistics issueStatistics = new IssueStatistics();
            		issueStatistics.issueStatistics();
            		log.info("IssueStatstic"+"start");
				} catch (Exception e) {
					// donothing
				}
            }
        }, 0, config.getIssueInterval(), TimeUnit.MILLISECONDS);
        log.info("IssueStatstic"+config.getIssueInterval());
	}
	
	private static void controller() throws Exception{
		JSONObject response = http.gettaskqueues();
		JSONArray taskQueuelist = response.getJSONArray("result");
		try {
			log.info("Controller-开始运行");
			Unlock lock = new Unlock();
			lock.unlockQueue();			
			TaskTimeout timeout = new TaskTimeout();
			taskQueuelist = timeout.checkTimeout(taskQueuelist);
			log.info("size"+taskQueuelist);
			if(taskQueuelist.size()>0){
				TaskClean clean = new TaskClean();
				taskQueuelist = clean.clean(taskQueuelist);
				log.info("clean");
	    		if(taskQueuelist.size()>0){
	    			TaskSplit split = new TaskSplit();
	    			split.split(taskQueuelist);
	    			TaskAssign assign =new TaskAssign();
	    			taskQueuelist = assign.assign(taskQueuelist);
	    			TaskSend send = new TaskSend();
	    		    send.send(taskQueuelist);
	    		    log.info("send");
	    		}
	    			log.info("Controller-运行完毕");
			}else{
				log.info("Controller-运行完毕-任务队列中无新任务");
			}
		} catch (Exception e) {
			e.printStackTrace();
			log.error(Launcher.class,e);
		}finally{
			unlockTaskJSONObject(taskQueuelist);
		}
   }

	/**
	 * 解锁任务
	 * @param taskQMapper
	 * @param taskQueueList
	 */
	private static void unlockTaskJSONObject(JSONArray taskQueuelist) {
		for (int i = 0; i < taskQueuelist.size(); i++) {
			Integer taskQid = taskQueuelist.getJSONObject(i).getInt("id");
			Integer taskType = taskQueuelist.getJSONObject(i).getInt("TaskType");
			try {
				if (taskType!=DatasEnum.TaskType_Taskflow.getValue()&&taskType!=DatasEnum.TaskType_Tasksection.getValue()) {
					http.unlocktask(taskQid);
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				log.error(Launcher.class, e);
			}
		}
	}	
}

//	/**
//	 * 根据优先级获取任务队列
//	 * @param taskQMapper
//	 * @return
//	 */
//	private static List<TaskQueue> getTaskQueueList(TaskQueueMapper taskQMapper){
//		TaskQueueExample example = new TaskQueueExample();
//		example.createCriteria().andIslockedEqualTo(false).andStatusNotEqualTo(DatasEnum.TaskInQueueStatus_Disaster.getValue()).andParentidEqualTo(0);
//		example.setOrderByClause("Priority Desc");
//		return taskQMapper.selectByExample(example);
//}
