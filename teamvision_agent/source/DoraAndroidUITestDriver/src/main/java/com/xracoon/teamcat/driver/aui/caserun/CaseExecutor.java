package com.xracoon.teamcat.driver.aui.caserun;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Collection;
import java.util.Date;
import java.util.HashSet;
import java.util.Iterator;
import java.util.StringTokenizer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.driver.aui.TestProcessListener;
import com.xracoon.teamcat.driver.aui.casequeue.CaseQueue;
import com.xracoon.teamcat.driver.aui.casequeue.CaseQueueItem;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestStatus;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.system.OS;

public class CaseExecutor extends Thread
{
	private Logger logger = LoggerFactory.getLogger(CaseExecutor.class);
	private OS os;
	private volatile boolean isDone;
	private volatile boolean isStoped;
	private Device device;
	private String logcatFilter;
	private CaseQueue queue;
	private String testPack;
	private String appPack;
	private String runner;
	
	public void setLogger(Logger logger)
	{
		this.logger=logger;
	}
	
	private Collection<TestProcessListener> listeners;
	public void addTestListener(TestProcessListener listener) {
        if (listeners == null) {
            listeners = new HashSet<TestProcessListener>();
        }
        listeners.add(listener);
    }
	public void removeTestListener(TestProcessListener listener) {
	        if (listeners == null)
	            return;
	        listeners.remove(listener);
	    }	    
	protected void fireEndCaseEvent(TestCase tcase) {
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.end(tcase);
        }
	  }
	protected void fireStartCaseEvent(TestCase tcase) {
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.start(tcase);
        }
	  }
	protected void fireFinishedEvent(TestSuite suite)
	{
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.finish(suite);
        }
	}
	
	public CaseExecutor(OS os,CaseQueue queue,Device dev, String testPack,String appPack, String runner,String logcatFilter)
	{
		this.os=os;
		this.queue=queue;
		this.device=dev;
		this.testPack=testPack;
		this.appPack=appPack;
		this.runner=runner;
		this.logcatFilter=logcatFilter;
	}
	
	public boolean isDone()
	{
		return isDone;
	}
	
	public boolean stopTest()
	{
		isStoped=true;
		String devSerialNo=device.getSerialNo();
		
		String cmd="adb ";
		if(devSerialNo!=null && devSerialNo.trim().length()>0)
			cmd+=" -s "+devSerialNo+" ";
		String testAppStopCmd=cmd+String.format(" shell am force-stop %s",  testPack);
		String result=os.execSyn(testAppStopCmd);
		logger.info("stop cmd result: "+result);
		
		String targetAppStopCmd=cmd+String.format(" shell am force-stop %s",  appPack);
		result=os.execSyn(targetAppStopCmd);
		logger.info("stop cmd result: "+result);
		
		isDone=true;
		return true;
	}
	
	@Override
	public void run() 
	{
		CaseQueueItem item=null;
		int i=1;
		int size=queue.getSize();
		while(!isStoped && (item=queue.getNextCase(0, null, null))!=null)
		{	
			try 
			{
				TestCase tcase = item.getCaseCopy();
				
				logger.info("-----["+i+"/"+size+"] run testcase id="+tcase.id+", name="+tcase.getFullName()+"-----");
				execCase(tcase, true);
				
//				if(rerun>0 && tcase.status.isFail())
//				{
//					for(int r=rerun; r>0; r--)
//						execCase(tcase, true);
//				}
				
				queue.updateCase(item.caseName, tcase);
			} catch (IOException e) {
				e.printStackTrace();
			}
			i++;
		}
		
		isDone=true;
	}
	
	private String[] buildCmdArray(String cmd)
	{
        StringTokenizer st = new StringTokenizer(cmd);
        String[] cmdarray = new String[st.countTokens()];
        for (int i = 0; st.hasMoreTokens(); i++)
            cmdarray[i] = st.nextToken();
        
        return cmdarray;
	}
	
	private void execCase(TestCase tcase, boolean isUpdate) throws IOException
	{
		if(isUpdate && tcase.status==TestStatus.PASS)
		{
			logger.info("case already passed, skip for update");
			return ;
		}
		
		String devSerialNo=device.getSerialNo();
		TestCase run=new TestCase();
		run.copy(tcase);
		run.start=new Date();
		
		
		File pwd=new File(".");
		String cmd="adb ";
		if(devSerialNo!=null && devSerialNo.trim().length()>0)
			cmd+=" -s "+devSerialNo+" ";
		cmd+=String.format(" shell am instrument -e class %s/%s#%s -w %s/%s", run.packName,run.className,run.name, testPack,runner);
		logger.info(cmd);
		ProcessBuilder pb=new ProcessBuilder(buildCmdArray(cmd)).directory(pwd);
		pb.redirectErrorStream(true);
		 
//		Execution logcatCapture=null;
//		if(logcatFilter!=null)
//		{
//			logger.info("-----capture logcat ( filter= '"+logcatFilter+"' )-----");
//			logcatCapture=device.captureLog(logcatFilter, true, new Log4jWriter(logger));
//		}
		
		Process p=pb.start();
		//logger.info("test process started: "+p);
		
		BufferedReader reader=new BufferedReader(new InputStreamReader(p.getInputStream(),"UTF-8"));
		StringBuilder infosBuff=new StringBuilder();
		String line=null;
		while ((line = reader.readLine()) != null)  
		{
			if(line.trim().length()==0)
				continue;
			
			logger.info(line);
			infosBuff.append(line+"\r\n");
		}
	
		String infos=infosBuff.toString();
		if(p.exitValue()!=0)
		{
			run.status=TestStatus.ERROR;
			run.info="instrument invoke failed";
			run.cause=infos;
		}
		else
		{
			String msgStatusError="INSTRUMENTATION_STATUS: Error=";
			String msgResultError="INSTRUMENTATION_RESULT: longMsg=";
			String msgRunFailure="Failure in "+run.name+":";
			String msgRunError="Error in "+run.name+":";
			int index=-1;
			if((index=infos.indexOf(msgStatusError))>=0)
			{
				run.status=TestStatus.ERROR;
				run.info=infos.substring(index, infos.indexOf("\n",index));
				run.cause=infos;
			}
			else if((index=infos.indexOf(msgResultError))>=0)
			{
				run.status=TestStatus.ERROR;
				run.info=infos.substring(index, infos.indexOf("\n",index));
				run.cause=infos;
			}
			else if((index=infos.indexOf(msgRunFailure))>=0)
			{
				run.status=TestStatus.ERROR;
				int startIdx=infos.indexOf("\n", index)+1;
				run.info=infos.substring(startIdx, infos.indexOf("\n",startIdx));
				run.cause=infos;
			}
			else if((index=infos.indexOf(msgRunError))>=0)
			{
				run.status=TestStatus.ERROR;
				int startIdx=infos.indexOf("\n", index)+1;
				run.info=infos.substring(startIdx, infos.indexOf("\n",startIdx));
				run.cause=infos;
			}
			else if(infos.contains("OK (1 test)"))
			{
				run.status=TestStatus.PASS;
				run.info=null;
				run.cause=null;
			}
			else
			{
				run.status=TestStatus.IGNORE;
				run.info="unknow status";
				run.cause=infos;
			}
		}
		
//		if(logcatCapture!=null)
//		{
//			logcatCapture.stop();
//			logger.info("-----logcat close-----");
//		}
		
		run.end=new Date();
		if(run.status==TestStatus.PASS)
		{
			run.pass=1;
			run.fail=0;
		}
		else if(run.status.isFail())
		{
			run.pass=0;
			run.fail=1;
		}
		
//		if(run.status.isFail())
//		{
//			logger.error(run.status+"\t\t"+run.inTime);
//			logger.error(run.cause);
//		}
//		else
//			logger.info(run.status+"\t\t"+run.inTime);
		
		logger.info(">reuslt: "+run.status+", start: "+run.start+",  end: "+run.end);
		if(isUpdate && tcase.status.compare(run.status)>0)
		{
			logger.info("test result is not better, skip for update");
		}
		else
		{
			tcase.copy(run);
			if(!isStoped)
			{
				fireEndCaseEvent(tcase);
				logger.info("testcase finished");
			}
			else
				logger.info("testcase was force stoped");
		}
		logger.info("");
	}
}
