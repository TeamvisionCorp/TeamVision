package com.xracoon.teamcat.driver.step;

import java.io.File;

import com.xracoon.teamcat.driver.BuildTools;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class AntStep extends BuildStep {
	@Override
	public boolean exec() throws Exception {
		OS os=OS.getSingleton();
		String jdk=stepConf.getParam("build_tool_jdk");
		String cmd=stepConf.getParam("ant_command_line");
		String outputFilter=stepConf.getParam("ant_target_path");
		String buildFile=stepConf.getParam("ant_build_file");
		
		//locate tools
		BuildTools bt=(BuildTools) env.get(Driver.ENV_BUILDTOOLS);
		File jdkPath=bt.getJDKPath(jdk);
		
		//build command
		String workspace=env.get(Driver.ENV_WORKSPACE).toString();
		StringBuilder sb=new StringBuilder();
		if(jdkPath!=null)
			sb.append(os.getEnvSettingClause("JAVA_HOME", jdkPath.getAbsolutePath())).append("\n");
		sb.append("ant ");
		if(!StringEx.isBlank(buildFile))
			sb.append(" -f ").append(buildFile).append(" ");
		sb.append(cmd);
		
		//execute command
		ExecStatus es= OS.getNewInstance().execScriptSyn(sb.toString(), null, new File(workspace));
		if(es.getRetVal()!=0)
			return false;
		
		//archive files
		return this.archiveFiles(outputFilter, Driver.ARCHIVE_PACKAGE);
	} 
}
