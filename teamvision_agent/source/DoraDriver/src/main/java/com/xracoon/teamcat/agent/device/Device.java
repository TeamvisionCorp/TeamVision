package com.xracoon.teamcat.agent.device;

import java.io.Writer;

import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

/**
 * 设备抽象基类
 * @author Yangtianxin
 */
public abstract class Device 
{
	private String serialNo;
	private String name;
	private String status;
	private String osType;
	private String osVersion;
	private String brand;
	private boolean isSimulated;
	private String resolution;
	private String dpi;
	private OS os;
	
   abstract public boolean isAppInstalled(String appIdentity);
   abstract public boolean installApp(String appPath);
   abstract public boolean removeApp(String appIdentity);
   abstract public String synExec(String shellcmd);
   abstract public Execution asynExec(String shellcmd, Writer writer, EndingLineListener endlistener);
   abstract public Execution captureLog(String filter, boolean cleanBeforeStart, Writer writer);
   
   @Deprecated
   abstract public ExecStatus synShellExec(String devShellLine);
   @Deprecated
   abstract public ExecStatus synDevExec(String devDevLine);
   
   public void setOS(OS os)
   {
	   this.os=os;
   }
   public OS getOS()
   {
	   return os;
   }
	public String getSerialNo() {
		return serialNo;
	}
	public void setSerialNo(String serialNo) {
		this.serialNo = serialNo;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getStatus() {
		return status;
	}
	public void setStatus(String status) {
		this.status = status;
	}
	public String getOsType() {
		return osType;
	}
	public void setOsType(String devOs) {
		this.osType = devOs;
	}
	public String getOsVersion() {
		return osVersion;
	}
	public void setOsVersion(String osVersion) {
		this.osVersion = osVersion;
	}
	public String getBrand() {
		return brand;
	}
	public void setBrand(String brand) {
		this.brand = brand;
	}
	public boolean isSimulated() {
		return isSimulated;
	}
	public void setIsSimulated(boolean isSimulated) {
		this.isSimulated = isSimulated;
	}
	public String getResolution() {
		return resolution;
	}
	public void setResolution(String resolution) {
		this.resolution = resolution;
	}
	public String getDpi() {
		return dpi;
	}
	public void setDpi(String dpi) {
		this.dpi = dpi;
	}

}
