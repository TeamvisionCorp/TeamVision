package com.xracoon.teamcat.driver.aui;
import java.text.ParseException;
import org.dom4j.DocumentException;
import org.junit.Test;
import org.xmlpull.v1.XmlPullParserException;

import com.xracoon.teamcat.driver.aui.ReportHelper;
import com.xracoon.teamcat.driver.aui.casequeue.CaseQueue;
import com.xracoon.teamcat.driver.aui.casequeue.CaseQueueItem;
import com.xracoon.testutil.model.TestSuite;


public class LauncherTestCase {

	@Test
	public void testCaseQueue() throws XmlPullParserException, DocumentException, ParseException 
	{
		String suiteFile="D:/agent/workdir/testsuite.xml";
		ReportHelper creator=new ReportHelper();
		TestSuite testsuite=creator.loadReport(suiteFile);
		
//		Map<String,String> map=new HashMap<String,String>();
//		map.put( "com.xracoon.mobileqa.uitest/FloatViewTestCase#testFloatBar_Display","ee44dc8a");
//		map.put("com.xracoon.mobileqa.uitest/FloatViewTestCase#testFloatBar_Entry","ee44dc8a");
		
		CaseQueue caseQueue=new CaseQueue(testsuite);

		for(int i=0; i<caseQueue.getSize(); i++)
		{
			CaseQueueItem item=caseQueue.getNextCase(0, null, "ee44dc8a");
			if(item!=null)
			{
				System.out.println("0:\t"+item.caseName+"==>"+item.deviceNo);
				caseQueue.updateCase(item.caseName, item.getCaseCopy());
			}
		}
		for(int i=0; i<caseQueue.getSize(); i++)
		{
			CaseQueueItem item=caseQueue.getNextCase(0, null, null);
			if(item!=null)
				System.out.println("1:\t"+item.caseName+"==>"+item.deviceNo);
		}
	}

}
