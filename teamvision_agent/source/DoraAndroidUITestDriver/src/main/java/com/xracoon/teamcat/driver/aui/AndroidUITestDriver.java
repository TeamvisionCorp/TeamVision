package com.xracoon.teamcat.driver.aui;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import org.apache.commons.io.IOUtils;

import com.xracoon.teamcat.agent.apppackage.PackageInspector;
import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.driver.CaseAssign;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.args.DriverArg;
import com.xracoon.teamcat.driver.aui.casequeue.CaseQueue;
import com.xracoon.teamcat.driver.aui.caserun.CaseExecutor;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestStatus;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class AndroidUITestDriver extends Driver {
	private List<CaseExecutor> executors=new ArrayList<CaseExecutor>();
	private OS os;
	private volatile boolean isStop=false;
	private final static String UtilApp="com.xracoon.wifisetter";
	private final static File wifiSetterfile=new File("res/WifiSetter-release.apk");
	private String testApp;
	private String targetApp;
	private String testRunner;
	private String logcatFilter="AAAAAA";
	private List<Device> devices;
	
	@Override
	public boolean init() 
	{
		logger.info("androidUITestDriver init");
		try {
			if(this.getNotifier()==null)
				throw new Exception("agent notifier is null");
			
			String driverArgs=(String) env.get(DriverArg.DRIVERARG);
			Device device=this.getDevice();
			int wifiTimeout=(int) env.get(DriverArg.WIFITIMEOUT);
			
			@SuppressWarnings("unchecked")
			Map<String,String> hostMap=(Map<String, String>) env.get(DriverArg.HOSTMAP);
			
			Map<String,String> args=getDriverArgs(driverArgs);
			String testPackageUrl=args.get("testPackageUrl");
			String appPackageUrl=args.get("appPackageUrl");
			String wifi_ssid=args.get("wifi_ssid");
			String wifi_pw=args.get("wifi_pw");
			String wifi_user=args.get("wifi_user");
			
			String filter=args.get("logcat_filter");
			if(filter!=null && filter.trim().length()>0)
				logcatFilter=args.get("logcat_filter");
			
			String testPackage=workspace+File.separator+getFileName(testPackageUrl);
			String appPackage=workspace+File.separator+getFileName(appPackageUrl);
			
			if(isStop)
				return false;
			
			download(testPackageUrl, testPackage);
			download(appPackageUrl, appPackage);
			
			//分析用例
//			TestProjectParser projParser=new TestProjectParser();
//			ManifestInfo minfo=projParser.parseManifest(codePath);
//	    	TestSuite suite= projParser.parsePath(codePath+File.separator+"src",includes, excludes);	 	
					
			//测试应用包信息查询
			os=this.getOs();
			PackageInspector apkInspector=new PackageInspector(os);
			String suiteFile=workspace+File.separator+"testsuite.xml";
			apkInspector.extractFileFromApk(testPackage, "testsuite.xml",suiteFile );
			
			if(isStop)
				return false;
			
			ReportHelper creator=new ReportHelper();
			TestSuite testsuiteAll=creator.loadReport(suiteFile);
			testApp=testsuiteAll.testApp;
			targetApp=testsuiteAll.targetApp;
			testRunner=testsuiteAll.testRunner;

				
//			ApkInfo testApkInfo=apkInspector.getApkInfo(testPackage);
//			ApkInfo appInfo=apkInspector.getApkInfo(appPackage);
			
			if(isStop)
				return false;
			
			//多设备处理（通过参数传入设备和用例映射）
			devices=new ArrayList<Device>();
			if(device!=null)
				devices.add(device);

			if(devices==null || devices.size()==0)
				throw new Exception("device not found on this agent");
			
			for(Device dev: devices)
			{
				if(wifi_ssid!=null && wifi_ssid.trim().length()>0)
					wifiPrepare(dev, wifi_ssid, wifi_user, wifi_pw, wifiTimeout); 
				
				if(hostMap!=null)
					checkHosts(dev,hostMap);
					
				if(isStop)
					return false;
				
				//安装
				dev.removeApp(testApp);
				dev.installApp(testPackage);
				dev.removeApp(targetApp);
				dev.installApp(appPackage);
			}
			
		} catch (Exception e) 
		{
			logger.error(e.getMessage(), e);
			setMessage("AndroidUITestDriver Init Error: "+e.getMessage());
			return false;
		}
		
		this.isInit=true;
		return true;
	}
	
	private TestSuite getTestSuite() throws Exception
	{
		if(!this.isInit)
			throw new Exception("driver does't have be initialized");
		
		Collection<CaseAssign> caseList=caseMap.values();
		
		TestSuite testsuite=null;
		if(caseList!=null && caseList.size()>0)
		{
			testsuite=parseCaseList(caseList);
			testsuite.targetApp=targetApp;
			testsuite.testApp=testApp;
			testsuite.testRunner=testRunner;
		}
		else
			//testsuite=testsuiteAll;
			throw new Exception("no testcase specified");
		
		return testsuite;
	}
	
	private TestSuite parseCaseList(Collection<CaseAssign> caseList)
	{
		TestSuite suite=new TestSuite("partial_testsuite");
		for(CaseAssign ca:caseList)
		{
			TestCase tcase=new TestCase();
			tcase.id=ca.getCaseId();
			String caseFullName=ca.getFullCaseName();
			int methodNameIdx = caseFullName.indexOf("#");
			int classNameIndex = caseFullName.lastIndexOf(".");	
			tcase.name = caseFullName.substring(methodNameIdx+1);
			tcase.className = caseFullName.substring(classNameIndex+1,methodNameIdx);
			tcase.packName = caseFullName.substring(0,classNameIndex);
			suite.put(tcase);
		}
		return suite;
	}
	
	private void wifiPrepare(Device dev, String wifi_ssid, String wifi_user, String wifi_pw, int wifiTimeout) throws Exception
	{
		//Wifi设置
		if(!dev.isAppInstalled(UtilApp))
		{
			logger.info("install WifiSet App");
			if(wifiSetterfile.exists())
				dev.installApp(wifiSetterfile.getAbsolutePath());
			else
				throw new Exception("WifiSetter app file not found at : "+wifiSetterfile.getAbsolutePath());
		}
		
		String userOption="";
		ExecStatus teststat=dev.synShellExec("am");
		if(teststat!=null && teststat.getLog().contains("--user"))
			userOption= " --user 0 ";
				
		logger.info("start WifiSet Service...");
		ExecStatus stat=dev.synShellExec("am startservice "+userOption+" -n com.xracoon.wifisetter/.WifiSetService");
		logger.info(stat.getLog().trim());
		if(stat.getError()!=null && stat.getError().trim().length()>0)
			logger.error(stat.getError().trim());
		
		logger.info("send Wifi config to WifiSet Service...: ssid="+wifi_ssid+", passwd= ****** , user="+wifi_user );
		String strUser="";
		if(wifi_user!=null && wifi_user.trim().length()>0)
			strUser=" --es user "+wifi_user;
		stat=dev.synShellExec("am broadcast -a com.xracoon.wifisetter.CONFIG_BROADCAST --es ssid "+wifi_ssid+" --es pw "+wifi_pw+strUser);
		logger.info(stat.getLog().trim());
		if(stat.getError()!=null && stat.getError().trim().length()>0)
			logger.error(stat.getError().trim());
		
		if(stat.getRetVal()!=0 || !stat.getLog().contains("Broadcast completed: result=1"))
			throw new Exception("wifi config Failed! ");
		
		int trycount=5;
		long timelit=Math.round(wifiTimeout*1.0/trycount);
		boolean connected=false;
		for(int count=0;count<trycount;count++)
		{
			logger.info("Wifi connect check... try "+(count+1));
			ExecStatus status=dev.synShellExec("am broadcast -a com.xracoon.wifisetter.QUERY_BROADCAST --es ssid "+wifi_ssid);
			logger.info(stat.getLog().trim());
			if(stat.getError()!=null && stat.getError().trim().length()>0)
				logger.error(stat.getError().trim());
			if(status.getRetVal()==0 && status.getLog().contains("Broadcast completed: result=1"))
			{
				connected=true;
				logger.info("Connected to  Wifi  '"+wifi_ssid+"' Successful");
				break;
			}
			Thread.sleep(timelit);
		}
		if(!connected)
			throw new Exception("Connect to  Wifi "+wifi_ssid+" Failed");
	}
	
	private void checkHosts(Device dev, Map<String,String> hostmap) throws Exception
	{
		logger.info("checkHosts... ");
		
		//拆分一行的多个host名
		Map<String,String> splitedHostMap=new LinkedHashMap<String, String>();
		for(Entry<String,String> entry: hostmap.entrySet())
		{
			String[] hosts=entry.getKey().split("\\s+");
			for(String h:hosts)
				if(h.trim().length()>0)
					splitedHostMap.put(h, entry.getValue());
		}
		
		
		for(Entry<String,String> entry: splitedHostMap.entrySet())
		{
			String host=entry.getKey();
			String ip=entry.getValue().trim();
			String actual="null";
			String cmd="am broadcast -a com.xracoon.wifisetter.QUERY_HOST --es host "+host+" --es ip "+ip;
			logger.info(cmd);
			ExecStatus status=dev.synShellExec(cmd);
			logger.info(status.getLog().trim());
			if(status.getError()!=null && status.getError().trim().length()>0)
				logger.error(status.getError().trim());
			String log=status.getLog();
			
			if(log.contains("["))
				actual=log.substring(log.indexOf("[")+1,log.indexOf("]"));
			if(status.getRetVal()!=0 || !status.getLog().contains("Broadcast completed: result=1"))
				throw new Exception("host verify exception: "+host+", expect: "+ip +", actual: "+actual);
				
			logger.info("ip of host '"+host+"' match '"+actual+"'");
		}
	}
	
	@Override
	public boolean exec() {
		logger.info("androidUITestDriver  exec");
		try {
			if(!this.isInit)
				throw new Exception("driver have not been initialized");
			
			if(isStop)
				return false;
			
			TestSuite testsuite=getTestSuite();
			CaseQueue caseQueue=new CaseQueue(testsuite);
			launch(caseQueue,devices,testsuite.testApp,testsuite.targetApp,testsuite.testRunner);
			
		} catch (Exception e) 
		{
			logger.error(e.getMessage(), e);
			setMessage("AndroidUITestDriver exec error: "+e.getMessage());
			return false;
		}
		
		return true;
	}

//	private void launchSingle(CaseQueue caseQueue, Device dev, String testApp, String testRunner)
//	{
//		CaseExecutor executor=new CaseExecutor(caseQueue,dev.getSerialNo(),testApp,testRunner);
//		executor.addTestListener(this);
//		executor.run();
//	}
	
	/**
	 * 有多少个设备，启动多少个执行线程。公用一个Case队列。
	 * @param testRunner 
	 * @param testApp 
	 */
	private void launch(CaseQueue caseQueue, List<Device> devices, String testApp, String targetApp, String testRunner) 
	{
		try 
		{
			for(Device dev:devices)
			{
				CaseExecutor executor=new CaseExecutor(os,caseQueue,dev,testApp,targetApp,testRunner,logcatFilter);
				executor.setLogger(logger);
				executor.addTestListener(new TestListenerImpl());
				executors.add(executor);
				//executor.start();
				executor.run();
			}
			boolean isDone=true;
			do
			{
				isDone=true;
				for(CaseExecutor exec:executors)
				{
					if(isStop)
					{
						exec.stopTest();
						exec.stop();
					}
						
					isDone&=exec.isDone();
					if(!isDone)
					{
						Thread.sleep(2000);
						break;
					}
				}
			}while(!isDone && !isStop);
			
		} catch (InterruptedException e) {
			logger.error(e.getMessage(), e);
		}
	}
	
	@Override
	public boolean stop() {
		
		isStop=true;
		for(CaseExecutor exec:executors)
		{
			exec.stopTest();
			exec.stop();
		}
		return true;
	}
	
	private void download(String url, String path) throws Exception
	{
		InputStream in=null;
		OutputStream out=null;
		try {
			logger.info("download package: "+url+"==>"+path);
			in = new URL( url ).openStream();
			out=new FileOutputStream(path);
			IOUtils.copy(in, out);
			logger.info("download package: Done");
		} catch (Exception e) {
			throw e;
		}
		finally
		{
			IOUtils.closeQuietly(in);
			IOUtils.closeQuietly(out);
		}
	}
	
	private String getFileName(String url)
	{
		url=url.replace("\\", "/");
		int idx=url.lastIndexOf("/");
		if(idx>=0)
			return url.substring(idx+1);
		return url;
	}


	private int caseStatus(TestStatus status)
	{
//		public static final int IGNORE=0;
//		public static final int  ERROR=1;
//		public static final int FAIL=2;
//		public static final int SUCCESS=3;

//		WAIT("WAIT",1),
//		UNKNOWN("UNKNOWN",0),
//		IGNORE("IGNORE",0),
//		ASSERT("ASSERT",2),
//		ERROR("ERROR",2),
//		CRASH("CRASH",2),
//		PASS("PASS",3);
		if(status==TestStatus.WAIT || status==TestStatus.IGNORE)
			return 0;
		else if(status==TestStatus.ASSERT || status==TestStatus.ERROR || status==TestStatus.CRASH)
			return 2;
		else if(status==TestStatus.PASS)
			return 3;
		return 0;
	}

	@Override
	public String[] getArgsDesc() {
		List<String> argDes=new ArrayList<String>();
		argDes.add("testPackageUrl=url of test apk");
		argDes.add("appPackageUrl=url of under-test apk");
		argDes.add("wifi_ssid=");
		argDes.add("wifi_pw=");
		argDes.add("wifi_user=");
		argDes.add("logcat_filter=");
		return argDes.toArray(new String[0]);
	}
	
	class TestListenerImpl implements TestProcessListener
	{
		@Override
		public void prepare(TestSuite suite) {
		}
		@Override
		public void start(TestCase tcase) {
		}
		@Override
		public void end(TestCase tcase) {
			if(!isStop)
				AndroidUITestDriver.this.getNotifier().reportCaseStatus(tcase.id, tcase.getFullName(), tcase.start, tcase.end, caseStatus(tcase.status), tcase.info, tcase.cause);
		}
		@Override
		public void start(TestClass tclass) {
		}
		@Override
		public void end(TestClass tclass) {
		}
		@Override
		public void start(TestPack tclass) {
		}
		@Override
		public void end(TestPack tclass) {
		}
		@Override
		public void start(TestSuite tclass) {
		}
		@Override
		public void end(TestSuite tclass) {
		}
		@Override
		public void finish(TestSuite suite) {
		}
	}
}
