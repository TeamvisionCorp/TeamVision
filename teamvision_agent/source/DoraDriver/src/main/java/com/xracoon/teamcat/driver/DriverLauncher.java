package com.xracoon.teamcat.driver;

import java.awt.print.Printable;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

import com.xracoon.teamcat.utils.PropertiesTools;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.driver.args.DriverArg;
import com.xracoon.teamcat.utils.FileUtils;
import com.xracoon.util.basekit.ArraysEx;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.hudson.proc.Proc;

import net.sf.json.JSONObject;

public class DriverLauncher {
	public static class LaunchParams {
		// taskId, taskType, tqId, historyID, paramId, agnetId, workspace,
		// agentPort, toolpath
		private long taskId;
		private int taskType;
		private long tqId;
		private long historyId;
		private String paramId;
		private String testTaskResult;
		private String testCaseIDList;

		private int agentId;

		private int agentPort;
		private String workspace;
		private String toolPath;

		public LaunchParams() {
		};

		public LaunchParams(TaskInfo info, int agentPort, String workspace, String buildToolsPath) {
			taskId = info.taskID;
			taskType = info.taskType;
			tqId = info.taskQueueID;
			historyId = info.historyID;
			paramId = info.paramID;
			testTaskResult = info.testTaskResultID;

			agentId = info.agentID;

			this.agentPort = agentPort;
			this.workspace = workspace;
			this.toolPath = buildToolsPath;
		};

		public String toJson() {
			JSONObject json = JSONObject.fromObject(this);
			return json.toString();
		}

		public TaskInfo toTaskInfo() {
			TaskInfo info = new TaskInfo();
			info.taskID = taskId;
			info.taskType = taskType;
			info.taskQueueID = tqId;
			info.historyID = historyId;
			info.paramID = paramId;
			info.agentID = agentId;
			info.testTaskResultID = testTaskResult;
			return info;
		}

		public static LaunchParams fromJson(String json) {
			LaunchParams launchParams = (LaunchParams) JSONObject.toBean(JSONObject.fromObject(json),
					LaunchParams.class);
			return launchParams;
		}

		public long getTaskId() {
			return taskId;
		}

		public void setTaskId(long taskId) {
			this.taskId = taskId;
		}

		public int getTaskType() {
			return taskType;
		}

		public void setTaskType(int taskType) {
			this.taskType = taskType;
		}

		public long getTqId() {
			return tqId;
		}

		public void setTqId(long tqId) {
			this.tqId = tqId;
		}

		public long getHistoryId() {
			return historyId;
		}

		public void setHistoryId(long historyId) {
			this.historyId = historyId;
		}

		public String getParamId() {
			return paramId;
		}

		public void setParamId(String paramId) {
			this.paramId = paramId;
		}

		public int getAgentId() {
			return agentId;
		}

		public void setAgentId(int agentId) {
			this.agentId = agentId;
		}

		public int getAgentPort() {
			return agentPort;
		}

		public void setAgentPort(int agentPort) {
			this.agentPort = agentPort;
		}

		public String getWorkspace() {
			return workspace;
		}

		public void setWorkspace(String workspace) {
			this.workspace = workspace;
		}

		public String getToolPath() {
			return toolPath;
		}

		public void setToolPath(String toolPath) {
			this.toolPath = toolPath;
		}

		public String getTestTaskResult() {
			return testTaskResult;
		}

		public void setTestTaskResult(String testTaskResult) {
			this.testTaskResult = testTaskResult;
		}
	}

	static Logger logger = LoggerFactory.getLogger(DriverLauncher.class);
	static String agentHome;
	static {
		try {
			addJarsToPath();
		} catch (MalformedURLException | NoSuchMethodException | SecurityException | IllegalAccessException
				| IllegalArgumentException | InvocationTargetException e) {
			e.printStackTrace();
		}
	}
	private TaskInfo info;
	private Driver driver;
	private String workspace;
	private ArchiveManager archiveManager;
	private String toolLib;
	private String commonSpace;
	private String buildBackupSpace;

	private static void listJars(File file, List<URL> list) throws MalformedURLException {
		File[] files = file.listFiles();
		for (File f : files) {
			if (f.isDirectory())
				listJars(f, list);
			else if (f.isFile() && f.getName().toLowerCase().endsWith(".jar"))
				list.add(f.toURI().toURL());
		}
	}

	private static void addJarsToPath() throws MalformedURLException, NoSuchMethodException, SecurityException,
			IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		agentHome = PropertiesTools.basePath;
		logger.info("addJarsToPath agentHome : " + agentHome);
		File libPath = new File(agentHome, "libs");

		List<URL> urls = new ArrayList<>();
		listJars(libPath, urls);

		URLClassLoader loader = (URLClassLoader) DriverLauncher.class.getClassLoader();
		Class<URLClassLoader> sysclass = URLClassLoader.class;
		Method method = sysclass.getDeclaredMethod("addURL", new Class[] { URL.class });
		method.setAccessible(true);
		for (URL u : urls) {
			method.invoke(loader, u);
		}
	}

	public static void prepare(String workspace, boolean clean) throws Exception {
		logger.info("===>prepare workspace, clean: " + clean);

		File taskDir = new File(workspace);
		// 不存在则创建，结束
		if (!taskDir.exists()) {
			taskDir.mkdirs();
			return;
		}
		// 已经存在并且需要清理
		else if (clean) {
			FilesEx.deleteContent(taskDir);
			// 未删除成功时多次尝试
			int tryNum = 1;
			while (taskDir.list().length > 0 && tryNum++ < 5) {
				FilesEx.deleteContent(taskDir);
				Thread.sleep(2000);
			}
		}

		if (clean && taskDir.list().length != 0) {
			logger.warn("uncleanable file(s)");
			for (String s : taskDir.list())
				logger.warn("\t" + s);
		}
	}

	// 异常抓取与传递
	public static void main(String[] args) throws Exception {
		String errorMsg = "";
		TaskInfo info = null;
		try {
			logger.info("parse args: " + ArraysEx.join(args, ", "));
			// taskId, taskType, tqId, historyID, paramId, agnetId, workspace,
			// agentPort, toolpath
			//String jsonString = "{\"taskId\":1,\"taskType\":4,\"tqId\":311,\"historyID\":3457,\"paramId\":\"59264c646a3c277a69313b49\",\"agentId\":12,\"workspace\":\"/Users/ethan/Documents/teamcatspace\",\"agentPort\":5001,\"toolPath\":\"/Users/ethan\"}";
			//String jsonString = "{\"agentId\":9,\"agentPort\":9001,\"historyId\":4460,\"paramId\":\"\",\"taskId\":59,\"taskType\":1,\"testTaskResult\":\"2518\",\"toolPath\":\"/usr/local/src/jdk1.8.0_144\",\"tqId\":2072,\"workspace\":\"/home/gaozhenbin/teamcatagenttest/t59_InterfaceTestTask\"}";
			LaunchParams params=LaunchParams.fromJson(args[0]);
			//LaunchParams params = LaunchParams.fromJson(jsonString);
			info = params.toTaskInfo();
			BuildTools bt = BuildTools.search(params.toolPath);

			// 查询构建和部署配置
			WebService.queryTaskConfig(info);
			info.options.put(Driver.ENV_BUILDTOOLS, bt);

			DriverLoader driverLoader = new DriverLoader(agentHome);
			driverLoader.setLogger(logger);
			Driver driver = driverLoader.loadDriver(info.taskType);
			// 加载Driver
			logger.info("driver instance : " + driver);

			DriverLauncher launcher = new DriverLauncher(info, params.workspace, params.getToolPath(), driver);
			errorMsg = launcher.runDriver();

			if (errorMsg != null) {
				DriverLauncher.sendErrorMsg(info.taskQueueID, errorMsg);
				logger.error("");
				System.exit(-1);
			}

		} catch (Exception e) {
			logger.error("exception when run task", e);
			errorMsg = e.getMessage() + (errorMsg != null ? "\n" + errorMsg : "");
			DriverLauncher.sendErrorMsg(info.taskQueueID, errorMsg);
			throw e;
		}
	}

	public static void sendErrorMsg(long tqId, String msg) {
		String message= "{cmd: \"RUNERROR\", tqId: " + tqId + ", msg: \"" + msg.replaceAll("\n", "{\\n}") + "\"}";
		try {
			WebService.sendErrorMsg(message);
		} catch (Exception e) {
			logger.error("Send ErrMessage Failed ErrInfo: "+e);
		}
	}

	public DriverLauncher(TaskInfo info, String workspace, String toolpath, Driver driver) {
		this.info = info;
		setTaskBuildID();
		this.workspace = workspace;
		this.driver = driver;
		this.toolLib = toolpath;
		this.commonSpace = workspace.replace("t" + String.valueOf(info.taskID) + "_" + info.taskConfig.getTaskName(),
				"") +FileUtils.getSlash()+"CommonSpace";
		this.buildBackupSpace = this.commonSpace + FileUtils.getSlash() + String.valueOf(info.taskID) + "_"
				+ info.taskConfig.getTaskName() + "_" + String.valueOf(info.taskConfig.getBuildId());
		archiveManager = new WebApiArchiveManager(info);
	}

	public String runDriver() throws Exception {
		// workspace
		prepare(workspace, true);
		prepare(this.commonSpace, false);
		prepare(this.buildBackupSpace, false);

		driver.setWorkspace(workspace);
		driver.setTaskConfig(info.taskConfig);
		driver.setEnvs(info.options);
		driver.setNotifier(new AgentNotifierImpl());

		// 设置env变量
		info.options.put(Driver.ENV_WORKSPACE, workspace);
		info.options.put(Driver.ENV_NOTIFIER, driver.getNotifier());
		info.options.put(Driver.ENV_TASKCONFIG, info.taskConfig);
		info.options.put(Driver.ENV_HISTORYID, info.historyID);

		if (!StringEx.isBlank(info.testTaskResultID))
			info.options.put(Driver.ENV_TESTRESULTID, info.testTaskResultID);

		// 查询lastVersion
		try {
			info.options.put(Driver.ENV_LASTVERSION, WebService.getLastVersion(info.taskID));
		} catch (Exception e0) {
			logger.error("exception when query last version", e0);
		}

		// 查询Parameters
		this.setGlobalVariables();

		// 打印任务信息
		printTaskSummary();

		if (!driver.init())
			throw new Exception("driver initialize failed");

		String message = "";
		boolean ret = false;

		ret = driver.exec();
		if (driver.getMessage() != null && driver.getMessage().trim().length() > 0)
			message = ret + " " + (message == null ? "" : message) + ": " + driver.getMessage();

		// 上传文件(Notifier中完成)
		// tqdone (Agent端实现)

		return ret ? null : message;
	}

	private void setTaskBuildID() {
		// 查询buildId
		try {
			System.out.println(info);
			this.info.taskConfig.setBuildId(WebService.getCurrentBuildId(this.info.taskID));
			logger.info("current build id " + info.taskConfig.getBuildId());
		} catch (Exception e0) {
			logger.error("exception when query build id", e0);
		}
	}

	private void setGlobalVariables() {
		Map<String, String> tokens = new LinkedHashMap<>();
		tokens.put(Driver.TOK_WORKSPACE, workspace);
		tokens.put(Driver.TOK_BUILDTOOL, this.toolLib);
		tokens.put(Driver.TOK_BUILDVERSION, info.taskConfig.getBuildId());
		tokens.put(Driver.TOK_COMMONSPACE, this.commonSpace);
		tokens.put(Driver.TOK_BUILDBACKUPSPACE, this.buildBackupSpace);
		tokens.put(Driver.TOK_HISTORYID,String.valueOf(this.info.historyID));
		// tokens.put(Driver.TOK_DEPLOYPATH,info.taskConfig.getDeployInfo().getDeployDir());
		tokens.put(Driver.TOK_TASKID, String.valueOf(info.taskConfig.getTaskId()));
		tokens.put(Driver.TOK_TASKNAME, info.taskConfig.getTaskName());
		info.options.put(Driver.ENV_TOKENS, tokens);
		this.printGlobalVariables(tokens);
		try {
			tokens.putAll(WebService.getParameters(info.paramID));
			if (tokens.containsKey(Driver.TOK_PARAMGROUP)) {
				info.taskConfig.setTokenGroup(tokens.remove(Driver.TOK_PARAMGROUP));
			}
		} catch (Exception e0) {
			logger.error("exception when query parameters", e0);
		}
	}

	private void printGlobalVariables(Map<String, String> tokens) {
		logger.info("---------------------------------------------");
		logger.info("-------------Global Variables---------------------");
		for (String key : tokens.keySet()) {
			logger.info(key + ": " + tokens.get(key));
		}
	}

	public void printTaskSummary() {
		logger.info("---------------------------------------------");
		logger.info("\t task detail");
		logger.info("---------------------------------------------");
		logger.info("taskId:\t" + info.taskID);
		logger.info("taskName:\t" + info.taskConfig.getTaskName());
		// logger.info("taskRun:\t"+info.runUUID);
		logger.info("taskQueueId:\t" + info.taskQueueID);
		logger.info("taskType:\t" + info.taskType);
		logger.info("taskBuildId:\t" + info.taskConfig.getBuildId());
		logger.info("paramGroup:\t" + info.taskConfig.getTokenGroup());
		logger.info("driverOptions:\t" + info.options.get(DriverArg.DRIVERARG));
		logger.info("---------------------------------------------");
		logger.info("---------------------------------------------");
	}

	public class AgentNotifierImpl implements AgentNotifier {
		private Logger logger = LoggerFactory.getLogger(AgentNotifier.class);

		@Override
		public boolean reportCaseStatus(Long caseId, String caseName, Date start, Date end, int result, String error,
				String trace) {
			logger.info("simulate insert case:  " + caseId + ",  " + result + ", " + caseName + ",  start@" + start
					+ ", end@" + end + ", error@" + error + ", trace@" + trace);
			return true;
		}

		@Override
		public boolean requestArchive(String file, int type) {
			archiveManager.processArchiveRequest(file, type);
			return true;
		}
	}

	static Proc p = null;

	public static void killTest() throws IOException, InterruptedException {
		final Timer timer = new Timer(false);
		timer.schedule(new TimerTask() {
			@Override
			public void run() {
				try {
					if (p != null)
						p.kill();
					System.out.println("kill....");
				} catch (Exception e) {
					e.printStackTrace();
				}
				timer.cancel();
			}
		}, 5000, 5000);

		String[] cmds = new String[] { "cmd.exe", "/c", "call", "F:/Temp/startcmd.bat" };
		// 必须是System.in才能kill掉
		p = new Proc.LocalProc(cmds, null, System.in, null, null, null, logger, true);
		p.join();

		System.out.println("Done");
	}

	public static void runProcessTest() throws IOException, InterruptedException {
		String[] cmds = new String[] { "cmd.exe", "/c", "call", "F:/Temp/startcmd.bat" };
		// 必须是System.in才能kill掉
		p = new Proc.LocalProc(cmds, null, System.in, null, null, null, logger, true);
		p.join();

		System.out.println("Done");
	}
}
