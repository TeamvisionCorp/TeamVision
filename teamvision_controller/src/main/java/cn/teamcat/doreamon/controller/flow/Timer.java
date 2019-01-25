package cn.teamcat.doreamon.controller.flow;

import java.text.ParsePosition;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.EmailHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;

/**
 * 扫描定时任务并将其添加到任务队列
 * 
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class Timer {
	public static CommonUtil util = new CommonUtil();
	private static Logger log = Logger.getLogger(Timer.class);
	private static HttpClientHelper http = new HttpClientHelper();
	private static List<JSONObject> timingtasklist= new ArrayList<JSONObject>();
	private static List<JSONObject> looptasklist= new ArrayList<JSONObject>();

	/**
	 * 监听CI任务 @throws
	 */
	public void detectCITask() {
		log.info("Timer-开始运行");
		JSONObject respose;
		try {
			respose = http.getci_tasklist();
			JSONArray taskresults = respose.getJSONObject("result").getJSONArray("results");
			log.info(respose);
			Date now = util.getUTCDate();
			if (taskresults.size() > 0) {
				for (int i = 0; i < taskresults.size(); i++) {
					JSONObject task = taskresults.getJSONObject(i);
					String schedule = taskresults.getJSONObject(i).getString("Schedule");
					if (schedule.length() == 8 && isFormatRight(schedule, "..:..:..") && !schedule.equals("**:**:**")) {					
						processScheduleCITask(task, schedule,now);				
					}
				}
				if (timingtasklist.size()>0) {
					for (int j = 0; j < timingtasklist.size(); j++) {
						try {
							insertScheduleCITask(timingtasklist.get(j), now);
						} catch (Exception e) {
							log.info(e);
						timingtasklist.remove(timingtasklist.get(j));
						}
						timingtasklist.remove(timingtasklist.get(j));
					}
				}
				if (looptasklist.size()>0) {
					for (int j = 0; j < looptasklist.size(); j++) {
						try {
							insertScheduleCITask(looptasklist.get(j), now);
						} catch (Exception e) {
							log.info(e);
						looptasklist.remove(looptasklist.get(j));
						}
						looptasklist.remove(looptasklist.get(j));
					}
				}
			}
		} catch (Exception e) {
			log.error("Timer-运行完毕 出现异常", e);
		} finally {
			log.info("Timer-运行完毕");
		}
	}

	/**
	 * 处理定时任务
	 * 
	 * @param taskMapper
	 * @param taskQMapper
	 * @param historyMapper
	 * @param task
	 * @param schedule
	 * @throws Exception
	 */
	private static void processScheduleCITask(JSONObject task, String schedule, Date now) throws Exception {
		if (!schedule.contains("*")) {
			long differenceTime = getTime(8) - getMillTime(schedule);
			if (differenceTime <= 2500 && differenceTime >= -2500)
				timingtasklist.add(task);
		} else if (schedule.contains("*")) {
			long formatSchedule = getScheduleTime(schedule);
			if (task.getString("LastScheduleRunTime") != null) {
				String date = task.getString("LastScheduleRunTime");
				
				String dateformate = date.substring(0, 19)+".000 CST";	
				SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS Z");
				
				Date d = format.parse(dateformate);
				System.out.println("!!!!!!!!!!!!"+dateformate);
				if (now.getTime() - d.getTime() >= formatSchedule) {
				System.out.println("定时运行时间到了！");
					looptasklist.add(task);
				}
			} else {
				String date = task.getString("CreateTime");
				String dateformate = date.substring(0, 19)+".000 CST";
//			    date = date.replace("000+08:00", " CST");
//				String dateregular = getLastScheduletime(date);				
//				String date2 = dateregular+" CST";	
				System.out.println("!!!!!!!!!!!!"+dateformate);
				SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS Z");
				Date d = format.parse(dateformate);
				if (now.getTime() - d.getTime() >= formatSchedule)
					looptasklist.add(task);

			}
		}
	}
	
	//正则表达式取EnqueueTime，期望取出来的结果为：2018-09-07T17:20:27
	public static String getLastScheduletime(String LastScheduleRunTime) {		
	     String regex = "[\\d\\d\\d\\d\\-\\d\\d\\-\\d\\d\\w\\d\\d\\:\\d\\d\\:\\d\\d]{19}";
	     Pattern p = Pattern.compile(regex);
	     Matcher m = p.matcher(LastScheduleRunTime);
	     // 循环，如果匹配正则，则打印输出
	     while (m.find()) {
	     System.out.println(m.group());
	     }
		 return m.group();
	     }
		
	public static List<String> getStrList(String inputString, int length) {
		int size = inputString.length() / length;
		if (inputString.length() % length != 0) {
			size += 1;
		}
		return getStrList(inputString, length);
	}

	/**
	 * 处理指定时间任务
	 * 
	 * @param taskMapper
	 * @param taskQMapper
	 * @param task
	 * @param taskSchedule
	 * @param runtime
	 * @throws Exception
	 */
	private static void insertScheduleCITask(JSONObject task, Date runtime) throws Exception {
		Integer taskId = task.getInt("id");
		Integer taskType = task.getInt("TaskType");
		Integer BuildVersion = task.getInt("BuildVersion");
		String TaskName = task.getString("TaskName");
		log.info("!" + taskId + "!" + taskType + "!" + BuildVersion + "!" + TaskName);
		log.info("taskId:" + taskId + " 指定时间已到，开始入列流程");
		if (taskType != DatasEnum.TaskType_Deploy.getValue()) {
			SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
			String runtimeString = String.valueOf(simpleDateFormat.format(runtime));
			http.updateTaskruntime(taskId, runtimeString,BuildVersion+1);
			String buildparameterid = setBuildParameterid(taskId);
			JSONObject taskQ = insertTaskQueue(taskId, taskType, buildparameterid);
			log.info("插入taskqueues成功");
			Integer taskhistoryId = insertCITaskHistory(taskQ, task, taskId, buildparameterid);
			updateCITasklastHistory(taskId, taskhistoryId);
		} else {
			log.info("taskId:" + taskId + "已在队列中存在");
		}
	}

	public static Long getScheduleTime(String schedule) {
		String[] sch = schedule.split(":");
		List<Integer> timeList = new ArrayList<Integer>();
		for (int i = 0; i < sch.length; i++) {
			String str = sch[i];
			if (str.contains("**")) {
				timeList.add(0);
			} else {
				str = str.replace("*", "");
				timeList.add(Integer.valueOf(str));
			}
		}
		long sec = (timeList.get(0) * 3600 + timeList.get(1) * 60 + timeList.get(2)) * 1000;
		return sec;
	}

	/**
	 * 插入任务历史记录
	 * 
	 * @param taskQMapper
	 * @param historyMapper
	 * @param taskQ
	 * @param task
	 * @param taskId
	 * @param buildparameterid
	 * @return
	 * @throws Exception
	 */
	public static Integer insertCITaskHistory(JSONObject taskQ, JSONObject task, Integer taskId,
			String buildparameterid) throws Exception {
		Integer taskhistoryid = null;
		try {
			JSONObject params = new JSONObject();
			params.put("BuildStatus", 0);
			params.put("BuildLog", 0);
			params.put("TaskQueueID", taskQ.getInt("id"));
			params.put("TaskUUID", taskQ.getString("TaskUUID"));
			params.put("Command", DatasEnum.TQCommandType_Start.getValue());
			params.put("IsLocked", false);
			params.put("Priority", 2);
			int buildVersion = task.getInt("BuildVersion")+1;
			if (buildVersion == 0)
				buildVersion = 1;
			params.put("ProjectVersion", http.getProjectVersion(task.getInt("Project")));
			params.put("BuildVersion", buildVersion);
			params.put("StartedBy", 0);
			params.put("CITaskID", taskId);
			if (!buildparameterid.equals(""))
				params.put("buildparameterid", 2);
			JSONObject response = HttpClientHelperBasic.postobj(Constants.API.CITASK + taskId + "/task_histories/",
					params);
			taskhistoryid = response.getJSONObject("result").getJSONObject("all_histories").getInt("id");
			log.info("插入taskhistroy成功");
		} catch (Exception e) {
			log.info(e.getMessage());
			log.error(e.getMessage());
			EmailHelper email = new EmailHelper();
			email.sendErrorMail(task);
		}
		return taskhistoryid;
	}

	/**
	 * 更新citask LastHistory
	 * 
	 * @param updateCITasklastHistory
	 * @param taskhistoryId
	 * @throws Exception
	 */
	public static void updateCITasklastHistory(Integer taskId, Integer taskhistoryId) throws Exception {
		try {
			JSONObject params = new JSONObject();
			params.put("LastHistory", taskhistoryId);
			JSONObject response = HttpClientHelperBasic.patchobj(Constants.API.CITASBASIC + taskId + "/", params);
			log.info("TaskHistory" + response);
		} catch (Exception e) {
			log.info(e.getMessage());
			log.error(e.getMessage());
		}
	}

	/**
	 * 添加任务至任务队列
	 * 
	 * @param taskMapper
	 * @param taskQMapper
	 * @param taskId
	 * @param taskType
	 * @return
	 * @throws Exception
	 */
	public static JSONObject insertTaskQueue(Integer taskId, Integer taskType, String buildparameterid)
			throws Exception {
		JSONObject params = new JSONObject();
		String uuid =UUID.randomUUID().toString();
		params.put("TaskID", taskId);
		params.put("Status", DatasEnum.TaskInQueueStatus_NoProcess.getValue());
		params.put("TaskType", taskType);
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		params.put("EnqueueTime", runtimeString+"+00:00");
		params.put("TaskUUID", uuid);
		params.put("Command", DatasEnum.TQCommandType_Start.getValue());
		params.put("IsLocked", false);
		params.put("Priority", 2);
		if (!buildparameterid.equals("")) {
		params.put("BuildParameterID", buildparameterid);
		}
		System.out.println(params);
		JSONObject aJsonObject =HttpClientHelperBasic.postobj(Constants.API.GET_AGENTTASK, params);
		System.out.println(aJsonObject);
		JSONObject result = aJsonObject.getJSONObject("result");
		return result;
	}

	public static String setBuildParameterid(int taskId) throws Exception {
		String buildParameterid = "";
		JSONArray paramList = http.getParameter(taskId);
		if (paramList.size() > 0) {
			for (int i = 0; i < paramList.size(); i++) {
				JSONObject param = paramList.getJSONObject(i);
				if (param.getBoolean("is_default")) {
					buildParameterid = param.getString("id");
					break;
				}
			}
		}
		return buildParameterid;
	}

	private static Long getMillTime(String date) throws Exception {
		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
		long millionSeconds = sdf.parse(date).getTime();
		return millionSeconds;
	}

	private Long getTime() throws Exception {
		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
		String strs = sdf.format(util.getUTCDate());
		return getMillTime(strs);
	}

	private static Long getTime(Integer timeDiff) throws Exception {
		SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
		Date nowDate = util.getUTCDate();
		Calendar rightNow = Calendar.getInstance();
		rightNow.setTime(nowDate);
		rightNow.add(Calendar.HOUR_OF_DAY, timeDiff);// 日期加减小时
		String strs = sdf.format(rightNow.getTime());
		System.out.println(strs);
		return getMillTime(strs);
	}

	private static Boolean isFormatRight(String str, String regEx) {
		Pattern p = Pattern.compile(regEx);
		Matcher m = p.matcher(str);
		boolean result = m.find();
		return result;
	}
}