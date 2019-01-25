package com.xracoon.teamcat.driver.aui.casequeue;

import com.xracoon.testutil.model.TestCase;


public class CaseQueueItem {
		public final String caseName;
		public final String deviceNo;
		
		TestCase tcase;
		int runtime;
		boolean running;
		
		public TestCase getCaseCopy()
		{
			TestCase tc=new TestCase();
			tc.copy(tcase);
			return tc;
		}
		
		public CaseQueueItem(String cname)
		{
			this.caseName=cname;
			this.deviceNo=null;
		}
		
		public CaseQueueItem(String cname,String dev)
		{
			this.caseName=cname;
			this.deviceNo=dev;
		}
}
