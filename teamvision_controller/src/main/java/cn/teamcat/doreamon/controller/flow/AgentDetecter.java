package cn.teamcat.doreamon.controller.flow;

import java.util.List;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import cn.teamcat.doreamon.controller.tools.SocketHelper;
import net.sf.json.JSONObject;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.zxing.Result;
import com.mysql.fabric.Response;
import com.google.gson.Gson;

/**
 * Agent 监控
 * 
 * @author Sirui.Zhang，Siyuan.Lu
 *
 */
public class AgentDetecter {
	Logger log = Logger.getLogger(AgentDetecter.class);
	private HttpClientHelper http = new HttpClientHelper();

	/**
	 * 心跳监测
	 * 
	 * @throws Exception
	 */
	public void detectAlive() throws Exception {
		log.info("AgentDetecter-开始运行");
		log.info("获取在线agent");
		JSONObject agents_response = http.getAgentOnline();
		log.info("获取在线agent");
		JSONArray agentList = agents_response.getJSONArray("result");
		for (int i = 0; i < agentList.size(); i++) {
			Integer agentId = agentList.getJSONObject(i).getInt("id");
			detect(agentId);
		}
		log.info("AgentDetecter-运行完毕");
	}

	/**
	 * 发送心跳
	 * 
	 * @param agentId
	 * @throws Exception
	 */
	private void detect(Integer agentId) {
		String cmd = Constants.ALIVE_CMD;
		JSONObject reponse = new JSONObject();
		try {
			reponse = HttpClientHelper.postMq("CI_AGENT_" + agentId.toString(), cmd);
		} catch (Exception e) {
			log.info(Constants.MQ_TIMEOUT_ERROR);
			e.printStackTrace();
		}
		try {
			int delivered_count = reponse.getJSONObject("result").getInt("delivered_count");
			if (delivered_count != 0) {
				log.info("AgentID：" + agentId + " 连接成功");
			} else {
				http.setofflineagentId(agentId);
				log.error("AgentID：" + agentId + " 无法连接");
				JSONObject Taskqueues_response = http.getTaskqueuesId(agentId);
				log.info("无法连接的agent上任务列表为" + "+++++++++" + Taskqueues_response);
				JSONArray TaskqueuesList = Taskqueues_response.getJSONArray("result");
				if (TaskqueuesList.size() > 0) {
					log.info("挂掉的机器上还有正在执行的任务！");
					for (int j = 0; j < TaskqueuesList.size(); j++) {
						Integer taskQueueId = TaskqueuesList.getJSONObject(j).getInt("id");
						log.info("taskqueueId" + taskQueueId);
						detecttaskQueue(taskQueueId);
					}

				}

			}

		} catch (Exception e) {
			e.printStackTrace();
			log.info("Mq connect error");
		}
	}

	private void detecttaskQueue(Integer taskQueueId) {
		try {
			Integer statuecode = http.setstatustaskqueueId(taskQueueId, DatasEnum.TaskInQueueStatus_Error.getValue());
			log.info("statue9 code" + statuecode);
			Integer errorcode = http.seterrormsgtaskqueueId(taskQueueId, Constants.RUNNING_ERROR);
			log.info("seterror code" + errorcode);
			http.setTaskdone(taskQueueId, DatasEnum.TaskInQueueStatus_Error.getValue(), Constants.RUNNING_ERROR);
			log.info("setTaskdone tqdone");
		} catch (Exception e) {
			try {
				http.setstatustaskqueueId(taskQueueId, DatasEnum.TaskInQueueStatus_Disaster.getValue());
			} catch (Exception e2) {
			}
		}
	}
}
