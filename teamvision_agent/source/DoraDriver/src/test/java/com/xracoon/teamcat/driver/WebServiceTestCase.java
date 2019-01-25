package com.xracoon.teamcat.driver;

import static org.junit.Assert.*;

import java.util.Date;
import java.util.List;
import java.util.Map;
import org.junit.Test;

import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.driver.WebService.CaseMapItem;
import com.xracoon.testutil.model.TestCase;

public class WebServiceTestCase {
	@Test
	public void testQueryTaskConfig() throws Exception{
		TaskInfo info=new TaskInfo();
		info.taskID=6;
		info.taskType=1;
		WebService.queryTaskConfig(info);
		assertEquals(info.agentID, 0);
	}
	
	@Test
	public void testQueryParamGroup() throws Exception{
		Map<String,String> map= WebService.getParameters("583e69136a3c27703eabe8b0");
		assertEquals(2, map.size());
	}
	
	@Test
	public void testQueryHost() throws Exception{
		Map<String,String> map= WebService.queryHosts(1);
		assertTrue(map.size()>0);
	}
	
	@Test
	public void testQueryTestCase() throws Exception{
		List<TestCase> cases= WebService.queryCases("52,53,54,55,56,");
		assertTrue(cases.size()>0);
	}
	
	@Test
	public void testQueryCaseResults() throws Exception{
		Map<String, CaseMapItem> cases= WebService.queryCaseResultsIdMap(5l);
		assertTrue(cases.size()>0);
	}
	
	@Test
	public void testUpdateCaseResults() throws Exception{
		WebService.updateCaseResult(1l, new Date(), new Date(), 1, "error", "trace",1l);
		System.out.println("");
	}
	
	@Test
	public void testQueryTaskQueueInfo() throws Exception{
		Map<String,Object> map=WebService.queryTaskQueueInfo(41);
		System.out.println("");
	}
}
