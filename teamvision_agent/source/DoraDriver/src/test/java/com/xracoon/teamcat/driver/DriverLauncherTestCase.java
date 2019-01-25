package com.xracoon.teamcat.driver;

import org.junit.Test;

import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.teamcat.driver.DriverLauncher.LaunchParams;

public class DriverLauncherTestCase {
	@Test
	public void test1(){
		TaskInfo info=new TaskInfo();
		info.taskID=11;
		info.taskType=1;
		info.taskQueueID=22;
		info.historyID=33;
		info.paramID="1231abcd";
		info.agentID=5;
		
		LaunchParams lp=new LaunchParams(info, 8899,"E:/temp/workspace","E:/");
		String json=lp.toJson();
		
		LaunchParams lpnew=LaunchParams.fromJson(json);
		
		TaskInfo info1=lpnew.toTaskInfo();
		System.out.println(info1.toString());
	}
}
