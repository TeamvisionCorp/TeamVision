package com.xracoon.teamcat.driver.aui.casequeue;

import java.util.ArrayList;
import java.util.List;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestStatus;
import com.xracoon.testutil.model.TestSuite;

public class CaseQueue 
{
	private List<CaseQueueItem> itemList=new ArrayList<CaseQueueItem>();
	
	/**
	 * 构造方法
	 * @param suite
	 * @param caseDevMap  Map<caseFullName,deviceSerialNo>
	 */
	public CaseQueue(TestSuite suite/*, Map<String,String> caseDevMap*/)
	{
		suite.pass=0;
		suite.fail=0;
		for(TestPack tp: suite.testPacks.values())
		{
			tp.pass=0;
			tp.fail=0;
			for(TestClass tc: tp.testClasses.values())
			{
				tc.pass=0;
				tp.pass=0;
				for(TestCase tr:tc.testCases.values())
				{
					CaseQueueItem item=new CaseQueueItem(tr.getFullName()/*,caseDevMap.get(tr.getFullName())*/);
					item.tcase=tr;
					itemList.add(item);
				}
			}
		}
	}
	
	public int getSize()
	{
		return itemList.size();
	}
	
	/**
	 * 获取一个用例，并且将当前用例标记为执行状态。必须要与updateCase方法结合使用，才会取消执行状态。
	 * @param runTimeLimit
	 * @param status
	 * @param dev
	 * @return
	 */
	public CaseQueueItem getNextCase(int runTimeLimit, TestStatus status, String dev)
	{
		synchronized(CaseQueue.class)
		{
			for(int i=0; i<itemList.size(); i++)
			{
				CaseQueueItem item=itemList.get(i);
				if(item.running)
					continue;
				if(item.runtime>runTimeLimit)
					continue;
				if(status!=null && item.tcase.status!=status)
					continue;
				if(dev!=null && !dev.equals(item.deviceNo))
					continue;
				item.running=true;
				return item;
			}
			return null;
		}
	}
	
	
	public void updateCase(String casename, TestCase tcase)
	{
		synchronized(CaseQueue.class)
		{	
			for(int i=0; i<itemList.size(); i++)
			{
				CaseQueueItem item=itemList.get(i);
				if(!item.caseName.equals(casename))
					continue;
				item.tcase.copy(tcase);
				
				item.runtime++;
				item.running=false;
			}
		}
	}

}
