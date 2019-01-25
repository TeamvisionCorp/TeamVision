package com.xracoon.teamcat.agent.device;

import java.io.Writer;

import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

/**
 * Android设备类
 * @author Yangtianxin
 */
@Deprecated
public  class DeviceAndroid  extends Device{
	public DeviceAndroid()
	{
		setOsType("android");
	}
	private int sdk;
	
	
	public int getSdk() {
		return sdk;
	}
	public void setSdk(int sdk) {
		this.sdk = sdk;
	}

	@Override
	public boolean isAppInstalled(String appIdentity) 
	{
		ExecStatus status=synDevExec("shell pm list packages | grep "+appIdentity);
		return status.getRetVal()==0 && status.getLog().contains(appIdentity);
	}
	@Override
	public boolean installApp(String appPath) {
		return synDevExec("install -r "+appPath).getRetVal()==0;
	}
	@Override
	public boolean removeApp(String appIdentity) {
		return synDevExec("uninstall "+appIdentity).getRetVal()==0;
	}
	
	@Deprecated
	@Override
	public ExecStatus synShellExec(String devShellLine) 
	{
		OS os=getOS();
		ExecStatus status=os.execSyn("adb -s "+this.getSerialNo()+" shell "+devShellLine,null,null);
		return status;
	}
	
	@Deprecated
	@Override
	public ExecStatus synDevExec(String devDevLine) {
		OS os=getOS();
		ExecStatus status=os.execSyn("adb -s "+this.getSerialNo()+" "+devDevLine,null,null);
		return status;
	}
	
	@Override
	public String synExec(String shellcmd) {
		return null;
	}
	@Override
	public Execution asynExec(String shellcmd, Writer writer,
			EndingLineListener endlistener) {
		return null;
	}
	@Override
	public Execution captureLog(String filter, boolean cleanBeforeStart,
			Writer writer) {
		return null;
	}
}
