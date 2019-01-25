package com.xracoon.teamcat.agent.debug;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Date;

import org.apache.log4j.Logger;

import com.xracoon.teamcat.driver.AgentNotifier;
import com.xracoon.teamcat.driver.CaseStatus;
import com.xracoon.teamcat.driver.Driver;

public class DebugTestDriver extends Driver {
	private Logger logger = Logger.getLogger(DebugTestDriver.class);
	
	@Override
	public boolean exec() {
		logger.info("InstrumentTestDriver");
		AgentNotifier agentNotifier=this.getNotifier();		
		for(int i=0; i<4; i++)
		{
			String name="instrumentCase"+i;
			Date start=null;
			int result=CaseStatus.IGNORE;
			StringWriter errorbuffer=new StringWriter(); 
			StringWriter tracebuffer=new StringWriter(); 
			PrintWriter error=new PrintWriter(errorbuffer);
			PrintWriter trace=new PrintWriter(tracebuffer);
			
			try{
				start=new Date();
				Thread.sleep(3000);

				switch(i)
				{
				case 0:break;
				case 1:
					String a=null;
					a.length();
					break;
				case 2:
					error.append("custom error");
					error.append("\n");
					trace.append("custom trace line1\ncustom trace line2");
					trace.append("\n");
					result=CaseStatus.FAIL;
					break;
				case 3:
					result=CaseStatus.PASS;
				}
			}catch(Exception e)
			{
				logger.error("Driver Exception: "+e.getMessage(), e);
				result=CaseStatus.FAIL;
				error.append(e.getMessage()+"\n");
				e.printStackTrace(trace);
			}
			finally
			{
				String errorStr=errorbuffer.toString().trim();
				String traceStr=tracebuffer.toString().trim();
				agentNotifier.reportCaseStatus(0l, name, start, new Date(), result, errorStr.length()>0?errorStr:null, traceStr.length()>0?traceStr:null);
			}
		}
		logger.error("Driver Finished");
		return true;
	}

	@Override
	public boolean stop() {
		// TODO Auto-generated method stub
		logger.warn("Driver Interupted");
		return false;
	}

	@Override
	public String[] getArgsDesc() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean init() {
		logger.info("DebugTestDriver initialized");
		return true;
	}

}
