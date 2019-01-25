package com.xracoon.teamcat.agent.debug;
import static org.junit.Assert.*;

import org.junit.Test;

import com.xracoon.teamcat.agent.archive.FtpArchiveManager;
import com.xracoon.teamcat.driver.TaskInfo;


public class FtpArchiveTest {

	@Test
	public void test() {
		TaskInfo ti=new TaskInfo();
		ti.taskID=1;
		FtpArchiveManager manager=new FtpArchiveManager(ti,"10.2.44.58",21,"root","root","archive/test1");
		manager.processArchiveRequest("F:/TestData/toFtp/1.txt", 0);
	}

}
