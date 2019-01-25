package com.xracoon.teamcat.driver.aui;
import static org.junit.Assert.*;

import java.util.Date;
import java.util.HashMap;

import org.apache.log4j.Logger;
import org.junit.Test;

import com.xracoon.teamcat.driver.AgentNotifier;
import com.xracoon.teamcat.driver.args.DriverArg;
import com.xracoon.teamcat.driver.aui.AndroidUITestDriver;


public class AndroidUITestDriverTest {

	@Test
	public void testDownload() 
	{
		TestAgentNotifierImpl notifier=new TestAgentNotifierImpl();
		AndroidUITestDriver driver=new AndroidUITestDriver();
		driver.setNotifier(notifier);
		driver.setWorkspace("D:/agent/workdir");
		HashMap<String,Object> options=new HashMap<String,Object>();
		

		String driverArgs="";
		driverArgs+="testPackageUrl=http://10.3.254.34:8085/androidapp/TestAndroid_LaohuSDK/unRef/NullProductVersion/2015-07-01_16-04-04/UITest_LaohuSDK_3.7-release.apk\n";
		driverArgs+="appPackageUrl=http://10.3.254.114:8085/androidapp/Develop-Android-LaohuSDK-3.7/247/3.7.4/2015-07-01_10-14-00/LaohuSDK_Demo-formal-proguard-3.7.4-r59261.apk\n";
		options.put(DriverArg.DRIVERARG, driverArgs.trim());
		options.put(DriverArg.USEDEVICESN, "ee44dc8a");
		
		driver.setEnvs(options);
		assertTrue(driver.exec());
	}

}

 class TestAgentNotifierImpl  implements AgentNotifier {

	private Logger logger = Logger.getLogger(TestAgentNotifierImpl.class);
	
	@Override
	public boolean reportCaseStatus(Long caseId, String caseName, Date start, Date end, int result, String error, String trace) 
	{
		logger.info("Report Case Status: "+caseId+"  "+caseName+"   "+start+"   "+end+"  "+result+"   "+error+"  "+trace);
		return true;
	}

	@Override
	public boolean requestArchive(String antStyleFilter, int type) {
		// TODO Auto-generated method stub
		return true;
	}
}