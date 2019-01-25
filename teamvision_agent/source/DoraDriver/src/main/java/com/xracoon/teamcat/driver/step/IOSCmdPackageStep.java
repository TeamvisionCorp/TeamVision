package com.xracoon.teamcat.driver.step;

import java.io.File;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class IOSCmdPackageStep extends IOSBuildStep {
	
	@Override
	public boolean exec() throws Exception {
		String xcode=stepConf.getParam("build_tool_xcode");
		String cmd=stepConf.getParam("ios_command_line");
		String outputFilter=stepConf.getParam("ios_target_path");
		String is_clean_outputs=stepConf.getParam("is_clean_outputs");
		String is_upload_file=stepConf.getParam("is_upload_file");
		boolean result=true;

		if(is_clean_outputs !=null)
		{
			this.cleanOutput(outputFilter);	
		}
		
		//locate tools
		this.changeXCodeVersion(xcode);
			
		//execute command
		ExecStatus es= OS.getNewInstance().execScriptSyn(cmd, null, new File(workspace));
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
