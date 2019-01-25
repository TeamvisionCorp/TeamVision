package com.xracoon.teamcat.utils.testngtools.caserunner;

import com.xracoon.util.basekit.hudson.proc.NullStream;
import com.xracoon.util.basekit.hudson.proc.Proc;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;

public class TestngRunner {
	private Logger logger = LoggerFactory.getLogger(TestngRunner.class);
	
	public void setLogger(Logger log){
		logger=log;
	}
	
	public void forceStop(){
		logger.info("force stop...");
		OS os=OS.getNewInstance();
		os.setLogger(logger);
		logger.info("Current OS: "+os.getOs()+"_"+os.getArch()+"_"+os.getVersion()+", "+os.getDomain()+"/"+os.getName()+", ip:"+os.getIP(null));
		 
		String[] pids=os.getJavaPid("classworlds");
		logger.info("pids: "+Arrays.toString(pids));
		if(pids!=null)
		{
			for(String pid: pids)
				os.killProcess(pid);
		}
	}
	
	public ExecStatus start(String buildPath) throws IOException{
		ExecStatus status=new ExecStatus();
		//String cmd="";
		Proc proc;
		//Process mvnProcess;
		OutputStream nos=new NullStream();
		if(OS.isUnixLike()){
			String[] cmds={"/bin/sh","-c","cd "+buildPath+" &&mvn clean  test  -Dmaven.test.failure.ignore=true"};
			//mvnProcess=Runtime.getRuntime().exec(cmds);
			proc=new Proc.LocalProc(cmds,null, System.in, nos, nos, new File("."), logger, true);
		}else{
			//cmd = "cmd /c mvn clean  test  -Dmaven.test.failure.ignore=true";// start
			String[] cmds={"cmd", "/c", buildPath.substring(0,2)+" && cd "+buildPath+" && mvn clean  test  -Dmaven.test.failure.ignore=true"};
			//mvnProcess=Runtime.getRuntime().exec(cmd,null,new File(buildPath));
			proc=new Proc.LocalProc(cmds,null, System.in, nos, nos, new File(buildPath), logger, true);
		}
		logger.info(">running maven...");
		int returnCode=-99;
		try {
			returnCode=proc.joinWithTimeout(30*60*1000, TimeUnit.MILLISECONDS,logger);
		} catch (InterruptedException e) {
			e.printStackTrace();
			logger.error("proc time out err");
		}
		status.setRetVal(returnCode);
//		BufferedReader reader=new BufferedReader(new InputStreamReader(proc.getStdout()));
//		BufferedReader readerErr=new BufferedReader(new InputStreamReader(proc.getStderr()));
//		String line=null;
//		while ((line = reader.readLine()) != null) {
//			logger.info(line);
//		}
//		try {
//			Thread.sleep(1000);
//		} catch (InterruptedException e) {
//			e.printStackTrace();
//		}
		if(status.getRetVal()==0)
			logger.info(">All testcases finished.");
		else{
//			String lineErr=null;
//			StringBuilder builder=new StringBuilder();
//			while ((lineErr = readerErr.readLine()) != null) {
//				//logger.info(lineErr);
//				builder.append(lineErr+"\r\n");
//			}
//			status.setError(builder.toString());
			logger.error(">error occured when maven running");
		}
		
		logger.info(">running maven done");
		return status;
	}
}
