package com.xracoon.teamcat.agent.debug;

import static org.junit.Assert.*;

import org.junit.Test;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.agent.taskrun.TaskExecutor;

public class TaskExecutorTest {

	private AgentConfig config;
	
	public void setUp()
	{
		config=new AgentConfig();
		config.agentId=1;
		config.workDir="./workdir";
	}
	
//	@Test
//	public void testTaskDone() throws InterruptedException {
//		TaskExecutor executor=new TaskExecutor(config);
//		Thread t=new Thread(executor);
//		t.start();
//		Thread.sleep(1000);
//		executor.addTask(2);
//		t.join();
//	}
//
//	@Test
//	public void testTaskError() throws InterruptedException {
//		TaskExecutor executor=new TaskExecutor(config);
//		Thread t=new Thread(executor);
//		t.start();
//		Thread.sleep(1000);
//		executor.addTask(3);
//		t.join();
//	}
//	
//	@Test
//	public void testTaskAbort() throws InterruptedException {
//		TaskExecutor executor=new TaskExecutor(config);
//		Thread t=new Thread(executor);
//		t.start();
//		Thread.sleep(1000);
//		executor.addTask(2);
//		Thread.sleep(1000);
//		executor.stopTask(2);
//		Thread.sleep(10000);
//		t.stop();
//	}
}
