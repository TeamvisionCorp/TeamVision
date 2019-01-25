package com.xracoon.teamcat.agent.device;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Writer;
import java.util.concurrent.TimeUnit;

import com.android.ddmlib.IDevice;
import com.android.ddmlib.InstallException;
import com.android.ddmlib.MultiLineReceiver;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

/**
 * Android设备类
 * @author Yangtianxin
 */
public class DeviceAndroidEx  extends Device{
	public static final int maxResponseTimeout=10;
	public static final TimeUnit maxResponseTimeoutUnit=TimeUnit.MINUTES;
	
	public DeviceAndroidEx()
	{
		setOsType("android");
	}

	private IDevice devRaw;
	public IDevice getDevRaw()
	{
		return devRaw;
	}
	public void setDevRaw(IDevice rdev)
	{
		this.devRaw=rdev;
	}
	
	private int sdk;
	public int getSdk() {
		return sdk;
	}
	public void setSdk(int sdk) {
		this.sdk = sdk;
	}
	
	public class CmdOutputReceiver extends MultiLineReceiver
	{
		private boolean isCancel;
		private StringBuilder strbuilder;
		private Writer writer;
		private EndingLineListener endlistener;
		
		public CmdOutputReceiver(Writer writer, EndingLineListener endlistener)
		{
			this.endlistener=endlistener;
			this.writer=writer;
			if(writer==null)
				strbuilder=new StringBuilder();
		}
		
		public String getOutput()
		{
			return strbuilder==null?null:strbuilder.toString();
		}
		
		public void cancel()
		{
			isCancel=true;
		}
		@Override
		public boolean isCancelled() {
			return isCancel;
		}

		@Override
		public void processNewLines(String[] lines) 
		{
			if(strbuilder!=null)
			{
				for(String line: lines)
				{
					strbuilder.append(line+"\r\n");
					if(endlistener!=null && (isCancel=endlistener.isEnding(line))==true)
						break;
				}
			}
						
			else
			{
				try 
				{
					for(String line: lines)
					{
						writer.write(line);
						writer.write("\r\n");
						if(endlistener!=null && (isCancel=endlistener.isEnding(line))==true)
							break;
					}
					writer.flush();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
	public class AndroidExecution implements Execution
	{
		private Thread thread;
		private CmdOutputReceiver receiver;
		private AndroidExecution(Thread thread, CmdOutputReceiver receiver)
		{
			this.thread=thread;
			this.receiver=receiver;
		}
		@Override
		public boolean isAlive()
		{
			return thread!=null && thread.isAlive();
		}
		@Override
		public void stop()
		{
			receiver.cancel();
		}
		@Override
		public void waitFor() throws InterruptedException
		{
			while(thread.isAlive())
				Thread.sleep(500);
		}
		@Override
		public String getOutput() {
			return receiver==null?null:receiver.getOutput();
		}
	}

	@Override
	public String synExec(final String cmdline)
	{
		final CmdOutputReceiver receiver=new CmdOutputReceiver(null, null);
		try {
			devRaw.executeShellCommand(cmdline, receiver, maxResponseTimeout, maxResponseTimeoutUnit);
		} catch (Exception e) {
			ByteArrayOutputStream baos=new ByteArrayOutputStream();
			e.printStackTrace(new PrintWriter(baos));
			e.printStackTrace();
			return "error in cmd ["+cmdline+"]: \n"+baos.toString();
		}  
		return receiver.getOutput();
	}
	
	@Override
	public Execution asynExec(final String shellcmd, final Writer writer, EndingLineListener endlistener)
	{
		final CmdOutputReceiver receiver=new CmdOutputReceiver(writer, endlistener);
		Thread t=new Thread(new Runnable(){
			@Override
			public void run() {
				try {
					devRaw.executeShellCommand(shellcmd, receiver, maxResponseTimeout, maxResponseTimeoutUnit);    //会阻塞
				} catch (Exception e) {
					PrintWriter pwriter=new PrintWriter(writer);
					pwriter.println("error in cmd ["+shellcmd+"]: ");
					e.printStackTrace(pwriter);
					e.printStackTrace();
				} 
			}});
		t.start();
		return new  AndroidExecution(t, receiver);
	}
	
	@Override
	public boolean isAppInstalled(String appIdentity) 
	{
		String output=synExec("pm list packages | grep "+appIdentity);
		return output!=null && output.contains(appIdentity);
	}
	
	@Override
	public boolean installApp(String appPath)  {
		//return synDevExec("install -r "+appPath).getRetVal()==0;

		try {
			String errorMsg=devRaw.installPackage(appPath, true);
			if(errorMsg!=null)
				System.out.println(errorMsg);
			return null==errorMsg;
		} catch (InstallException e) {
			e.printStackTrace();
			return false;
		}
	}
	@Override
	public boolean removeApp(String appIdentity) {
		//return synDevExec("uninstall "+appIdentity).getRetVal()==0;
		
		try {
			String errorMsg=devRaw.uninstallPackage(appIdentity);
			if(errorMsg!=null)
				System.out.println(errorMsg);
			return null==errorMsg;
		} catch (InstallException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	
	public Execution captureLog(String filter, boolean cleanBeforeStart, Writer writer)
	{	
		if(cleanBeforeStart)
			synExec("logcat -c");
		
		Execution exec=asynExec("logcat -s %s "+filter, writer, null);
		return exec;
	}
	
	@Deprecated
	@Override
	public ExecStatus synShellExec(String devShellLine) 
	{
		ExecStatus status=new ExecStatus();
		status.setRetVal(0);
		status.setLog(synExec(devShellLine));
		return status;
	}
	
	//not overide
	@Deprecated
	@Override
	public ExecStatus synDevExec(String devDevLine) {
		OS os=getOS();
		ExecStatus status=os.execSyn("adb -s "+this.getSerialNo()+" "+devDevLine,null,null);
		return status;
	}
}
