package com.xracoon.teamcat.driver;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 加载Driver
 * @author Yangtianxin
 */
public class DriverLoader {
	Logger logger = LoggerFactory.getLogger(DriverLoader.class);
	private ClassLoader loader;
	private String doraHome=".";
	
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	public DriverLoader(String doraHome){
		this.doraHome=doraHome;
	}
	
	private void init() throws IOException {
		if(loader!=null)
			return;
		
		File pluginPath=new File(doraHome, "libs");
		logger.info("load driver from pluginPath: "+pluginPath.getCanonicalPath());
		
		List<URL> jarurls=new ArrayList<URL>();
		File[] files=pluginPath.listFiles(new FileFilter(){
			@Override
			public boolean accept(File pathname) {
				if(pathname.getName().toLowerCase().endsWith(".jar"))
					return true;
				return false;
			}});
		for(File f: files){
			jarurls.add(f.toURI().toURL());
		}
		loader=new URLClassLoader(jarurls.toArray(new URL[0]));
	}
	
	public Driver loadDriver(int taskType) throws Exception{
		String driverClassName="";
		
		if(taskType==DatasEnum.AutoTaskType_PACKAGE.getValue() 
				|| taskType==DatasEnum.AutoTaskType_DEPLOY.getValue()
				|| taskType==DatasEnum.AutoTaskType_APPUI.getValue()
				|| taskType==DatasEnum.AutoTaskType_Interface.getValue())
			
			driverClassName="com.xracoon.teamcat.driver.StepDriver";
		
		else
			throw new Exception("unhandlable taskType: "+taskType);
		
		return loadDriver(driverClassName);
	}
	
	public Driver loadDriver(String driverClassName) throws Exception{
		init();
		Class<?> cls=loader.loadClass(driverClassName);
		if(!Driver.class.isAssignableFrom(cls))
			throw new Exception(cls.getName()+"不是Driver的子类");
		
		Driver driver=(Driver) cls.newInstance();
		return driver;
	}
}
