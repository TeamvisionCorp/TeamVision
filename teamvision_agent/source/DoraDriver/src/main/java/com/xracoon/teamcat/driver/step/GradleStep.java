package com.xracoon.teamcat.driver.step;

import java.io.File;

import com.xracoon.teamcat.driver.BuildTools;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class GradleStep extends BuildStep {
	@Override
	public boolean exec() throws Exception {
		OS os=OS.getSingleton();
		String jdk=stepConf.getParam("build_tool_jdk");
		String gradle=stepConf.getParam("build_tool_gradle");
		String cmd=stepConf.getParam("gradle_command_line");
		String outputFilter=stepConf.getParam("gradle_target_path");
		String gradleFile=stepConf.getParam("gradle_file");
		String is_clean_outputs=stepConf.getParam("is_clean_outputs");
		String is_upload_file=stepConf.getParam("is_upload_file");
		boolean result=true;
		if(is_clean_outputs !=null)
		{
			this.cleanOutput(outputFilter);	
		}
		
		//locate tools
		BuildTools bt=(BuildTools) env.get(Driver.ENV_BUILDTOOLS);
		File jdkPath=bt.getJDKPath(jdk);
		File gradlePath=bt.getGradlePath(gradle);
		
		//build command
		String workspace=env.get(Driver.ENV_WORKSPACE).toString();
		StringBuilder sb=new StringBuilder();
		if(jdkPath!=null)
			sb.append(os.getEnvSettingClause("JAVA_HOME", jdkPath.getAbsolutePath())).append("\n");
		if(gradlePath!=null)
			sb.append(new File(gradlePath, "bin/gradle"+(OS.isUnixLike()?"":".bat")));
		else
			sb.append(" gradle ");
		sb.append(" ");
		if(!StringEx.isBlank(gradleFile))
			sb.append(" -b ").append(gradleFile).append(" ");
		sb.append(cmd);
		
		//execute command
		ExecStatus es= OS.getNewInstance().execScriptSyn(sb.toString(), null, new File(workspace));
		if(es.getRetVal()!=0)
			return false;
		
		//archive files
		 if(is_upload_file!=null)
	        {
	        	   result=this.archiveFiles(outputFilter, Driver.ARCHIVE_PACKAGE);
	        }
	        else
	        {
	        	    result=true;
	        }
		
		
		return result;
	}
}
